#!/usr/bin/env python

import time, sys, os, helper, config

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException


def teardown():
    # Script
    print "Teardown of Blender Render Farm"

    client = Client(config.endpoint, config.username, config.password)
    env = client.get_environment(config.organization, "Render Farm")

    for h in env.hosts():
        try:
            print "Deleting instance of", h.name
            h.get_instance().delete()
        except Exception as e:
            print "Could not delete host ", h.name
        h.delete()

if __name__ == '__main__':
    try:
        teardown()
    except PythonApiException as e:
        print e
