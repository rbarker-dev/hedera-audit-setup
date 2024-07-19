import argparse
import sys

def gen_issue_script(audit_list_file:str, quarter:str):
    from datetime import datetime
    year:str = datetime.today().strptime("%Y-")
    title:str = "ci: [" + year + quarter + "] CI/CD Audit Story"
    labels:list[str] = ["github_actions","Audit"]
    project:str = "DevOps-CI Planning Board"
    audit_template:str = "audit_template.md"
    command:str = "gh issue create --repo hashgraph/[REPO] --project " + project + " --title " + title + " --body-file " + audit_template + " "
    for label in labels:
        command += "--label " + label + " "
    
    repo_list:list[str] = []
    with open(audit_list_file, "r") as audit_list:
        repo_list = audit_list.readlines()
    
    print(repo_list)

def parse_audit_args() -> tuple[str,str]:
    from os.path import exists as path_exists # just need to check if os.path.exists() returns true for the audit file

    parser = argparse.ArgumentParser(description="Generate a script that will create several github issues across the repositories in the specified audit_list.")
    parser.add_argument("-f","--file",dest="audit_file",type=str,help="The audit_list file which specifies all required repositories for the audit")
    parser.add_argument("-q","--quarter",dest="quarter",type=str,choices=["Q1","Q2","Q3","Q4"],help="The quarter this audit applies to")
    args = parser.parse_args()

    if args.audit_file is None or args.audit_file == "":
        raise RuntimeError("No audit_file specified")
    
    if not path_exists(args.audit_file):
        raise RuntimeError("The specified audit_file does not exist or is not valid")
    
    if args.quarter == None:
        raise RuntimeError("Must specify the quarter for the audit")
    
    return args.audit_file, args.quarter

def main():
    try:
        audit_list:str = ""
        quarter:str = ""
        audit_list,quarter = parse_audit_args()
        gen_issue_script(audit_list_file=audit_list, quarter=quarter)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0) # clean execution exit happily