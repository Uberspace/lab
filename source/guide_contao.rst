.. author:: xchs <https://github.com/xchs>
.. author:: luto <http://luto.at>
.. author:: brutus <brutus.dmc@googlemail.com>

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

We are using PHP_ in version ``8.1``:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your :manual_anchor:`website domain <web-domains.html#setup>` needs to be set up:

.. include:: includes/web-domain-list.rst

Create Database
===============

Contao saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_contao``) instead of the default database.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_contao"
 [isabell@stardust ~]$


Document Root Preparation
=========================

Since Contao uses the subdirectory ``public/`` as web root of your website you should **not** install Contao in your default Uberspace :manual:`DocumentRoot <web-documentroot>`. Instead, we install it next to that and then use a symlink to make it accessible to the web.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ mkdir -p contao/public
 [isabell@stardust isabell]$ ln -s contao/public html
 [isabell@stardust isabell]$


Installation
============

Download the `Contao Manager`_ to your web root:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://download.contao.org/contao-manager/stable/contao-manager.phar
 [isabell@stardust isabell]$ mv contao-manager.phar html/contao-manager.phar.php
 [isabell@stardust isabell]$


Configuration
=============

To complete the installation, you need to run the Contao Manager, which will guide you through the installation process.

Contao Manager
--------------

Point your web browser to your website URL and append ``contao-manager.phar.php`` (e.g. ``https://isabell.example/contao-manager.phar.php``) to start the Contao configuration.

1. **Manager Account** When you run the Contao install tool the first time, the web based installer will prompt you for a new username & password combination for access to the manager tool. For all future accesses, the Contao Manager will ask for this again.

2. **Contao Version** Choose the version you want to install.

3. **Database Configuration** To configure your database connection, you need to enter the MySQL database :manual_anchor:`credentials <database-mysql.html#login-credentials>`:

  - MySQL hostname (use ``localhost``)
  - MySQL username (equals your Uberspace username, e.g. ``isabell``)
  - MySQL password
  - Contao database name (e.g. ``isabell_contao``)

4. **Database Migration** Update the database (this will create the database table structure).

5. **Backend Account** Create a Contao backend administrator account.

You have successfully installed the Contao CMS on Uberspace 7!


Contao Backend
==============

Point your web browser to your website URL and append ``/contao`` (or ``/contao/login``) to open the Contao Backend login mask (e.g. ``https://isabell.example/contao/login``)

Log into the Contao Backend by entering the credentials of the Backend account.


Updates
=======

.. note:: Check the GitHub repository releases_ and the update feed_ regularly to stay informed about new updates and releases. Also read the news_ and announcements posted on `contao.org <https://contao.org/>`_.

To update an existing Contao installation (or switch to another PHP version), start the **Contao Manager** again (e.g. visit ``https://isabell.example/contao-manager.phar.php``).

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

Tested with Contao 5.0.6 (API-Version 2) / Uberspace 7.13.0

.. author_list::
