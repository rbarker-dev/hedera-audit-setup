echo "Calling Python:"
python3 setup-ci-audit.py -q 2 -i
echo "Changing permissions on audit_setup.sh"
chmod 755 audit_setup.sh
echo "Calling audit_setup.sh (takes a bit)"
./audit_setup.sh > 2024-Q3-audit_list.txt
rm audit_setup.sh
cat 2024-Q3-audit_list.txt