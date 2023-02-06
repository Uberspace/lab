.. author:: ezra <ezra@posteo.de>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: collaborative-editing

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/etherpad.svg
      :align: center

#############
Etherpad Lite
#############

.. tag_list::

`Etherpad Lite`_ is a real-time collaborative writing tool. It is based on :manual:`Node.js <lang-nodejs>` and comes with lots of possible plugins.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 12:

::

 [isabell@stardust ~]$ uberspace tools version use node 12
 Using 'Node.js' version: '12'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your URL needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

First get the Etherpad Lite source code from Github_, be sure to replace the version number ``1.8.3`` here with the latest version number from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 1.8.3 --depth=1 https://github.com/ether/etherpad-lite ~/etherpad
  Cloning into '/home/isabell/etherpad'...
  remote: Enumerating objects: 504, done.
  remote: Counting objects: 100% (504/504), done.
  remote: Compressing objects: 100% (486/486), done.
  remote: Total 504 (delta 22), reused 143 (delta 1), pack-reused 0
  Receiving objects: 100% (504/504), 3.50 MiB | 7.56 MiB/s, done.
  Resolving deltas: 100% (22/22), done.
  Note: checking out '62101147a0c3495dc80daa87ab53a3366321a205'.

  You are in 'detached HEAD' state. You can look around, make experimental
  changes and commit them, and you can discard any commits you make in this
  state without impacting any branches by performing another checkout.

  If you want to create a new branch to retain commits you create, you may
  do so (now or later) by using -b with the checkout command again. Example:

    git checkout -b <new-branch-name>

  [isabell@stardust ~]$


Then run the etherpad script to install the dependencies:

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

Set up a database
-----------------

Run the following code to create the database ``<username>_etherpad`` in MySQL:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_etherpad COLLATE utf8mb4_unicode_ci;"
  [isabell@stardust ~]$

Change the configuration
------------------------

You need to set up the MySQL database settings in ``~/etherpad/settings.json``. Comment this code block by adding ``/*`` before and ``*/`` after like shown below:

.. code-block:: none

  /*
    "dbType" : "dirty",
    "dbSettings" : {
     "filename" : "var/dirty.db"
   },
  */

Uncomment the block for MySQL below by removing ``/*`` and ``*/``. Update the configuration data as shown below. Replace ``<username>`` with your username (2 times) and ``<mysql_password>`` with your password that you looked up in the prerequisites. Update the database name to ``<username>_etherpad`` with your username replaced.

.. code-block:: none
 :emphasize-lines: 3,6,7

  "dbType" : "mysql",
  "dbSettings" : {
    "user":     "<username>",
    "host":     "localhost",
    "port":     3306,
    "password": "<mysql_password>",
    "database": "<username>_etherpad",
    "charset":  "utf8mb4"
  },

Configure the web server
------------------------

.. note::

    etherpad-lite is running on port 9001. Additionally, the ``--remove-prefix`` parameter is needed if you want to run Etherpad Lite under a sub URI like ``/pad`` instead of the root URI ``/``.

.. include:: includes/web-backend.rst

Set up the daemon
-----------------

Create ``~/etc/services.d/etherpad.ini`` with the following content:

.. code-block:: ini

 [program:etherpad]
 directory=%(ENV_HOME)s/etherpad
 command=node %(ENV_HOME)s/etherpad/node_modules/ep_etherpad-lite/node/server.js
 environment=NODE_ENV="production"
 autorestart=true
 startsecs=60


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Best practices
==============

Personalization
---------------

Take a deeper look into the ``~/etherpad/settings.json``, you still might want to adjust the title or the welcoming text of new created pads. If you want to use plugins, you will also need to set up an admin account there. If you've updated the settings, you need to restart etherpad using ``supervisorctl restart etherpad``.

You can also personalize the look of your installation by using your own skin or change an existing one. See `Skins`_ in the documentation for further information.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the pseudo version number ``1.8.3`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/etherpad
  [isabell@stardust etherpad]$ git checkout  -- src/package.json
  [isabell@stardust etherpad]$ git pull origin 1.8.3
  From https://github.com/ether/etherpad-lite
   * tag                 1.8.3      -> FETCH_HEAD
  Updating b8b2e4bc..96ac381a
  Fast-forward
  […]
  [isabell@stardust ~]$

Update the dependencies.

.. code-block:: console

  [isabell@stardust ~]$ ~/etherpad/bin/installDeps.sh
  […]
  [isabell@stardust ~]$


Then you need to restart the service daemon, so the new code is used by the web server:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart etherpad
  etherpad: stopped
  etherpad: started
  [isabell@stardust ~]$


.. _`Etherpad Lite`: http://etherpad.org/
.. _Github: https://github.com/ether/etherpad-lite
.. _feed: https://github.com/ether/etherpad-lite/releases.atom
.. _`Skins`: http://etherpad.org/doc/v1.8.3/#skins

----

Tested with Etherpad Lite 1.8.3 and Uberspace 7.6.0.0

.. author_list::
