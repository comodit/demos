#!/bin/sh

<#if clear_data_on_uninstall>rm -rf /var/lib/mysql</#if>
rm -rf /usr/share/comodit/mysql
