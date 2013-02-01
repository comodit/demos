#!/bin/sh

<#if users??>
# Setup users
<#list users as u>
cat <<EOF > /tmp/script.sql
<#if u.host??>
CREATE USER '${u.name}'@'${u.host}' IDENTIFIED BY '${u.password}' ;
<#else>
CREATE USER '${u.name}'@localhost IDENTIFIED BY '${u.password}' ;
</#if>
EOF
mysql -u root --password=${root_pass} < /tmp/script.sql
</#list>
</#if>

rm -f /tmp/script.sql