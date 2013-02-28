#!/usr/bin/env python

import config

from comodit_client.api import Client
from comodit_client.api.importer import Import

def clean_up():
    # Connect to the ComodIT API
    client = Client(config.endpoint, config.username, config.password)
    org = client.get_organization(config.organization)

    print "Cleaning up ComodIT..."

    # Delete environment (if empty)
    env = org.environments().delete('Openshift')

    # Delete applications
    org.applications().delete('openshift-bind-server')
    org.applications().delete('openshift-broker')
    org.applications().delete('openshift-client')
    org.applications().delete('openshift-dhcp-dns-config')
    org.applications().delete('openshift-mcollective-client')
    org.applications().delete('openshift-mcollective-node')
    org.applications().delete('openshift-mongodb')
    org.applications().delete('openshift-cartridges')
    org.applications().delete('openshift-node')
    org.applications().delete('openshift-rabbitmq-server')



    print "Done."


if __name__ == '__main__':
    try:
        clean_up()
    except Exception as e:
        print e
