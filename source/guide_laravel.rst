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

 * https://laravel.com/docs/13.x/license

Prerequisites
=============

We're using :manual:`PHP <lang-php>` version 8.5:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.5'
 [isabell@stardust ~]$

Your web domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============


``cd`` to your user dir, then install the Laravel installer via Composer. Finally, create a new project using the installer and choose your `starter kit <https://laravel.com/docs/13.x/starter-kits>`.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer global require "laravel/installer"
 [isabell@stardust isabell]$ laravel new my_project
 

Use the arrow keys to select your desired starter kit. In this example, we'll proceed without a starter kit. Confirm with Enter.

::

 ┌ Which starter kit would you like to install? ────────────────┐
 │ None                                                         │
 └──────────────────────────────────────────────────────────────┘


Next, choose your testing framework. We'll use Pest and confirm with Enter.

::

 ┌ Which testing framework do you prefer? ──────────────────────┐
 │ Pest                                                         │
 └──────────────────────────────────────────────────────────────┘


Now you'll be asked about Laravel Boost, which we don't need for this guide. Select "No" and confirm with Enter.

::

 ┌ Do you want to install Laravel Boost to improve AI assisted coding? ┐
 │ No                                                                  │
 └─────────────────────────────────────────────────────────────────────┘


Next, select your database. We're using MySQL, so select that option. Since we haven't configured the MySQL credentials yet, select "No" when asked to run the default database migrations.

::

 ┌ Which database will your application use? ───────────────────┐
 │ MySQL                                                        │
 └──────────────────────────────────────────────────────────────┘

 ┌ Default database updated. Would you like to run the default database migrations? ┐
 │ No                                                                               │
 └──────────────────────────────────────────────────────────────────────────────────┘


The installer will now create all files for you. Finally, you'll be asked whether to run ``npm install --ignore-scripts`` and ``npm run build``. Select "No" and confirm. We'll run these commands later after configuring the database.

::

  Application ready in [my_project]. You can start your local development using:

 ➜ cd my_project
 ➜ npm install --ignore-scripts && npm run build
 ➜ composer run dev

 New to Laravel? Check out our documentation. Build something amazing!
 [isabell@stardust isabell]$
 

Change the DocumentRoot
=======================

After the installation has finished, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``my_project/public`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/my_project/public html
 [isabell@stardust isabell]$


Configuration
=============

Set up the database
###################

First figure out your SQL Credentials that uberspace has created for you.

.. include:: includes/my-print-defaults.rst

You'll need to add this information to the ``.env`` file located in the project root directory.

Update the following lines:

::

 APP_NAME=LARAVEL
 
 DB_CONNECTION=mysql
 DB_HOST=127.0.0.1
 DB_PORT=3306
 DB_DATABASE=isabell
 DB_USERNAME=isabell
 DB_PASSWORD=MySuperSecretPassword


Create database tables and build assets
########################################

The database is still empty. Create the tables defined in the migrations and build the frontend assets:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/my_project
 [isabell@stardust my_project]$ php artisan migrate
 [isabell@stardust my_project]$ npm install --ignore-scripts && npm run build



When you open your domain, you should now see the Laravel welcome page and are ready to start development.

----

Tested with Laravel 13, Uberspace 7.17.3, and PHP 8.5

.. author_list::
