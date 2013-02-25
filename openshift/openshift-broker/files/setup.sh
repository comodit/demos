#!/bin/sh

(
# Exit on errors
set -e

# Disable iptables
/bin/systemctl stop iptables.service
/bin/systemctl disable iptables.service

# Disable SELinux
/sbin/setenforce 0

# Configure bind plugin
KEY="$(grep Key: /var/named/K${domain}*.private | cut -d ' ' -f 2)"

cat <<EOF > /etc/openshift/plugins.d/openshift-origin-dns-bind.conf
BIND_SERVER="127.0.0.1"
BIND_PORT=53
BIND_KEYNAME="##domain##"
BIND_KEYVALUE="${KEY}"
BIND_ZONE="##domain##"
EOF

# Setup inter-host access keys
openssl genrsa -out /etc/openshift/server_priv.pem 2048
openssl rsa -in /etc/openshift/server_priv.pem -pubout > /etc/openshift/server_pub.pem

# We also need to generate a key pair for the broker to use to move gears between nodes
ssh-keygen -t rsa -b 2048 -f ~/.ssh/rsync_id_rsa
cp ~/.ssh/rsync_id_rsa* /etc/openshift/

# Configure bundler
cd /var/www/openshift/broker
sed -i "s/, '0.12.1'//" Gemfile
sed -i "s/, '1.6.1'//" Gemfile
sed -i "s/, '<= 0.9.2.2'//" Gemfile
sed -i "s/, '3.2.0'//" Gemfile
sed -i "s/, '0.5.2'//" Gemfile

# Install missing gems
gem install mongoid
gem install open4
gem install simplecov
gem install mocha
gem install minitest
bundle --local

# Fix folder permissions
touch /var/log/mcollective-client.log
chown -R apache:root /var/log/openshift
chown -R apache:root /var/log/mcollective-client.log 

echo ------

) > /var/log/comodit/openshift-broker/setup.log 2>&1