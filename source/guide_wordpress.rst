.. author:: Nico Graf <hallo@uberspace.de>

.. spelling:word-list::
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

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP in the stable version 8.3:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.3'
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
 :emphasize-lines: 1,6,8,10

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wp core download --locale=en_US
 Downloading WordPress 6.7.1 (en_US)...
 md5 hash verified: aac77b8e3674c1e6aa7704b5d35fb2c4
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

By default, WordPress `automatically updates`_ itself to the latest stable minor version. Use ``wp`` (wp-cli) to update all plugins:

::

 [isabell@stardust ~]$ wp plugin update --all --path=/var/www/virtual/$USER/html/
 Success: Plugin already updated.
 [isabell@stardust ~]$


Performance / Optimization
==========================

All steps described in the following are optional and serve to optimize runtime as well as automation of maintenance and care of the WordPress instance.


PHP Optimization
----------------

As `PHP Optimization`_ describes in detail, there are certain PHP settings that are particularly beneficial to WordPress performance. You can set all of these by creating a ``~/etc/php.d/wordpress.ini`` with the following content:

.. code-block:: ini

  max_execution_time = 180
  memory_limit = 128M
  post_max_size = 64M
  upload_max_filesize = 64M
  max_input_time = 60
  max_input_vars = 3000


Then restart your PHP:

::

  [isabell@stardust ~]$ uberspace tools restart php
  Your PHP configuration has been loaded.
  [isabell@stardust ~]$


Real cronjob
------------

By default, regularly occurring tasks are handled by the web server via ``wp-cron.php``, which can result in longer page loading times for users. Using the `system task scheduler`_ instead frees up additional resources for visitors.

To achieve this, first deactivate the execution via ``wp-cron.php``:

::

  [isabell@stardust ~]$ wp config set DISABLE_WP_CRON true --path=/var/www/virtual/${USER}/html
  Success: Updated the constant 'DISABLE_WP_CRON' in the 'wp-config.php' file with the value 'true'.
  [isabell@stardust ~]$


Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

  */5 * * * * sleep $(( 1 + RANDOM \% 60 )) ; wp cron event run --due-now --path=/var/www/virtual/${USER}/html/ >> ${HOME}/logs/wp-cron.log 2>&1



Cache
-----
In the advanced administration handbook you can read about `caching`_:

    "WordPress caching is the fastest way to improve performance. If your site is getting hit right now install W3 Total Cache, WP Super Cache or Cache Enabler."

In this example, we are using `W3 Total Cache`_ or `Redis Object Cache`_, PHP's own OPcache and `Redis`_ as non PHP backend to distribute the load. So at first you may follow the
:lab:`redis guide <guide_redis>` on the lab and eanble `OPcache`_, which caches script bytecode in shared memory, so that scripts need not to be loaded, parsed
and compiled on every request.

To enable it, determine your user id and create the file ``~/etc/php.d/opcache.ini`` with the following content - replace ``<uid>`` with your own - and restart PHP:

::

  [isabell@stardust ~]$ echo $UID
  1337
  [isabell@stardust ~]$


.. code-block:: ini

  opcache.enable=1
  opcache.enable_cli=0
  opcache.validate_timestamps=1
  opcache.revalidate_freq=300
  opcache.revalidate_path=0
  opcache.max_accelerated_files=16229
  opcache.max_wasted_percentage=5
  opcache.memory_consumption=256
  opcache.interned_strings_buffer=64
  opcache.fast_shutdown=1
  opcache.file_cache=/var/run/user/<uid>/cache
  opcache.save_comments=1

::

  [isabell@stardust ~]$ uberspace tools restart php
  Your PHP configuration has been loaded.
  [isabell@stardust ~]$


Then install and activate the w3 total cache plugin:

::

  [isabell@stardust ~]$ wp plugin install w3-total-cache --activate --path=/var/www/virtual/${USER}/html
  ...
  Activating 'w3-total-cache'...
  Plugin 'w3-total-cache' activated.
  Success: Installed 1 of 1 plugins.
  [isabell@stardust ~]$


Now log in to your Wordpress and configure W3 Total Cache via the web interface that is now available. Opcode and browser cache are already active by default, additionally you can now activate page, database and object cache, save and enter ``/home/<user>/.redis/sock`` as redis host under the advanced settings, uncheck ``Verify TLS Certificates`` - the connection to redis is internal and via a socket that only you can access - and save again.

Alternatively, you can use the simpler Redis Object Cache plugin:

::

  [isabell@stardust ~]$ wp plugin install redis-cache --activate --path=/var/www/virtual/${USER}/html
  ...
  Activating 'redis-cache'...
  Plugin 'redis-cache' activated.
  Success: Installed 1 of 1 plugins.
  [isabell@stardust ~]$

The new ``Redis`` option page will ask you to enable the drop-in. After you have done so, the Redis socket on  ``/home/<user>/.redis/sock`` should be found automatically.

It is also recommended to make use of the option to empty the cache via WP-Cron. Daily at a time with as little expected usage as possible should work for most instances.

.. _Wordpress: https://wordpress.org
.. _automatically updates: https://wordpress.org/support/article/configuring-automatic-background-updates/
.. _system task scheduler: https://developer.wordpress.org/plugins/cron/hooking-wp-cron-into-the-system-task-scheduler/
.. _caching: https://developer.wordpress.org/advanced-administration/performance/cache/
.. _W3 Total Cache: https://wordpress.org/plugins/w3-total-cache/
.. _Redis Object Cache: https://wordpress.org/plugins/redis-cache/
.. _Redis: https://redis.io
.. _OPcache: https://www.php.net/manual/en/book.opcache.php
.. _PHP Optimization: https://developer.wordpress.org/advanced-administration/performance/php/

----

Tested with WordPress 6.7.1, Uberspace 7.16.2, and PHP 8.3

.. author_list::
