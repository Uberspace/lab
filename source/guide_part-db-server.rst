
.. highlight:: console

.. author:: Phil <development@beph.de>

.. tag:: lang-php
.. tag:: web
.. tag:: inventory-management

.. sidebar:: Logo

  .. image:: _static/images/partdb.svg
      :align: center

##############
Part-DB-Server
##############

.. tag_list::

Part-DB-Server_ is a web-based database for managing electronic components and is distributed under the `AGPL-3.0`_ license.

It's the successor of Part-DB_ which is not under active development anymore. You'll find upgrade information in the section `Upgrade from Part-DB-legacy`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Node.js <lang-nodejs>` 
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`Mail <mail-access>`
  * :manual:`cronjobs <daemons-cron>`
  * composer_

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.2:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

We're using :manual:`Node.js <lang-nodejs>` in the stable version 20:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show node:
 Using 'Node.js' version: '20'
 [isabell@stardust ~]$

 .. include:: includes/my-print-defaults.rst

Download and Configuration
==========================

``cd`` to your :manual:`document root <web-documentroot>`, create and switch to a new directory named ``partdb``, download the latest release of Part-DB and extract it into the directory:

.. note:: The link to the latest version can be found at the `release page`_.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ mkdir partdb/ && cd partdb/
 [isabell@stardust partdb]$ curl --location https://github.com/Part-DB/Part-DB-server/archive/refs/tags/v1.10.0.tar.gz | tar -xzf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
 100 40.1M    0 40.1M    0     0  18.3M      0 --:--:--  0:00:02 --:--:-- 27.3M
 [isabell@stardust partdb]$


For the configuration file you have to create a secret value:

.. code-block:: console

 [isabell@stardust partdb]$ hexdump -vn16 -e'4/4 "%08x" 1 "\n"' /dev/urandom
 5192a149b12c2baccc74f16d2590c882
 [isabell@stardust partdb]$

Create a copy of the default configuration file:

.. code-block:: console

 [isabell@stardust partdb]$ cp .env .env.local
 [isabell@stardust partdb]$

Now modify the ``.env.local`` configuration file.
For this, you need your MySQL credentials, your :manual:`Mail <mail-access>` credentials (optional) and the secret you've created before:

.. code-block:: ini

 DATABASE_URL=mysql://isabell:password@127.0.0.1:3306/isabell_partdb
 APP_SECRET=5192a149b12c2baccc74f16d2590c882
 DEFAULT_URI=https://isabell.uber.space/
 MAILER_DSN=smtp://isabell:password@host.uberspace.de:587

Optional change other entries like ``DEFAULT_LANG`` to your needs.

Installation
============

First of all run ``composer``:

.. code-block:: console

 [isabell@stardust partdb]$ composer install -o --no-dev
 [...]
   - Installing twig/inky-extra (v3.8.0): Extracting archive
   - Installing twig/intl-extra (v3.8.0): Extracting archive
   - Installing twig/markdown-extra (v3.8.0): Extracting archive
   - Installing web-token/jwt-core (3.2.8): Extracting archive
   - Installing web-token/jwt-signature (3.2.8): Extracting archive
   - Installing spomky-labs/cbor-bundle (v3.0.0): Extracting archive
   - Installing web-auth/webauthn-symfony-bundle (4.7.7): Extracting archive
 Generating optimized autoload files
 composer/package-versions-deprecated: Generating version class...
 composer/package-versions-deprecated: ...done generating version class
 126 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!

 Run composer recipes at any time to see the status of your Symfony recipes.

 Executing script cache:clear	 [OK]
 Executing script assets:install public [OK]

 [isabell@stardust partdb]$

Run ``yarn``:

.. code-block:: console

 [isabell@stardust partdb]$ yarn install
 yarn install v1.22.19
 [1/5] Resolving packages...
 [2/5] Fetching packages...
 [3/5] Linking dependencies...
 warning " > stimulus-use@0.52.1" has unmet peer dependency "hotkeys-js@>= 3".
 [4/5] Building fresh packages...
 [5/5] Cleaning modules...
 Done in 114.55s.
 [isabell@stardust partdb]$

Build the assets with ``node`` and terminate the analyzer by pressing ``Ctrl+C``:

.. note::
 Normally you will just run ``yarn build``, but we circumvent the memory limit on your uberspace.

.. code-block:: console

 [isabell@stardust partdb]$ node --max_old_space_size=800 ./node_modules/webpack/bin/webpack.js

 WARNING  Be careful when using Encore.configureLoaderRule(), this is a low-level method that can potentially break Encore and Webpack when not used carefully.
 [BABEL] Note: The code generator has deoptimised the styling of /var/www/virtual/removeme/partdb/var/translations/index.js as it exceeds the max of 500KB.
 DONE  Compiled successfully in 87854ms                                                                                                                                                       23:33:48

 211 files written to public/build
 Webpack Bundle Analyzer is started at http://127.0.0.1:8888
 Use Ctrl+C to close it
 webpack compiled successfully
 ^C
 [isabell@stardust partdb]$

Warm-up cache:

.. code-block:: console

 [isabell@stardust partdb]$ php bin/console cache:warmup
  // Warming up the cache for the prod environment with debug false                                                      

 [OK] Cache for the "prod" environment (debug=false) was successfully warmed.                                           
                                                                                                                        
 [isabell@stardust partdb]$

Create a database for Part-DB, like described :manual_anchor:`here <database-mysql.html#additional-databases>`:

.. code-block:: console

 [isabell@stardust partdb]$ mysql -e "CREATE DATABASE ${USER}_partdb" && echo "Created database ${USER}_partdb"
 Created database isabell_partdb
 [isabell@stardust partdb]$

Run migration and confirm with ``yes``:

.. code-block:: console

 [isabell@stardust partdb]$ php bin/console doctrine:migrations:migrate
  WARNING! You are about to execute a migration in database "removeme_partdb" that could result in schema changes and data loss. Are you sure you wish to continue? (yes/no) [yes]:
 > yes

 [notice] Migrating up to DoctrineMigrations\Version20231130180903
 [warning] 
 [warning] The initial password for the "admin" user is: f5f746396a
 [warning] 
 [warning] Empty database detected. Skip migration.
 [warning] Migration DoctrineMigrations\Version20190902140506 was executed but did not result in any SQL statements.
 [notice] finished in 18890.4ms, used 14M memory, 27 migrations executed, 367 sql queries
                                                                                                                        
 [OK] Successfully migrated to version: DoctrineMigrations\Version20231130180903                                        
                                                                                                                        
 [isabell@stardust partdb]$

The prompted password is the password for the initial user named ``admin``.

Edit ``.htaccess``:

As the option ``FollowSymlinks`` is not allowed on Uberspace, these entries have to be changed to an alternative.

.. code-block:: console

 [isabell@stardust partdb]$ sed -i 's/+FollowSymlinks/+SymLinksIfOwnerMatch/g' public/.htaccess
 [isabell@stardust partdb]$

Remove your empty :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``partdb/public`` directory:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/partdb/public html
 [isabell@stardust ~]$

Now you should be able to access Part-DB and login as admin user.

Upgrade from Part-DB-legacy
===========================

Before starting an upgrade, you should do a backup of your MySQL database and the folder of your existing installation.
More information can be found in the official `Part-DB Upgrade Guide`_

Use this guide to create a new Part-DB instance. Do not create a new database and perform the following steps before running ``php bin/console doctrine:migrations:migrate``: 

Copy the ``data/media`` folder from the old Part-DB instance into ``public/media``:

.. code-block:: console

 [isabell@stardust pardtb]$ cp -r path-to-partdb-legacy/data/media/ public/media
 [isabell@stardust partdb]$

Clear the cache, convert the BBCode and run the migration:

.. code-block:: console

 [isabell@stardust pardtb]$ php bin/console cache:clear
 [isabell@stardust partdb]$ php bin/console doctrine:migrations:migrate
 [isabell@stardust partdb]$ php bin/console partdb:migrations:convert-bbcode
 [isabell@stardust partdb]$ php bin/console cache:clear

Afterwards you should be able to login to the Part-DB instance with your old main user account. Other users have to be activated separately.

Backup
======

Part-DB offers to create a backup:  

.. code-block:: console

 [isabell@stardust partdb]$ php bin/console partdb:backup --full /home/${USER}/partdb-backup.zip
                                                                                                                        
 [INFO] Backup Part-DB to /home/isabell/partdb-backup.zip                                                              
                                                                                                                        
 ! [NOTE] Starting backup...                                                                                            
 ! [NOTE] Backing up config files...                                                                                    
 ! [NOTE] Backing up attachments files...                                                                               
 ! [NOTE] Backup database...                                                                                            
 ! [NOTE] MySQL database detected. Dump DB to SQL using mysqldump...                                                    
                                                                                                                        
 [OK] Backup finished! You can find the backup file at /home/isabell/partdb-backup.zip                                 
                                                                                                                        
 [isabell@stardust partdb]$

Updates
=======

Part-DB will announce a new version on the start page of your installation.

To update Part-DB create a backup of the current installation and follow this guide to install a new version.

.. _Part-DB-Server: https://github.com/Part-DB/Part-DB-server
.. _Part-DB: https://github.com/Part-DB/Part-DB
.. _Part-DB Upgrade Guide: https://docs.part-db.de/upgrade_legacy.html
.. _composer: https://getcomposer.org
.. _release page: https://github.com/Part-DB/Part-DB-server/releases
.. _`AGPL-3.0`: https://www.gnu.org/licenses/agpl-3.0.html

----

Tested with Part-DB-Server 1.10.0, Uberspace 7.15, and PHP 8.2

.. author_list::
