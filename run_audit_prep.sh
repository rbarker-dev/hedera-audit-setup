# pull in arguments

# $1 = output_file_name
if [[ -z "$1" ]]; then
  echo "Please provide an output file name as the first argument. (example: 2025-Q2-audit-list.txt")
  exit 1
fi

# $2 = start_date
if [[ -z "$2" ]]; then
  echo "Please provide a start date as the second argument. (example: 2025-01-01)"
  exit 1
fi

# $3 = end_date
if [[ -z "$3" ]]; then
  echo "Please provide an end date as the third argument. (example: 2025-12-31)"
  exit 1
fi

export AUDIT_LIST_FILE=$1
export START_DATE=$2
export END_DATE=$3

echo "Calling Python:"
python3 setup-ci-audit.py --start "${START_DATE}" --end "${END_DATE}" --use-initial-ci-review-date --org "hashgraph" "hiero-ledger" "swirlds" "swirldslabs"
echo "Changing permissions on audit_setup.sh"
chmod 755 audit_setup.sh
echo "Calling audit_setup.sh (takes a bit)"
./audit_setup.sh > ${AUDIT_LIST_FILE}
rm audit_setup.sh
echo "Complete."
