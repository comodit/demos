import time, sys, os, config, string, random

from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

def create_host(env, name, platform, distribution, applications = []):
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

def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def track_changes(host):
  changes = host.changes().list()
  c = changes[-1]
  current_task = -1
  done = False
  while not done:
    for t in c.tasks:
      # Skip already processed tasks
      if t.order_num < current_task:
        continue

      # If the current task
      if t.order_num == current_task:
        if t.status == "OK":
          print " [OK]"
          if current_task == len(c.tasks) -1:
              done = True
          continue
        elif t.status == "ERROR":
          print " [ERROR](%s...)" % t.error[:80]
          if current_task == len(c.tasks) -1:
              done = True
          continue
        if t.status == "PENDING":
          break
       
      # Moved to a new task
      current_task = t.order_num
      sys.stdout.write("  - %s..." % t.description)
      sys.stdout.flush()
      break

    # Otherwise we wait, refresh, and loop
    time.sleep(1)
    c.refresh()
