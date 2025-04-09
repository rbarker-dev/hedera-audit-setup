# !/bin/bash

set -e

DRY_RUN=0 # Default so dry-run is disabled
ACTIVE_DAYS=365 # Default active days
ORG_LIST=()

while getopts "a:r:s:e:o:q:d" opt; do
  case $opt in
    a) AUDIT_LIST_FILE="$OPTARG" ;;
    r) ACTIVE_DAYS="$OPTARG" ;;
    s) START_DATE="$OPTARG" ;;
    e) END_DATE="$OPTARG" ;;
    q) QUARTER="$OPTARG" ;;
    o) ORGS="$OPTARG" ;;
    d) DRY_RUN=1 ;;
    *) echo "Usage: $0 -a AUDIT_LIST_FILE -s START_DATE -e END_DATE -q QUARTER -o \"ORG1 ORG2 ...\" [-r ACTIVE_DAYS] [-d]" >&2; exit 1 ;;
  esac
done

if [[ -z "${AUDIT_LIST_FILE}" ]]; then
  echo "Audit list file is required."
  exit 1
fi

if [[ -z "${START_DATE}" ]]; then
  echo "Start date is required."
  exit 1
fi

if [[ -z "${END_DATE}" ]]; then
  echo "End date is required."
  exit 1
fi

if [[ -z "${ORGS}" ]]; then
  echo "Organizations are required. Using default (hashgraph)"
  ORG_LIST=("hashgraph")
else
  IFS=' ' read -r -a ORG_LIST <<< "$ORGS"
fi

if [[ -z "${QUARTER}" ]]; then
  echo "Error: Quarter is required." >&2
  exit 1
fi

if [[ ! "$QUARTER" =~ ^Q[1-4]$ ]]; then
  echo "Error: Quarter must be one of: Q1, Q2, Q3, Q4" >&2
  exit 1
fi

if ! [[ "$ACTIVE_DAYS" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: ACTIVE_DAYS must be a positive integer greater than 0." >&2
  exit 1
fi

echo "Dry run: ${DRY_RUN}"
echo "Audit list file: ${AUDIT_LIST_FILE}"
echo "Start date: ${START_DATE}"
echo "End date: ${END_DATE}"
echo "Quarter: ${QUARTER}"
echo "Active days: ${ACTIVE_DAYS}"
echo "Organizations: ${ORG_LIST}"

echo "Calling Python to generate audit_setup.sh"
python3 setup-ci-audit.py --start "${START_DATE}" --end "${END_DATE}" --use-initial-ci-review-date --org "${ORG_LIST[@]}"

echo "Changing permissions on audit_setup.sh"
chmod 755 audit_setup.sh

echo "Calling audit_setup.sh (takes a bit)"
./audit_setup.sh > ${AUDIT_LIST_FILE}

echo "Calling Python to generate audit_issue_gen.sh"
python3 audit_issue_script_generator.py --file "${AUDIT_LIST_FILE}" --quarter "${QUARTER}" --active-days ${ACTIVE_DAYS}

if [ $DRY_RUN -eq 1 ]; then
  echo "Skipping audit_issue_gen.sh because of dry run mode"
else
  echo "Changing permissions on audit_issue_gen.sh"
  chmod 755 audit_issue_gen.sh

  echo "Running audit_issue_gen.sh"
  ./audit_issue_gen.sh
fi

echo "Clean up"
rm audit_setup.sh
rm audit_issue_gen.sh

echo "Complete."

set +e
