.. highlight:: console

.. author:: Felix Wienss <https://github.com/FelixWienss>

.. tag:: lang-php
.. tag:: web


.. sidebar:: Logo

  .. image:: _static/images/laravel-logo.png

          :align: center

#######
Laravel
#######


.. tag_list::

Laravel is a web application framework with expressive, elegant syntax. We’ve already laid the foundation — freeing you to create without sweating the small things.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`DocumentRoot <web-documentroot>`

License
=======

All relevant legal information can be found here

 * https://laravel.com/docs/12.x/license

Prerequisites
=============

We're using :manual:`PHP <lang-php>` version 8.3:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.3'
 [isabell@stardust ~]$

Your web domain needs to be setup:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Installation
============


``cd`` to your user dir, then get Laravel installer via Composer. Finally create a new project using the installer and chose your `starter kit <https://laravel.com/docs/12.x/starter-kits>`.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust html]$ composer global require "laravel/installer"
 [isabell@stardust html]$ laravel new my_project
 Application ready! Build something amazing.
 [isabell@stardust ~]$
 

Change the DocumentRoot
=======================

After the installation has finished, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``my_project/public`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/my_project/public html
 [isabell@stardust isabell]$


Config
======

Set Database up
###############

First figure out your SQL Credentials that uberspace has created for you.

.. include:: includes/my-print-defaults.rst

This information we need to set in the .env file located in the project root folder.

Adjust the following lines:

.. code-block:: console
 APP_NAME=LARAVEL
 DB_CONNECTION=mysql
 DB_HOST=127.0.0.1
 DB_PORT=3306
 DB_DATABASE=<UBERSPACE USERNAME>
 DB_USERNAME=<UBERSPACE USERNAME>
 DB_PASSWORD=<SQL TOP SECRED CREDENTIAL>


Create Database tables
######################

The Database is still empty. We need to create the tables specified by migrations folder by using:

::

[isabell@stardust ~]$ php artisan migrate



Tested with Laravel 12 , Uberspace 7.16.7, and PHP 8.3

.. author_list::