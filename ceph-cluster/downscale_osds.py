#!/usr/bin/env python

import time, config

from optparse import OptionParser

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.host import Host

from helper import get_latest_id, get_short_hostname, create_host


def downscale_osds(count):
    # Script
    print "Down-scaling Ceph cluster (OSDs)"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    latest_id = get_latest_id('Object Store ', env)
    if latest_id < 0:
        raise Exception("No OSD found")

    if latest_id - count + 1 <= 1:
        raise Exception("Cannot down-scale to less than 2 OSDs")

    osd_hosts = []
    for i in xrange(latest_id - count + 1, latest_id + 1):
        osd = env.get_host('Object Store ' + str(i))
        print "Bringing Object Store %i out of cluster..." % i
        osd.settings().create("status", "out")
        osd_hosts.append(osd)

    for h in osd_hosts:
        h.wait_for_pending_changes()

    print "Configure cluster..."
    next_id = latest_id + 1
    osds = env.get_setting("osds").value
    for i in xrange(0, len(osds)):
        osd = osds[i]
        id = int(osd["id"])
        if id >= latest_id - count + 1 and id < latest_id + 1:
            del osds[i]
    env.settings().update("osds", osds)
    time.sleep(3)

    print "Deleting OSD(s)..."
    for h in osd_hosts:
        h.get_instance().delete()
        h.delete()

    total_time = time.time() - start_time
    print "Down-scaling time: " + str(total_time)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", type = "int", help = "the number of OSDs to remove", default = 1)
    (options, args) = parser.parse_args()

    try:
        downscale_osds(options.count)
    except PythonApiException as e:
        print e
