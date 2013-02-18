# Deploy and scale Openshift Origin

In this orchestration example, we explain how to deploy and scale an [Openshift Origin](https://openshift.redhat.com/community/open-source) cluster,
using ComodIT's orchestration possibilities.

We successfully tested the deployment of Openshift on Amazon EC2 and Openstack, however it should be possible to
use any platform supported by ComodIT (Eucalyptus, Rackspace, etc.) or even deploy the cluster on a bare-metal infrastructure.

These scripts target a Fedora 18 distributions.

These scripts are simplified for educational purposes. Deploying and automaticalt scaling a high-availability openshift cluster would
require more work. If you are interested by such a use case, we'd be happy to help out. Contact us at support@comodit.com and let's discuss about it.

## Deployment topology

The following diagram shows you the deployment topology we selected for these recipes. It closely matches the one described
in [this tutorial](https://openshift.redhat.com/community/wiki/build-your-own). In summary, we have a *broker* server which 
manages everything and holds all the storage, dns, messaging components. We then have one or more *nodes* which are responsible
for hosting and executing the end-user applications.

Deploying a high-availability cluster would require to decouple the various components of the broker. This can easily be done
while re-using most of the recipes from this orchestration scenarion.

[![Deployed topology](http://comodit.com/static/images/posts/openshift-topology.jpg)](http://comodit.com)

## Requirements

1. A ComodIT account (you can register for free [here](https://my.comodit.com/#register)).

2. A ComodIT platform.
    
    If you havn&#39;t done it yet, add your cloud platform to ComodIT. In the 'Platform'
    section, click the *Add* button, pick a driver and fill in the specific details. For
    more information, you can follow one of these [tutorials](/resources/index.html).

    Note that you won't be able to deploy this example on the 'Demo Platform' 
    provided by default, which is limited to maximum one provisioning at a time per user.

3. A ComodIT distribution.

    The application templates used in this orchestration scripts have been written for 
    Fedora 18. You should therefore deploy on a compatible distribution. If you deploy
    on EC2, the easier is to get the 'Fedora 18 (AMI)' image from the ComodIT 
    marketplace.

4. The ComodIT Python library (bundled with command-line interface, see [this
tutorial](/resources/tutorials/cli.html) for information about how to install it).


## Deployment

1. Clone the demos public repository and enter Ceph cluster's folder:

        git clone git@github.com:comodit/demos.git
        cd demos/openshift

2. Create a `config.py` file with the following content:

        endpoint = "https://my.comodit.com/api"
        
        username = "<user>"
        password = "<password>"
        organization = "<org_name>"
        
        time_out = 60 * 30  # seconds
        
        domain = "example.com"
        
        platform = {"name" : "Amazon EC2",
            "settings" : {
                     "ec2.instanceType": "m1.large",
                     "ec2.securityGroups": "openshift",
                     "ec2.zone": "eu-west-1a",
                     "ec2.keyPair": "eschnou"
                     }
        }
        
        distribution = {"name" : "Fedora 18 (AMI)", "settings" : {}}

    where `<user>` and `<password>` are your ComodIT credentials, `<org_name>` the name of your organization. 
    You should replace/update the 'Amazon EC2' platform with the one you intend to use, and update/replace the 
    distribution if you arn't using the Fedora 18 distribution provided by ComodIT.

    Warning: The applications you will deploy in next step are
    only compatible with Fedora 18! Therefore choose your ComodIT distribution
    accordingly. A distribution from the store like 'Fedora 18 (AMI)'can be used.

3. Setup you ComodIT account i.e. create all required applications and create
an environment that will contain cluster's hosts:

        ./setup.py

4. Deploy the broker: the following script will deploy and configure a broker. It creates a first user with username `openshift` and password `secret`.
You can of course easily change the recipes to modify these default settings.

        ./deploy-broker.py
        
    Once the broker is deployed, the script returns the public hostname where it can be reached.

5. Deploy a node: when you have your broker online, you can add your first node by executing this script.

        ./add-node.py

    You can execute it as many time as you wish to add additional node to your cluster. It would be quite easy to 
    make this script a bit more elaborate, for example reacting to some events to automaticaly scale your cluster.

6. Deploy a client (optional): If you don't want to install the openshift client tools on your 
local host, you can deploy a client host using the following script:

       ./deploy-client.py

## Using your Openshift Cluster

If you are using the remote client, ssh to the machine. We are using the Amazon convention and the 
user is named `ec2-user`.

    ssh <client-hostname> -l ec2-user -i <path-to-key>

The first thing to do is to export in a variable the hostname of the broker:

    export LIBRA_SERVER=broker.example.com

Now you can launch the setup command, using the openshift account that was previously created:

    rhc setup

You are now ready to go ! Create your first app, push and enjoy your new PaaS.

## Shutting down cluster

You can delete all hosts created during deployment and scaling operations:

    ./teardown.py

If you also want to clean-up your organization i.e. delete the applications and
environment created by setup script:

    ./cleanup.py


