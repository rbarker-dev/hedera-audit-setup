# CI/CD Repository Audit

**Description**:
Perform repository audit.

**If there has not been a significant commit in the last year, add a note indicating so.**
**Skip to `Acceptance Criteria` section at the bottom to complete close this issue.**

# Administrative Audit Criteria

### Actions State
If actions have not been run in the previous 6 months they should be disabled:
- [ ] Actions are/have been disabled

If actions have run in the last 6 months then actions shall remain enabled:
- [ ] Actions are enabled

## Settings Window
### General Tab
- [ ] Require contributors to sign off on web-based commits

#### Features Section:
- [ ] Disable Wiki
  - If it is in use, leave Wiki enabled. If not in use, remove functionality (uncheck Wiki option). Should be disabled whenever possible.
- [ ] Enable Issues
- [ ] Enable Preserve this Repository
- [ ] Enable Discussions if repository is public
- [ ] Enable Projects
  
#### Pull Requests Section:
- [ ] Enable Allow Squash Merging
- [ ] Enable Always suggest updating pull request branches
- [ ] Enable Automatically delete head branches
 
#### Pushes Section:
- [ ] Pushes: Limit how many branches and tags can be updated in a single push (Default # is 5)

### Collaborators and Teams Tab
- [ ] Teams are assigned to the repository
- [ ] Individual contributors that are part of assigned teams are removed from contributors list

### Branches Tab
- [ ] Individual branch protections are turned off

### Tags Tab
- [ ] Individual tag protections are turned off

### Rules/Rulesets Tab
- [ ] The repository uses the current rulesets
- [ ] If appropriate, global rules are enabled/disabled for the repo

### Actions Tab
**If actions are enabled**:
- [ ] Codecov is enabled on the repository
- [ ] Title check is enabled
- [ ] DCO check is enabled

### Webhooks Tab
- [ ] All webhooks present are needed and in use
- [ ] Snyk is enabled on the repo (check to see if the webhook exists and is in use)

### Code Security Tab
- [ ] Dependabot is enabled on the repository

### Secrets and Variables Tab
- [ ] GitHub secrets are employed to store sensitive data
- [ ] Tokens are stored securely as GitHub Secrets

### GitHub Apps
- [ ] Code Coverage Reporting
- [ ] CodeQL is enabled on the repository
- [ ] Codacy is enabled on the repository

## App Integrations
- [ ] Dependabot is configured to monitor all relevant ecosystems (verify through `dependabot.yaml` file)
  - Link to [relevant ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- [ ] DCO-2 is configured as the DCO check

## Code Formatting
- [ ] NodeJS Projects use ESLint/Prettier formatting
- [ ] Java Projects use Checkstyle/Spotless formatting
- [ ] CPP Projects use Clang Tidy
- [ ] Rust
- [ ] Swift
- [ ] Go

## CODEOWNERS
- [ ] `.github/CODEOWNERS` is valid and up-to-date

# Workflow Audit Criteria

## Security Checks in Workflows
- [ ] Secrets Management In Workflow Files (`/.github/workflows/`)
  - [ ] No hardcoded secrets in the workflow files or code
  - [ ] Secrets are referenced in CI via config files or environment variables
- [ ] Executable Path Integrity
  - [ ] Integrity checks for executables are implemented
    - integrity checks should use either checksums or cryptographic hashes for verification
  - [ ] Checksums/hashes are verified during CI process to detect unauthorized changes
  - [ ] Expected checksums/hashes are stored securely and referenced through the CI pipeline
  - [ ] Use pinned versions of Docker files
- [ ] `npx playwright install deps` is used to install OS dependencies instead of `aptitude`

## Workflow checks

- [ ] Appropriate permissions are set within the GitHub workflows
- [ ] All steps are named
- [ ] All workflow actions are using pinned commits
- [ ] The step-security hardened security action is enabled on each workflow job
  - [ ] If the step-security dashboard reports action with score of <6, request a step-security version of the action

## Self Hosted Runners

- [ ] The Repository is using the latitude runner group label for the `runs-on` stanza

## Build Process Best Practices
- [ ] The build system implemented in the repo adheres to best practices. See [best practices](https://github.com/PandasWhoCode/gh-audit-setup/blob/main/best-practices.md) for details.

## Other

- [ ] *If Applicable*: Alert repository owners of software versions that are no longer supported
- [ ] *If Applicable*: Alert repository owners when software versions are within 3 months of losing support

---

## Acceptance Criteria

- [ ] All Audit Criteria have been met
- [ ] Inactive Repo (>1 year since last significant commit)
- [ ] Empty Repo

## Custom Properties - Marking Complete

Update the `repo-properties.json` file in the `ORG/governance` repository

- [ ] Custom properties: `initial-ci-review-by-team` is set
- [ ] Custom properties: `initial-ci-review-date` is set (Use format: `YYYY-MM-DD`)
- [ ] Custom properties: `last-ci-review-by-team` is set
- [ ] Custom properties: `last-ci-review-date` is set (Use format: `YYYY-MM-DD`)

*Note: assumes `ORG/governance` is a valid repository in the Github Organization being audited*
