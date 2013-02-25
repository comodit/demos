#!/bin/sh

(
set -e

/bin/patch -t -p1 -d /usr/libexec/mcollective/ < /var/lib/comodit/applications/mcollective-client/bug-892764.patch

echo -----

) > /var/log/comodit/mcollective-client/install.log 2>&1