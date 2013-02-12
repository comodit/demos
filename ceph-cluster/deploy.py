#!/usr/bin/env python

import time, sys, os, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.rest.exceptions import ApiException
from comodit_client.api.host import Host

from helper import create_host, get_short_hostname


def deploy():
    # Script
    print "Deploying Ceph cluster"
    start_time = time.time()

    NUM_OF_MON = 1
    NUM_OF_OSD = 2

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')


    # Initialize empty cluster
    for key in ("monitors", "osds", "mdss"):
        try:
            env.settings().create(key, [])
        except:
            pass
        time.sleep(1)
    try:
        env.settings().create("admin_key", config.admin_key)
    except:
        pass
    time.sleep(1)

    conf_app = [{"name": "Ceph Configuration", "settings": {}}]


    # Provision hosts
    mon_hosts = []
    for i in xrange(0, NUM_OF_MON):
        try:
            mon = env.get_host('Monitor ' + str(i))
        except EntityNotFoundException:
            mon = create_host(env, 'Monitor ' + str(i), config.platform, config.distribution, conf_app)
            print "Deploying Monitor " + str(i)
            mon.provision()
        mon_hosts.append(mon)

    osd_hosts = []
    for i in xrange(0, NUM_OF_OSD):
        try:
            osd = env.get_host('Object Store ' + str(i))
        except EntityNotFoundException:
            osd = create_host(env, 'Object Store ' + str(i), config.platform, config.distribution, conf_app)
            print "Deploying Object Store " + str(i)
            osd.provision()
        osd_hosts.append(osd)

    print "Waiting for all hosts to be deployed..."
    for h in mon_hosts + osd_hosts:
        h.wait_for_state(Host.State.READY, config.time_out)


    # Configure the cluster as it is now known
    mon_ips = []
    mon_names = []
    mon_addrs = []
    for h in mon_hosts:
        ip = h.get_instance().wait_for_property("ip.eth0", config.time_out)
        mon_ips.append(ip)
        mon_names.append(get_short_hostname(h.get_instance().wait_for_property("hostname", config.time_out)))
        mon_addrs.append(ip + ":6879")

    osd_ips = []
    osd_names = []
    for h in osd_hosts:
        osd_ips.append(h.get_instance().wait_for_property("ip.eth0", config.time_out))
        osd_names.append(get_short_hostname(h.get_instance().wait_for_property("hostname", config.time_out)))

    for i in xrange(0, len(mon_addrs)):
        print "Monitor %i has address %s and hostname %s" % (i, mon_addrs[i], mon_names[i])

    for i in xrange(0, len(osd_ips)):
        print "OSD %i has IP %s and hostname %s" % (i, osd_ips[i], osd_names[i])

    print

    print "Configure cluster..."
    monitors = []
    for i in xrange(0, len(mon_addrs)):
        monitors.append({"id": str(i), "host": mon_names[i], "addr": mon_addrs[i]})

    osds = []
    for i in xrange(0, len(osd_names)):
        osds.append({"id": str(i), "host": osd_names[i]})

    mdss = []
    for i in xrange(0, len(mon_names)):
        mdss.append({"id": str(i), "host": mon_names[i]})

    env.settings().update("monitors", monitors)
    time.sleep(3)
    env.settings().update("osds", osds)
    time.sleep(3)
    env.settings().update("mdss", mdss)
    time.sleep(3)
    env.settings().update("admin_key", config.admin_key)
    time.sleep(3)


    # Install Ceph
    print "Installing first monitor and meta-data service..."
    mon_hosts[0].install("Ceph Monitor", {"bootstrap": True, "mon_id": "0", "mon_addr": mon_addrs[0]})
    time.sleep(3)
    mon_hosts[0].install("Ceph Metadata", {"mds_id": "0"})
    mon_hosts[0].wait_for_pending_changes()

    print "Installing additional monitors (if any) and meta-data service(s)..."
    for i in xrange(1, len(mon_hosts)):
        mon_hosts[i].install("Ceph Metadata", {"mds_id": str(i)})
        time.sleep(3)
        mon_hosts[i].install("Ceph Monitor", {"mon_id": str(i)})
        time.sleep(3)

    for h in mon_hosts:
        h.wait_for_pending_changes()

    print "Installing OSD(s)..."
    for i in xrange(0, len(osd_hosts)):
        osd_hosts[i].install("Ceph Object Store", {"osd_id": str(i), "osd_hostname": osd_names[i]})
        time.sleep(3)

    for h in osd_hosts:
        h.wait_for_pending_changes()

    total_time = time.time() - start_time
    print "Master node's public IP: %s" % (mon_hosts[0].get_instance().wait_for_address(config.time_out))
    print "Deployment time: " + str(total_time)


if __name__ == '__main__':
    try:
        deploy()
    except PythonApiException as e:
        print e
