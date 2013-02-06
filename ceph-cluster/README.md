# Auto-scaling of a Ceph cluster

In this orchestration example, we deploy a [Ceph](http://ceph.com/) cluster. Ceph Ceph is a
distributed object store and file system designed to provide excellent
performance, reliability and scalability. The cluster is initially made of 3 hosts:

- the master server hosting a monitor (MON) and a meta-data service (MDS),
- 2 object storage servers (OSDs).

When scaling up, additional OSDs or MONs are instantiated and, once they are
available, included in the cluster.

## Pre-requisites

In order to execute this example, you need:

1. a ComodIT account,
2. an organization with a platform and a distribution (other than the demo
platform and distribution). For instance, you may configure an EC2 platform
and use the CentOS 6.3 AMI from the store as distribution.
3. the ComodIT Python library (bundled with command-line interface, see [this
tutorial](http://comodit.com/resources/tutorials/cli.html) for information about
how to install it).

## Usage

1. Rename *config.py.sample* into *config.py* and fill-in your ComodIT credentials
and organization name as well as the platform and distribution to use. 'admin\_key'
may be left unchanged.
2. Setup ComodIT by executing *setup.py*. This will create an environment for the
cluster as well as the applications needed to deploy it.
3. Deploy the initial cluster by executing *deploy.py*.
4. You can test the cluster by connecting to given public IP with SSH and
executing the command 'ceph -s' as root. It should display the current state
of the cluster.
5. Add an OSD by executing *scale\_osds.py*.
6. Re-execute 'ceph -s' on master node, you should see the new OSD.
5. Add a MON by executing *scale\_mons.py*.
6. Re-execute 'ceph -s' on master node, you should see the new monitor (this can
take some time).
7. Remove an OSD by executing *downscale_osds.py*.
8. Re-execute 'ceph -s' on master node, you should that latest OSD is gone (not
"in" the cluster anymore).
9. Tear down your cluster by executing *teardown.py* (all hosts created by *deploy.py*
and *scale\_\*.py* are deleted).
10. Clean-up your ComodIT organization by executing *cleanup.py*.

## Files

Here are the main files (i.e. the ones that can be executed) of this example:

- *setup.py*: setups ComodIT by creating/importing all required entities.
- *deploy.py*: creates initial cluster with its 3 hosts.
- *scale\_osds.py*: scales cluster up by instantiating a given number of OSDs
(1 by default).
- *scale\_mons.py*: scales cluster up by instantiating a given number of MONs
(1 by default).
- *downscale\_osds.py*: scales cluster down by removing a given number of OSDs
(1 by default).
- *downscale\_mons.py*: scales cluster down by removing a given number of MONs
(1 by default).
- *teardown.py*: clears the cluster.
- *cleanup.py*: removes entities created by *setup.py*.

The other files and directory have the following role:

- *config.py.sample*: contains some configuration variables, in particular the
credentials to connect to ComodIT; must be updated and renamed into *config.py*.
- *helper.py*: defines some helpers.
- *config*, *mds*, *mon*, *osd*: directories containing the recipes of the
applications used to create the Ceph cluster.
