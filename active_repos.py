import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ACTIVE_REPOS_FILE:str = "active_repos.csv"

def write_to_file(repositories:list[dict]) -> bool:
  """Write the repo list to a .csv file."""
  file_was_written:bool = False
  try:
    with open(ACTIVE_REPOS_FILE, "w") as file:
      for repo in repositories:
        file.write(f"{repo['org']},{repo['name']}\n")
      file_was_written = True
  except Exception as e:
    print(f"Error writing to file: {e}")
  return file_was_written

def get_repositories(orgs:list[str]) -> dict[str, list[dict]]:
  """Retrieve all repositories in an organization using gh CLI."""
  repo_list:dict[str,list[dict]] = {}
  for org in orgs:
    try:
      result = subprocess.run(
          ["gh", "repo", "list", org, "--json", "name,updatedAt", "--limit", "1000"],
          capture_output=True,
          text=True,
          check=True,
      )
      repo_list[org] = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
      print(f"Error retrieving repositories: {e.stderr}")
      repo_list[org] = []
  return repo_list

def filter_active_repos(repositories:dict[str,list[dict]], days:int=365) -> list[dict]:
  """Filter repositories updated within the last specified days."""
  cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
  active_repos:list[dict] = []
  for org,repository_set in repositories.items():
    for repo in repository_set:
      if datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00")) > cutoff_date:
        active_repos.append(
          dict(
            org=org,
            name=repo["name"],
            updated_time=datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00")))
        )
  return active_repos

def write_active_repos_file(orgs:list[str], days:int) -> bool:
  """
  List all active repositories in the given organization(s) that have been updated
  within the last time period.

  Args:
    orgs (list[str]): List of GitHub organization names
    days (int): Number of days to check for activity
  Returns:
    bool: True if successful, False otherwise

  Prints a list of active repositories, sorted in descending order by updated_time date.
  """
  wrote_file:bool = False
  repositories:dict[str,list[dict]] = get_repositories(orgs=orgs)

  if not repositories:
    print("No repositories found or an error occurred.")

  active_repos = filter_active_repos(repositories=repositories, days=days)
  if active_repos:
    print(f"\nActive repositories (updated in the last {days} days):")
    for repo in active_repos:
      print(f"- {repo['org']}/{repo['name']} (Last updated: {repo['updated_time'].strftime('%Y-%m-%d %H:%M:%S %Z')})")

    wrote_file = write_to_file(repositories=active_repos)
    if not wrote_file:
      print("Error writing to file.")
  else:
    print(f"\nNo repositories were active in the last {days} days.")
  return wrote_file

def parse_args() -> tuple[list[str],int]:
  """
  Parse command line arguments.

  Returns:
      org_names (list[str]): List of GitHub organization names
      days (int): Number of days to check for activity
  """
  parser = argparse.ArgumentParser(description="List active repositories in an organization.")
  parser.add_argument("-o", "--org", type=str, nargs="+", default=["hashgraph"], dest="org_names", help="GitHub organization name (default: hashgraph)")
  parser.add_argument("-d", "--days", type=int, default=365, dest="days", help="Number of days to check for activity (default: 365)")

  org_names:list[str] = []
  days:int = 0
  args:argparse.Namespace = parser.parse_args()

  if args.org_names is None or args.org_names == [] or "" in args.org_names:
    print("No organization name provided. Using default: hashgraph")
    org_names = ["hashgraph"]
  else:
    org_names = args.org_names

  if args.days is None or args.days <= 0:
    print("No days provided. Using default: 365")
    days = 365
  else:
    days = args.days

  return org_names, days

def main():
  org_names, days = parse_args() # org_name is a list of strings; days is a positive int
  if not write_active_repos_file(orgs=org_names, days=days):
    sys.exit(1)

if __name__ == "__main__":
  main()
