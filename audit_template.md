# CI/CD Quarterly Audit

**Description**:
Perform quarterly CI/CD audit

---

## Administrative Audit Criteria

- [ ] Actions are enabled
- [ ] Actions are disabled

### Check if Actions should be disabled

**If actions have not been run in the previous 6 months they should be disabled**:

- [ ] Actions have run in the last 6 months and shall remain enabled
- [ ] Actions have been disabled on the inactive repository

### Repository Settings Checks

- [ ] [Repository settings](#repository-settings) are configured per organization standard
- [ ] Individual branch protections are turned off
- [ ] Individual tag protections are turned off
- [ ] The repository uses the current rulesets
- [ ] Teams are assigned to the repository
- [ ] Individual contributors that are part of assigned teams are removed from contributors list
- [ ] All webhooks present are needed and in use

### App Integrations

- [ ] Snyk is enabled on the repository

**If actions are enabled**:

- [ ] Dependabot is enabled on the repository
- [ ] Codecov is enabled on the repository
- [ ] CODECOV_TOKEN is configured on the repository
- [ ] Codacy is enabled on the repository
- [ ] Codacy is configured on the repository
- [ ] Ensure there are no hard-coded keys in the workflows
  - [ ] Necessary keys are captured as github secrets

### Custom Properties

- [ ] Custom properties: `last-ci-review-by-team` is set
- [ ] Custom properties: `last-ci-review-date` is set (Use format: `YYYY-MM-DD`)

## Non-Administrative Audit Criteria

### Dependabot

- [ ] dependabot.yml is up to date

### Workflow checks

- [ ] Appropriate permissions are set within the github workflows
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

## Repository Settings

- [x] Require contributors to sign off on web-based commits
- [x] Features: Issues
- [x] Features: Preserve this Repository
- [x] Features: Discussions
- [x] Features: Projects
- [x] Pull Requests: Allow Squash Merging
- [x] Pull Requests: Always suggest updating pull request branches
- [x] Pull Requests: Automatically delete head branches
- [x] Pushes: Limit how many branches and tags can be updated in a single push

---

## Acceptance Criteria

- [ ] All Audit Criteria have been met
