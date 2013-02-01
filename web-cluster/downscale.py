#!/usr/bin/env python

import time, sys, os, helper, config, data

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser


def downscale(count):
    # Script
    print "Down-scaling web cluster"
    start_time = time.time()

    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, "Cluster")

    # Lookup LB host
    try:
        lb_host = env.get_host("LB")
    except EntityNotFoundException:
        print "Could not find the Load Balancer"
        sys.exit(-1)

    for i in range(int(count)):
        # Lookup highest index
        index = 0
        for h in env.hosts():
            name = h.name
            if name.startswith("Web"):
                i = int(name[3:].rstrip())
                if i > index:
                    index = i

        # Remove host from load balancer
        name = "Web %s" % index
        web_host = env.get_host(name)

        print "Removing %s from load balancer configuration" % name
        web_hostname = web_host.get_instance().wait_for_address(config.time_out)

        setting = lb_host.get_application(data.lb["name"]).get_setting("upstream")
        setting.value.remove(web_hostname)
        setting.update()

        # Delete host
        try:
            print "Deleting instance of", web_host.name
            web_host.get_instance().delete()
            web_host.delete()
        except Exception as e:
            print "Could not delete host ", web_host.name
            print e

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of hosts to destroy", default = 1)
    (options, args) = parser.parse_args()
    try:
        downscale(options.count)
    except PythonApiException as e:
        print e
