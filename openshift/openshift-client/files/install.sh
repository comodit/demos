#!/bin/sh

mkdir -p /var/log/comodit/openshift-client

(

rpm -ivh --nodeps https://mirror.openshift.com/pub/openshift-origin/nightly/fedora-18/latest/x86_64/rhc-1.5.1-1.git.0.ba60a4b.fc18.noarch.rpm

gem install httpclient

) > /var/log/comodit/openshift-client/install.log 2>&1