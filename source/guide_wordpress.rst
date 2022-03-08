.. author:: Nico Graf <hallo@uberspace.de>

.. spelling::
    xxxx

.. tag:: lang-php
.. tag:: blog
.. tag:: cms
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/wordpress.png
      :align: center

#########
WordPress
#########

.. tag_list::

WordPress_ is an open source blogging platform written in PHP and distributed under the GPLv2 licence.

WordPress was released in 2003 by Matt Mullenweg and Mike Little as a fork of b2/cafelog. It is maintained by the WordPress foundation.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP_ in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download and configure WordPress with ``wp`` (wp-cli):

You will need to enter the following information:

  * your blog URL: The URL for your blog. For example: isabell.uber.space
  * your MySQL username and password: you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your WordPress database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_wordpress
  * Admin User: The name and the email address of the admin user.

.. note:: The database name has to start with the user name and an underscore (isabell_xxxx). Otherwise the creation of the database will fail with a permission denied.


.. code-block:: console
 :emphasize-lines: 1,6,10

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wp core download --locale=en_US
 Downloading WordPress 5.9.1 (en_US)...
 md5 hash verified: 5bbe205b48cf9255fd7c954040aeb125
 Success: WordPress downloaded.
 [isabell@stardust html]$ wp config create --dbname=${USER}_wordpress --dbuser=${USER} --dbpass=<password>
 Success: Generated 'wp-config.php' file.
 [isabell@stardust html]$ wp db create
 Success: Database created.
 [isabell@stardust html]$ wp core install --url=${USER}.uber.space --title="Super Blog" --admin_user=<adminuser> --admin_email=<emailadress>
 Admin password: SuperSecretSecurePassword
 Success: WordPress installed successfully.
 [isabell@stardust html]$

WordPress will generate a secure password for the admin user.

Updates
=======

By default, WordPress `automatically updates`_ itself to the latest stable minor version. Use ``wp-cli`` to update all plugins:

::

 [isabell@stardust ~]$ wp plugin update --all --path=/var/www/virtual/$USER/html/
 Success: Plugin already updated.
 [isabell@stardust ~]$

.. _Wordpress: https://wordpress.org
.. _PHP: http://www.php.net/
.. _automatically updates: https://wordpress.org/support/article/configuring-automatic-background-updates/

----

Tested with WordPress 5.9.1, Uberspace 7.12.1

.. author_list::
