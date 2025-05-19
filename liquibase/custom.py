from liquibase_checks_python import liquibase_utilities as lb
import sys

obj = lb.get_database_object()
status = lb.get_status()

if lb.is_table(obj):
	status.fired = True
	status.message = "No tables allowed!"
	sys.exit(1)