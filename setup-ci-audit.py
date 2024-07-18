import argparse
import sys
from datetime import datetime,timedelta

"""
gh search repos props.initial-ci-review-date:2024-05-01 --owner=hashgraph --visibility=public --limit 200 --json name --jq '.[].name' | cat

"""

def run_gh_query(date_list:list[str], use_init_date:bool=False):
    command_template:str = "gh search repos props.last-ci-review-date:[TEMPLATE_DATE] --owner=hashgraph --limit 200 --json name --jq '.[].name' | cat\n"
    if use_init_date == True:
        command_template = "gh search repos props.initial-ci-review-date:[TEMPLATE_DATE] --owner=hashgraph --limit 200 --json name --jq '.[].name' | cat\n"
    with open("audit_setup.sh","w") as shell:
        for day in date_list:
            command = command_template
            shell.write(command.replace("[TEMPLATE_DATE]",day))
            shell.write("sleep 2\n")

def get_quarter_date_range(quarter:int) -> tuple[str,str]:
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
    start_date:str = start
    end_date:str = end
    if use_range:
        start_date,end_date = get_quarter_date_range(quarter)
    init:datetime = datetime.strptime(start_date,"%Y-%m-%d")
    final:datetime = datetime.strptime(end_date,"%Y-%m-%d")

    delta_days = (final - init).days + 1

    dateList:list[str] = []
    for x in range(0,delta_days):
        dateList.append((final - timedelta(days=x)).strftime("%Y-%m-%d"))
    dateList.reverse()
    return dateList

def parse_args() -> tuple[str,str,int,bool]:
    parser = argparse.ArgumentParser(description="The setup-ci-audit script generates a list of repositories that will be audited for this quarter")
    parser.add_argument("-q","--quarter",dest="quarter",type=int,metavar="quarter(1,2,3,4)", help="The quarter to start the audit for")
    parser.add_argument("-s","--start",dest="start",type=str,metavar="START (YYYY-MM-DD)", help="Specify a start date for audit prep within a date range")
    parser.add_argument("-e","--end",dest="end",type=str,metavar="END (YYYY-MM-DD)", help="Specify an end date for audit prep within a date range")
    parser.add_argument("-i","--use-initial-ci-review-date",dest="use_init",action="store_true",help="Specify whether or not to use initial-ci-review-date custom property")

    args = parser.parse_args()
    
    check_quarter:bool = True
    if args.start is not None and args.end is not None:
        check_quarter = False

    quarter:int = -1
    start:str = ""
    end:str = ""
    if check_quarter and args.quarter in [1,2,3,4]:
        raise RuntimeError("Quarter must be of 1, 2, 3, or 4")
    else:
        quarter = args.quarter
    
    if not check_quarter:
        if len(args.start) != 10:
            raise RuntimeError("Start date must be formatted as YYYY-MM-DD")
        else:
            start = args.start
        if len(args.end) != 10:
            raise RuntimeError("End date must be formatted as YYYY-MM-DD")
        else:
            end = args.end

    
    return start, end, quarter, args.use_init

def main():
    try:
        start:str = ""
        end:str = ""
        quarter:int = -1
        start, end, quarter, use_init = parse_args()
        use_date_range:bool = quarter not in [1,2,3,4]
        dateList:list[str] = get_date_list(start=start,end=end,quarter=quarter,use_range=use_date_range)
        run_gh_query(date_list=dateList, use_init_date=use_init)
    except Exception as e:
        print(e)
        sys.exit(1) # error code

if __name__ == "__main__":
    main()
    sys.exit(0) # clean execution
