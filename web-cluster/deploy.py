#!/usr/bin/env python

import time, sys, os, helper, config, data

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.rest.exceptions import ApiException
from comodit_client.api.host import Host

from helper import create_host, override_email


def deploy():
    # Override email in data
    override_email(config.email)

    # Script
    print "Deploying web cluster"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, 'Cluster')

    # Deploy database host
    try:
        db_host = env.get_host('DB Master')
    except EntityNotFoundException:
        db_host = create_host(env, 'DB Master', data.ec2, data.centos, [data.db])
        print "Deploying DB Master"
        db_host.provision()

    # Deploy wordpress host
    try:
        web_host = env.get_host('Web 1')
    except EntityNotFoundException:
        web_host = create_host(env, 'Web 1', data.ec2, data.centos, [data.web])
        print "Deploying Web 1"
        web_host.provision()

    # Deploy load balancer
    try:
        lb_host = env.get_host('LB')
    except EntityNotFoundException:
        lb_host = create_host(env, 'LB', data.ec2, data.centos, [data.lb])
        print "Deploying LB"
        lb_host.provision()

    # Wait for database to be deployed
    print "Waiting for Database Master to be deployed"
    db_host.wait_for_state(Host.State.READY, config.time_out)
    db_hostname = db_host.get_instance().wait_for_address(config.time_out)
    print "DB Master hostname: " + db_hostname

    # Wait for web tier to be ready and then configure it
    print "Waiting for Web Tier to be deployed"
    web_host.wait_for_state(Host.State.READY, config.time_out)
    web_hostname = web_host.get_instance().wait_for_address(config.time_out)
    print "Web Tier hostname: " + web_hostname

    print "Configuring Web Tier"
    web_host.get_application(data.web['name']).settings().create('wp_db_host', db_hostname)

    # Wait for LB to be delployed and then configure it
    print "Waiting for Load Balancer to be deployed"
    lb_host.wait_for_state(Host.State.READY, config.time_out)
    lb_hostname = lb_host.get_instance().wait_for_address(config.time_out)
    print "Load Balancer hostname: " + lb_hostname

    print "Configuring Load Balancer"
    lb_host.get_application(data.lb['name']).settings().create('upstream', [web_hostname])

    total_time = time.time() - start_time
    print "Cluster deployed - Public hostname: " + lb_hostname
    print "Deployment time: " + str(total_time)


if __name__ == '__main__':
    try:
        deploy()
    except PythonApiException as e:
        print e
