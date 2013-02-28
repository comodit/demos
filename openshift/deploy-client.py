#!/usr/bin/env python

import time, sys, os, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser

from helper import create_host,track_changes


def deploy():

    # Script
    print "Deploy a server with the openshift client tools"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Openshift')

    # Lookup nfs server
    try:
        broker = env.get_host('Openshift Broker')
    except EntityNotFoundException:
        print "Could not find the broker"
        sys.exit(-1)

    # Deploy the client
    name = 'Openshift Client'
    node = create_host(env, name, config.platform, config.distribution, [])
    print "Deploying %s" % name 
    node.provision()

    # Wait for host to be deployed
    print "Waiting for host %s to be deployed" % node.name
    node.wait_for_state('READY', config.time_out)
    if node.state == "PROVISIONING":
      raise Exception("Timed out waiting for host to be deployed.")

    # Get network details
    node_ip = node.get_instance().wait_for_property("ip.eth0", config.time_out)

    # Add dns record for this new host
    setting = broker.get_application("openshift-bind-server").get_setting("dns_records")
    setting.value.append({"host": "client", "type": "A", "ttl": "180", "target": node_ip})
    setting.update()

    # Configure network
    print "Reconfiguring network"
    node.install("openshift-dhcp-dns-config", {"hostname": "client"})
    track_changes(node)

    # Install openshift-client
    print "Installing Openshift Client"
    node.install("openshift-client", {})
    track_changes(node)

    # Cleanup changes
    node.changes().clear()

    public_hostname = node.get_instance().wait_for_address(config.time_out)
    print "Openshift client deployed at %s" % public_hostname

    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

if __name__ == '__main__':
    try:
        deploy()
    except PythonApiException as e:
        print e
