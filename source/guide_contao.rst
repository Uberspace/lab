.. author:: xchs <https://github.com/xchs>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/contao.svg
      :align: center

######
Contao
######

Contao_ is a free, web-based Open Source Content Management System (CMS) written in PHP and distributed under the LGPL 3.0 or later licence.

Contao is used to build and manage professional websites of different types and size ranges that are easy to maintain.

As of Contao 4, it is based on Symfony_, a popular high performance PHP framework for web development. Contao 4 has been designed as a Symfony bundle, which can be used to add CMS functionality to any Symfony application.

Contao (formerly TYPOlight) was released for the first time in 2006 by Leo Feyer. Since then it has been continuously developed and it is actively maintained by the Contao Core Development Workgroup and other contributors.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * MySQL_
  * domains_


Prerequisites
=============

We are using PHP_ in the stable version ``7.1``:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your `website domain`_ needs to be set up:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.example
 isabell.uber.space
 [isabell@stardust ~]$


Installation
============

Since Contao uses the subdirectory ``web/`` as web root of your website you should **not** install Contao in your `document root`_. Instead we install it next to that and then use a symlink to make it accessible.

``cd`` to one level above your `document root`_, then use the PHP Dependency Manager Composer_ to create a new project based on the **Contao Managed Edition**:

.. note:: The given Composer_ command always installs the latest stable release. If you want to install a particular version, you must specify the version in the command as well: ``composer create-project contao/managed-edition <target> '42.23.*'``
  
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

Next, remove the unused `document root`_ and create a new **symbolic link** to the Contao ``web/`` subdirectory:

.. warning:: Please make sure your `document root`_ is empty before removing it!

  Replace again ``<target>`` by the folder name where the Contao project files sit in.

.. code-block:: console
 :emphasize-lines: 1,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -rf html/
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/<target>/web/ html
 [isabell@stardust isabell]$


Configuration
=============

Point your web browser to your website URL and append ``/contao/install`` (e.g. ``https://isabell.example/contao/install``) to run the Contao install tool.

.. note:: The URL fragment ``/contao/install`` is only a *route*, not a physical path.

.. warning:: You have to create the database yourself. The Contao install tool does not automatically create the database for you.

Step 1: When you run the Contao install tool the first time, the web based installer will prompt to set a new password. For all future accesses, the install tool will ask for this password.

Step 2: To configure your database connection, you need to enter the MySQL and database credentials_:

  * MySQL hostname (use ``localhost``)
  * MySQL username (equals your Uberspace username, e.g. ``isabell``)
  * MySQL password
  * Contao database name (it is recommended to use an additional_ database instead of the default database, e.g. ``isabell_contao``)

Step 3: Update the database (this will create the database and table structure).

Step 4: Create an Contao back end administrator account.

Step 5: You have successfully installed the Contao CMS on Uberspace 7!


Finishing installation
======================

Point your web browser to your website URL and append ``/contao`` (or ``/contao/login``) to open the Contao back end login mask (e.g. ``https://isabell.example/contao/login``)

.. note:: The URL fragment ``/contao/login`` is only a *route*, not a physical path.

Log into the Contao back end by entering the credentials of the administrator account.


Updates
=======

.. note:: Check the GitHub repository update feed_ regularly to stay informed about new releases.

Check the Contao Managed Edition repository releases_ for the latest versions. Also read the news_ and announcements posted on `contao.org <https://contao.org/>`_.

By using Composer_, you can update an existing Contao installation and all its dependencies without having to create a new project.

All further information can be found on the official download_ page.

.. warning:: The Contao Managed Edition and especially **additional bundles and modules** are **not** updated automatically, so make sure to regularly check for security and maintenance updates.


.. _Contao: https://contao.org/
.. _Symfony: https://symfony.com/
.. _PHP: http://www.php.net/
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _website domain: https://manual.uberspace.de/en/web-domains.html#setup
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _Composer: https://getcomposer.org/
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _feed: https://github.com/contao/managed-edition/releases.atom
.. _releases: https://github.com/contao/managed-edition/releases
.. _news: https://contao.org/news.html
.. _download: https://contao.org/download.html

----

Tested with Contao 4.5.8, Uberspace 7.1.6.0

.. authors::
