#!/bin/bash

# Create and use temp directory
rm -rf /tmp/ceph-mon
mkdir -p /tmp/ceph-mon
cd /tmp/ceph-mon

# Create "run" dir for services
mkdir -p /var/run/ceph

# Create data dir
mkdir -p /var/lib/ceph/mon/ceph-${mon_id}

<#if bootstrap>
# Create monitors map
monmaptool --create --add ${mon_id} <#list monitors as m><#if m.id == mon_id>${m.addr}</#if></#list> --print monmap

# Generate OSDs map
osdmaptool --create-from-conf osdmap -c /etc/ceph/ceph.conf

# Generate monitor keyring
cp /etc/ceph/keyring keyring.mon
ceph-authtool -n client.admin --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow' keyring.mon
ceph-authtool --gen-key -n mon. keyring.mon

# Configure monitor
ceph-mon -c /etc/ceph/ceph.conf --mkfs -i ${mon_id} --monmap monmap --osdmap osdmap -k keyring.mon
<#else>
# Retrieve monitors keyring and map
ceph auth get mon. -o keyring.mon <#if mon_addr??>-m ${mon_addr}</#if>
ceph mon getmap -o monmap <#if mon_addr??>-m ${mon_addr}</#if>

# Configure monitor
ceph-mon -i ${mon_id} --mkfs --monmap monmap --keyring keyring.mon
</#if>

# Setup service
chkconfig ceph on