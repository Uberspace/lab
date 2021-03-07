.. highlight:: console

.. author:: Lukas Wolfsteiner <lukas@wolfsteiner.media>

.. tag:: lang-c
.. tag:: database

#######
CouchDB
#######

.. tag_list::

CouchDB_ is a document-oriented database system. We provide binaries ready to start your own instance.

Initialization
==============

Environment
-----------

First set the CouchDB admin password as an environment variable:

.. code-block:: bash

  [eliza@dolittle ~]$ export COUCHDB_ADMIN_PASSWORD=asdfghjkl

Next we need to create directories for our configuration and application data:

.. code-block:: bash

  [eliza@dolittle ~]$ mkdir -p ~/etc/couchdb
  [eliza@dolittle ~]$ mkdir -p ~/opt/couchdb

Configuration
-------------

We create the CouchDB configuration file at ``~/etc/couchdb/local.ini``:

.. code-block:: bash

  [eliza@dolittle ~]$ mkdir -p $HOME/etc/couchdb
  [eliza@dolittle ~]$ cat > $HOME/etc/couchdb/local.ini <<- EOM
  [couchdb]
  single_node=true
  database_dir = /home/$USER/opt/couchdb/data
  view_index_dir = /home/$USER/opt/couchdb/index

  [chttpd]
  port = 5984
  bind_address = 0.0.0.0

  [admins]
  admin = $COUCHDB_ADMIN_PASSWORD
  EOM

Supervisor Service
------------------

Then we need a new supervisord service by creating the file ``~/etc/services.d/couchdb.ini`` with the following command:

.. code-block:: bash

  [isabell@stardust ~]$ cat > ~/etc/services.d/couchdb.ini <<- EOM
  [program:couchdb]
  command=couchdb -couch_ini /opt/couchdb/etc/default.ini %(ENV_HOME)s/etc/couchdb/local.ini
  autostart=yes
  autorestart=yes
  stderr_logfile=/home/$USER/logs/services.d/couchdb/err.log
  stdout_logfile=/home/$USER/logs/services.d/couchdb/out.log
  EOM

Afterwards, ask ``supervisord`` to look for our new service:

.. code-block:: bash

  [eliza@doolittle ~]$ supervisorctl reread
  couchdb: available

And then start your daemon:

.. code-block:: bash

  [eliza@doolittle ~]$ supervisorctl update
  couchdb: added process group

Check the status:

.. code-block:: bash

  [eliza@doolittle ~]$ supervisorctl status
  couchdb                          RUNNING   pid 1312, uptime 0:1:12

If everything looks fine, you should now be able to query CouchDB using ``localhost:5984``:

.. code-block:: bash

  [eliza@dolittle ~]$ curl http://localhost:5984
  {"couchdb":"Welcome","version":"3.1.1","git_sha":"CENSORED","uuid":"CENSORED","features":["access-ready","partitioned","pluggable-storage-engines","reshard","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}

Web Backend
-----------

To expose your CouchDB using a web backend:

.. code-block:: bash

 [eliza@doolittle ~]$ uberspace web backend set /couchdb --http --port 5984 --remove-prefix
