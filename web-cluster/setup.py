#!/usr/bin/env python

import config, data

from comodit_client.api import Client
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.api.importer import Import

def setup():
    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    org = client.get_organization(config.organization)

    print "Setting up ComodIT..."

    # Create environment (if not already present)
    try:
        org.environments().create("Cluster", "Environment containing the web cluster.")
    except:
        pass

    # Import applications
    importer = Import()
    importer.import_application(org, 'db')
    importer.import_application(org, 'lb')
    importer.import_application(org, 'web')

    print "Done."


if __name__ == '__main__':
    try:
        setup()
    except Exception as e:
        print e
