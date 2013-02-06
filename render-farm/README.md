# Deploy and scale a Blender Render Farm in the cloud

In this orchestration example, we deploy a [Blender](http://www.blender.org/) cluster. Blender
is one of the leading 3D animation software, already used to create animations in well known 
movies and series. They are also the creators of [Big Buck Bunny](http://www.bigbuckbunny.org), 
an 'open-source' short animated film.

When rendering complex scenes with blender, the rendering of a single frame can take a couple 
hours, depending on the kind of harwdare used. Imagine how long it would take to render a 
complete animated movie on a single server! Hopefully, rendering scenes is a task that can be
easily distributed amongst a cluster of computers. A simple approach is simploy to distribute 
the frames to render evenly accross your render servers.

In this example, we deploy such a 'render farm' in the cloud. These scripts have been tested
on Amazon EC2 and Rackspace. You should be able to use them on private cloud such as Openstack,
Cloudstack and Eucalyptus.

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
3. the ComodIT Python library, which can be installed from [here](http://www.comodit.com/resources/tutorials/cli.html).

## Usage

1. Rename *config.py.sample* into *config.py* and fill-in your ComodIT credentials
and organization name as well as the platform and distribution to use. 

2. Setup ComodIT by executing *setup.py*. This will create an environment for the
render farm as well as the applications needed to deploy it.

    ./setup.py

3. Deploy the initial render farm by executing *deploy.py*. You can use the argument `--count=` to specify
the number of render slaves to deploy.

    ./deploy.py --count=10

4. If at a later stage you want to deploy more slaves, just use the *scale.py* command.

    ./scale.py --count=5

5. When you don't need your cluster, you can also downscale it using *downscale.py*.

    ./downscale --count=15

6. If you want to teardown the complete render farm, just execute teardown.py

   ./teardown.py

7. Finally, you can clean up all applications and environments created by these scripts.

   ./cleanup.py

10. Clean-up your ComodIT organization by executing *cleanup.py*.

## Rendering a scene on the render farm

This render farm has a very simple deployment architecture. We deploy a master
file server exposing its storage over NFS. The render slaves are mounting the 
remote date store and come with blender pre-installed.

The first thing you want to do is go on the master and prepare your scene files.

    ssh master.example.com -l ec2-user
    cd /data
    wget http://download.blender.org/demo/test/test249.zip
    unzip test249.zip

From that point, you can launch a rendering on each render slave. In order to distribute
the load evenly, just use the `-j` command line argument. For example, if you have three
render servers, you could do:

    blender -b animation/bowl.blend -F JPEG -o output/bowl_# -s 1 -e 600 -j 3 -t 0 -a

And on the second server:

    blender -b animation/bowl.blend -F JPEG -o output/bowl_# -s 2 -e 600 -j 3 -t 0 -a

Etc. This command will render frame by frame, and store the in the output folder. The `-s` flag
specifies the first frame and `-j` the increment when jumping to the next frame.

