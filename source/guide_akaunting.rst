.. highlight:: console

.. author:: Daniel Kratz <uberlab@danielkratz.com>

.. sidebar:: Logo

  .. image:: _static/images/akaunting.png
      :align: center

#########
Akaunting
#########

Akaunting_  is a free, open source accounting software designed for small businesses and freelancers. With features like invoicing, expense tracking and accounting it can be used to manage money online while retaining full data ownership.

The software is based on top of the Laravel_ framework and therefore written in PHP_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * MySQL_
  * domains_

License
=======

Akaunting is released under the GPLv3_ license. The licence can be found in the GitHub repository. Please also regard the Akaunting terms.

  * https://github.com/akaunting/akaunting/blob/master/LICENSE.txt
  * https://akaunting.com/terms


Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Step 1: Download latest release
-------------------------------

``cd`` to your DocumentRoot_ and download the latest release, then unzip it into the ``html`` directory:

.. code-block:: console
 :emphasize-lines: 1,2,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget --output-document=latest.zip https://akaunting.com/download.php?version=latest
 --2018-10-09 10:23:04--  https://akaunting.com/download.php?version=latest
 Resolving akaunting.com (akaunting.com)... 139.162.160.225
 […]
 [isabell@stardust isabell]$ unzip latest.zip -d html
 […]
 inflating: html/routes/api.php
 inflating: html/routes/channels.php
 [isabell@stardust ~]$

Step 2: Modify htaccess file
----------------------------

Open the file ``/var/www/virtual/$USER/.htaccess`` and add ``RewriteBase /`` after ``RewriteEngine On``:

.. code-block::

 # Prevent Directory Listing
 <IfModule mod_rewrite.c>
     # Prevent Directory Listing
     [...]
 
     RewriteEngine On
     RewriteBase /
     
     # Prevent Direct Access to Protected Files
     [...]


Configuration
=============

Point your browser to your domain (e.g. isabell.uber.space) to set up and configure your Akaunting installation.

Step 1: Language Selection
--------------------------

Choose your desired language.

Step 2: Database Setup
----------------------

Akaunting saves your data in a MySQL database. We suggest you use an `additional database`_. You need to create this database before you enter the database credentials in the installer.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_akaunting"
 [isabell@stardust ~]$

Enter the following informations into the installer:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * the name of your newly created Akaunting database (e.g. ``isabell_akaunting``)

Step 3: Company and Admin Details
---------------------------------

Fill in the name of your company, the company email adress (email sender if you send e.g. invoices), an admin email adress and your admin password.

**That's it.** After the installation you can login with your chosen admin credentials.

Usage
=====

There is a user manual available which describes the interface, concepts and workflows:

    * https://akaunting.com/docs


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

You will be additionally notified about available updates in the built in notification center.
You can update the installation in the update wizzard which you can find in the Akaunting web interface.

.. warning:: Please note that third-party apps (plugins) need to be updated seperately. Available app updates are listed directly under the core updates. Make sure to check these regularly.


.. _Akaunting: https://akaunting.com
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/akaunting/akaunting/releases.atom
.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
.. _PHP: http://www.php.net/
.. _additional database: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _Laravel: https://laravel.com/
.. _DocumentRoot: https://manual.uberspace.de/en/web-documentroot.html


----

Tested with Akaunting 1.2.16, Uberspace 7.1.13

.. authors::
