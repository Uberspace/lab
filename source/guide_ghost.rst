.. author:: nichtmax <https://moritz.in>
.. author:: Peleke <https://www.peleke.de>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: blog

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ghost.svg
      :align: center

#####
Ghost
#####

.. tag_list::

Ghost_ is a open source blogging platform written in JavaScript and distributed under the MIT License, designed to simplify the process of online publishing for individual bloggers as well as online publications.

The concept of the Ghost platform was first floated publicly in November 2012 in a blog post by project founder John O'Nolan, which generated enough response to justify coding a prototype version with collaborator Hannah Wolfe.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 10:

::

 [isabell@stardust ~]$ uberspace tools version use node 10
 Using 'Node.js' version: '10'
 Selected node version 10
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [eliza@dolittle ~]$

.. include:: includes/my-print-defaults.rst

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install ghost-cli and knex-migrator
-----------------------------------

Use ``npm`` to install ``ghost-cli`` and ``knex-migrator`` globally:

::

 [isabell@stardust ~]$ npm i -g ghost-cli knex-migrator
 [...]
 + ghost-cli@1.9.1
 + knex-migrator@3.2.3
 added 690 packages in 31.543s
 [isabell@stardust ~]$

Install Ghost
-------------

Create a ``ghost`` directory in your home, ``cd`` to it and then run the installer. Since the installer expects to be run with root privileges, we need to adjust some settings_:

  * ``--no-stack``: Disables the system stack check during setup. Since we're a shared hosting provider, the stack is maintained by us.
  * ``--no-setup-linux-user``: Skips creating a linux user. You can't do that without root privileges.
  * ``--no-setup-systemd``: Skips creation of a systemd unit file. We'll use :manual:`supervisord <daemons-supervisord>` later instead.
  * ``--no-setup-nginx``: Skips webserver configuration. We'll use a :manual_anchor:`htaccess <web-documentroot.html#own-configuration>` file for :manual_anchor:`apache <lang-nodejs.html#connection-to-webserver>` later instead.
  * ``--no-setup-mysql``: Skips setup of :manual:`MySQL <database-mysql>`. You can't do that without root privileges.

You will need to enter the following information:

  * your blog URL: The URL for your blog. Since we don't allow HTTP, use HTTPS. For example: https://isabell.uber.space
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Ghost database name: we suggest you use a :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_ghost
  * Do you want to start Ghost?: Answer No.

.. code-block:: console
 :emphasize-lines: 1,2,3,12,13,14,15,16,25

 [isabell@stardust ~]$ mkdir ~/ghost
 [isabell@stardust ~]$ cd ~/ghost
 [isabell@stardust ghost]$ ghost install --no-stack --no-setup-linux-user --no-setup-systemd --no-setup-nginx --no-setup-mysql
 ✔ Checking system Node.js version
 ✔ Checking current folder permissions
 ℹ Checking operating system compatibility [skipped]
 ✔ Checking for a MySQL installation
 ✔ Checking for latest Ghost version
 ✔ Setting up install directory
 ✔ Downloading and installing Ghost v2.0.0
 ✔ Finishing install process
 ? Enter your blog URL: https://isabell.uber.space
 ? Enter your MySQL hostname: localhost
 ? Enter your MySQL username: isabell
 ? Enter your MySQL password: [hidden]
 ? Enter your Ghost database name: isabell_ghost
 ✔ Configuring Ghost
 ✔ Setting up instance
 ℹ Setting up "ghost" mysql user [skipped]
 ℹ Setting up Nginx [skipped]
 Task ssl depends on the 'nginx' stage, which was skipped.
 ℹ Setting up SSL [skipped]
 ℹ Setting up Systemd [skipped]
 ✔ Running database migrations
 ? Do you want to start Ghost? No
 [isabell@stardust ghost]$

Configuration
=============

Change network interface
------------------------

You need to adjust your ``~/ghost/config.production.json`` to use the right
network interface. Find the following block and change host ``127.0.0.1`` to
``0.0.0.0``:

.. code-block:: none
 :emphasize-lines: 5

 {
   "url": "https://isabell.uber.space",
   "server": {
     "port": 2368,
     "host": "0.0.0.0"
   },

Configure web server
--------------------

.. note::

    Ghost is running on port 2368.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/ghost.ini`` with the following content:

.. code-block:: ini

 [program:ghost]
 directory=%(ENV_HOME)s/ghost
 command=env NODE_ENV=production /bin/node current/index.js

.. include:: includes/supervisord.rst

Finishing installation
======================

Point your browser to your blog URL and create a user account.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Download and unzip new version
------------------------------

Check Ghost's `releases <https://github.com/TryGhost/Ghost/releases/latest>`_ for the latest version and copy the link to the ``.zip`` archive. In this example the version is 23.42.1, which of course does not exist. Change the version to the latest one in the highlighted lines.

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd ~/ghost/versions/
 [isabell@stardust versions]$ wget https://github.com/TryGhost/Ghost/releases/download/23.42.1/Ghost-23.42.1.zip
 [isabell@stardust versions]$ unzip Ghost-23.42.1.zip -d 23.42.1
 Archive:  Ghost-23.42.1.zip
 [isabell@stardust versions]$

Install the required ``node`` modules
-------------------------------------

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd ~/ghost/versions/23.42.1/content
 [isabell@stardust content]$ npm install --production
 [...]
 added 91 packages, removed 134 packages and updated 544 packages in 27.303s
 [isabell@stardust content]$

Migrate your database
---------------------

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/ghost
 [isabell@stardust ~]$ NODE_ENV=production knex-migrator migrate --mgpath ./versions/23.42.1/
 [2018-08-22 14:18:21] INFO Creating database backup
 […]
 [2018-08-22 16:18:23] INFO Finished database migration!

Replace the ``current`` symlink and link to the newest version
--------------------------------------------------------------

Again, replace the version number with the newest version.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ ln -sfn $HOME/ghost/versions/23.42.1 $HOME/ghost/current
 [isabell@stardust ~]$ supervisorctl restart ghost
 ghost: stopped
 ghost: started
 [isabell@stardust ~]$ supervisorctl status
 ghost                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Update via script
-----------------

As an alternative to this manual process of updating Ghost to a new version you can also use the following script:

.. code-block:: console
 :emphasize-lines: 4

 #!/bin/bash
 #set -v
 # created by peleke.de
 GHOSTDIR=~/ghost
 PACKAGE_VERSION_OLD=$(sed -nE 's/^\s*"version": "(.*?)",$/\1/p' $GHOSTDIR/current/package.json)
 CURRENT_GHOST=$(curl -s https://api.github.com/repos/TryGhost/Ghost/releases | grep tag_name | head -n 1 | cut -d '"' -f 4)
 CURRENT_GHOST_DOWNLOAD=$(curl -s https://api.github.com/repos/TryGhost/Ghost/releases/latest | grep browser_download_url | cut -d '"' -f 4)
 CURRENT_GHOST_FILE=$(echo $CURRENT_GHOST_DOWNLOAD | sed 's:.*/::')
 echo "installed version: $PACKAGE_VERSION_OLD"
 echo "available version: $CURRENT_GHOST"
 cd $GHOSTDIR
 if [[ $CURRENT_GHOST != $PACKAGE_VERSION_OLD ]]
 then
   read -r -p "Do you want to update Ghost $PACKAGE_VERSION_OLD to version $CURRENT_GHOST? [Y/n] " response
   if [[ $response =~ ^([yY]|"")$ ]]
   then
     echo "downloading and unpacking ghost $CURRENT_GHOST ..."
     cd $GHOSTDIR/versions/
     curl -LOk $CURRENT_GHOST_DOWNLOAD
     unzip $GHOSTDIR/versions/$CURRENT_GHOST_FILE -d $CURRENT_GHOST
     rm $GHOSTDIR/versions/$CURRENT_GHOST_FILE
     echo "Updating ghost ..."
     cd $GHOSTDIR/versions/$CURRENT_GHOST
     npm install --production
     echo "Migrating ghost database ..."
     cd $GHOSTDIR
     NODE_ENV=production knex-migrator migrate --mgpath $GHOSTDIR/versions/$CURRENT_GHOST
     ln -sfn $GHOSTDIR/versions/$CURRENT_GHOST $GHOSTDIR/current
     PACKAGE_VERSION=$(sed -nE 's/^\s*"version": "(.*?)",$/\1/p' $GHOSTDIR/current/package.json)
     echo "Ghost $PACKAGE_VERSION_OLD has been updated to version $PACKAGE_VERSION"
     echo "Restarting Ghost. This may take a few seconds ..."
     supervisorctl restart ghost
     supervisorctl status
     echo "If something seems wrong, please check the logs: 'supervisorctl tail ghost'"
     echo "To revert to version $PACKAGE_VERSION_OLD run the following command: 'ln -sfn $GHOSTDIR/versions/$PACKAGE_VERSION_OLD $GHOSTDIR/current' and restart ghost using 'supervisorctl restart ghost'."
   fi
 else
   echo "-> Ghost is already up-to-date, no update needed."
 fi


.. _Ghost: https://ghost.org
.. _settings: https://docs.ghost.org/api/ghost-cli/
.. _feed: https://github.com/TryGhost/Ghost/releases.atom

----

Tested with Ghost 2.15.0, Uberspace 7.2.4

.. author_list::
