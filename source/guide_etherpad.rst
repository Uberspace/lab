.. sectionauthor:: ezzra <ezra@posteo.de>
.. tags:: nodejs, text
.. highlight:: console

#############
Etherpad Lite
#############

`Etherpad Lite`_ is a real-time collaborative writing tool. It is based on Node.js_ and comes with lots of possible plugins.

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

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First get the Etherpad Lite source code from Github_, be sure to replace the pseudo version number ``66.6.6`` here with the latest version number from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch release/66.6.6 https://github.com/ether/etherpad-lite ~/etherpad
  Cloning into '/home/isabell/etherpad'...
  remote: Counting objects: 29789, done.
  remote: Compressing objects: 100% (14/14), done.
  remote: Total 29789 (delta 9), reused 16 (delta 7), pack-reused 29768
  Receiving objects: 100% (29789/29789), 19.25 MiB | 6.07 MiB/s, done.
  Resolving deltas: 100% (21251/21251), done.
  [isabell@stardust ~]$


Then run the etherpad script, to install the dependencies:

.. code-block:: console

  [isabell@stardust ~]$ ~/etherpad/bin/installDeps.sh
  Copy the settings template to settings.json...
  Ensure that all dependencies are up to date...  If this is the first time you have run Etherpad please be patient.
  [...]
  Clearing minified cache...
  Ensure custom css/js files are created...
  [isabell@stardust ~]$


Configuration
=============

Configure port
--------------

Since Node.js applications use their own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Set up a Database
-----------------

Run the following code to create the database ``<username>_etherpad`` in MySQL:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_etherpad COLLATE utf8mb4_unicode_ci;"
  [isabell@stardust ~]$

Change the configuration
------------------------

You need to adjust your ``~/etherpad/settings.json`` with the new port. Find the following code block and change port 9001 to your own port:

.. code-block:: none
 :emphasize-lines: 3

  //IP and port which etherpad should bind at
  "ip": "0.0.0.0",
  "port" : 9001,

You also need to set up the MySQL_ database settings, therefore you should completely replace these codeblocks:

.. code-block:: none

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

with the following. Be sure to replace ``<username>`` with your username (2 times) and ``<mysql_password>`` with your password that you looked up in the prerequisites:

.. code-block:: none
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
 command=/home/isabell/etherpad/bin/run.sh

Tell supervisord_ to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 etherpad: available
 [isabell@stardust ~]$ supervisorctl update
 etherpad: added process group
 [isabell@stardust ~]$ supervisorctl status
 etherpad                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Best practices
==============

Personalization
---------------

Take a deeper look into the ``~/etherpad/settings.json``, you still might want to adjust the title or the welcoming text of new created pads. If you want to use plugins, you will also need to set up a admin account there.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the pseudo version number ``66.6.6`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/etherpad
  [isabell@stardust ~]$ git pull origin release/66.6.6
  From git://github.com/ether/etherpad-lite
  * branch              release/66.6.6 -> FETCH_HEAD
  Updating e84c6962..1e25e7fc
  Fast-forward
  [...]
  32 files changed, 2033 insertions(+), 212 deletions(-)
  [...]
  [isabell@stardust ~]$

Then you need to restart the service daemon, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart etherpad
  etherpad: stopped
  etherpad: started
  [isabell@stardust ~]$
  


.. _`Etherpad Lite`: http://etherpad.org/
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _Github: https://github.com/ether/etherpad-lite
.. _feed: https://github.com/ether/etherpad-lite/releases.atom

----

Tested with Etherpad Lite 1.6.3 and Uberspace 7.1.1 
