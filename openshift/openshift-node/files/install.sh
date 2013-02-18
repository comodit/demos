#!/bin/sh

mkdir -p /var/log/comodit/openshift-node/

(

# Disable iptables
/bin/systemctl stop iptables.service
/bin/systemctl disable iptables.service

# Patch to enable openshift-cgroups service to start
/bin/patch -t -p1 /bin/oo-admin-ctl-cgroups < /var/lib/comodit/applications/openshift-node/systemd.patch

# Restart mcollective server to integrate node gem
/bin/systemctl restart mcollective.service

) > /var/log/comodit/openshift-node/install.log 2>&1
