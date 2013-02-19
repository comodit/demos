#!/usr/bin/env python

import config, data

from comodit_client.api import Client
from comodit_client.api.importer import Import

def clean_up():
    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    org = client.get_organization(config.organization)

    print "Cleaning up ComodIT..."

    # Delete distribution (if not in use by a host)
    try:
        org.distributions().delete(data.centos['name'])
    except:
        pass

    # Delete environment (if empty)
    env = org.get_environment('Cluster')
    if len(env.hosts().list()) == 0:
        env.delete()

    # Delete applications
    org.applications().delete(data.db['name'])
    org.applications().delete(data.lb['name'])
    org.applications().delete(data.web['name'])

    print "Done."


if __name__ == '__main__':
    try:
        clean_up()
    except Exception as e:
        print e
