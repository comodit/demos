#!/bin/sh

(
nsupdate -k /var/named/${domain}.key /var/lib/comodit/applications/bind-server/nsupdate.conf
) >> /var/log/comodit/openshift-bind-server/configure.log 2>&1