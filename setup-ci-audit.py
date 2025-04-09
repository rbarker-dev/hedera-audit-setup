import argparse
import sys
from datetime import datetime,timedelta

def run_gh_query(date_list:list[str], orgs:list[str], use_init_date:bool=False):
    command_template:str = "gh search repos props.last-ci-review-date:[TEMPLATE_DATE] --archived=false --include-forks=false --owner=[ORG_NAME] --limit 200 --json owner,name --jq '.[] | \"\\(.owner.login),\\(.name)\"' | cat"
    if use_init_date:
        command_template = "gh search repos props.initial-ci-review-date:[TEMPLATE_DATE] --archived=false --include-forks=false --owner=[ORG_NAME] --limit 200 --json owner,name --jq '.[] | \"\\(.owner.login),\\(.name)\"' | cat"
    with open("audit_setup.sh","w") as shell:
        for org in orgs:
            for day in date_list:
                command = command_template.replace("[TEMPLATE_DATE]",day).replace("[ORG_NAME]",org)
                shell.write(command + "\n")
                shell.write("sleep 2\n")

def get_quarter_date_range(quarter:int) -> tuple[str,str]:
    """
    Given a quarter of the year (1,2,3,4), returns a tuple of strings representing
    the start and end dates of that quarter in the format "YYYY-MM-DD".
    """
    start:str = ""
    end:str = ""
    year:str = datetime.today().strftime("%Y-")
    if quarter == 1:
        start = year + "01-01"
        end = year + "03-31"
    elif quarter == 2:
        start = year + "04-01"
        end = year + "06-30"
    elif quarter == 3:
        start = year + "07-01"
        end = year + "09-30"
    else:
        start = year + "10-01"
        end = year + "12-31"
    return start, end

def get_date_list(start:str="",end:str="",quarter:int=-1,use_range:bool=False) -> list[str]:
    """
    Generate a list of dates for a given quarter or a range of dates.

    Generates a list of dates, given a start date, end date, and a quarter.
    If `use_range` is True, the start date and end date are used. If `use_range`
    is False, the start date and end date are determined by the quarter.

    Args:
        start (str): Start date of the date range (inclusive) in the format
            "YYYY-MM-DD".
        end (str): End date of the date range (inclusive) in the format "YYYY-MM-DD".
        quarter (int): The quarter to generate the date list for.
        use_range (bool): If true, use the start and end dates as the range.
            Otherwise, use the quarter to determine the range.

    Returns:
        list[str]: A list of dates in the format "YYYY-MM-DD".
    """
    start_date:str = start
    end_date:str = end
    if not use_range:
        start_date,end_date = get_quarter_date_range(quarter)
    init:datetime = datetime.strptime(start_date,"%Y-%m-%d")
    final:datetime = datetime.strptime(end_date,"%Y-%m-%d")

    delta_days = (final - init).days + 1

    date_list:list[str] = []
    for x in range(0,delta_days):
        date_list.append((final - timedelta(days=x)).strftime("%Y-%m-%d"))
    date_list.reverse()
    return date_list

def parse_args() -> tuple[str,str,int,list[str],bool]:
    """
    Parse the command line arguments passed to the script

    Returns:
        tuple[str,str,int,list[str],bool]:
            start (str): The start date for the audit
            end (str): The end date for the audit
            quarter (int): The quarter to start the audit for
            org_names (list[str]): The list of GitHub organization names
            use_init (bool): Specify whether or not to use initial-ci-review-date custom property
    """
    parser = argparse.ArgumentParser(description="The setup-ci-audit script generates a list of repositories that will be audited for this quarter")
    parser.add_argument("-q","--quarter",dest="quarter",type=int,metavar="quarter(1,2,3,4)", help="The quarter to start the audit for")
    parser.add_argument("-s","--start",dest="start",type=str,metavar="START (YYYY-MM-DD)", help="Specify a start date for audit prep within a date range")
    parser.add_argument("-e","--end",dest="end",type=str,metavar="END (YYYY-MM-DD)", help="Specify an end date for audit prep within a date range")
    parser.add_argument("-i","--use-initial-ci-review-date",dest="use_init",action="store_true",help="Specify whether or not to use initial-ci-review-date custom property")
    parser.add_argument("-o", "--org", type=str, nargs="+", default=["hashgraph"], dest="org_names", help="GitHub organization name (default: hashgraph)")

    args:argparse.Namespace = parser.parse_args()

    org_names:list[str] = args.org_names
    if args.org_names is None or args.org_names == [] or "" in args.org_names:
        print("No organization name provided. Using default: hashgraph")
        org_names = ["hashgraph"]

    check_quarter:bool = True
    if args.start is not None and args.end is not None:
        check_quarter = False

    quarter:int = -1
    if check_quarter and args.quarter in [1,2,3,4]:
        quarter = args.quarter

    start:str = ""
    end:str = ""
    if not check_quarter:
        if len(args.start) != 10:
            raise RuntimeError("Start date must be formatted as YYYY-MM-DD")
        else:
            start = args.start
        if len(args.end) != 10:
            raise RuntimeError("End date must be formatted as YYYY-MM-DD")
        else:
            end = args.end
    
    return start, end, quarter, org_names, args.use_init

def main():
    """
    Main entrypoint for the script

    Parses command line arguments, and if valid, generates a list of dates
    to query the GitHub API with. Calls the `run_gh_query` function with the
    generated date list and the parsed arguments.

    If an exception occurs during execution, it will be caught, printed, and
    the script will exit with a non-zero status code.
    """
    try:
        start, end, quarter, org_names, use_init = parse_args()
        print("Start date:", start, "\nEnd date:", end, "\nQuarter:", quarter, "\nOrgs:", org_names, "\nUse Initial Date:", use_init)
        use_date_range:bool = quarter not in [1,2,3,4]
        date_list:list[str] = get_date_list(start=start,end=end,quarter=quarter,use_range=use_date_range)
        print("Running GitHub query")
        run_gh_query(date_list=date_list, orgs=org_names, use_init_date=use_init)
    except Exception as e:
        print(e)
        sys.exit(1) # error code

if __name__ == "__main__":
    main()
    sys.exit(0) # clean execution
