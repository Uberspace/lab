.. highlight:: console

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. tag:: lang-php
.. tag:: web


.. sidebar:: Logo

  .. image:: _static/images/laravel-logo.png
      :align: center

##########
Laravel
##########

.. tag_list::

Laravel is a web application framework with expressive, elegant syntax. We’ve already laid the foundation — freeing you to create without sweating the small things.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`



Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Your web domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Fresh Installation
======================

``cd`` to your user dir, then get Laravel installer via Composer. Finally create a new project using the installer.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust html]$ composer global require "laravel/installer"
 [isabell@stardust html]$ laravel new <projectname>
 Application ready! Build something amazing.
 [isabell@stardust ~]$
 
 Clone your project from github
======================

If you like to have your own project just clone it into your personal folder /var/www/virtual/$USER/
Normaly the vendor files should not be included we get them via composer

::

 [isabell@stardust ~]$ cd <projectname>
 [isabell@stardust <projectname>]$ composer install


Set a symbolic link
======================

The Laravel project is now in your user folder. But Uberspace serves only the /html folder. 
The accessible files from Laravel are contained in the project/public folder. Therefore we build a symbilic link.
You can wether built it for a domain already listed on your uberspace or your default domain $user.uber.space. 

First we rename the old html folder then we create the symbolic link. If you browse now $USER.uber.space you get redirected to /var/www/virtual/$USER/<PROJEKTNAME>/public where your index.php start the application up.

::

 [isabell@stardust ~]$ mv html/ htmlbackup/
 [isabell@stardust html]$ ln -s /var/www/virtual/$USER/<PROJEKTNAME>/public /var/www/virtual/$USER/html

Adjust the .htaccess file
======================

The most importend Part is the adjusting of the .htaccess file in your public folder. Laravel brings his file with it but for getting it on uberspace to run we need to add one additional line.
If you don't make the adjust you will end up with an 500 Internal Server Error. 

In your $user/<projectname>/public/.htaccess
Add: 
Options +SymLinksIfOwnerMatch
Above
RewriteEngine On

Config
======

Set Database up
======================

First figure out your SQL Credentials that uberspace has created for you. Just use

my_print_defaults client

to show them

This information we need to set in the .env file located in the project root folder.
Adjust the following lines:

APP_NAME=LARAVEL
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=<UBERSPACE USERNAME>
DB_USERNAME=<UBERSPACE USERNAME>
DB_PASSWORD=<SQL TOP SECRED CREDENTIAL>


Create an App Key
======================
We need to have an App Key in the .env file. If you created a new Laravel project with the installer you already have the key. If not create one with

::

[isabell@stardust ~]$ php artisan key:generate


Create Database tables
======================
The Database is still empty. We need to create the tables specified by migrations folder by using:

::

[isabell@stardust ~]$ php artisan migrate


Update
======
Just make a git pull request and use 
composer install - for checking new dependencies
php artisan migrate - creating new tables


Tested with Laravel 8 , Uberspace 7.2.1.0

.. author_list::
