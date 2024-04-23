.. highlight:: console

.. author:: Kevin Jost <https://github.com/systemsemaphore>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/linkace.png
      :align: center

#######
LinkAce
#######

.. tag_list::

`LinkAce`_ is a self-hosted archive to collect links of your favorite websites. LinkAce comes with a lot of features while keeping a clean and minimal interface.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 8.2:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ uberspace tools version use php 8.2
 Selected PHP version 8.2
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to the directory one level above your :manual:`DocumentRoot <web-documentroot>`, then download LinkAce. You can find the latest version on the `release page`_, replace the version below with the version number.

.. code-block:: console
 :emphasize-lines: 1,2,3,6,7

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/Kovah/LinkAce/releases/download/v1.13.0/linkace-v1.13.0.zip
 [isabell@stardust isabell]$ unzip -d linkace/ linkace-v1.13.0.zip
 Archive:  linkace-v1.13.0.zip
 [...]
 [isabell@stardust isabell]$ rm linkace-v1.13.0.zip
 [isabell@stardust isabell]$

After the installation has finished, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``linkace/public`` directory.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/linkace/public html
 [isabell@stardust isabell]$

Configuration
=============

Set up a database
-----------------

Run the following code to create the database ``<username>_linkace`` in MySQL:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_linkace COLLATE utf8mb4_bin;"
 [isabell@stardust ~]$

.. note:: Other collations like utf8mb4_general_ci may cause issues with different Unicode characters.

Create the .env file
--------------------

Create a copy of the .env.example file and name it .env

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/linkace
 [isabell@stardust linkace]$ cp .env.example .env
 [isabell@stardust ~]$

Generate a secret key
---------------------

Run the following command to generate a secret key for your application and prepare LinkAce for the setup:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/linkace
 [isabell@stardust linkace]$ php artisan key:generate
 [isabell@stardust ~]$

Finishing installation
======================

Point your browser to ``https://isabell.uber.space/`` The built-in setup should start. Follow the instructions, enter your database credentials and register your user account.

Updates
=======

Check LinkAce's `release page`_ for the latest version. If a newer version is available, download the package. Overwrite all existing files with the new ones.

.. code-block:: console
 :emphasize-lines: 1,2,3,6,7

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/Kovah/LinkAce/releases/download/vx.x.x/linkace-vx.x.x.zip
 [isabell@stardust isabell]$ unzip -d linkace/ -o linkace-vx.x.x.zip
 [isabell@stardust isabell]$ rm "*".zip
 [...]
 [isabell@stardust isabell]$

Run the database migrations which are needed after all updates and delete the current cache:

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/linkace
 [isabell@stardust linkace]$ php artisan migrate
 [isabell@stardust linkace]$ php artisan cache:clear

.. note:: You may get a warning about running the migration in production mode. You should confirm the migration by answering with yes. Make sure to check the `LinkAce upgrade guide`_ so you don’t miss additional important steps.

Acknowledgements
================
This guide is based on the official `LinkAce setup guide`_.

.. _LinkAce: https://www.linkace.org/
.. _release page: https://github.com/Kovah/LinkAce/releases/
.. _LinkAce setup guide: https://www.linkace.org/docs/v1/setup/setup-without-docker/
.. _LinkAce upgrade guide: https://www.linkace.org/docs/v1/upgrade/

----

Tested with LinkAce v1.13.0 and Uberspace 7.15.8

.. author_list::
