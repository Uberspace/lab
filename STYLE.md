## Rules for guides

You're welcome to add your own guides to this repository.

Please follow our rules to keep the guides maintainable and consistent.

 * Guides have to be written in [reST](http://www.sphinx-doc.org/en/stable/rest.html).
 * Use English language. You don't have to be a native speaker or a poet.
 * Upload a logo to `_static/images/`, preferably SVG, a PNG file with transparent background is also fine.
 * Don't use URLs with actual versions. Change the version to something like 42.23.1 and tell where to find the actual version instead.
 * Always use the same username `isabell`.
 * Always use the same hostname `stardust`. For bash snippets, use `[isabell@stardust ~]`.
 * Always use full paths in commands. Don't assume the home directory or the html folder.
 * Don't mention additional document roots. *Keep it simple*. Don't use subfolders. Always use the standard document root `~/html`. Always assume the document root is empty.
 * If any applications need to bind to one or more ports (like Node.js apps), use port 9000 - 9010 in your examples, which are never free on our servers.
 * Use the templates in `source/includes/` where appropriate.
 * Document all steps for setup. E.g. [create a database](https://github.com/Uberspace/lab/issues/39) when that's necessary. [Create directories](https://github.com/Uberspace/lab/issues/36) when needed.
 * When there is a license needed for the software mention it.
 * If there are interactive shell sessions, emphasize the lines that expect input from the user. For example:

```
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
```

 * Always end your console code blocks with `[isabell@stardust ~]$`.
 * If you use flags, explain them. Don't use short flags, always use the long versions. We want everybody to be able to know what they're doing. Example:

```
Since the installer expects to be run with root privileges, we need to adjust some settings_:

  * ``--no-stack``: Disables the system stack check during setup. Since we're a shared hosting provider, the stack is maintained by us.
  * ``-no-setup-linux-user``: Skips creating a linux user. You can't do that without root privileges.
  * ``--no-setup-systemd``: Skips creation of a systemd unit file. We'll use supervisord_ later instead.
  * ``--no-setup-nginx``: Skips webserver configuration. We'll use a htaccess_ file for apache_ later instead.
  * ``--no-setup-mysql``: Skips setup of MySQL_. You can't do that without root privileges.
```

 * Try to find an RSS feed for updates and document it.
 * If there are any standard passwords, tell the user to change them *immediately*.
 * If there are files to edit, don't do stuff like `cat > ~/.npmrc <<__EOF__`, just tell the user to _edit_ the file. Don't mention an editor like `vi` or `nano`. Example:

```
Create ``~/etc/services.d/ghost.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

 [program:ghost]
 directory=%(ENV_HOME)s/ghost
 command=env NODE_ENV=production /bin/node current/index.js

In our example this would be:

.. code-block:: ini

 [program:ghost]
 directory=%(ENV_HOME)s/ghost
 command=env NODE_ENV=production /bin/node current/index.js
```

Please use the following structure. Only document applicable steps, leave out headlines you don't need.

 * Short description
 * Prerequisites
 * Installation
 * Configuration
 * Finishing installation
 * Best practices
 * Tuning
 * Updates

## Boilerplate

```
.. highlight:: console

.. author:: YourName <YourURL/YourMail>

.. sidebar:: About

  .. image:: _static/images/loremipsum.png
      :align: center

##########
Loremipsum
##########

Loremipsum_ dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Node.js_ and its package manager npm_
  * MySQL_
  * supervisord_
  * domains_

License
=======

All relevant legal information can be found here 

  * http://www.loremipsum.com/legal/privacy

Prerequisites
=============

We're using Node.js_ in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

You'll need your MySQL credentials_. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your blog URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

Step 2
------

Configuration
=============

Configure port
--------------

Setup .htaccess
---------------

Setup daemon
------------

Finishing installation
======================

Point your browser to URL and create a user account.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!

Tuning
======

Disable all plugins you don't need. Configure caching.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _Loremipsum: https://en.wikipedia.org/wiki/Lorem_ipsum
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/lorem/ipsum/releases.atom

----

Tested with Loremipsum 1.22.1, Uberspace 7.1.1

.. authors::

```

When you're happy with your guide create a [pull request](https://github.com/Uberspace/lab/compare). We'll look at it and we'll give you feedback until we're happy too.
