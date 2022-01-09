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

Version
=======

Select the desired MongoDB version using:

::

 [isabell@stardust ~]$ uberspace tools version use mongodb 4.4
 Using 'MongoDB' version: '4.4'
 Selected mongodb version 4.4
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Configuration
=============

Create database folder
----------------------

Create the folder ``~/mongodb``. Your databases will be stored there.

.. code-block::

 [isabell@stardust ~]$ mkdir ~/mongodb
 [isabell@stardust ~]$

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

.. code-block::

 [isabell@stardust ~]$ pwgen 32 1
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

.. code-block::
 :emphasize-lines: 1

 [isabell@stardust ~]$ mongo admin ~/mongodb/setup.js
 MongoDB shell version v4.4.3
 connecting to: mongodb://127.0.0.1:27017/admin?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("5309a64f-0c83-44a6-83d9-bdb347a94af0") }
 MongoDB server version: 4.4.3
 Successfully added user: { "user" : "mongodb_mongoroot", "roles" : [ "root" ] }
 [isabell@stardust ~]$

.mongorc.js (optional)
----------------------

To make CLI access using the ``mongo`` command easier, you can create a ``~/.mongorc.js`` file. Every command in this file is executed whenever you run ``mongo``, so to avoid having to enter your password every time, you can store an authentication command there. Replace ``<username>`` and ``<password>`` with your own values.

.. code-block:: none

 db = connect("mongodb://<username>_mongoroot:<password>@127.0.0.1:27017/admin")

Now you can just run ``mongo`` to connect to your MongoDB instance:

.. code-block::

 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.4.3
 connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("cb614de8-7748-4530-b4d4-d42f0e430424") }
 MongoDB server version: 4.4.3
 connecting to: mongodb://127.0.0.1:27017/admin
 Implicit session: session { "id" : UUID("2ec1cc81-3c00-45a9-9f1c-423f7f5d46be") }
 MongoDB server version: 4.4.3
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

When a new version of MongoDB is released, use the `uberspace tools version use`
command to update your installation. Afterwards, restart your instance.

.. warning::

  You may need to perform additional steps to upgrade to the latest version. Please read the
  `release notes <MongoDB release notes_>`_ before you begin.

.. _MongoDB: https://www.mongodb.com/
.. _MongoDB Community Server download page: https://www.mongodb.com/download-center/community
.. _MongoDB Tools download page: https://www.mongodb.com/try/download/database-tools
.. _MongoDB release notes: https://docs.mongodb.com/manual/release-notes/

----

Tested with MongoDB 4.4.3, MongoDB Tools 100.2.0, Uberspace 7.8.1.0

.. author_list::
