.. highlight:: console

.. sidebar:: About

  This guide has been tested with Uberspace 7.1.1 and Etherpad Lite 1.6.3

#############
Etherpad Lite
#############

Etherpad Lite is a real-time collaborative writing tool. It is based on NodeJs and comes with lot of possible plugins.

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * Node.js_ and its package manager npm_ 
  * MySQL_ 
  * supervisord_
  * domains_

Prerequisites
=============

We're using Node.js_ in the stable version 8:

::

 [etherpad@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [etherpad@stardust ~]$ 

You'll need your MySQL_ credentials. Get them with ``my_print_defaults``:

::

 [etherpad@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=etherpad
 --password=MySuperSecretPassword
 [etherpad@stardust ~]$ 

Your domain needs to be setup:

::

 [etherpad@stardust ~]$ uberspace web domain list
 etherpad.uber.space
 [etherpad@stardust ~]$ 

Installation
============

First get the Etherpad Lite source code from Github_:

.. code-block:: console

  [etherpad@stardust ~]$ git clone https://github.com/ether/etherpad-lite ~/etherpad

Then run the etherpad script, to install the dependencies:

.. code-block:: console

  [etherpad@stardust ~]$ ~/etherpad/bin/installDeps.sh

Configuration
=============

Configure port
--------------

Since Node.js applications use their own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Set up a Database
-----------------

Run the following code to create the database ``<username>_etherpad``:

.. code-block:: console

  [etherpad@stardust ~]$ mysql -e "CREATE DATABASE $USER_etherpad COLLATE utf8mb4_unicode_ci;"

Change the configuration
------------------------

You need to adjust your ``~/etherpad/settings.json`` with the new port. Find the following code block and change port 9001 to your own port:

.. code-block:: console
 :emphasize-lines: 3

  //IP and port which etherpad should bind at
  "ip": "0.0.0.0",
  "port" : 9001,

You also need to set up the MySQL_ databse settings, therefore you should completely replace these codeblocks:

::

  //The Type of the database. You can choose between dirty, postgres, sqlite and mysql
  //You shouldn't use "dirty" for for anything else than testing or development
  "dbType" : "dirty",
  //the database specific settings
  "dbSettings" : {
                   "filename" : "var/dirty.db"
                 },

  /* An Example of MySQL Configuration
   "dbType" : "mysql",
   "dbSettings" : {
                    "user"    : "root",
                    "host"    : "localhost",
                    "password": "",
                    "database": "store",
                    "charset" : "utf8mb4"
                  },
  */

with the following. Watch out to replace ``<username>`` with your username (2 times) and ``<mysql_password>`` with your password that you looked up in the prerequisites:

.. code-block:: console
 :emphasize-lines: 4,6,7
 
  //MySQL Configuration
  "dbType" : "mysql",
  "dbSettings" : {
                    "user"    : "<username>",
                    "host"    : "localhost",
                    "password": "<mysql_password>",
                    "database": "<username>_etherpad",
                    "charset" : "utf8mb4"
                  },

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

Create ``~/etc/services.d/etherpad.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

 [program:etherpad]
 command=/home/<username>/etherpad/bin/run.sh

In our example this would be:

.. code-block:: ini

 [program:etherpad]
 command=/home/etherpad/etherpad/bin/run.sh

Tell supervisord_ to refresh its configuration and start the service:

::

 [etherpad@stardust ~]$ supervisorctl reread
 etherpad: available
 [etherpad@stardust ~]$ supervisorctl update
 etherpad: added process group
 [etherpad@stardust ~]$ supervisorctl status
 etherpad                            RUNNING   pid 26020, uptime 0:03:14
 [etherpad@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

Best practices
==============

Personalization
---------------

Take a deeper look into the ``~/etherpad/settings.json``, you still might want to adjust the title or the welcoming text of new created pads. If you want to use plugins, you will also need to set up a admin account there.

Updates
=======

.. note:: You need to keep Etherpad Lite updated by pulling the current sourcecode from Github with ``git pull origin``. Afterwards, use ``supervisorctl restart etherpad`` to restart with the new codebase.


.. _Loremipsum: https://en.wikipedia.org/wiki/Lorem_ipsum
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/lorem/ipsum/releases.atom
.. _Github: https://github.com/ether/etherpad-lite