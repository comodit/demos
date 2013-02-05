#!/bin/bash

# Create and use temp directory
rm -rf /tmp/ceph-osd
mkdir -p /tmp/ceph-osd
cd /tmp/ceph-osd

# Create "run" dir for services
mkdir -p /var/run/ceph

# Create and register OSD
mkdir -p /var/lib/ceph/osd/ceph-${osd_id}
ceph-osd -i ${osd_id} --mkfs --mkkey

# Setup service
chkconfig ceph on