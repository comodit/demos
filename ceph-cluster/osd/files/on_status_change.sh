#!/bin/bash

<#if status == "in">
ceph osd create `cat /var/lib/ceph/osd/ceph-${osd_id}/fsid`
ceph auth add osd.${osd_id} osd 'allow *' mon 'allow rwx' -i /var/lib/ceph/osd/ceph-${osd_id}/keyring
service ceph start osd.${osd_id}
ceph osd crush set osd.${osd_id} 1.0 root=default
ceph osd in ${osd_id}
<#else>
ceph osd out ${osd_id}
service ceph stop osd.${osd_id}
ceph osd crush remove osd.${osd_id}
ceph auth del osd.${osd_id}
ceph osd rm ${osd_id}
</#if>
