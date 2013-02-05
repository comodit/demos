#!/bin/bash

<#if status == "up">
service ceph start mon.${mon_id}
<#if !bootstrap>
ceph mon add ${mon_id} <#list monitors as m><#if m.id == mon_id>${m.addr}</#if></#list> <#if mon_addr??>-m ${mon_addr}</#if>
</#if>
<#else>
ceph mon remove ${mon_id} <#if mon_addr??>-m ${mon_addr}</#if>
service ceph stop mon.${mon_id}
</#if>