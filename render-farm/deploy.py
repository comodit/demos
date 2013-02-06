#!/usr/bin/env python

import time, sys, os, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.rest.exceptions import ApiException
from comodit_client.api.host import Host

from optparse import OptionParser

from helper import create_host, get_short_hostname


def deploy(slaves_count):

    # Script
    print "Deploying Blender Render Farm"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Render Farm')
    
    # Deploy NFS Server
    try:
      nfs_master = env.get_host('NFS Server')
    except EntityNotFoundException:
      nfs_master = create_host(env, 'NFS Server', config.platform, config.distribution, [{"name": "NFS Server", "settings": {"shares":[{"path":"/data", "source":"*", "options":"rw,sync,no_root_squash,no_subtree_check", "create": True}]}}])
      print "Deploying NFS Server"
      nfs_master.provision()

    # Deploy Blender client
    hosts = []
    for i in range(0, int(slaves_count)):
        name = 'Render Server %s' % i
        render_host = create_host(env, name, config.platform, config.distribution, [{"name":"NFS Client", "settings": {}},{"name":"Blender", "settings":{}}])
        render_host.provision()
        hosts.append(render_host)    

    # Wait for NFS Server to be deployed and retrieve IP
    print "Waiting for NFS Server to be deployed"
    nfs_master.wait_for_state('READY', config.time_out)
    master_ip = nfs_master.get_instance().wait_for_property("ip.eth0", config.time_out)
    location = "%s:/data" % master_ip   

    # Wait for slaves to be ready and configure NFS Shares
    print "Waiting for render servers to be deployed"
    for h in hosts:
        h.wait_for_state(Host.State.READY, config.time_out)
    
    # Configuring render servers
    for h in hosts:
        print "Configuring %s" % h.name
        h.get_application("NFS Client").settings().create('shares', [{"key":"data", "location": location, "options": "rw,soft,intr,rsize=8192,wsize=8192"}])

    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--count", dest = "count", help = "the number of slaves to deploy", default = 1)
    (options, args) = parser.parse_args()

    try:
        deploy(options.count)
    except PythonApiException as e:
        print e
