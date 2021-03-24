.. author:: TheForcer <https://github.com/TheForcer>

.. tag:: lang-php
.. tag:: web
.. tag:: photo-management

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/lychee.png
      :align: center

#########
Lychee
#########

.. tag_list::

Lychee_ is a open source photo-management software written in PHP and distributed under the MIT license. It allows you to easily upload, sort and manage your photos, all while presenting those with a beautiful web interface.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual_anchor:`composer <lang-php.html#package-manager>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Also, the domain you want to use for Lychee must be set up as well:

.. include:: includes/web-domain-list.rst

Installation
============

Since version 4.0, Lychee requires the web server to actually point to the ``public`` subfolder instead of the main Lychee folder. Therefore, we are going to put the Lychee base folder into the parent folder of the default DocumentRoot, i.e. ``/var/www/virtual/$USER``.

Clone the Lychee code from GitHub_:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ git clone https://github.com/LycheeOrg/Lychee Lychee
 Cloning into '/var/www/virtual/isabell/Lychee'...
 remote: Enumerating objects: 5, done.
 remote: Counting objects: 100% (5/5), done.
 remote: Compressing objects: 100% (5/5), done.
 remote: Total 6469 (delta 0), reused 0 (delta 0), pack-reused 6464
 Receiving objects: 100% (6469/6469), 28.55 MiB | 13.36 MiB/s, done.
 Resolving deltas: 100% (4511/4511), done.
 [isabell@stardust isabell]$

Next update the Composer repository:

::

 [isabell@stardust isabell]$ Lychee/composer.phar update
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 Package operations: 134 installs, 7 updates, 0 removals
 ...
 [isabell@stardust isabell]$

After this, the required dependencies need to be installed:

::

 [isabell@stardust isabell]$ Lychee/composer.phar install --no-dev
 Loading composer repositories with package information
 Installing dependencies from lock file
 Package operations: 0 installs, 0 updates, 52 removals
 ...
 [isabell@stardust isabell]$

Finally, setup a symbolic link for the ``public`` folder within the ``html`` folder or in the current folder if you use a custom subdomain:

::

 [isabell@stardust isabell]$ ln -s Lychee/public html/Lychee

Now point your browser to your Lychee URL and follow the instructions.

You will need to enter the following information:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Lychee database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_lychee. Enter that, you can leave the prefix field empty.

For the last step you have to enter the username/password you want to use for the Lychee user.

Updates
=======

You can regularly check their GitHub's Atom Feed_ for any new Lychee releases.

If a new version is available, ``cd`` to your Lychee folder and do a simple ``git pull origin master``:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/Lychee
 [isabell@stardust Lychee]$ git pull origin master
 Already up to date.
 [isabell@stardust Lychee]$

Or you use the automatic update function available in the web interface.

.. _Lychee: https://lycheeorg.github.io/
.. _GitHub: https://github.com/LycheeOrg/Lychee/releases
.. _Feed: https://github.com/LycheeOrg/Lychee/releases.atom

----

Tested with Lychee 4.0.9, Uberspace 7.7.2.0

.. author_list::
