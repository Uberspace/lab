.. sidebar:: Logo
  
  .. image:: _static/images/ghost.png 
      :align: center

#####
Ghost
#####

Ghost_ is a open source blogging platform written in JavaScript and distributed under the MIT License, designed to simplify the process of online publishing for individual bloggers as well as online publications.

The concept of the Ghost platform was first floated publicly in November 2012 in a blog post by project founder John O'Nolan, which generated enough response to justify coding a prototype version with collaborator Hannah Wolfe.

.. note:: For this guide you should be familiar with the basic concepts of 

  * Node.js_ and its package manager npm_ 
  * MySQL_ 
  * supervisord_
  * domains_

Prerequisites
=============

We're using Node.js_ in the stable version 8:

.. code-block:: none

 [moritz@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [moritz@stardust ~]$ 

You'll need your MySQL credentials_. Get them with ``my_print_defaults``:

.. code-block:: none

 [moritz@stardust ghost]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=moritz
 --password=MySuperSecretPassword
 [moritz@stardust ghost]$ 

Installation
============

Install ghost-cli
-----------------

Use ``npm`` to install ``ghost-cli`` globally:

.. code-block:: none

 [moritz@stardust ~]$ npm i -g ghost-cli
 [...]
 + ghost-cli@1.5.2
 added 470 packages in 16.495s
 [moritz@stardust ~]$ 

Install Ghost
-------------

Create a ``ghost`` directory in your home, ``cd`` to it and then run the installer. Since the installer expects to be run with root privileges, we need to adjust some settings_:

  * ``--no-stack``: Disables the system stack check during setup. Since we're a shared hosting provider, the stack is maintained by us.
  * ``-no-setup-linux-user``: Skips creating a linux user. You can't do that without root privileges.
  * ``--no-setup-systemd``: Skips creation of a systemd unit file. We'll use supervisord_ later instead.
  * ``--no-setup-nginx``: Skips webserver configuration. We'll use a htaccess_ file for apache_ later instead.
  * ``--no-setup-mysql``: Skips setup of MySQL_. You can't do that without root privileges.

You will need to enter the following information:

  * your blog URL: The URL for your blog. Since we don't allow HTTP, use HTTPS. For example: https://moritz.uber.space
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Ghost database name: we suggest you use a additional_ database. For example: moritz_ghost
  * Do you want to start Ghost?: Answer No.

.. code-block:: none

 [moritz@stardust ~]$ mkdir ~/ghost
 [moritz@stardust ~]$ cd ~/ghost
 [moritz@stardust ghost]$ ghost install --no-stack --no-setup-linux-user --no-setup-systemd --no-setup-nginx --no-setup-mysql
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
 [moritz@stardust ghost]$ 

Setup
=====

Configure port
--------------

Since Node.js applications use their own webserver, you need to find a free port and bind your application to it.

.. code-block:: none

 [moritz@stardust ghost]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9000
 [moritz@stardust ghost]$ 

Write the port down. In our example it is 9000. In reality you'll get a free port between 61000 and 65535.

Change the configuration
------------------------

You need to adjust your ``~/ghost/config.production.json`` with the new port. Find the following code block and change port 2369 to your own port:

.. code-block:: json

 "server": {
   "port": 2369,
   "host": "127.0.0.1"
 },

In our example this would be:

.. code-block:: json

 "server": {
   "port": 9000,
   "host": "127.0.0.1"
 },

Setup .htaccess
---------------

Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: none

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteRule ^(.*) http://localhost:<yourport>/$1 [P]

In our example this would be:

.. code-block:: none

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteRule ^(.*) http://localhost:9000/$1 [P]

Set up ``supervisord``
======================

Create ``~/etc/services.d/ghost.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

 [program:ghost]
 directory=/home/<username>/ghost
 command=env NODE_ENV=production /bin/node current/index.js


Let ``supervisord`` re-read its configuration and start the Ghost service:

.. code-block:: bash

 [moritz@stardust ghost]$ supervisorctl reread
 ghost: available
 [moritz@stardust ghost]$ supervisorctl update
 ghost: added process group
 [moritz@stardust ~]$ supervisorctl status
 ghost                            RUNNING   pid 26020, uptime 0:03:14
 [moritz@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your blog URL and create a user account.

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
