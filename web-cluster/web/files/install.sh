#/bin/bash

echo "Install wordpress"
/var/lib/comodit/wordpress/install.php

echo "Make sure httpd is started"
service httpd start