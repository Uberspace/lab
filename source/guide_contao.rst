.. author:: xchs <https://github.com/xchs>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/contao.svg
      :align: center

######
Contao
######

.. tag_list::

Contao_ is a free, web-based Open Source Content Management System (CMS) written in PHP and distributed under the LGPL 3.0 or later licence.

Contao is used to build and manage professional websites of different types and size ranges that are easy to maintain.

As of Contao 4, it is based on Symfony_, a popular high performance PHP framework for web development. Contao 4 has been designed as a Symfony bundle, which can be used to add CMS functionality to any Symfony application.

Contao (formerly TYPOlight) was released for the first time in 2006 by Leo Feyer. Since then it has been continuously developed and it is actively maintained by the Contao Core Development Workgroup and other contributors.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`


Prerequisites
=============

We are using PHP_ in the stable version ``8.0``:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.0
 Selected PHP version 8.0
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.0'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your :manual_anchor:`website domain <web-domains.html#setup>` needs to be set up:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.example
 isabell.uber.space
 [isabell@stardust ~]$


Installation
============

Since Contao uses the subdirectory ``web/`` as web root of your website you should **not** install Contao in your default Uberspace :manual:`DocumentRoot <web-documentroot>`. Instead, we install it next to that and then use a symlink to make it accessible to the web.

``cd`` to one level above your :manual:`DocumentRoot <web-documentroot>`, then use either Contao Manager or the PHP Dependency Manager Composer_ to create a new project based on the **Contao Managed Edition**.

Contao Manager
--------------

Create a folder for Contao Manager, download it and make it accessible:

.. code-block:: console
 :emphasize-lines: 1,8

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ mkdir -p <target>/web
 [isabell@stardust web]$ cd <target>/web
 [isabell@stardust web]$ wget https://download.contao.org/contao-manager/stable/contao-manager.phar
 [isabell@stardust web]$ mv contao-manager.phar contao-manager.phar.php
 [isabell@stardust web]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/<target>/web/ html
 [isabell@stardust isabell]$

Point your web browser to your website URL and append ``contao-manager.phar.php`` (e.g. ``https://isabell.example/contao-manager.phar.php``) to run the Contao Manager.

Follow the steps to install Contao. Make sure to use the Cloud Resolver as it will resolve the dependencies in the cloud, rather on the local Uberspace host.

When the setup is done, continue with the `Configuration`_. section in this guide.

Composer
--------

.. warning:: Your ``php`` command line processes might not be able to allocate enough memory to complete the expensive ``composer`` call.

.. note:: The given Composer_ command always installs the latest stable release. If you want to install a particular version, you must specify the version in the command as well, e.g.: ``composer create-project contao/managed-edition <target> '42.23.*'``

  Composer_ will install all necessary dependencies Contao needs to run. This can take some time though.

.. warning:: You have to replace the ``<target>`` parameter with a path to a folder where the Contao project files should be created. If the target folder does not exist yet, it will be created automatically.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project contao/managed-edition <target>
 Installing contao/managed-edition (42.23.1)
   - Installing contao/managed-edition (42.23.1): Downloading (100%)
 Created project in <target>
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 [...]

 [isabell@stardust isabell]$

Next, remove the unused :manual:`DocumentRoot <web-documentroot>` and create a new **symbolic link** to the Contao ``web/`` subdirectory:

.. warning:: Please make sure your :manual:`DocumentRoot <web-documentroot>` is empty before removing it!

  Again, replace ``<target>`` by the folder name where the Contao project files sit in.

.. code-block:: console
 :emphasize-lines: 1,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/<target>/web/ html
 [isabell@stardust isabell]$


Configuration
=============

.. _create-database:

Create Database
---------------

Contao saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_contao``) instead of the default database.

.. note:: You need to create the database **before** you enter the database :manual_anchor:`credentials <database-mysql.html#login-credentials>` in the `Contao install tool`_.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_contao"
 [isabell@stardust ~]$

Contao Install Tool
-------------------

To complete the installation, you need to run the Contao install tool, which will guide you through the installation process.

Point your web browser to your website URL and append ``/contao/install`` (e.g. ``https://isabell.example/contao/install``) to run the Contao install tool.

.. note:: The URL fragment ``/contao/install`` is only a Contao *route* and not a physical path within your installation.

**Step 1:** When you run the Contao install tool the first time, the web based installer will prompt to set a new password. For all future accesses, the Contao install tool will ask for this password again.

**Step 2:** To configure your database connection, you need to enter the MySQL database :manual_anchor:`credentials <database-mysql.html#login-credentials>`:

  * MySQL hostname (use ``localhost``)
  * MySQL username (equals your Uberspace username, e.g. ``isabell``)
  * MySQL password
  * Contao database name (e.g. ``isabell_contao``)

.. warning:: You have to create the database yourself (see :ref:`create-database`). The Contao install tool does not automatically create the database for you.

**Step 3:** Update the database (this will create the database table structure).

**Step 4:** Create a Contao back end administrator account.

You have successfully installed the Contao CMS on Uberspace 7!


Contao Back End
===============

Point your web browser to your website URL and append ``/contao`` (or ``/contao/login``) to open the Contao back end login mask (e.g. ``https://isabell.example/contao/login``)

.. note:: The URL fragment ``/contao/login`` is only a Contao *route* and not a physical path within your installation.

Log into the Contao back end by entering the credentials of the administrator account.


Updates
=======

.. note:: Check the GitHub repository releases_ and the update feed_ regularly to stay informed about new updates and releases. Also read the news_ and announcements posted on `contao.org <https://contao.org/>`_.

To update an existing Contao installation just perform a Composer Update in the root directory of your application (e.g. ``/var/www/virtual/$USER/<target>/``). This will update the Contao Managed Edition core application and all its dependencies as well as all your installed third-party packages:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/<target>/
 [isabell@stardust <target>]$ composer update
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 [...]

 [isabell@stardust <target>]$

Alternatively, the update can also be performed via the `Contao Manager`_ which can be downloaded from the official Contao download_ page.

.. warning:: The Contao Managed Edition and especially **additional bundles and modules** are **not** updated automatically, so make sure to regularly check for security and maintenance updates.


.. _Contao: https://contao.org/
.. _Symfony: https://symfony.com/
.. _PHP: http://www.php.net/
.. _Composer: https://getcomposer.org/
.. _feed: https://github.com/contao/contao/releases.atom
.. _releases: https://github.com/contao/contao/releases
.. _news: https://contao.org/news.html
.. _Contao Manager: https://docs.contao.org/manual/en/installation/contao-manager/
.. _download: https://contao.org/download.html

----

Tested with Contao 4.11.0 / Uberspace 7.9.0.0

.. author_list::
