.. author:: ezra <ezra@posteo.de>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/etherpad.svg
      :align: center

#############
Etherpad Lite
#############

`Etherpad Lite`_ is a real-time collaborative writing tool. It is based on :manual:`Node.js <lang-nodejs>` and comes with lots of possible plugins.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

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

  [isabell@stardust ~]$ git clone --branch 66.6.6 https://github.com/ether/etherpad-lite ~/etherpad
  Cloning into '/home/isabell/etherpad'...
  remote: Counting objects: 29789, done.
  remote: Compressing objects: 100% (14/14), done.
  remote: Total 29789 (delta 9), reused 16 (delta 7), pack-reused 29768
  Receiving objects: 100% (29789/29789), 19.25 MiB | 6.07 MiB/s, done.
  Resolving deltas: 100% (21251/21251), done.
  Note: checking out '96ac381afb9ea731dad48968f15d77dc6488bd0d'.

  You are in 'detached HEAD' state. You can look around, make experimental
  changes and commit them, and you can discard any commits you make in this
  state without impacting any branches by performing another checkout.

  If you want to create a new branch to retain commits you create, you may
  do so (now or later) by using -b with the checkout command again. Example:

    git checkout -b <new-branch-name>

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

Set up a Database
-----------------

Run the following code to create the database ``<username>_etherpad`` in MySQL:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_etherpad COLLATE utf8mb4_unicode_ci;"
  [isabell@stardust ~]$

Change the configuration
------------------------

You need to set up the MySQL_ database settings in ``~/etherpad/settings.json``. Replace the whole codeblocks:

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

Configure web server
--------------------

.. note::

    etherpad-lite is running on port 9001. Additionally, the ``--remove-prefix`` parameter is needed.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/etherpad.ini`` with the following content:

.. code-block:: ini

 [program:etherpad]
 command=%(ENV_HOME)s/etherpad/bin/run.sh
 environment=NODE_ENV="production"
 autorestart=true

Tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

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

You can also personalize the look of your installation by including custom css- oder js-files. See `Custom static files`_ in the documentation for further information.

**Important**: You need to place your custom-files in ``~/etherpad/node_modules/ep_etherpad-lite/static/custom`` **not** ``~/etherpad/static/custom`` for being recognized by your installation.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the pseudo version number ``66.6.6`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/etherpad
  [isabell@stardust etherpad]$ git checkout  -- src/package.json
  [isabell@stardust etherpad]$ git pull origin 66.6.6
  From https://github.com/ether/etherpad-lite
   * tag                 66.6.6      -> FETCH_HEAD
  Updating b8b2e4bc..96ac381a
  Fast-forward
  […]
  [isabell@stardust ~]$

Then you need to restart the service daemon, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart etherpad
  etherpad: stopped
  etherpad: started
  [isabell@stardust ~]$

It might take a few minutes before your Etherpad comes back online because ``npm`` re-checks and installs dependencies. You can check the service's log file using ``supervisorctl tail -f etherpad``.

.. _`Etherpad Lite`: http://etherpad.org/
.. _Github: https://github.com/ether/etherpad-lite
.. _feed: https://github.com/ether/etherpad-lite/releases.atom
.. _`Custom static files`: http://etherpad.org/doc/v1.6.2/#index_custom_static_files

----

Tested with Etherpad Lite 1.7.0 and Uberspace 7.1.15.0

.. authors::
