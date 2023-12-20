.. author:: Lukas Herzog <hallo@lukasherzog.de>

.. tag:: lang-php
.. tag:: blog
.. tag:: cms
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/bedrock.png
      :align: center

######################
WordPress with Bedrock
######################

.. tag_list::

WordPress_ is an open source blogging platform written in PHP and distributed under the GPLv2 licence.

WordPress was released in 2003 by Matt Mullenweg and Mike Little as a fork of b2/cafelog. It is maintained by the WordPress foundation.

Bedrock_ is a Wordpress-Boilerplate with an improved folder structure, easier configuration options and development. Dependencies like themes or plugins are managed with Composer. Since Bedrock separates the non-web files from the document root, it is also more secure.

It is maintained by roots.io and released and distributed under MIT Licence.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_ with Composer
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using PHP in the stable version 8.3:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.2
 Selected PHP version 8.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

We suggest using an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. Create one with:

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_wp"

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

``cd`` to the path above your :manual:`document root <web-documentroot>` and download bedrock with ``composer``:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project roots/bedrock
 Creating a "roots/bedrock" project at "./bedrock"
 Installing roots/bedrock (1.23.1)
   - Downloading roots/bedrock (1.23.1)
   - Installing roots/bedrock (1.23.1): Extracting archive
 Created project in /var/www/virtual/eatest/bedrock
 Installing dependencies from lock file (including require-dev)
 Verifying lock file contents can be installed on current platform.
 Package operations: 18 installs, 0 updates, 0 removals
  [...]
 Generating optimized autoload files
 No security vulnerability advisories found.
 [isabell@stardust isabell]$


Configuration
=============

Wordpress-Configuration is done using .env-Files. Copy the example and edit it with your favourite editor.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/bedrock
 [isabell@stardust bedrock]$ cp .env.example .env
 [isabell@stardust isabell]$

In here you need to enter your :manual_anchor:`MySQL credentials <database-mysql.html#login-credentials>` database connection parameters and the name of your database (e.g. ``isabell_wp``).

.. code-block:: ini
 :emphasize-lines: 1,2,3,14,15,18,19,20,21,22,23,24,25

 DB_NAME='isabell_wp'
 DB_USER='isabell'
 DB_PASSWORD='MySuperSecretPassword'

 # Optionally, you can use a data source name (DSN)
 # When using a DSN, you can remove the DB_NAME, DB_USER, DB_PASSWORD, and DB_HO$
 # DATABASE_URL='mysql://database_user:database_password@database_host:database_$

 # Optional variables
 # DB_HOST='localhost'
 # DB_PREFIX='wp_'

 WP_ENV='development'
 WP_HOME='https://isabell.uber.space'
 WP_SITEURL="${WP_HOME}/wp"

 # Generate your keys here: https://roots.io/salts.html
 AUTH_KEY='generateme'
 SECURE_AUTH_KEY='generateme'
 LOGGED_IN_KEY='generateme'
 NONCE_KEY='generateme'
 AUTH_SALT='generateme'
 SECURE_AUTH_SALT='generateme'
 LOGGED_IN_SALT='generateme'
 NONCE_SALT='generateme'

You can use Roots' `Salt-Creator <https://roots.io/salts.html>`_ to generate the Salts.

.. note:: You can leave the ``WP_ENV`` Setting on ``development`` for now, but don't forget to set it on ``production`` when launching your site.
  See the Bedrock-Documentation_ for more Info on Environment-Settings

You now need to set your :manual:`document root <web-documentroot>` to the ``bedrock/web/`` directory. To do this, we delete the standard document root folder and create a symlink instead.

.. code-block:: console

 [isabell@stardust ~]$ rm -f /var/www/virtual/$USER/html/nocontent.html
 [isabell@stardust ~]$ rmdir /var/www/virtual/$USER/html

 [isabell@stardust ~]$ ln -s /var/www/virtual/$USER/bedrock/web /var/www/virtual/$USER/html
 [isabell@stardust ~]$


Point your browser to your domain, ``https://isabell.uber.space/wp/wp-admin`` in this example, to start the wordpress installation process. Here you will

 * Set a language
 * Choose a Site title
 * Set a administrative account and password

Your site is now ready to use.

.. note:: Your Website will be available in your root-directory (e.g. ``https://isabell.uber.space/``). Unlike a standard WordPress-Installation, the Backend will be available in the ``/wp`` subdirectory. To get there point your browser to ``https://isabell.uber.space/wp/wp-admin``.

Installing Plugins
=============================

Unlike a "normal" Wordpress-Installation, with bedrock, you cannot install Plugins or edit Code via the Wordpress-Backend. This is intended behaviour and part of the reason to use bedrock in the first place.

Instead you can use composer to manage Plugins. Every Plugin (or Theme) listed in on Wordpress.org is present as a Composer-Package in the  `WPackagist-Repository`_.

To install a plugin, find the exact plugin name (e.g. ``classic-editor``) from the `Wordpress Plugin Directory <https://wordpress.org/plugins/>`_ and get it via composer:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/bedrock/
 [isabell@stardust bedrock]$ composer require wpackagist-plugin/classic-editor
 ./composer.json has been updated
 Running composer update wpackagist-plugin/classic-editor
 Loading composer repositories with package information
 Updating dependencies
 Lock file operations: 1 install, 0 updates, 0 removals
   - Locking wpackagist-plugin/classic-editor (1.6.3)
 Writing lock file
 Installing dependencies from lock file (including require-dev)
 Package operations: 1 install, 0 updates, 0 removals
   - Downloading wpackagist-plugin/classic-editor (1.6.3)
   - Installing wpackagist-plugin/classic-editor (1.6.3): Extracting archive
 Generating optimized autoload files
 Using version ^1.6 for wpackagist-plugin/classic-editor
 [isabell@stardust bedrock]$

You can do the same thing with themes, using ``wpackagist-theme``:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/bedrock/
 [isabell@stardust bedrock]$ composer require wpackagist-theme/twentytwenty
 ./composer.json has been updated
 Running composer update wpackagist-theme/twentytwenty
 Loading composer repositories with package information
 Updating dependencies
 Lock file operations: 1 install, 0 updates, 0 removals
   - Locking wpackagist-theme/twentytwenty (2.4)
 Writing lock file
 Installing dependencies from lock file (including require-dev)
 Package operations: 1 install, 0 updates, 0 removals
   - Downloading wpackagist-theme/twentytwenty (2.4)
   - Installing wpackagist-theme/twentytwenty (2.4): Extracting archive
 Generating optimized autoload files
 Using version ^2.4 for wpackagist-theme/twentytwenty
 [isabell@stardust bedrock]$


Updates
=======

.. warning:: Whilst using Wordpress with bedrock it does **not** update itself automatically by default. Also updating via the wordpress Admin-Backend is not possible as soon as your environment is set to ``production``. Checkout the `Wordpress-Blog`_ for Updates.

Updating Plugins
---------------------------

For Plugins and themes installed with composer, you can simply use ``composer update`` in the ``bedrock`` directory:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/bedrock/
 [isabell@stardust bedrock]$ composer update
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 Package operations: 0 installs, 3 updates, 0 removals
  - Updating phpoption/phpoption (1.7.2 => 1.7.3): Downloading (100%)
  - Updating vlucas/phpdotenv (v4.1.0 => v4.1.2): Downloading (100%)
  - Updating roave/security-advisories (dev-master 0365bf2 => dev-master b81a572)
 Writing lock file
 Generating optimized autoload files
 [isabell@stardust bedrock]$

Updating Wordpress core
-----------------------

To update Wordpress itself you have several options:

 - Requiring the new version with ``composer require``. In this example we want to update to version ``6.4.2``:

  .. code-block:: console

   [isabell@stardust ~]$ cd /var/www/virtual/$USER/bedrock/
   [isabell@stardust bedrock]$ composer require roots/wordpress 6.4.2

 - Editing ``/var/www/virtual/$USER/bedrock/composer.json`` to always update wordpress when running ``composer update``.

  Change the line ``"roots/wordpress": "6.4.2"`` to ``"roots/wordpress": "^6.4.2"`` (your version number might vary) and safe. Then run ``composer update`` as for plugins. This will always update wordpress core until the next main version (7).



.. _Wordpress: https://wordpress.org
.. _PHP: http://www.php.net/
.. _automatically updates: https://codex.wordpress.org/Configuring_Automatic_Background_Updates
.. _Bedrock: https://roots.io/bedrock/
.. _Bedrock-Documentation: https://roots.io/bedrock/docs/installation/
.. _WPackagist-Repository: https://wpackagist.org/
.. _Wordpress-Blog: https://wordpress.org/news/

----

Tested with Bedrock 1.23.1, Wordpress 6.4.2, Uberspace 7.15.6, and PHP 8.2

.. author_list::
