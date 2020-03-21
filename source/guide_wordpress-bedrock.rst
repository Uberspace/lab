.. author:: Lukas Herzog <uber@lukasherzog.de>

.. tag:: lang-php
.. tag:: blog
.. tag:: cms
.. tag:: web
.. tag:: bedrock

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/bedrock.png
      :align: center

#########
WordPress with Bedrock
#########

.. tag_list::

WordPress_ is an open source blogging platform written in PHP and distributed under the GPLv2 licence.

WordPress was released in 2003 by Matt Mullenweg and Mike Little as a fork of b2/cafelog. It is maintained by the WordPress foundation.

Bedrock_ is a Wordpress-Boilerplate with an improved folder structure, easier configuration options and development. Dependencies like themes or plugins are managed with Composer

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_ with Composer
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Wordpress recommends PHP_ in version 7.3:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$ uberspace tools version use php 7.3
 Selected PHP version 7.3

.. include:: includes/my-print-defaults.rst

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

``cd`` to the path above your :manual:`document root <web-documentroot>` and download bedrock with ``composer``:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project roots/bedrock
 Installing roots/bedrock (1.13.1)
  - Installing roots/bedrock (1.13.1): Loading from cache
 Created project in /var/www/virtual/$USER/bedrock
 > php -r "copy('.env.example', '.env');"
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 Package operations: 11 installs, 0 updates, 0 removals
  - Installing roots/wordpress-core-installer (1.1.0): Downloading (100%)
  - Installing composer/installers (v1.8.0): Downloading (100%)
  - Installing oscarotero/env (v1.2.0): Downloading (100%)
  - Installing roots/wordpress (5.3.2): Downloading (100%)
  - Installing roots/wp-config (1.0.0): Downloading (100%)
  - Installing roots/wp-password-bcrypt (1.0.0): Downloading (100%)
  - Installing symfony/polyfill-ctype (v1.14.0): Downloading (100%)
  - Installing phpoption/phpoption (1.7.2): Downloading (100%)
  - Installing vlucas/phpdotenv (v4.1.0): Downloading (100%)
  - Installing roave/security-advisories (dev-master 0365bf2)
  - Installing squizlabs/php_codesniffer (3.5.4): Downloading (100%)
 Generating optimized autoload files

Wordpress-Configuration is done using .env-Files:

.. code-block:: console
 [isabell@stardust isabell]$ cd /var/www/virtual/$USER/bedrock/
 [isabell@stardust bedrock]$ nano .env

  
 
 
 

You will need to enter the following information:

  * your blog URL: The URL for your blog. For example: isabell.uber.space
  * your MySQL username and password: you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your WordPress database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_wordpress
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


Updates
=======

By default, WordPress `automatically updates`_ itself to the latest stable minor version. Use ``wp-cli`` to update all plugins:

::

 [isabell@stardust ~]$ wp plugin update --all --path=/var/www/virtual/$USER/html/
 Success: Plugin already updated.
 [isabell@stardust ~]$

.. _Wordpress: https://wordpress.org
.. _PHP: http://www.php.net/
.. _automatically updates: https://codex.wordpress.org/Configuring_Automatic_Background_Updates
.. _Bedrock: https://roots.io/bedrock/

----

Tested with WordPress 4.9.6, Uberspace 7.1.2

.. author_list::
