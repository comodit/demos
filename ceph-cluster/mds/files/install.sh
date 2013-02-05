#!/bin/bash

# Create and use temp directory
rm -rf /tmp/ceph-mds
mkdir -p /tmp/ceph-mds
cd /tmp/ceph-mds

# Create "run" dir for services
mkdir -p /var/run/ceph

# Create and register key
mkdir -p /var/lib/ceph/mds/ceph-${mds_id}
ceph-authtool --create-keyring --gen-key -n mds.${mds_id} /var/lib/ceph/mds/ceph-${mds_id}/keyring
ceph auth add mds.${mds_id} osd 'allow *' mon 'allow rwx' mds 'allow' -i /var/lib/ceph/mds/ceph-${mds_id}/keyring

# Setup service
chkconfig ceph on
service ceph start