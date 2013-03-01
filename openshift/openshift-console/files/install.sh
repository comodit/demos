#!/bin/sh

(

# Exit on error
set -e

# Relax the gem versions
sed -i "s/~>/>=/g" /usr/share/gems/specifications/openshift-origin-console-1.5.5.gemspec
sed -i "s/1.2.4/1.2.3/g" /usr/share/gems/specifications/openshift-origin-console-1.5.5.gemspec
sed -i "s/~>/>=/g" /var/www/openshift/console/Gemfile 

# Install missing dependencies
yum install --assumeyes http://ftp.heanet.ie/pub/fedora/linux/development/rawhide/x86_64/os/Packages/r/rubygem-net-http-persistent-2.8-2.fc19.noarch.rpm
yum install --assumeyes http://ftp.heanet.ie/pub/fedora/linux/development/rawhide/x86_64/os/Packages/r/rubygem-haml-3.1.7-1.fc19.noarch.rpm
yum install --assumeyes http://ftp.heanet.ie/pub/fedora/linux/development/rawhide/x86_64/os/Packages/r/rubygem-formtastic-1.2.3-8.fc19.noarch.rpm


# Perform the local gem bundle
cd /var/www/openshift/console
bundle --local

# Great, we made it !
echo "------ done -----"

) > /var/log/comodit/openshift-console/install.log 2>&1