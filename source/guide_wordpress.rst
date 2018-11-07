.. author:: Nico Graf <hallo@uberspace.de>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/wordpress.png
      :align: center

#########
WordPress
#########

WordPress_ is an open source blogging platform written in PHP and distributed under the GPLv2 licence.

WordPress was released in 2003 by Matt Mullenweg and Mike Little as a fork of b2/cafelog. It is maintained by the WordPress foundation.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * MySQL_
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your `document root`_, then download and configure WordPress with ``wp-cli``:

You will need to enter the following information:

  * your blog URL: The URL for your blog. For example: isabell.uber.space
  * your MySQL username and password: you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your WordPress database name: we suggest you use an additional_ database. For example: isabell_wordpress
  * Admin User: The name and the email address of the admin user.

.. code-block:: console
 :emphasize-lines: 1,6,10

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wp core download
 Downloading WordPress 23.42.1 (en_US)...
 md5 hash verified: f009061b9d24854bfdc999c7fbeb7579
 Success: WordPress downloaded.
 [isabell@stardust html]$ wp config create --dbname=isabell_wordpress --dbuser=isabell --dbpass=MySuperSecretPassword
 Success: Generated 'wp-config.php' file.
 [isabell@stardust html]$ wp db create
 Success: Database created.
 [isabell@stardust html]$ wp core install --url=isabell.uber.space --title="Super Blog" --admin_user=<adminuser> --admin_email=<emailadress>
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
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _automatically updates: https://codex.wordpress.org/Configuring_Automatic_Background_Updates

----

Tested with WordPress 4.9.6, Uberspace 7.1.2

.. authors::
