echo "Calling Python:"
python3 setup-ci-audit.py --start 2024-05-16 --end 2024-06-30 --use-initial-ci-review-date
echo "Changing permissions on audit_setup.sh"
chmod 755 audit_setup.sh
echo "Calling audit_setup.sh (takes a bit)"
./audit_setup.sh > 2024-Q3-audit_list_pt_2.txt
rm audit_setup.sh
echo "Complete."