import argparse
import sys
from active_repos import write_active_repos_file, ACTIVE_REPOS_FILE

PROJECT_BOARD_MAP:dict[str,str] = {
    "hashgraph": "\"Platform-CI Planning Board\"", # Hashgraph
    "hiero-ledger": "\"Platform-CI Team\"", # Hiero-Ledger"
    "swirlds": "\"Platform-CI Team\"", # Swirlds
    "swirldslabs": "\"Platform-CI Team\"" # Swirlds Labs
}

AUDITABLE_REPOS_FILE:str = "auditable_repos.md"

def write_audit_repos_list(repositories:list[dict[str,str]]) -> bool:
    """Write the repo list to a .txt file."""
    file_was_written:bool = False
    try:
        with open(AUDITABLE_REPOS_FILE, "w") as file:
            file.write("# Audit List\n\n")
            file.write("| Repository | Project Board |\n")
            file.write("|------------|----------------|\n")
            for repo in repositories:
                file.write(f"| {repo['owner']}/{repo['repository']} | {repo['project']} |\n")
            file_was_written = True
    except Exception as e:
        print(f"Error writing to file: {e}")
    return file_was_written

def get_repositories(all_repos_list:list[str]) -> list[dict[str,str]]:
    repositories:list[dict[str,str]] = []
    active_repos_list:list[str] = []
    try:
        with open(ACTIVE_REPOS_FILE,"r") as active_repos:
            active_repos_list = active_repos.readlines()
    except Exception as e:
        print(f"Error reading the {ACTIVE_REPOS_FILE} file:", e)

    all_repos = [repo for repo in all_repos_list if repo in active_repos_list]
    for repo in all_repos:
        org:str = repo.strip().split(',')[0]
        name:str = repo.strip().split(',')[1]
        project:str = PROJECT_BOARD_MAP[org]
        repositories.append(dict(
            owner=org,
            repository=name,
            project=project
        ))
    return repositories

def get_orgs(file_contents:list[str]) -> list[str]:
    orgs:set[str] = set()
    for line in file_contents:
        orgs.add(line.strip().split(',')[0])
    return list(orgs)

def gen_issue_script(audit_list_file:str, quarter:str, active_days:int=365):
    from datetime import datetime
    from os import chmod

    print("Generating the Issue Gen shell script")

    year:str = datetime.today().strftime("%Y-")
    title:str = "\"ci: [" + year + quarter + "] CI/CD Audit Story\""
    audit_template:str = "audit_template.md"
    command:str = "gh issue create --repo [ORG]/[REPO] --project [PROJECT] --title " + title + " --body-file " + audit_template + " --label Audit"
    
    cmd_list:list[str] = []
    try:
        with open(audit_list_file, "r") as audit_list:
            file_contents:list[str] = audit_list.readlines()

        orgs = get_orgs(file_contents)
        if not write_active_repos_file(orgs=orgs, days=active_days):
            raise Exception("Error writing to file: {}".format(ACTIVE_REPOS_FILE))

        repositories:list[dict[str,str]] = get_repositories(all_repos_list=file_contents)
        if not write_audit_repos_list(repositories=repositories):
            print(f"Error writing to file: {AUDITABLE_REPOS_FILE}")

        for repository in repositories:
            repo:str = repository["repository"]
            org:str = repository["owner"]
            project:str = repository["project"]
            cmd:str = command.replace("[ORG]",org).replace("[REPO]",repo).replace("[PROJECT]",project)
            cmd_list.append(cmd)

        audit_script:str = "audit_issue_gen.sh"
        with open(audit_script, "w") as script:
            for line in cmd_list:
                line += "\n"
                print(line)
                script.write(line)
                script.write("sleep 2\n") # need sleep 2 for gh api to be happy

        print("Generation complete. chmod to 755 to enable execution of the script")
        chmod(audit_script,0o755)
    
    except Exception as e:
        raise e

    print("Complete.")

def parse_audit_args() -> tuple[str,str, int]:
    from os.path import exists as path_exists # just need to check if os.path.exists() returns true for the audit file

    parser = argparse.ArgumentParser(description="Generate a script that will create several github issues across the repositories in the specified audit_list.")
    parser.add_argument("-a","--active-days",dest="active_days",type=int,help="The number of days to check for activity")
    parser.add_argument("-f","--file",dest="audit_file",type=str,help="The audit_list file which specifies all required repositories for the audit")
    parser.add_argument("-q","--quarter",dest="quarter",type=str,choices=["Q1","Q2","Q3","Q4"],help="The quarter this audit applies to")
    args = parser.parse_args()

    if args.audit_file is None or args.audit_file == "":
        raise RuntimeError("No audit_file specified")
    
    if not path_exists(args.audit_file):
        raise RuntimeError("The specified audit_file does not exist or is not valid")
    
    if args.quarter is None:
        raise RuntimeError("Must specify the quarter for the audit")

    if args.active_days is None or args.active_days <= 0:
        raise RuntimeError("Active Days must be greater than 0")
    
    return args.audit_file, args.quarter, args.active_days

def main():
    try:
        audit_list:str = ""
        quarter:str = ""
        active_days:int = 0
        audit_list,quarter,active_days = parse_audit_args()
        print("Audit_List file:",audit_list,"Quarter:",quarter)
        gen_issue_script(audit_list_file=audit_list, quarter=quarter, active_days=active_days)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0) # clean execution exit happily
