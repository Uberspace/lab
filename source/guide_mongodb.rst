.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-cpp
.. tag:: database
.. tag:: audience-developers

.. sidebar:: Logo

  .. image:: _static/images/mongodb.svg
      :align: center

##########
MongoDB
##########

.. tag_list::

MongoDB_ is a NoSQL database, developed by MongoDB Inc.

----

.. note:: For this guide you should be familiar with the basic concepts of :manual:`supervisord <daemons-supervisord>`.

License
=======

All relevant legal information can be found here

  * https://www.mongodb.com/community/licensing

Installation
============

Download MongoDB
----------------

Go to the `MongoDB Community Server download page`_ and select the current version, OS ``RHEL 7.0 Linux 64-bit x64``, package ``TGZ``. Copy the download link and use ``wget`` to download it to your Uberspace:

.. code-block:: bash

 [isabell@stardust ~]$ wget -O ~/mongodb.tgz https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.4.1.tgz
 --2020-10-28 22:40:46--  https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.4.1.tgz
 Resolving fastdl.mongodb.org (fastdl.mongodb.org)... 99.86.2.52, 99.86.2.36, 99.86.2.55, ...
 Connecting to fastdl.mongodb.org (fastdl.mongodb.org)|99.86.2.52|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 71253687 (68M) [application/gzip]
 Saving to: ‘/home/isabell/mongodb.tgz’

 100%[==============================================================================================================================>] 71.253.687  22,9MB/s   in 3,0s   

 2020-10-28 22:40:49 (22,9 MB/s) - ‘/home/isabell/mongodb.tgz’ saved [71253687/71253687]

 [isabell@stardust ~]$

Extract the archive
-------------------

Use ``tar`` to extract the archive. To only extract the binaries, specify the relative path ``mongo*/bin`` and use ``--strip-components=1`` to remove the ``mongodb-linux-x86_64-rhel70-4.4.1/`` prefix from the path.

.. code-block:: bash

 [isabell@stardust ~]$ tar xfv mongodb.tgz mongo*/bin/ --strip-components=1
 mongodb-linux-x86_64-rhel70-4.4.1/bin/install_compass
 mongodb-linux-x86_64-rhel70-4.4.1/bin/mongo
 mongodb-linux-x86_64-rhel70-4.4.1/bin/mongod
 mongodb-linux-x86_64-rhel70-4.4.1/bin/mongos
 [isabell@stardust ~]$

You can now delete the archive:

.. code-block:: bash

 [isabell@stardust ~]$ rm mongodb.tgz
 [isabell@stardust ~]$

Download MongoDB Tools
----------------------

Go to the `MongoDB Tools download page`_ and select the current version, OS ``RHEL 7.0 Linux 64-bit x64``, package ``TGZ``. Copy the download link and use ``wget`` to download it to your Uberspace:

.. code-block:: bash

 [isabell@stardust ~]$ wget -O ~/mongodb_tools.tgz https://fastdl.mongodb.org/tools/db/mongodb-database-tools-rhel70-x86_64-100.2.0.tgz
 --2020-10-28 22:44:20--  https://fastdl.mongodb.org/tools/db/mongodb-database-tools-rhel70-x86_64-100.2.0.tgz
 Resolving fastdl.mongodb.org (fastdl.mongodb.org)... 99.86.2.50, 99.86.2.52, 99.86.2.55, ...
 Connecting to fastdl.mongodb.org (fastdl.mongodb.org)|99.86.2.50|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 67141659 (64M) [binary/octet-stream]
 Saving to: ‘/home/isabell/mongodb_tools.tgz’

 100%[==============================================================================================================================>] 67.141.659  41,3MB/s   in 1,5s   

 2020-10-28 22:44:22 (41,3 MB/s) - ‘/home/isabell/mongodb_tools.tgz’ saved [67141659/67141659]
 
 [isabell@stardust ~]$



Extract the tool archive
------------------------

Use ``tar`` to extract the archive. To only extract the binaries, specify the relative path ``mongo*/bin`` and use ``--strip-components=1`` to remove the ``mongodb-database-tools-rhel70-x86_64-100.2.0/`` prefix from the path.

.. code-block:: bash

 [isabell@stardust ~]$ tar xfv mongodb_tools.tgz mongo*/bin/ --strip-components=1
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/bsondump
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongodump
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongoexport
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongofiles
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongoimport
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongorestore
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongostat
 mongodb-database-tools-rhel70-x86_64-100.2.0/bin/mongotop 
 [isabell@stardust ~]$

You can now delete the archive:

.. code-block:: bash

 [isabell@stardust ~]$ rm mongodb_tools.tgz
 [isabell@stardust ~]$



Create database folder
----------------------

Create the folder ``~/mongodb``. Your databases will be stored there.

.. code-block:: bash

 [isabell@stardust ~]$ mkdir ~/mongodb
 [isabell@stardust ~]$

Configuration
=============

Setup daemon
------------

Use your favourite editor to create the file ``~/etc/services.d/mongodb.ini`` with the following content.

.. code-block:: ini

 [program:mongodb]
 command=mongod
   --dbpath %(ENV_HOME)s/mongodb
   --bind_ip 127.0.0.1
   --auth
   --unixSocketPrefix %(ENV_HOME)s/mongodb
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.

Create root user
-----------------

Choose a root password or generate a random one using this snippet:

.. code-block:: bash

 [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-15};echo;
 randompassword
 [isabell@stardust ~]$

Create ``~/mongodb/setup.js``. Replace ``<username>`` with your Uberspace user name and ``<password>`` with the password you just chose or generated.

.. code-block:: none
 :emphasize-lines: 3,4

 db.createUser(
    {
      user: "<username>_mongoroot",
      pwd: "<password>",
      roles: [ "root" ]
    }
 )

Use ``mongo`` to run ``setup.js``.

.. code-block:: bash
 :emphasize-lines: 1

 [isabell@stardust ~]$ mongo admin ~/mongodb/setup.js
 MongoDB shell version v4.4.1
 connecting to: mongodb://127.0.0.1:27017/admin?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("5309a64f-0c83-44a6-83d9-bdb347a94af0") }
 MongoDB server version: 4.4.1
 Successfully added user: { "user" : "mongodb_mongoroot", "roles" : [ "root" ] }
 [isabell@stardust ~]$

.mongorc.js (optional)
----------------------

To make CLI access using the ``mongo`` command easier, you can create a ``~/.mongorc.js`` file. Every command in this file is executed whenever you run ``mongo``, so to avoid having to enter your password every time, you can store an authentication command there. Replace ``<username>`` and ``<password>`` with your own values.

.. code-block:: none

 db = connect("mongodb://<username>_mongoroot:<password>@127.0.0.1:27017/admin")

Now you can just run ``mongo`` to connect to your MongoDB instance:

.. code-block:: none

 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.4.1
 connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("cb614de8-7748-4530-b4d4-d42f0e430424") }
 MongoDB server version: 4.4.1
 connecting to: mongodb://127.0.0.1:27017/admin
 Implicit session: session { "id" : UUID("2ec1cc81-3c00-45a9-9f1c-423f7f5d46be") }
 MongoDB server version: 4.4.1
 ---
 The server generated these startup warnings when booting: 
        2020-10-28T22:49:35.811+01:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
        2020-10-28T22:49:35.811+01:00: /sys/kernel/mm/transparent_hugepage/defrag is 'always'. We suggest setting it to 'never'
        2020-10-28T22:49:35.811+01:00: Soft rlimits too low
        2020-10-28T22:49:35.811+01:00:         currentValue: 1024
        2020-10-28T22:49:35.811+01:00:         recommendedMinimum: 64000
 ---
 ---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()

 >

You can exit the shell by entering ``exit``.

Updates
=======

When a new version of MongoDB is released, use the following steps to update your installation:

Stop your MongoDB
-----------------

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl stop mongodb
 mongodb: stopped
 [isabell@stardust ~]$

Download and extract
--------------------

Go through the same steps as above to download and extract the archive.

Restart and check version
-------------------------

Restart your MongoDB and login to check the version.

.. code-block:: bash
 :emphasize-lines: 4,7

 [isabell@stardust ~]$ supervisorctl start mongodb
 mongodb: started
 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.4.1
 connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("cb614de8-7748-4530-b4d4-d42f0e430424") }
 MongoDB server version: 4.4.1
 connecting to: mongodb://127.0.0.1:27017/admin
 Implicit session: session { "id" : UUID("2ec1cc81-3c00-45a9-9f1c-423f7f5d46be") }
 MongoDB server version: 4.4.1
 ---
 The server generated these startup warnings when booting: 
        2020-10-28T22:49:35.811+01:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
        2020-10-28T22:49:35.811+01:00: /sys/kernel/mm/transparent_hugepage/defrag is 'always'. We suggest setting it to 'never'
        2020-10-28T22:49:35.811+01:00: Soft rlimits too low
        2020-10-28T22:49:35.811+01:00:         currentValue: 1024
        2020-10-28T22:49:35.811+01:00:         recommendedMinimum: 64000
 ---
 ---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()

 > exit
 bye
 [isabell@stardust ~]$

.. _MongoDB: https://www.mongodb.com/
.. _MongoDB Community Server download page: https://www.mongodb.com/download-center/community
.. _MongoDB Tools download page: https://www.mongodb.com/try/download/database-tools

----

Tested with MongoDB 4.4.1, Uberspace 7.7.9.0

.. author_list::

