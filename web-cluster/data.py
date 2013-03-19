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
