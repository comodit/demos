#!/usr/bin/env python

import time, sys, os, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser

from helper import create_host


def scale(count):

    # Script
    print "Up-scaling render farm cluster"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Render Farm')

    # Lookup nfs server
    try:
        nfs_master = env.get_host('NFS Server')
    except EntityNotFoundException:
        print "Could not find the NFS Master"
        sys.exit(-1)

    # Lookup next index
    index = 0
    for h in env.hosts():
        name = h.name
        if name.startswith('Render'):
            i = int(name[14:].rstrip())
            if i > index:
                index = i
    index += 1

    # Prepare NFS Configuration
    master_ip = nfs_master.get_instance().wait_for_property("ip.eth0", config.time_out)
    location = "%s:/data" % master_ip

    # Deploy the required number of hosts
    hosts = []
    for i in range(index, index + int(count)):
        name = 'Render Server %s' % i
        render_host = create_host(env, name, config.platform, config.distribution, [{"name": "NFS Client", "settings": {"shares": [{"key": "data", "location": location, "options": "rw,soft,intr,rsize=8192,wsize=8192"}]}}, {"name": "Blender", "settings": {}}])
        render_host.provision()
        hosts.append(render_host)

    # Wait and configured provisioned hosts
    for h in hosts:
        print "Waiting for host %s to be deployed" % h.name
        h.wait_for_state('READY', config.time_out)

    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of render servers to deploy", default = 1)
    (options, args) = parser.parse_args()

    try:
        scale(options.count)
    except PythonApiException as e:
        print e
