.. highlight:: console
.. author:: Arian Malek <https://fetziverse.de>

.. tag:: lang-php
.. tag:: photo-management
.. tag:: gallery
.. tag:: photo

.. sidebar:: Logo

  .. image:: _static/images/pixelfed.svg
      :align: center

########
Pixelfed
########

.. tag_list::

Pixelfed_ is a free, denzentralized and ethical photo sharing platform, powered by ActivityPub federation. It comes with an modern user interface similiar to instagram.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`PHP <lang-php>`
  * :lab:`Redis <guide_redis>`
  * :manual:`Cron <daemons-cron>`
  * :manual:`Mail access <mail-access>`

License
=======

Pixelfed is open-sourced software licensed under the AGPL license.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for Pixelfed:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_pixelfed"
 [isabell@stardust ~]$

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

Setup Redis
===========

Configuration
-------------

.. note:: We need Redis for in-memory caching and background task queueing. Since Uberspace version 7.7.0 Redis is preinstalled and we only need to setup a service.

Create the directory ``~/.redis/`` in your home directory:

::

 [isabell@stardust ~]$ mkdir ~/.redis/
 [isabell@stardust ~]$

Now create the config file ``~/.redis/conf`` with an editor of your choice and enter these settings. Replace ``isabell`` with your user name:

.. code-block:: none

 unixsocket /home/isabell/.redis/sock
 daemonize no
 port 0

Setup daemon
------------

Create ``~/etc/services.d/redis.ini`` with the following content:

.. code-block:: ini

 [program:redis]
 command=redis-server %(ENV_HOME)s/.redis/conf
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Installation
============

.. note:: Pixelfed uses the subdirectory ``public`` as web root and you should not install Pixelfed in your :manual:`DocumentRoot <web-documentroot>`. Instead we install it next to that and then use a symlink to make it accessible.

Clone the source one level above your :manual:`DocumentRoot <web-documentroot>` using Git:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone https://github.com/pixelfed/pixelfed
 Cloning into 'pixelfed'...
 [...]
 [isabell@stardust isabell]$

``cd`` into your Pixelfed directory and install the necessary dependencies using Composer:

::

 [isabell@stardust isabell]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ composer install
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 Package operations: 154 installs, 0 updates, 0 removals
 [...]
 Package manifest generated successfully.
 58 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!
 [isabell@stardust pixelfed]$

Remove your empty DocumentRoot and create a new symbolic link to the ``pixelfed/public`` directory:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/pixelfed/public html
 [isabell@stardust isabell]$

Configuration
=============

.. warning:: Whenever you edit the ``.env`` file, you must ``run php artisan config:cache`` in the root directory for the changes to take effect.

Copy the example configuration file ``.env.example`` to ``.env`` and generate a key into the config:

:: 

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ cp .env.example .env
 [isabell@stardust pixelfed]$ php artisan key:generate
 Application key set successfully.
 [isabell@stardust pixelfed]$

Open the file ``.env`` in your favourite editor and adjust the following blocks accordingly. For minimum privacy we recommend to disable the open registrations:

.. code-block:: none
 :emphasize-lines: 1, 3-6, 9, 11-13, 15-16, 18-25, 27

 APP_NAME="Pixelfed"

 APP_URL=https://isabell.uber.space
 APP_DOMAIN="isabell.uber.space"
 ADMIN_DOMAIN="isabell.uber.space"
 SESSION_DOMAIN="isabell.uber.space"
 
 DB_CONNECTION=mysql
 DB_HOST=localhost
 DB_PORT=3306
 DB_DATABASE=isabell_pixelfed
 DB_USERNAME=isabell
 DB_PASSWORD=MySuperSecretPassword

 REDIS_SCHEME=unix
 REDIS_PATH=/home/isabell/.redis/sock

 MAIL_DRIVER=smtp
 MAIL_HOST=stardust.uberspace.de
 MAIL_PORT=587
 MAIL_USERNAME=isabell@uber.space
 MAIL_PASSWORD=MySuperSecretPassword
 MAIL_ENCRYPTION=tls
 MAIL_FROM_ADDRESS="isabell@uber.space"
 MAIL_FROM_NAME="Pixelfed"

 OPEN_REGISTRATION=false

Run database migrations:

.. code-block:: console
 :emphasize-lines: 8

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan migrate
 **************************************
 *     Application In Production!     *
 **************************************

  Do you really wish to run this command? (yes/no) [no]:
  > yes
 [...]
 Migrating: 2020_07_25_230100_create_media_blocklists_table
 Migrated:  2020_07_25_230100_create_media_blocklists_table (0.09 seconds)
 [isabell@stardust pixelfed]$

.. note:: If you get a database error when running the migrations, ensure you updated the ``.env`` with proper database variables and then run ``php artisan config:cache``.

Cache + Optimization Commands
-----------------------------

Running the following commands is recommend when running Pixelfed in production:

:: 

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan config:cache
 Configuration cache cleared!
 Configuration cached successfully!
 [isabell@stardust pixelfed]$ php artisan route:cache
 Route cache cleared!
 Routes cached successfully!
 [isabell@stardust pixelfed]$ php artisan view:cache
 Compiled views cleared!
 Blade templates cached successfully!
 [isabell@stardust pixelfed]$

Storage link
------------

Link the storage directory:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan storage:link
 The [/var/www/virtual/isabell/pixelfed/public/storage] link has been connected to [/var/www/virtual/isabell/pixelfed/storage/app/public].
 The links have been created.
 [isabell@stardust pixelfed]$

Import Places Data
------------------

Run the following command to import the Places data:

:: 

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan import:cities
 Importing city data into database ...

 Found 128769 cities to insert ...

  128769/128769 [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%

 Successfully imported 128769 entries!

 [isabell@stardust pixelfed]$

Installing Horizon
------------------

.. note:: Horizon provides a beautiful dashboard and code-driven configuration for our Redis queues. Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. 

To install Horizon, run the following commands and recache the routes:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan horizon:install
 Publishing Horizon Service Provider...
 Publishing Horizon Assets...
 Publishing Horizon Configuration...
 Horizon scaffolding installed successfully.
 [isabell@stardust pixelfed]$ php artisan route:cache
 Route cache cleared!
 Routes cached successfully!
 [isabell@stardust pixelfed]$

Setup the daemon. Create ``~/etc/services.d/horizon.ini`` with the following content: 

.. note:: Make sure to replace ``Isabell`` with your user name. 

.. code-block:: ini

 [program:horizon]
 command=php /var/www/virtual/isabell/pixelfed/artisan horizon
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configuring Scheduler
---------------------

.. note:: The scheduler is used to run periodic commands in the background. The following commands are used in the scheduler:

 * ``media:optimize`` - Finds any un-optimized media and performs optimization
 * ``media:gc`` - Finds any media not used in statuses older than 1 hour and deletes them
 * ``horizon:snapshot`` - Generates Horizon analytics snapshot
 * ``story:gc`` - Finds expired Stories and deletes them

Add the following cronjob to your :manual:`crontab <daemons-cron>` to run the scheduler every minute:

.. code-block:: none

 * * * * * cd /var/www/virtual/$USER/pixelfed && php artisan schedule:run >> /dev/null 2>&1

Finishing installation
======================

Create your first user as admin with ``php artisan user:create``. This is also a good time to check your email configuration with the email verification:

.. code-block:: console
 :emphasize-lines: 2, 6, 9, 12, 15, 18, 21, 24, 27

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ php artisan user:create
 Creating a new user...

 Name:
 > isabell

 Username:
 > isabell

 Email:
 > isabell@uber.space

 Password:
 > MySuperSecretPassword

 Confirm Password:
 > MySuperSecretPassword

 Make this user an admin? (yes/no) [no]:
 > yes

 Manually verify email address? (yes/no) [no]:
 > no

 Are you sure you want to create this user? (yes/no) [no]:
 > yes

 Created new user!

Now you can now login by visiting your domain and using the credentials you defined above.

Updates
=======

Run ``git pull`` in the pixelfed directory to pull the latest changes from upstream. After that install new dependencies, run the cache commands and migrate the database.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/pixelfed
 [isabell@stardust pixelfed]$ git pull origin dev
 From https://github.com/pixelfed/pixelfed
  * branch              dev        -> FETCH_HEAD
 [...]
 [isabell@stardust pixelfed]$ composer install
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 [...]
 [isabell@stardust pixelfed]$ php artisan config:cache
 Configuration cache cleared!
 Configuration cached successfully!
 [isabell@stardust pixelfed]$ php artisan route:cache
 Route cache cleared!
 Routes cached successfully!
 [isabell@stardust pixelfed]$ php artisan migrate --force
 [...]
 [isabell@stardust pixelfed]$

----

Tested with Pixelfed 0.10.9, Uberspace 7.7.2.0

.. _Pixelfed: https://pixelfed.org
.. _Redis: https://redios.io

.. author_list::
