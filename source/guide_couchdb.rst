.. highlight:: console

.. author:: Lukas Wolfsteiner <lukas@wolfsteiner.media>

.. tag:: self-hosting
.. tag:: database

.. sidebar:: About

.. image:: _static/images/couchdb.svg
      :align: center

#######
CouchDB
#######

.. tag_list::

Apache CouchDB_ is an open-source document-oriented NoSQL database, implemented in Erlang.

CouchDB uses multiple formats and protocols to store, transfer, and process its data, it uses JSON to store data, JavaScript as its query language using MapReduce, and HTTP for an API.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`the shell <basics-shell>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * http://www.apache.org/licenses/LICENSE-2.0

Prerequisites
=============

We're using :manual:`CouchDB <database-couchdb>` in the stable version 3:

.. code-block:: bash

  [isabell@stardust ~]$ uberspace tools version use couchdb 3
  Selected couchdb version 3
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Installation
============

Uberspace provides the latest binaries, see :manual:`CouchDB <database-couchdb>` on how to interact with them. No extra installation required!

Configuration
=============

Environment setup
-----------------

Next we need to create directories for our configuration and application data:

.. code-block:: bash

  [isabell@stardust ~]$ mkdir -p ~/etc/couchdb
  [isabell@stardust ~]$ mkdir -p ~/opt/couchdb

Application config
------------------

Create ``~/etc/couchdb/local.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. warning:: Replace ``<adminpassword>`` with your super secure password!

.. code-block:: ini

  [couchdb]
  single_node=true
  database_dir = /home/<username>/opt/couchdb/data
  view_index_dir = /home/<username>/opt/couchdb/index

  [chttpd]
  port = 5984
  bind_address = 0.0.0.0

  [admins]
  admin = <adminpassword>

.. note:: Make sure to set your own super secure admin password!

Setup daemon
------------

Create ``~/etc/services.d/couchdb.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

  [program:couchdb]
  command=couchdb -couch_ini /opt/couchdb/etc/default.ini %(ENV_HOME)s/etc/couchdb/local.ini
  autostart=yes
  autorestart=yes

Afterwards, ask ``supervisord`` to look for our new service:

.. code-block:: bash

  [isabell@stardust ~]$ supervisorctl reread
  couchdb: available

And then start your daemon:

.. code-block:: bash

  [isabell@stardust ~]$ supervisorctl update
  couchdb: added process group

Check the status:

.. code-block:: bash

  [isabell@stardust ~]$ supervisorctl status
  couchdb                          RUNNING   pid 1312, uptime 0:1:12

Finishing installation
======================

If everything looks fine, you should now be able to query CouchDB using ``localhost:5984``:

.. code-block:: bash

  [isabell@stardust ~]$ curl http://localhost:5984
  {"couchdb":"Welcome","version":"3.1.1","git_sha":"CENSORED","uuid":"CENSORED","features":["access-ready","partitioned","pluggable-storage-engines","reshard","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}

Best practices
==============

Security
--------

Change all default passwords. Especially the admin password within the config file. Don't get hacked!

Web Backend
-----------

To expose your CouchDB using a web backend (not recommended!):

.. code-block:: bash

 [isabell@stardust ~]$ uberspace web backend set /couchdb --http --port 5984 --remove-prefix

----

.. author_list::
