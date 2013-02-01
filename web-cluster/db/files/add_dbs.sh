#!/bin/sh

<#if dbs??>
# Setup databases
<#list dbs as db>
cat <<EOF > /tmp/script.sql
CREATE DATABASE ${db} ;
EOF
mysql -u root --password=${root_pass} < /tmp/script.sql
</#list>
</#if>

rm -f /tmp/script.sql