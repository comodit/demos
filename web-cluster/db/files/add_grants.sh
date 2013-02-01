#!/bin/sh

<#if grants??>
# Setup grants
<#list grants as g>
cat <<EOF > /tmp/script.sql
GRANT ${g.priv_type} ON ${g.db}.${g.tab} TO '${g.user}'@'${g.host}' ;
EOF
mysql -u root --password=${root_pass} < /tmp/script.sql
</#list>
</#if>

rm -f /tmp/script.sql