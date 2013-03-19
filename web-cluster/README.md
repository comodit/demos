# Auto-scaling of a web cluster

In this orchestration example, we deploy a web cluster hosting a Wordpress blog.
The cluster is initially made of 3 hosts:

- the database server,
- the load balancer,
- a single web server.

When scaling up, additional web servers are instantiated and, once they are
available, the load balancer is configured to point to them. All web servers
point to the same database server. Finally, when scaling down,
load balancer is re-configured to stop pointing to some web servers which are
removed from the cluster.

## Support

If you run into issues using this script, or if you have more complex requirements, feel free
to reach out to us by sending an email to *support@comodit.com*. You can also reach out
through our other [support channels](http://www.comodit.com/resources/support.html).

## Pre-requisites

In order to execute this example, you need:

1. a ComodIT account,
2. an organization containing a valid platform and a valid distribution.
3. the ComodIT Python library (bundled with command-line interface, see [this
tutorial](http://comodit.com/resources/tutorials/cli.html) for information about
how to install it).

## Usage

1. Rename *config.py.sample* into *config.py*, fill-in your ComodIT credentials
and organization name, and configure your distribution and platform.
2. Setup ComodIT by executing *setup.py*.
3. Deploy the initial cluster by executing *deploy.py*.
4. Test the cluster by connecting to given public hostname with your browser.
5. Scale cluster up by executing *scale.py*.
6. Refresh the page you have opened in your browser, you should see in the footer
that the host serving it is different on each reload.
7. Scale cluster down by executing *downscale.py*.
8. Refresh the page you have opened in your browser, you should see that it is again
always served by the same host.
9. Tear down your cluster by executing *teardown.py* (all hosts created by *deploy.py*
and *scale.py* are deleted).
10. Clean-up your ComodIT organization by executing *cleanup.py*.

## Files

Here are the main files (i.e. the ones that can be executed) of this example:

- *setup.py*: setups ComodIT by creating/importing all required entities.
- *deploy.py*: creates initial cluster with its 3 hosts.
- *scale.py*: scales cluster up by instantiating a given number of web servers
(1 by default).
- *downscale.py*: scales cluster down by removing a given number of web servers
(1 by default).
- *teardown.py*: clears the cluster.
- *cleanup.py*: removes entities created by *setup.py*.

The other files and directory have the following role:

- *config.py.sample*: contains some configuration variables, in particular the
credentials to connect to ComodIT; must be updated and renamed into *config.py*.
- *data.py*: some data describing applications' configuration.
- *helper.py*: defines some helpers.
- *db*, *lb*, *web*: directories containing the recipes of the applications used
to create the web cluster.
