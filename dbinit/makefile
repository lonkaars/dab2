SQL = mysql
USER = $(shell id -un)
HOST = localhost

.PHONY: clean permissions init data procedures full

all: full

# delete old tables and create new tables
init: base.sql
	$(SQL) < $<

# fill tables with data
data: data.sql
	$(SQL) < $<

# add procedures/sql functions
procedures: procedures.sql
	$(SQL) < $<

# do all of the above in one go
full: full.sql
	$(SQL) < $<

base.sql: reset.sql init.sql
	cat $^ > $@

full.sql: reset.sql init.sql demo.sql views.sql functions.sql procedures.sql
	cat $^ > $@

data.sql:
	./import.py > $@

# grant all database permissions (development only)
permissions:
	echo "grant all privileges on formula1.* to '$(USER)'@'$(HOST)';" | sudo $(SQL)
	echo "grant file on *.* to '$(USER)'@'$(HOST)';" | sudo $(SQL)

# delete generated sql files
clean:
	$(RM) full.sql base.sql data.sql

