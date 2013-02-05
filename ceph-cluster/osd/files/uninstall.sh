#!/bin/bash

service ceph stop osd.${osd_id}
rm -rf /var/lib/ceph/osd/ceph-${osd_id}
