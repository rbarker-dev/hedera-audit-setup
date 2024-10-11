# CI/CD Repository Audit

**Description**:
Perform repository audit

---

## Contents

::TODO::
Update the links below
- [CI/CD Repository Audit](#cicd-repository-audit)
  - [Contents](#contents)
  - [Administrative Audit Criteria](#administrative-audit-criteria)
    - [Check Actions State](#check-actions-state)
    - [Check if Actions should be disabled](#check-if-actions-should-be-disabled)
    - [Repository Settings Checks](#repository-settings-checks)
    - [App Integrations](#app-integrations)
    - [Security Checks](#security-checks)
    - [Custom Properties](#custom-properties)
  - [Non-Administrative Audit Criteria](#non-administrative-audit-criteria)
    - [Dependabot](#dependabot)
    - [Workflow checks](#workflow-checks)
    - [Self Hosted Runners](#self-hosted-runners)
    - [CODEOWNERS](#codeowners)
    - [Other](#other)
  - [Repository Settings](#repository-settings)
  - [Acceptance Criteria](#acceptance-criteria)

## Administrative Audit Criteria

### Actions State
Actions are:
- [ ] Enabled
- [ ] Disabled

**If actions have not been run in the previous 6 months they should be disabled**:
- [ ] Actions have been disabled on the inactive repository

**Check if actions have run in the last 6 months**:
- [ ] Actions have run in the last 6 months and shall remain enabled

# Settings
- [ ] Repository settings are configured per organization standard (listed below)

## General Tab
- [ ] Require contributors to sign off on web-based commits

### Features Section:
- [ ] Disable Wiki
  - If it is in use, leave Wiki enabled. If not in use, remove functionality (uncheck Wiki option).
- [ ] Enable Issues
- [ ] Enable Preserve this Repository
- [ ] Enable Discussions
- [ ] Enable Projects
  
### Pull Requests Section:
- [ ] Enable Allow Squash Merging
- [ ] Enable Always suggest updating pull request branches
- [ ] Enable Automatically delete head branches
 
### Pushes Section:
- [ ] Pushes: Limit how many branches and tags can be updated in a single push

## Branches Tab
- [ ] Individual branch protections are turned off

## Tags Tab
- [ ] Individual tag protections are turned off

## Rules/Rulesets Tab
- [ ] The repository uses the current rulesets
- [ ] Teams are assigned to the repository
- [ ] Individual contributors that are part of assigned teams are removed from contributors list
- [ ] All webhooks present are needed and in use

### App Integrations

**If actions are enabled**:

- [ ] Dependabot is enabled on the repository
- [ ] Codecov is enabled on the repository

### Security Checks

- [ ] Snyk is enabled on the repository
- [ ] Dependabot is configured to monitor all relevant ecosystems
  - npm
  - electron
  - github actions
  - etc.
- [ ] Secrets Management
  - [ ] No hardcoded secrets in the workflow files or code
  - [ ] GitHub secrets are employed to store sensitive data
  - [ ] Secrets are referenced in CI via config files or environment variables
- [ ] Tokens are stored securely as GitHub Secrets
- [ ] Executable Path Integrity
  - [ ] Integrity checks for executables are implemented
    - integrity checks should use either checksums or cryptographic hashes for verification
  - [ ] Checksums/hashes are verified during CI process to detect unathorized changes
  - [ ] Expected checksums/hashes are stored securely and referenced through the CI pipeline
- [ ] Code Coverage Reporting - Configure codecov on the repository
- [ ] CodeQL is enabled on the repository
- [ ] `npx playwright install deps` is used to install OS dependencies instead of `aptitude`
- [ ] Code Formatting
  - [ ] ESLint rules are applied to the codebase
  - [ ] Prettier Formatting rules are applied to the codebase


## Non-Administrative Audit Criteria

### Dependabot

- [ ] dependabot.yml is up to date

### Workflow checks

- [ ] Appropriate permissions are set within the github workflows
- [ ] All steps are named
- [ ] All workflow actions are using pinned commits
- [ ] The Step-Security Hardened Security action is enabled on each workflow job
- [ ] Ensure no hard-coded keys in workflows
  - [ ] Alert devops-ci administrative team if new github secrets are needed to resolve hard-coded keys

### Self Hosted Runners

- [ ] The Repository is using the latitude runner group label for the `runs-on` stanza

### CODEOWNERS

- [ ] `.github/CODEOWNERS` is valid and up-to-date

### Other

- [ ] *If Applicable*: Alert repository owners of software versions that are no longer supported
- [ ] *If Applicable*: Alert repository owners when software versions are within 3 months of losing support

---

## Acceptance Criteria

- [ ] All Audit Criteria have been met

## Custom Properties - Marking Complete

- [ ] Custom properties: `last-ci-review-by-team` is set
- [ ] Custom properties: `last-ci-review-date` is set (Use format: `YYYY-MM-DD`)