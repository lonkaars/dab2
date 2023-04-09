SQL = mysql
USER = $(shell id -un)
HOST = localhost

.PHONY: clean permissions base data full

all: full

# delete old tables and create new tables
base: base.sql
	$(SQL) < $<

# fill tables with data
data: data.sql
	$(SQL) < $<

# do everything
full: full.sql
	$(SQL) < $<

base.sql: reset.sql init.sql
	cat $^ > $@

data.sql:
	./import.py 2018 > $@

full.sql: base.sql data.sql views.sql functions.sql procedures.sql triggers.sql update.sql
	cat $^ > $@

# grant all database permissions (development only)
permissions:
	echo "grant all privileges on formula1.* to '$(USER)'@'$(HOST)';" | sudo $(SQL)
	echo "grant file on *.* to '$(USER)'@'$(HOST)';" | sudo $(SQL)

# delete generated sql files
clean:
	$(RM) full.sql base.sql data.sql

