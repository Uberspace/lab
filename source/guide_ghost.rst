.. author:: nichtmax <https://moritz.in>
.. author:: Nico Graf <hallo@uberspace.de>
.. author:: Peleke <https://www.peleke.de>
.. author:: Noah <https://noahwagner.de>
.. author:: tobimori <tobias@moeritz.cc>
.. author:: Patrick Brunck <https://www.patrick-brunck.de/>

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

We're using :manual:`Node.js <lang-nodejs>` in the stable version 16:

::

 [isabell@stardust ~]$ uberspace tools version use node 16
 Using 'Node.js' version: '16'
 Selected node version 16
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [eliza@dolittle ~]$

.. include:: includes/my-print-defaults.rst

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install ghost-cli, knex-migrator and yarn
-----------------------------------------

Use ``npm`` to install ``ghost-cli`` and ``knex-migrator`` globally.
In order to avoid issues and bugs with Ghost_, we need to also install the package manager ``yarn`` to use for further updates.

::

 [isabell@stardust ~]$ npm i -g ghost-cli knex-migrator yarn
 [...]
 + ghost-cli@1.9.1
 + knex-migrator@3.2.3
 + yarn@1.22.4
 added 690 packages in 31.543s
 [isabell@stardust ~]$

Install Ghost
-------------

Create a ``ghost`` directory in your home, ``cd`` to it and then run the installer. Since the installer expects to be run with root privileges, we need to adjust some settings_:

  * ``--no-stack``: Disables the system stack check during setup. Since we're a shared hosting provider, the stack is maintained by us.
  * ``--no-setup-linux-user``: Skips creating a linux user. You can't do that without root privileges.
  * ``--no-setup-systemd``, ``--no-start``, ``--no-enable``: Skips creation of a systemd unit file. We'll use :manual:`supervisord <daemons-supervisord>` later instead.
  * ``--no-setup-nginx``: Skips webserver configuration. We'll use a :manual_anchor:`web backend <web-backends>` later instead.
  * ``--no-setup-mysql``: Skips setup of :manual:`MySQL <database-mysql>`. You can't do that without root privileges.

You will need to enter the following information:

  * `y` or `yes` to just continue after the reputed MySQL error (everything is fine here, ghost does just look at the wrong places)
  * your blog URL: The URL for your blog. Since we don't allow HTTP, use HTTPS. For example: https://isabell.uber.space
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Ghost database name: we suggest you use a :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_ghost

.. code-block:: console
 :emphasize-lines: 1,2,3,14,16,17,18

 [isabell@stardust ~]$ mkdir ~/ghost
 [isabell@stardust ~]$ cd ~/ghost
 [isabell@stardust ghost]$ ghost install --no-stack --no-setup-linux-user --no-setup-systemd --no-setup-nginx --no-setup-mysql --no-start --no-enable
 ✔ Checking system Node.js version
 ✔ Checking logged in user
 ✔ Checking current folder permissions
 ℹ Checking system compatibility [skipped]
 Local MySQL install was not found or is stopped. You can ignore this if you are using a remote MySQL host.
 Alternatively you could:
 a) install/start MySQL locally
 b) run `ghost install --db=sqlite3` to use sqlite
 c) run `ghost install local` to get a development install using sqlite3.
 ? Continue anyway? Yes
 MySQL check skipped
 ℹ Checking for a MySQL installation [skipped]
 ✔ Checking memory availability
 ✔ Checking memory availability
 ✔ Checking for latest Ghost version
 ✔ Setting up install directory
 ✔ Downloading and installing Ghost v3.2.0
 ✔ Finishing install process
 ? Enter your blog URL: https://isabell.uber.space
 ? Enter your MySQL hostname: localhost
 ? Enter your MySQL username: isabell
 ? Enter your MySQL password: [hidden]
 ? Enter your Ghost database name: isabell_ghost
 ✔ Configuring Ghost
 ✔ Setting up instance
 ℹ Setting up SSL [skipped]

 Ghost uses direct mail by default. To set up an alternative email method read our docs at https://ghost.org/docs/concepts/config/#mail

 ------------------------------------------------------------------------------

 Ghost was installed successfully! To complete setup of your publication, visit:

 https://isabell.uber.space/ghost/


Configuration
=============

Change network interface
------------------------

You need to change the network interface from ``127.0.0.1`` to
``0.0.0.0`` and the process manager to ``local``:

.. code-block:: none

 [isabell@stardust ghost] ghost config --port 2368 --ip 0.0.0.0  --process local
 [isabell@stardust ghost]


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
 startsecs=60

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your blog URL and Ghost Admin page (https://isabell.uber.space/ghost/) to create a user account.

Replace uber.space domain with your own domain
==============================================

.. note::

    You should already have set up your additional external URL as described in :manual:`domains <web-domains>`.

Update URL with ghost-cli as followed. Change the URL to your external URL in the highlighted line.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/ghost/
 [isabell@stardust ghost]$ ghost config --url https://example.com
 [isabell@stardust ghost]$

Restart Ghost (also check the restarted process with second command):

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl restart ghost
 ghost: stopped
 ghost: started
 [isabell@stardust ~]$ supervisorctl status
 ghost                            RUNNING   pid 26020, uptime 0:00:56
 [isabell@stardust ~]$

Now the URLs in your Ghost installation always use your newly configured URL. This is especially seen in the RSS feeds which if this part is not run will always use the uber.space URL even though you access your blog via an external domain already. This is due to Ghost using the configured URL as a variable in some templates etc. which is the case for the RSS URLs for example in the main Casper theme.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

You can use ``ghost-cli``'s built-in update mechanism. Make sure that the process manager is set to local, then stop ghost, run ``ghost update`` and restart ghost. Sometimes ``ghost update`` will overwrite the port and network interface, so make sure to set that them to 2368 and 0.0.0.0 again.

.. code-block:: none

 [isabell@stardust ~] supervisorctl stop ghost
 [isabell@stardust ~] cd ~/ghost
 [isabell@stardust ghost] ghost config --process local
 [isabell@stardust ghost] ghost update
 ✔ Checking system Node.js version - found v16.14.2
 […]
 ✔ Fetched release notes
 ✔ Downloading and updating Ghost to v4.45.0
 ✔ Linking latest Ghost and recording versions
 ℹ Removing old Ghost versions [skipped]
 [isabell@stardust ghost] ghost config --port 2368 --ip 0.0.0.0
 [isabell@stardust ghost] supervisorctl start ghost


.. _Ghost: https://ghost.org
.. _settings: https://docs.ghost.org/api/ghost-cli/
.. _feed: https://github.com/TryGhost/Ghost/releases.atom

----

Tested with Ghost v4.45.0, Uberspace 7.12.1

.. author_list::
