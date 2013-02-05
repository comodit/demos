#!/bin/bash

service ceph stop mds.${mds_id}
rm -rf /var/lib/ceph/mds/ceph-${mds_id}
