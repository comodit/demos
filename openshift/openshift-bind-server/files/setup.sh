#!/bin/sh

(
# Exit on errors
set -e

# We will be referring frequently to the domain name with which we are configuring 
# this OpenShift installation, so let us set the $domain environment variable for 
# easy reference
domain=${domain}

# Set the $keyfile environment variable to contain the filename for a new DNSSEC
# key for our domain (we will create this key shortly)
keyfile=/var/named/${domain}.key

<#noparse>

# We will use the dnssec-keygen tool to generate the new DNSSEC key for the domain. 
rm -vf /var/named/K${domain}*
pushd /var/named
dnssec-keygen -a HMAC-MD5 -b 512 -n USER -r /dev/urandom ${domain}
KEY="$(grep Key: K${domain}*.private | cut -d ' ' -f 2)"
popd

# Next, we must ensure we have a key for the broker to communicate with BIND. 
# We use the rndc-confgen command to generate the appropriate configuration files
# for rndc, which is the tool that the broker will use to perform this communication.
rndc-confgen -a -r /dev/urandom

# We must ensure that the ownership, permissions, and SELinux context are set 
# appropriately for this new key
restorecon -v /etc/rndc.* /etc/named.*
chown -v root:named /etc/rndc.key
chmod -v 640 /etc/rndc.key

# We must ensure that the permissions and SELinux context are set appropriately 
# for the forwarders.conf file
restorecon -v /var/named/forwarders.conf
chmod -v 755 /var/named/forwarders.conf

# Now, create an initial named database in a new file named /var/named/dynamic/<domain>.db 
# (where <domain> is your chosen domain)
cat <<EOF > /var/named/dynamic/${domain}.db
\$ORIGIN .
\$TTL 1	; 1 seconds (for testing only)
${domain} IN SOA ns1.${domain}. hostmaster.${domain}. (
                         2011112904 ; serial
                         60         ; refresh (1 minute)
                         15         ; retry (15 seconds)
                         1800       ; expire (30 minutes)
                         10         ; minimum (10 seconds)
                          )
                     NS ns1.${domain}.
\$ORIGIN ${domain}.
ns1	              A        127.0.0.1

EOF

# Next, we install the DNSSEC key for our domain. Create the file /var/named/${domain}.key 
# (where ${domain} is your chosen domain)
cat <<EOF > /var/named/${domain}.key
key ${domain} {
  algorithm HMAC-MD5;
  secret "${KEY}";
};
EOF

# We need to set the permissions and SELinux contexts appropriately
chown -Rv named:named /var/named
restorecon -rv /var/named

# Set /etc/named.conf permissions and SELinux contexts appropriately
chown -v root:named /etc/named.conf
restorecon /etc/named.conf

# Start
/bin/systemctl start named.service

echo -----

</#noparse>

)  > /var/log/comodit/openshift-bind-server/setup.log 2>&1