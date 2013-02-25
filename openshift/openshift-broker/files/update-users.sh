#!/bin/sh

(
# Exit on errors
set -e

touch /etc/openshift/htpasswd
<#if users??>
  <#list users as user>
htpasswd -b /etc/openshift/htpasswd ${user.username} ${user.password}
  </#list>
</#if>

echo -----

) >> /var/log/comodit/openshift-broker/update-users.log 2>&1