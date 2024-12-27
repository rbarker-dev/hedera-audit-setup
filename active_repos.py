import subprocess
import json
from datetime import datetime, timedelta, timezone

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
  cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
  active_repos = [
    {
      "name": repo["name"],
      "updatedAt": datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00")),
    }
    for repo in repositories
    if datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00")) > cutoff_date
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
    # Sort by updatedAt in descending order (newest to oldest)
    active_repos.sort(key=lambda repo: repo["updatedAt"], reverse=True)

    print("\nActive repositories (updated in the last year):")
    for repo in active_repos:
      print(f"- {repo['name']} (Last updated: {repo['updatedAt'].strftime('%Y-%m-%d %H:%M:%S %Z')})")
  else:
    print("\nNo repositories were active in the last year.")

if __name__ == "__main__":
  main()
