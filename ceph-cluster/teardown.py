#!/usr/bin/env python

import time, sys, os, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException


def teardown():
    # Script
    print "Teardown of Ceph cluster"

    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, "Cluster")

    for h in env.hosts():
        try:
            print "Deleting instance of", h.name
            h.get_instance().delete()
        except Exception as e:
            print "Could not delete host ", h.name
        h.delete()

    print "Deleting settings..."
    env.settings().delete('monitors')
    env.settings().delete('osds')
    env.settings().delete('mdss')
    env.settings().delete('admin_key')


if __name__ == '__main__':
    try:
        teardown()
    except PythonApiException as e:
        print e
