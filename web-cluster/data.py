# EC2 platform description
ec2 = {"name" : "EC2",
       "settings" : {
                     "ec2.instanceType": "t1.micro",
                     "ec2.securityGroups": "demo"
                     }
       }

# CentOS image description
centos = {"name" : "CentOS 6.3 (AMI)",
          "pub_uuid" : "A82DCF50661F11E2960D58C2AC1F0212",
          "settings" : {}
          }

db = {"name" : "Cluster-Database",
      "settings" : {
                    "root_pass" : "uLz01PcA",
                    "dbs" : ["wordpress"],
                    "users": [{"name": "wordpress", "password": "b9q67vFMP6jxK8K1", "host": "%"}],
                    "grants": [{"name": "wordpress", "priv_type": "ALL", "tab": "*", "db": "wordpress", "user": "wordpress", "host": "%"}]
                    }
         }

web = {"name":  "Cluster-Web",
       "settings" : {
                     "wp_admin_email" : "sample@server.com",
                     "wp_admin_password": "secret",
                     "wp_db_password": "b9q67vFMP6jxK8K1"
                    }
       }

lb = {"name": "Cluster-LoadBalancer",
      "settings" : {}
      }
