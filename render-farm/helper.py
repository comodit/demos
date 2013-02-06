import time, sys, os, config

from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

def create_host(env, name, platform, distribution, applications = []):
    print "Defining host %s" % name
    host = env.hosts().create(name, "", platform['name'], distribution['name'])

    # Configure platform
    context = host.get_platform()
    for key, value in platform['settings'].iteritems():
        context.settings().create(key, value)

    # Configure distribution
    context = host.get_distribution()
    for key, value in distribution['settings'].iteritems():
        context.settings().create(key, value)

    # Install applications
    for app in applications:
        host.install(app['name'], app['settings'])

    return host

def get_short_hostname(hostname):
    parts = hostname.split('.')
    return parts[0]

def get_latest_id(prefix, env):
    names = env.hosts_f
    last_id = -1
    for name in names:
        if name.startswith(prefix):
            i = int(name[len(prefix):].rstrip())
            if i > last_id:
                last_id = i
    return last_id
