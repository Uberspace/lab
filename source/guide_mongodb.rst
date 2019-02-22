.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. sidebar:: Logo

  .. image:: _static/images/mongodb.svg
      :align: center

##########
MongoDB
##########

MongoDB_ is a NoSQL database, developed by MongoDB Inc.

----

.. note:: For this guide you should be familiar with the basic concepts of  supervisord_.

License
=======

All relevant legal information can be found here 

  * https://www.mongodb.com/community/licensing

Installation
============

Download MongoDB
----------------

Go to the MongoDB Community Server `download page`_ and select the current version, OS ``RHEL 7.0 Linux 64-bit x64``, package ``TGZ``. Copy the download link and use ``wget`` to download it to your Uberspace:

.. code-block:: bash

 [isabell@stardust ~]$ wget -O ~/mongodb.tgz https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.0.5.tgz
 --2019-01-05 17:15:54--  https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.0.5.tgz
 Resolving fastdl.mongodb.org (fastdl.mongodb.org)... 13.35.198.38, 13.35.198.45, 13.35.198.57, ...
 Connecting to fastdl.mongodb.org (fastdl.mongodb.org)|13.35.198.38|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 88063053 (84M) [application/x-gzip]
 Saving to: /home/isabell/mongodb.tgz’ 
 
 100%[=============================================================>] 88,063,053  27.9MB/s   in 3.0s
 
 2019-01-05 17:15:57 (27.9 MB/s) - ‘/home/isabell/mongodb.tgz’ saved [88063053/88063053]
 [isabell@stardust ~]$



Extract the archive
-------------------

Use ``tar`` to extract the archive. To only extract the binaries, specify the relative path ``mongo*/bin`` and use ``--strip-components=1`` to remove the ``mongodb-linux-x86_64-rhel70-4.0.5/`` prefix from the path.

.. code-block:: bash

 [isabell@stardust ~]$ tar xfv mongodb.tgz mongo*/bin/ --strip-components=1
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongodump
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongorestore
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongoexport
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongoimport
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongostat
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongotop
 mongodb-linux-x86_64-rhel70-4.0.5/bin/bsondump
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongofiles
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongoreplay
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongod
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongos
 mongodb-linux-x86_64-rhel70-4.0.5/bin/mongo
 mongodb-linux-x86_64-rhel70-4.0.5/bin/install_compass
 [isabell@stardust ~]$

You can now delete the archive:

.. code-block:: bash

 [isabell@stardust ~]$ rm mongodb.tgz
 [isabell@stardust ~]$

Create database folder
----------------------

Create the folder ``~/mongodb``. Your databases will be stored there.

.. code-block:: bash

 [isabell@stardust ~]$ mkdir ~/mongodb
 [isabell@stardust ~]$ 

Configuration
=============

Configure port
--------------

MongoDB needs a free TCP port to listen for connections. Run this snippet to find one:

.. include:: includes/generate-port.rst

Setup daemon
------------

Use your favourite editor to create the file ``~/etc/services.d/mongodb.ini`` with the following content. Replace ``<yourport>`` with the port from the previous step.

.. code-block:: ini
 :emphasize-lines: 5

 [program:mongodb]
 command=mongod
   --dbpath %(ENV_HOME)s/mongodb
   --bind_ip 127.0.0.1
   --port <yourport>
   --auth
   --smallfiles
   --unixSocketPrefix %(ENV_HOME)s/mongodb
 autostart=yes
 autorestart=yes

Tell supervisord to refresh its configuration and start the service:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl reread
 mongodb: available
 [isabell@stardust ~]$ supervisorctl update
 mongodb: added process group
 [isabell@stardust ~]$ supervisorctl status 
 mongodb                          RUNNING   pid 24458, uptime 0:00:09
 [isabell@stardust ~]$

If it’s not in state RUNNING, check your configuration.

Create admin user
-----------------

Choose an admin password or generate a random one one using this snippet:

.. code-block:: bash

 [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-15};echo;
 randompassword
 [isabell@stardust ~]$ 

Create ``~/mongodb/setup.js``. Replace ``<username>`` with your Uberspace user name and ``<password>`` with the password you just chose or generated.

.. code-block:: none
 :emphasize-lines: 3,4

 db.createUser(
    {
      user: "<username>_mongoadmin",
      pwd: "<password>",
      roles: [ "root" ]
    }
 )

Use ``mongo`` to run ``setup.js``. Replace ``<yourport>`` with your MongoDB port.

.. code-block:: bash
 :emphasize-lines: 1

 [isabell@stardust ~]$ mongo --port <yourport> admin ~/mongodb/setup.js
 MongoDB shell version v4.0.5
 connecting to: mongodb://127.0.0.1:63325/admin?gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("0ddef66e-e716-4ef2-bbc2-a50dfc3fad7e") }
 MongoDB server version: 4.0.5
 Successfully added user: { "user" : "isabell_mongoadmin", "roles" : [ "root" ] }
 [isabell@stardust ~]$

.mongorc.js (optional)
----------------------

To make CLI access using the ``mongo`` command easier, you can create a ``~/.mongorc.js`` file. Every command in this file is executed whenever you run ``mongo``, so to avoid having to enter your password every time, you can store an authentication command there. Replace ``<username>``, ``<password>`` and ``<yourport>`` with your own values.

.. code-block:: none

 db = connect("mongodb://<username>_mongoadmin:<password>@127.0.0.1:<yourport>/admin")

Since ``mongo`` tries to connect to the default MongoDB port before executing ``.mongorc.js``, you need to run it with the ``--nodb`` parameter. Set an alias in your ``~/.bash_profile`` to do this automatically:

.. code-block:: bash

 [isabell@stardust ~]$ echo "alias mongo='mongo --nodb'" >> ~/.bash_profile
 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$ 

Now you can just run ``mongo`` to connect to your MongoDB instance:

.. code-block:: none

 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.0.5
 connecting to: mongodb://127.0.0.1:61026/admin
 Implicit session: session { "id" : UUID("6fd371f6-e1fa-461c-be0c-ea3cbe230a01") }
 MongoDB server version: 4.0.5
 >

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
 MongoDB shell version v4.0.5
 connecting to: mongodb://127.0.0.1:61026/admin
 Implicit session: session { "id" : UUID("78d3c750-5119-4e2f-aa5b-2b0b4ede919b") }
 MongoDB server version: 4.0.5
 > exit
 bye
 [isabell@stardust ~]$

.. _MongoDB: https://www.mongodb.com/
.. _download page: https://www.mongodb.com/download-center/community
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

----

Tested with MongoDB 4.0.5, Uberspace 7.2.1.0

.. authors::

