import subprocess
import json
from datetime import datetime, timedelta

def get_repositories(org_name):
  """Retrieve all repositories in an organization using gh CLI."""
  try:
    result = subprocess.run(
        ["gh", "repo", "list", org_name, "--json", "name,updatedAt", "--limit", "1000"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)
  except subprocess.CalledProcessError as e:
    print(f"Error retrieving repositories: {e.stderr}")
    return []

def filter_active_repos(repositories, days=365):
  """Filter repositories updated within the last specified days."""
  cutoff_date = datetime.utcnow() - timedelta(days=days)
  active_repos = [
    repo["name"]
    for repo in repositories
    if datetime.strptime(repo["updatedAt"], "%Y-%m-%dT%H:%M:%SZ") > cutoff_date
  ]
  return active_repos

def main():
  org_name = input("Enter the organization name: ").strip()
  print("Fetching repositories...")
  repositories = get_repositories(org_name)
  if not repositories:
    print("No repositories found or an error occurred.")
    return

  active_repos = filter_active_repos(repositories)
  if active_repos:
    print("\nActive repositories (updated in the last year):")
    for repo in active_repos:
      print(f"- {repo}")
  else:
    print("\nNo repositories were active in the last year.")

if __name__ == "__main__":
  main()
