#!/usr/bin/env python

import time, sys, os, socket, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException

from optparse import OptionParser

from helper import create_host,track_changes


def scale():

    # Script
    print "Adding a node to openshift cluster"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Openshift')

    # Lookup broker server
    try:
        broker = env.get_host('Openshift Broker')
    except EntityNotFoundException:
        print "Could not find the broker"
        sys.exit(-1)
 
    # Fetch broker public key
    public_key = broker.get_instance().get_file_content("/etc/openshift/rsync_id_rsa.pub").read()

    # Lookup next index
    index = 0
    for h in env.hosts():
        name = h.name
        if name.startswith('Openshift Node'):
            i = int(name[15:].rstrip())
            if i > index:
                index = i
    index += 1

    # Deploy the required number of hosts
    name = 'Openshift Node %s' % index
    node = create_host(env, name, config.platform, config.distribution, [])
    print "Deploying %s" % name 
    node.provision()

    # Wait for host to be deployed
    print "Waiting for host %s to be deployed" % node.name
    node.wait_for_state('READY', config.time_out)
    if node.state == "PROVISIONING":
      raise Exception("Timed out waiting for host to be deployed.")

    # Fetch network details
    node_ip = node.get_instance().wait_for_property("ip.eth0", config.time_out)
    hostname = "node-%s" % index

    # Add dns record for this new host
    setting = broker.get_application("openshift-bind-server").get_setting("dns_records")
    setting.value.append({"host": hostname, "type": "A", "ttl": "180", "target": node_ip})
    setting.update()

    # Configure network
    print "Reconfiguring network"
    node.install("openshift-dhcp-dns-config", {"hostname": hostname})
    track_changes(node)

    # Install mcollective
    print "Installing mcollective server"
    node.install("openshift-mcollective-node", {"mcollective_stomp_host": "broker." + config.domain, 
                                                "mcollective_stomp_username": "guest", 
                                                "mcollective_stomp_password": "guest"})
    track_changes(node)

    # Install cartridges
    print "Installing openshift-cartridges"
    node.install("openshift-cartridges", {})
    track_changes(node)

    # Install openshift-node
    print "Installing Openshift Node"
    public_ip = node.get_instance().wait_for_property('publicIp', config.time_out)
    try:
        public_hostname = socket.gethostbyaddr(public_ip)
    except:
        public_hostname = node.get_instance().wait_for_address(config.time_out)
        
    node.install("openshift-node", {"broker_host": "broker." + config.domain, 
                                    "public_hostname": public_hostname[0], 
                                    "public_ip": public_ip, 
                                    "unsercure_port": "80",
                                    "keys": [public_key]
                                    })
    track_changes(node)

    # Cleanup changes
    node.changes().clear()
   
    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

if __name__ == '__main__':
    try:
        scale()
    except PythonApiException as e:
        print e
