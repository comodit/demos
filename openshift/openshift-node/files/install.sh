#!/bin/sh

mkdir -p /var/log/comodit/openshift-node/

(

# Disable iptables
/bin/systemctl stop iptables.service
/bin/systemctl disable iptables.service

# Configure PAM
sed -i -e 's|pam_selinux|pam_openshift|g' /etc/pam.d/sshd

for f in "runuser" "runuser-l" "sshd" "su" "system-auth-ac"
do
  t="/etc/pam.d/$f"
  if ! grep -q "pam_namespace.so" "$t"
  then
    echo -e "session\t\trequired\tpam_namespace.so no_unmount_on_close" >> "$t"
  fi
done

# Update SSH configuration
perl -p -i -e "s/^#MaxSessions .*$/MaxSessions 40/" /etc/ssh/sshd_config
perl -p -i -e "s/^#MaxStartups .*$/MaxStartups 40/" /etc/ssh/sshd_config
echo AcceptEnv GIT_SSH >> /etc/ssh/sshd_config
systemctl restart sshd.service

# Patch to enable openshift-cgroups service to start
/bin/patch -t -p1 /bin/oo-admin-ctl-cgroups < /var/lib/comodit/applications/openshift-node/systemd.patch

# Restart mcollective server to integrate node gem
/bin/systemctl restart mcollective.service

) > /var/log/comodit/openshift-node/install.log 2>&1