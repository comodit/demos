#!/bin/sh -e
<#if users??>
  <#list users as user>
mongo ${user.database} --eval 'db.addUser("${user.username}", "${user.password}")'
  </#list>
</#if>
