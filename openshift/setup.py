#!/usr/bin/env python

import config 

from comodit_client.api import Client
from comodit_client.api.application import Package
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.api.importer import Import

def setup():
    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    org = client.get_organization(config.organization)

    print "Setting up ComodIT..."

    # Create environment (if not already present)
    try:
        org.environments().create("Openshift", "Environment containing the openshift cluster.")
    except:
        pass

    # Import applications
    importer = Import()
    importer.import_application(org, 'openshift-bind-server')
    importer.import_application(org, 'openshift-broker')
    importer.import_application(org, 'openshift-client')
    importer.import_application(org, 'openshift-dhcp-dns-config')
    importer.import_application(org, 'openshift-mcollective-client')
    importer.import_application(org, 'openshift-mcollective-node')
    importer.import_application(org, 'openshift-mongodb')
    importer.import_application(org, 'openshift-node')
    importer.import_application(org, 'openshift-cartridges')
    importer.import_application(org, 'openshift-rabbitmq-server')

    # Update repositories
    if hasattr(config, "repo"):
      updaterepo(org.get_application("openshift-broker"), config.repo)
      updaterepo(org.get_application("openshift-node"), config.repo)
      updaterepo(org.get_application("openshift-client"), config.repo)

    # Append cartridges
    if hasattr(config, "cartridges"):
        app = org.get_application("openshift-cartridges")
        for cart in config.cartridges:
          app.add_package(Package({"name": cart}))
        app.update()

    print "Done."


def updaterepo(app, location):
  for repo in app.repositories:
    if repo.name == "openshift-origin-nightly":
      repo.location = config.repo
      app.update()
      return
    

if __name__ == '__main__':
    try:
        setup()
    except Exception as e:
        print e
