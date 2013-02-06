#!/usr/bin/env python

import time, sys, os, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser


def downscale(count):
    # Script
    print "Down-scaling render farm"
    start_time = time.time()

    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, "Render Farm")

    for i in range(int(count)):
        # Lookup highest index
        index = 0
        for h in env.hosts():
            name = h.name
            if name.startswith("Render"):
                i = int(name[14:].rstrip())
                if i > index:
                    index = i

        # Remove host from load balancer
        name = "Render Server %s" % index
        host = env.get_host(name)

        # Delete host
        try:
            print "Deleting instance of", host.name
            host.get_instance().delete()
            host.delete()
        except Exception as e:
            print "Could not delete host ", host.name
            print e

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of hosts to destroy", default = 1)
    (options, args) = parser.parse_args()
    try:
        downscale(options.count)
    except PythonApiException as e:
        print e
