#!/bin/sh

(
# Exit on errors
set -e

nsupdate -k /var/named/${domain}.key /var/lib/comodit/applications/bind-server/nsupdate.conf

echo -----
) >> /var/log/comodit/openshift-bind-server/configure.log 2>&1