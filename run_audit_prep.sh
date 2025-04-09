# pull in arguments
# $1 = output_file_name
if [[ -z "$1" ]]; then
  echo "Please provide an output file name as the first argument. (example: 2025-Q2-audit-list.txt")
  exit 1
fi

echo "Calling Python:"
python3 setup-ci-audit.py --start 2024-03-01 --end 2024-05-31 --use-initial-ci-review-date --org "hashgraph" "hiero-ledger" "swirlds" "swirldslabs"
echo "Changing permissions on audit_setup.sh"
chmod 755 audit_setup.sh
echo "Calling audit_setup.sh (takes a bit)"
./audit_setup.sh > $1
rm audit_setup.sh
echo "Complete."
