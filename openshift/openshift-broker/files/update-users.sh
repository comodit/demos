#!/bin/sh

(

touch /etc/openshift/htpasswd
<#if users??>
  <#list users as user>
htpasswd -b /etc/openshift/htpasswd ##user.username## ##user.password##
  </#list>
</#if>

) >> /var/log/comodot/openshift-broker/update-users.log 2>&1