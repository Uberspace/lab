.. highlight:: console
.. author:: Kevin Jost <https://github.com/systemsemaphore>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/benotes.png
      :align: center

#######
Benotes
#######

.. tag_list::

Benotes_ allows you to save bookmarks and notes side by side. It supports multiple users, (nested) collections, tagging, sharing, markdown and import / export of bookmarks.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Use the recommended :manual:`PHP <lang-php>` version. Refer to the `manual installation guide`_ for help.

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Your domain should be set up:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Set up a database
-----------------

Create the database ``<username>_benotes`` in MySQL:

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_benotes"
 [isabell@stardust ~]$

Download
=========

Benotes
-------

.. note:: Benotes uses the subdirectory ``public`` as web root. You should not install Benotes in your :manual:`DocumentRoot <web-documentroot>`. Instead, we will create a directory next to that and use a symlink to make it accessible.

Clone the source using Git:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone https://github.com/fr0tt/benotes
 Cloning into 'benotes'...
 [...]
 [isabell@stardust isabell]$

Dependencies
------------

``cd`` into your Benotes directory and install the necessary dependencies using Composer:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust isabell]$ cd /var/www/virtual/$USER/benotes
 [isabell@stardust benotes]$ composer install
 Installing dependencies from lock file (including require-dev)
 Package operations: 126 installs, 0 updates, 0 removals
 [...]
 Package manifest generated successfully.
 86 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!
 [isabell@stardust benotes]$

Remove your empty DocumentRoot and create a symlink to the ``benotes/public`` directory:

.. code-block:: console
 :emphasize-lines: 2-3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/benotes/public html
 [isabell@stardust isabell]$

Configuration
=============

Create the .env file
--------------------

Create a copy of the .env.example file and name it .env

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/benotes
 [isabell@stardust benotes]$ cp .env.example .env
 [isabell@stardust ~]$

Open the file ``.env`` in your favourite editor and change the default settings in the following lines to use your settings:

.. code-block:: none
 :emphasize-lines: 1-2, 4, 13, 15-17, 20, 22-23, 25-26

 APP_NAME=Benotes
 APP_ENV=production
 APP_DEBUG=false
 APP_URL=http://isabell.uber.space

 APP_KEY=
 JWT_SECRET=
 GENERATE_MISSING_THUMBNAILS=false
 USE_FILESYSTEM=true
 RUN_BACKUP=false

 DB_CONNECTION=mysql
 DB_HOST=localhost
 DB_PORT=3306
 DB_DATABASE=isabell_benotes
 DB_USERNAME=isabell
 DB_PASSWORD=MySuperSecretPassword

 MAIL_DRIVER=smtp
 MAIL_HOST=stardust.uberspace.de
 MAIL_PORT=587
 MAIL_USERNAME=isabell@uber.space
 MAIL_PASSWORD=MySuperSecretPassword
 MAIL_ENCRYPTION=tls
 MAIL_FROM_ADDRESS=isabell@uber.space
 MAIL_FROM_NAME=Benotes

 JWT_ALGO=HS256

Installation
============

Populating database
-----------------

After saving the ``.env`` file, you need to create the database tables. When prompted, answer with "yes". Lastly, provide a username, an email address and a strong password.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust benotes]$ php artisan install

 Initiate installation...

 0/4 [                            ]   0%

 **************************************
 *     Application In Production!     *
 **************************************

 Do you really wish to run this command? (yes/no) [no]:
 > yes

 [...]

 Installation complete.

 [isabell@stardust benotes]$

Storage Symlink
---------------

Create a symlink for storage as stated in  the `manual installation guide`_:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/benotes
 [isabell@stardust benotes]$ ln -sfn ../storage/app/public/ public/storage
 [isabell@stardust benotes]$

Updates
=======

.. warning:: In case of future changes to the ``.env`` file, you must run ``php artisan config:cache`` in the ``benotes`` directory for these changes to take effect.

.. note:: Check the Changelog_ regularly to stay informed about the newest version.

If an update is available, follow these four steps to upgrade the files, the dependencies, the database schemas and to clear the cache:

.. code-block:: console
 :emphasize-lines: 2-5

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/benotes
 [isabell@stardust benotes]$ git pull
 [isabell@stardust benotes]$ composer install
 [isabell@stardust benotes]$ php artisan migrate
 [isabell@stardust benotes]$ php artisan cache:clear
 [isabell@stardust benotes]$

----

Tested with Benotes 2.8.1, Uberspace 7.15.15, and PHP 8.1

.. _Benotes: https://benotes.org/
.. _`manual installation guide`: https://benotes.org/docs/installation/classic
.. _Changelog: https://benotes.org/docs/resources/changelog


.. author_list::
