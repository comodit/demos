#!/usr/bin/env python

import time, sys, os, helper, config, data

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser

from helper import create_host, override_email


def scale(count):
    # Override email in data
    override_email(config.email)

    # Script
    print "Up-scaling web cluster"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    # Lookup database host
    try:
        db_host = env.get_host('DB Master')
    except EntityNotFoundException:
        print "Could not find the DB Master"
        sys.exit(-1)

    # Lookup LB host
    try:
        lb_host = env.get_host('LB')
    except EntityNotFoundException:
        print "Could not find the Load Balancer"
        sys.exit(-1)

    # Lookup next index
    index = 0
    for h in env.hosts():
        name = h.name
        if name.startswith('Web'):
            i = int(name[3:].rstrip())
            if i > index:
                index = i
    index += 1

    # Update configuration with db hostname
    db_hostname = db_host.get_instance().wait_for_address()
    data.web['settings']['wp_db_host'] = db_hostname

    # Deploy the required number of hosts
    hosts = []
    for i in range(index, index + int(count)):
        name = 'Web %s' % i
        web_host = create_host(env, name, config.platform, config.distribution, [data.web])
        web_host.provision()
        hosts.append(web_host)

    # Wait and configured provisioned hosts
    for h in hosts:
        print "Waiting for host %s to be deployed" % h.name
        h.wait_for_state('READY', config.time_out)

        # Update load balancer
        print "Updating load balancer configuration"
        web_hostname = h.get_instance().wait_for_address(config.time_out)
        setting = lb_host.get_application(data.lb['name']).get_setting('upstream')
        setting.value.append(web_hostname)
        setting.update()

    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of hosts to deploy", default = 1)
    (options, args) = parser.parse_args()

    try:
        scale(options.count)
    except PythonApiException as e:
        print e
