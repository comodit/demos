# Auto-scaling of a Ceph cluster

In this orchestration example, we deploy a [Ceph](http://ceph.com/) cluster. Ceph is a
distributed object store and file system designed to provide excellent
performance, reliability and scalability. The cluster is initially made of 3 hosts:

- the master server hosting a monitor (MON) and a meta-data service (MDS),
- 2 object storage servers (OSDs).

When scaling up, additional OSDs or MONs are instantiated and, once they are
available, included in the cluster.


## Support

If you run into issues using this script, or if you have more complex requirements, feel free
to reach out to us by sending an email to *support@comodit.com*. You can also reach out
through our other [support channels](http://www.comodit.com/resources/support.html).


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
and organization name as well as the platform and distribution to use. `admin_key`
may be left unchanged.
2. Setup ComodIT by executing *setup.py*. This will create an environment for the
cluster as well as the applications needed to deploy it.

        ./setup.py

3. Deploy the initial cluster by executing *deploy.py*.

        ./deploy.py

5. If you want to add an OSD to the cluster, execute *scale\_osds.py*.

        ./scale_osds.py -c 1

    where `-c` option is the number of OSDs to add.

5. If you want to add a monitor to the cluster, execute *scale\_mons.py*.

        ./scale_mons.py -c 1

    where `-c` option is the number of monitors to add.

7. If you want to remove an OSD from the cluster, execute *downscale_osds.py*.

        ./downscale_osds.py -c 1

    where `-c` option is the number of OSDs to remove.

7. If you want to remove a monitor from the cluster, execute *downscale_mons.py*.

        ./downscale_mons.py -c 1

    where `-c` option is the number of monitors to remove.

9. If you want to tear down (i.e. delete all hosts created by *deploy.py*
and *scale\_\*.py*) the cluster, execute *teardown.py*.

        ./teardown.py

10. Finally, you can clean up all applications and environments created by these
scripts.

        ./cleanup.py

