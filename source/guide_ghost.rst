.. author:: Uberspace <hallo@uberspace.de>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/ghost.png 
      :align: center

#####
Ghost
#####

Ghost_ is a open source blogging platform written in JavaScript and distributed under the MIT License, designed to simplify the process of online publishing for individual bloggers as well as online publications.

The concept of the Ghost platform was first floated publicly in November 2012 in a blog post by project founder John O'Nolan, which generated enough response to justify coding a prototype version with collaborator Hannah Wolfe.

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

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install ghost-cli
-----------------

Use ``npm`` to install ``ghost-cli`` globally:

::

 [isabell@stardust ~]$ npm i -g ghost-cli
 [...]
 + ghost-cli@1.5.2
 added 470 packages in 16.495s
 [isabell@stardust ~]$ 

Install Ghost
-------------

Create a ``ghost`` directory in your home, ``cd`` to it and then run the installer. Since the installer expects to be run with root privileges, we need to adjust some settings_:

  * ``--no-stack``: Disables the system stack check during setup. Since we're a shared hosting provider, the stack is maintained by us.
  * ``-no-setup-linux-user``: Skips creating a linux user. You can't do that without root privileges.
  * ``--no-setup-systemd``: Skips creation of a systemd unit file. We'll use supervisord_ later instead.
  * ``--no-setup-nginx``: Skips webserver configuration. We'll use a htaccess_ file for apache_ later instead.
  * ``--no-setup-mysql``: Skips setup of MySQL_. You can't do that without root privileges.

You will need to enter the following information:

  * your blog URL: The URL for your blog. Since we don't allow HTTP, use HTTPS. For example: https://isabell.uber.space
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Ghost database name: we suggest you use a additional_ database. For example: isabell_ghost
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
 ✔ Downloading and installing Ghost v1.21.2
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

Configure port
--------------

Since Node.js applications use their own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Change the configuration
------------------------

You need to adjust your ``~/ghost/config.production.json`` with the new port. Find the following code block and change port 2369 to your own port:

::

 "server": {
   "port": 2369,
   "host": "127.0.0.1"
 },

In our example this would be:

::

 "server": {
   "port": 9000,
   "host": "127.0.0.1"
 },

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

Create ``~/etc/services.d/ghost.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

 [program:ghost]
 directory=/home/<username>/ghost
 command=env NODE_ENV=production /bin/node current/index.js

In our example this would be:

.. code-block:: ini

 [program:ghost]
 directory=/home/isabell/ghost
 command=env NODE_ENV=production /bin/node current/index.js

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ghost]$ supervisorctl reread
 ghost: available
 [isabell@stardust ghost]$ supervisorctl update
 ghost: added process group
 [isabell@stardust ~]$ supervisorctl status
 ghost                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your blog URL and create a user account.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Ghost's `releases <https://github.com/TryGhost/Ghost/releases/latest>`_ for the latest version and copy the link to the ``.zip`` archive. In this example the version is 23.42.1, which of course does not exist. Change the version to the latest one in the highlighted lines.

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd ~/ghost/versions/
 [isabell@stardust versions]$ wget https://github.com/TryGhost/Ghost/releases/download/23.42.1/Ghost-23.42.1.zip
 [isabell@stardust versions]$ unzip Ghost-23.42.1.zip -d 23.42.1
 [isabell@stardust versions]$

Install the required ``node`` modules:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd ~/ghost/versions/23.42.1/content
 [isabell@stardust content]$ npm install --production
 [...]
 added 91 packages, removed 134 packages and updated 544 packages in 27.303s
 [isabell@stardust content]$ 

Replace the ``current`` symlink and link to the newest version. Again, replace the version number with the newest version.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ rm ~/ghost/current
 [isabell@stardust ~]$ ln -s $HOME/ghost/versions/23.42.1 $HOME/ghost/current
 [isabell@stardust ~]$ supervisorctl restart ghost
 ghost: stopped
 ghost: started
 [isabell@stardust ~]$ supervisorctl status
 ghost                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

.. _Ghost: https://ghost.org
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _settings: https://docs.ghost.org/v1/docs/cli-install
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _htaccess: https://manual.uberspace.de/en/web-documentroot.html#own-configuration
.. _apache: https://manual.uberspace.de/en/lang-nodejs.html#connection-to-webserver
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _feed: https://github.com/TryGhost/Ghost/releases.atom

----

Tested with Ghost 1.22.1, Uberspace 7.1.1

.. authors::
