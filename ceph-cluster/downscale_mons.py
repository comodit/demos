#!/usr/bin/env python

import time, config

from optparse import OptionParser

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.host import Host

from helper import get_latest_id, get_short_hostname, create_host


def downscale_osds(count):
    # Script
    print "Down-scaling Ceph cluster (monitors)"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    latest_id = get_latest_id('Monitor ', env)
    if latest_id < 0:
        raise Exception("No monitor found")

    if latest_id - count + 1 <= 2:
        raise Exception("Cannot down-scale to less than 3 monitors")

    mon_hosts = []
    for i in xrange(latest_id - count + 1, latest_id + 1):
        mon = env.get_host('Monitor ' + str(i))
        print "Bringing Monitor %i out of cluster..." % i
        mon.settings().create("status", "down")
        mon_hosts.append(mon)

    for h in mon_hosts:
        h.wait_for_pending_changes()

    print "Configure cluster..."
    next_id = latest_id + 1
    monitors = env.get_setting("monitors").value
    for i in xrange(0, len(monitors)):
        mon = monitors[i]
        id = int(mon["id"])
        if id >= latest_id - count + 1 and id < latest_id + 1:
            del monitors[i]
    env.settings().update("monitors", monitors)
    time.sleep(3)

    print "Deleting monitor(s)..."
    for h in mon_hosts:
        h.get_instance().delete()
        h.delete()

    total_time = time.time() - start_time
    print "Down-scaling time: " + str(total_time)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", type = "int", help = "the number of monitors to remove", default = 1)
    (options, args) = parser.parse_args()

    try:
        downscale_osds(options.count)
    except PythonApiException as e:
        print e
