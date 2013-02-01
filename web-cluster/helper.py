import time, sys, os, config, data

from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

def override_email(email):
    data.web["settings"]["wp_admin_email"] = email

def get_override(var, key, default_value):
    if var.__dict__.has_key(key):
        return var.__dict__[key]
    else:
        return default_value

def create_host(env, name, platform, distribution, applications):
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
