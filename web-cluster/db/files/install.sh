#!/bin/sh

SCRIPTS_DIR=/usr/share/comodit/mysql/

# Ensure service is running
service mysqld start

# Secure install
mysqladmin -f -u root drop test
mysql -u root < $SCRIPTS_DIR/clear_anonymous.sql
mysql -u root < $SCRIPTS_DIR/restrict_access.sql

# Set root password
mysqladmin -u root password ${root_pass}
