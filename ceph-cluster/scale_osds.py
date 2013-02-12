#!/usr/bin/env python

import time, config

from optparse import OptionParser

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.host import Host

from helper import get_latest_id, get_short_hostname, create_host


def scale_osds(count):
    # Script
    print "Up-scaling Ceph cluster (OSDs)"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    latest_id = get_latest_id('Object Store ', env)
    if latest_id < 0:
        raise Exception("No OSD found")

    conf_app = [{"name": "Ceph Configuration", "settings": {}}]
    osd_hosts = []
    for i in xrange(latest_id + 1, latest_id + count + 1):
        osd = create_host(env, 'Object Store ' + str(i), config.platform, config.distribution, conf_app)
        print "Deploying Object Store " + str(i)
        osd.provision()
        osd_hosts.append(osd)

    print "Waiting for all hosts to be deployed..."
    for h in osd_hosts:
        h.wait_for_state(Host.State.READY, config.time_out)

    osd_ips = []
    osd_names = []
    for h in osd_hosts:
        osd_ips.append(h.get_instance().wait_for_property("ip.eth0", config.time_out))
        osd_names.append(get_short_hostname(h.get_instance().wait_for_property("hostname", config.time_out)))

    for i in xrange(0, len(osd_ips)):
        print "OSD %i has IP %s and hostname %s" % (latest_id + i + 1, osd_ips[i], osd_names[i])

    print "Configure cluster..."
    next_id = latest_id + 1
    osds = env.get_setting("osds").value
    for name in osd_names:
        osds.append({"id": str(next_id), "host": name})
        next_id += 1

    env.settings().update("osds", osds)
    time.sleep(3)

    print "Installing OSD(s)..."
    i = 0
    next_id = latest_id + 1
    for h in osd_hosts:
        h.install("Ceph Object Store", {"osd_id": str(next_id), "osd_hostname": osd_names[i]})
        next_id += 1
        i += 1
        time.sleep(3)

    for h in osd_hosts:
        h.wait_for_pending_changes()

    total_time = time.time() - start_time
    print "Up-scaling time: " + str(total_time)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of OSDs to deploy", default = 1)
    (options, args) = parser.parse_args()

    try:
        scale_osds(options.count)
    except PythonApiException as e:
        print e
