#!/usr/bin/env python

import config 

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
        org.environments().create("Render Farm", "Environment containing the render farm.")
    except:
        pass

    # Import applications
    importer = Import()
    importer.import_application(org, 'nfs-server')
    importer.import_application(org, 'nfs-client')
    importer.import_application(org, 'blender')

    print "Done."


if __name__ == '__main__':
    try:
        setup()
    except Exception as e:
        print e
