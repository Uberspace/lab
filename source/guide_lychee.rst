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

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.

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

 [isabell@stardust isabell]$ cd /var/www/virtual/$USER/Lychee
 [isabell@stardust Lychee]$ composer update
 Loading composer repositories with package information
 Info from https://repo.packagist.org: #StandWithUkraine
 Updating dependencies
 Lock file operations: 0 installs, 25 updates, 0 removals
  ...
 [isabell@stardust Lychee]$

After this, the required dependencies need to be installed:

::

  [isabell@stardust Lychee]$ composer install --no-dev
  Installing dependencies from lock file
  Verifying lock file contents can be installed on current platform.
  Package operations: 0 installs, 0 updates, 51 removals
  ...
  [isabell@stardust Lychee]$ npm install
  
  up to date, audited 292 packages in 1s
  
  44 packages are looking for funding
    run `npm fund` for details
  
  found 0 vulnerabilities
  
  [isabell@stardust Lychee]$ npm run build
  
  > build
  > vite build
  […]
  ✓ built in 7.01s
  [isabell@stardust Lychee]$



Set up the environment file:

::

 [isabell@stardust Lychee]$ cp .env.example .env
 [isabell@stardust Lychee]$


Now edit following lines of your ``/var/www/virtual/$USER/Lychee/.env`` with
the editor of your choice. Replace ``isabell`` with your username and fill
the ``DB_PASSWORD`` password with yours.

::

 DB_CONNECTION=mysql
 DB_HOST=localhost
 DB_PORT=3306
 DB_DATABASE=isabell
 DB_USERNAME=isabell
 DB_PASSWORD=<MySQL_PASSWORD>


.. hint ::

  The file contains a lot more lines with configuration options, but for a working basic setup they can
  all just stay there untouched. You may change it depending on your needs and knowledge.
  See https://lycheeorg.github.io/docs/configuration.html
  for more configuration possibilities.


Generate a application key:

::

  [isabell@stardust Lychee]$ php artisan key:generate
  [isabell@stardust Lychee]$


And prepare the database:

::

  [isabell@stardust Lychee]$ php artisan migrate
  [isabell@stardust Lychee]$


Finally, replace your ``html`` directory with a symbolic link for the ``public`` folder:

.. warning ::
  Please be aware that this tutorial is designed for a new fresh without any other projects or own content in the ``html`` directory.

::

 [isabell@stardust isabell]$ rm -r /var/www/virtual/$USER/html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/Lychee/public /var/www/virtual/$USER/html
 [isabell@stardust isabell]$

Now point your browser to your Lychee URL and create your admin user.


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

Tested with Lychee 4.5.1, Uberspace 7.12.2

.. author_list::
