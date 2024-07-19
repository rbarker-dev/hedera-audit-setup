# Hedera-Audit-Setup README

The Hedera-Audit-Setup Repository is intended to hold the scripts and templates
for configuring an audit within the hashgraph org on github.

## Table of Contents

1. [run_audit_prep.sh](run_audit_prep.sh) - The worker script that generates the audit files
2. [setup-ci-audit.py](setup-ci-audit.py) - Python script that generates a series of gh queries
3. [audit-template.md](audit-template.md) - Default body for audit stories

## Running Audit Setup

The CI/CD Audits are a quarterly task for the DevOps-CI team; these audits are tailored and will
include a subset of all repositories checked. The auditor needs to perform the following tasks

- Update `run_audit_prep.sh` to modify the following information
  - Modify the `--start` and `--end` dates for the `setup-ci-audit.py` script inputs
    - These dates should represent a two month rolling period
  - set or unset the `--use-initial-ci-review-date` flag for the `setup-ci-audit.py` script inputs
  - Update the filename (`2024_Q3_audit_list.txt` for example) used to capture the output of `audit_setup.sh`
    The file should be representative of the audit period. Referred to as the `audit_list`
- Execute `./run_audit_prep.sh` at the command line

## Running Audit_Issue_Script_Generator

- Run the `audit_issue_script_generator.py` script
  - Pass in the appropriate `audit_list` file as `--file audit_list.txt`
- Verify the repositories in `audit_issue_gen.sh` match the repositories in `audit_list`
- Execute `audit_issue_gen.sh` script to generate the issues in the various repos
- Verify that the issues have been created and are on the project board for the quarterly audit
