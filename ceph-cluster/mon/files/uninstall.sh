#!/bin/bash

service ceph stop mon.${mon_id}
ceph mon remove ${mon_id}
rm -rf /var/lib/ceph/mon/ceph-${mon_id}
