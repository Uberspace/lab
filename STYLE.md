## Rules for guides

You're welcome to add your own guides to this repository.

Please follow our rules to keep the guides maintainable and consistent.

 * Guides have to be written in [reST](http://www.sphinx-doc.org/en/stable/rest.html).
 * Use English language. You don't have to be a native speaker or a poet.
 * Upload a logo to `_static/images/`, preferably SVG, a PNG file with transparent background is also fine.
 * If possible use a download URL that points to the latest version (e.g. `latest.zip` on some platforms). If such an URL is not available, use the newest version instead.
 * Always use the same username `isabell`.
 * Always use the same hostname `stardust`. For bash snippets, use `[isabell@stardust ~]$`.
 * Always use full paths in commands. Don't assume the home directory or the html folder.
 * Don't mention additional document roots. *Keep it simple*. Don't use subfolders. Always use the standard document root `~/html`. Always assume the document root is empty.
 * Use the templates in `source/includes/` where appropriate.  
 For example `.. include:: includes/web-domain-list.rst` generates the following snippet:
 ```
 ::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$
 ```
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

 * If you want to include links to https://manual.uberspace.de, please use the corresponding directives `manual` and `manual_anchor`. Use the `lab` and `lab_anchor` directives for linking other UberLab guides. Examples:

```
This is a link to the Python manual: :manual:`Python <lang-python>`.

This is a link to a section of the Python manual: :manual_anchor:`pip <lang-python.html#pip>`.

This is a link to another guide: :lab:`Django <guide_django>`.
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

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/loremipsum.png
      :align: center

##########
Loremipsum
##########

.. tag_list::

Loremipsum_ dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * http://www.loremipsum.com/legal/privacy

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Step 1
------

Step 2
------

Configuration
=============

Configure Webserver
-------------------

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
.. _feed: https://github.com/lorem/ipsum/releases.atom

----

Tested with Loremipsum 1.22.1, Uberspace 7.1.1

.. author_list::

```

## Add your changes to the Uberspace Lab

Please choose a [good commit message](https://chris.beams.io/posts/git-commit/) for all your changes. Start each commit message with `[toolname]` and a space, like `[wordpress] add update info`. If you create a new guide, your first commit message should be phrased as: `[wordpress] add guide for wordpress`. 

If you already commited your changes without following this styleguide, you are still able to [change the message](https://help.github.com/en/articles/changing-a-commit-message) afterwards.

When you're happy with your guide create a [pull request](https://github.com/Uberspace/lab/compare). We'll look at it and we'll give you feedback until we're happy too.
