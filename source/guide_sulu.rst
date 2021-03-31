.. highlight:: console

.. author:: Clemens Krack <info@clemenskrack.com>

.. tag:: lang-php
.. tag:: cms
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/sulu.png
      :align: center

#############
Sulu CMS
#############

.. tag_list::

`Sulu CMS`_ is a content management platform based on Symfony made for businesses. It's a flexible CMS to create and manage enterprise multi-sites and a reliable development environment for high-performance apps. With powerful features for developers and a simple UI for editors it's the ideal engine for state-of-the-art business websites and web-based software.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`


License
=======

`Sulu CMS`_ is released under the `MIT License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Since Sulu CMS uses the subdirectory ``public/`` as document root of your website you should **not** install Sulu in your default Uberspace :manual:`DocumentRoot <web-documentroot>`. Instead, we install it next to that and then use a symlink to make it accessible to the web.

``cd`` to one level above your :manual:`DocumentRoot <web-documentroot>`, then use the PHP Dependency Manager Composer_ to create a new project based on the **Sulu Skeleton**.

.. note:: Replace ``sulucms`` in the examples with your desired name for the directory/database.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project sulu/skeleton sulucms
 Creating a "sulu/skeleton" project at "./sulucms"
 Installing sulu/skeleton (2.0.7)
   - Installing sulu/skeleton (2.0.7): Loading from cache
 Created project in /var/www/virtual/ckrack/sulucms
 […]
 [isabell@stardust isabell]$

Remove your empty :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``sulucms/public`` directory.

.. code-block:: console

 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/sulucms/public html
 [isabell@stardust isabell]$ cd ~
 [isabell@stardust ~]$


Configuration
=============

During the setup process you need to configure an ``.env.local`` file with database credentials. We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for Sulu CMS to save your data. You have to create this database first using the following command.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_sulucms"
 [isabell@stardust ~]$

.. note:: As uberspace uses MariaDb, you need to find the version and prefix the serverVersion with mariadb.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "SELECT VERSION()"
  +-----------------+
  | VERSION()       |
  +-----------------+
  | 10.3.22-MariaDB |
  +-----------------+
 [isabell@stardust ~]$

Review the sample configuration file ``.../sulucms/.env``. Then edit the ``.env.local`` file and change the values of ``APP_ENV`` and ``DATABASE_URL``, to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` and save the file.

.. code-block:: ini

 APP_ENV=prod
 DATABASE_URL=mysql://isabell:MySuperSecretPassword@localhost/isabell_sulucms?serverVersion=mariadb-10.3.22

.. note:: You can optionally configure Sulu to send emails in the same place.


When you’re done with the configuration, populate the database with Sulu’s default data by following the build walkthrough.

.. code-block:: console
 :emphasize-lines: 31

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/sulucms
 [isabell@stardust sulucms]$ ./bin/adminconsole sulu:build prod
 Build Targets
 =============

 +---+--------------------+-----------------------------------------------------------------+
 | # | Builder            | Deps                                                            |
 +---+--------------------+-----------------------------------------------------------------+
 | 0 | database           |                                                                 |
 | 1 | phpcr              | database                                                        |
 | 2 | fixtures           | database, phpcr                                                 |
 | 3 | phpcr_migrations   | phpcr                                                           |
 | 4 | system_collections | database, fixtures                                              |
 | 5 | prod               | database, phpcr, fixtures, phpcr_migrations, system_collections |
 +---+--------------------+-----------------------------------------------------------------+

 Options:

   - nodeps: false
   - destroy: false
   - help: false
   - quiet: false
   - verbose: false
   - version: false
   - ansi: false
   - no-ansi: false
   - no-interaction: false
   - env: 'prod'
   - no-debug: false

 Look good? (y)y
 […]
 [isabell@stardust ~]$

Sulu will create the database schema and populate it with sample data for the skeleton.


Finishing installation
======================

Before we can login, we must create a security role and a first user.

.. code-block:: console
 :emphasize-lines: 3,6,9,10,11,12,16,19,20

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/sulucms
 [isabell@stardust sulucms]$ ./bin/adminconsole sulu:security:role:create
 Please choose a rolename: admin
 Please choose a system:
 [0] Sulu
 > 0
 Created role "admin" in system "Sulu".
 [isabell@stardust sulucms]$ ./bin/adminconsole sulu:security:user:create
 Please choose a username: isabell
 Please choose a FirstName: Isabell
 Please choose a LastName: Stardust
 Please choose a Email: isabell@stardust.uberspace.de
 Please choose a locale
   [0] de
   [1] en
  > 1
 Please choose a role:
   [0] admin
  > 0
 Please choose a Password:
 Created user "isabell" in role "admin"
 [isabell@stardust sulucms]$

To finish the installation you need to point your browser to the sulu administration on your domain (e.g. ``https://isabell.uber.space/admin/``) and login.


Best practices
==============

To develop your website, you need to setup a webspace and templates for the pages - Sulu CMS comes as a bare system without any theming.
Find out more about the concepts in the `Sulu documentation`_.

You probably want to develop your templates locally on your machine. It's recommended to initialize a git repository, add a remote and clone from the remote to your machine.

Updates
=======

.. note:: Check the Releases_ on Github regularly to stay informed about the newest version.

.. warning:: Follow the upgrade guidelines before updating the code via composer..

To update `Sulu CMS`_ you can run the following command in the root directory of the application.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/sulucms
 [isabell@stardust sulucms]$ composer update
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 […]
 [isabell@stardust ~]$



.. _Sulu CMS: https://sulu.io/
.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE: https://github.com/sulu/sulu/blob/master/LICENSE
.. _Composer: https://getcomposer.org/
.. _Releases: https://github.com/sulu/sulu/releases
.. _Sulu documentation: https://docs.sulu.io/en/latest/book/index.html


----

Tested with Sulu CMS v2.0.7, Uberspace 7.6.1.2

.. author_list::
