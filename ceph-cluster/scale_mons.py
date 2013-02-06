#!/usr/bin/env python

import time, config

from optparse import OptionParser

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.host import Host

from helper import get_latest_id, get_short_hostname, create_host


def scale_mons(count):
    # Script
    print "Up-scaling Ceph cluster (monitors)"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    latest_id = get_latest_id('Monitor ', env)
    if latest_id < 0:
        raise Exception("No monitor found")

    conf_app = [{"name": "Ceph Configuration", "settings": {}}]
    mon_hosts = []
    for i in xrange(latest_id + 1, latest_id + count + 1):
        mon = create_host(env, 'Monitor ' + str(i), config.platform, config.distribution, conf_app)
        print "Deploying Monitor " + str(i)
        mon.provision()
        mon_hosts.append(mon)

    print "Waiting for all hosts to be deployed..."
    for h in mon_hosts:
        h.wait_for_state(Host.State.READY, config.time_out)

    mon_ips = []
    mon_names = []
    mon_addrs = []
    for h in mon_hosts:
        ip = h.get_instance().wait_for_property("ip.eth0", config.time_out)
        mon_ips.append(ip)
        mon_names.append(get_short_hostname(h.get_instance().wait_for_property("hostname", config.time_out)))
        mon_addrs.append(ip + ":6879")

    for i in xrange(0, len(mon_addrs)):
        print "Monitor %i has address %s and hostname %s" % (latest_id + i + 1, mon_addrs[i], mon_names[i])

    print "Configure cluster..."
    next_id = latest_id + 1
    monitors = env.get_setting("monitors").value
    for name in mon_names:
        monitors.append({"id": str(next_id), "host": mon_names[i], "addr": mon_addrs[i]})
        next_id += 1

    env.settings().update("monitors", monitors)
    time.sleep(3)

    print "Installing monitor(s)..."
    next_id = latest_id + 1
    for h in mon_hosts:
        h.install("Ceph Monitor", {"mon_id": str(next_id)})
        next_id += 1
        time.sleep(3)

    for h in mon_hosts:
        h.wait_for_pending_changes()

    total_time = time.time() - start_time
    print "Up-scaling time: " + str(total_time)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of monitors to deploy", default = 1)
    (options, args) = parser.parse_args()

    try:
        scale_mons(options.count)
    except PythonApiException as e:
        print e
