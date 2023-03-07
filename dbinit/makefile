dbinit.sql: base.sql data.sql
	cat $^ > $@

data.sql:
	./import.py > $@
