# CI/CD Quarterly Audit

- Description: Perform quarterly CI/CD audit

## Audit Criteria

- [ ] All workflow items are using pinned actions
- [ ] Appropriate permissions are set within the github workflows
- [ ] Dependabot is enabled on the repository
- [ ] The Repository is using self-hosted runners (if appropriate)
- [ ] The repository uses the current rulesets
- [ ] Individual branch protections are turned off
- [ ] Individual tag protections are turned off
- [ ] The Step-Security Hardened Security action is enabled
- [ ] CODEOWNERS is valid and up-to-date
- [ ] Teams are assigned to the repository
- [ ] Individual contributors that are part of assigned teams are removed from contributors list
- [ ] Actions are disabled if not in use within last 6 months
- [ ] [Repository settings](#repository-settings) are configured per organization standard
- [ ] All webhooks present are needed and in use
- [ ] *If Applicable*: Alert repository owners of software versions that are no longer supported
- [ ] *If Applicable*: Alert repository owners when software versions are within 3 months of losing support
- [ ] Custom properties: `last-ci-review-by-team` is set
- [ ] Custom properties: `last-ci-review-date` is set (Use format: `YYYY-MM-DD`)

### Repository Settings

- [x] Require contributors to sign off on web-based commits
- [x] Features: Issues
- [x] Features: Preserve this Repository
- [x] Features: Discussions
- [x] Features: Projects
- [x] Pull Requests: Allow Squash Merging
- [x] Pull Requests: Always suggest updating pull request branches
- [x] Pull Requests: Automatically delete head branches
- [x] Pushes: Limit how many branches and tags can be updated in a single push

## Acceptance Criteria

- [ ] All Audit Criteria have been met
