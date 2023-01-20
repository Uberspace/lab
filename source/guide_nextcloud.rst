.. highlight:: console
.. author:: Andreas Matschl | SpaceCode <andreas@spacecode.it>
.. author:: EV21 <uberlab@ev21.de>

.. tag:: lang-php
.. tag:: web
.. tag:: photo-management
.. tag:: file-storage
.. tag:: collaborative-editing
.. tag:: groupware
.. tag:: sync
.. tag:: project-management
.. tag:: voip
.. tag:: video-chat

.. sidebar:: Logo

  .. image:: _static/images/nextcloud.svg
      :align: center

#########
Nextcloud
#########

.. tag_list::

Nextcloud_ is an open source cloud solution written in PHP and distributed under the AGPLv3 license.

Nextcloud was initially released in 2016 as a fork of ownCloud_ and is maintained by Nextcloud GmbH.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`cronjobs <daemons-cron>`

Prerequisites
=============

Use the recommended :manual:`PHP <lang-php>` version as listed in the `system requirements`_:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

You can use the domains that are currently configured :

.. include:: includes/web-domain-list.rst

If you want to use your cloud with a domain not shown here, such as your own domain, :manual:`setup your domain <web-domains>` for use with your Uberspace account.

Installation
============

PHP settings
------------

Before you start the Nextcloud installation you should adapt some PHP settings:

 #. enable the `PHP OPcache <https://www.php.net/manual/en/book.opcache.php>`_
 #. increase the PHP memory limit
 #. disable PHP output buffering
 #. restart PHP

Otherwise Nextcloud would warn you after each command execution because of the wrong set memory limit.

opcache
^^^^^^^

OPcache caches script bytecode in shared memory, so scripts need not to be loaded, parsed and compiled on every request. To enable it, create the file ``~/etc/php.d/opcache.ini`` with the following content:

.. code-block:: ini

 opcache.enable=1
 opcache.enable_cli=1
 opcache.interned_strings_buffer=16
 opcache.max_accelerated_files=10000
 opcache.memory_consumption=128
 opcache.save_comments=1
 opcache.revalidate_freq=1

APCu
^^^^

APCu is an in-memory key-value store for PHP. Installations after 21.0.1 may fail to update without this setting. To enable it, create the file ``~/etc/php.d/apcu.ini`` with the following content:

.. code-block:: ini

 apc.enable_cli=1

PHP Memory
^^^^^^^^^^

Nextcloud `recommends 512 MB <https://docs.nextcloud.com/server/latest/admin_manual/installation/system_requirements.html>`_ of memory for an installation. To set the PHP memory limit to 512 MB, create the file ``~/etc/php.d/memory_limit.ini`` with the following content:

.. code-block:: ini

 memory_limit=512M

Output Buffering
^^^^^^^^^^^^^^^^

To disable output buffering, create the file ``~/etc/php.d/output_buffering.ini`` with the following content:

.. code-block:: ini

 output_buffering=off

.. note:: After setting these PHP parameters, restart PHP to activate the changes

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$

Downloading
-----------
.. note:: This Lab uses a well-known link to the latest Nextcloud package. You can find more versions and formats on the Nextcloud `download page <https://nextcloud.com/install/#instructions-server>`_.

``cd`` to your :manual:`document root <web-documentroot>`, download the latest Nextcloud release found at `https://download.nextcloud.com/server/releases/latest.tar.bz2 <https://download.nextcloud.com/server/releases/latest.tar.bz2>`_ and extract it on the fly, omitting the top-level directory from the archive:

.. code-block:: console

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ rm nocontent.html
 [isabell@stardust html]$ curl https://download.nextcloud.com/server/releases/latest.tar.bz2 | tar -xjf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

Setup
-----
.. warning:: We strongly recommend to use the MySQL backend, consistent with the Nextcloud recommendation: `Using MariaDB/MySQL instead of SQLite <https://docs.nextcloud.com/server/latest/admin_manual/installation/server_tuning.html#using-mariadb-mysql-instead-of-sqlite>`_. This yields better performance and reduces disk load on the host you share. Do not use the SQLite backend for production.

Create the database
^^^^^^^^^^^^^^^^^^^

First, create a MySQL database to hold your Nextcloud installation

.. code-block:: console

  [isabell@stardust html]$ mysql --verbose --execute="CREATE DATABASE ${USER}_nextcloud"
  --------------
  CREATE DATABASE isabell_nextcloud
  --------------
  [isabell@stardust html]$

Run the installation script
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, execute the Nextcloud maintenance PHP script ``occ`` with the parameters shown below. Set the three highlighted parameters to your account-specific values before executing the command:

* ``NEXTCLOUD_ADMIN_USER`` the name of the Nextcloud admin user you have to use when logging on for the first time on your new Nextcloud Instance
* ``NEXTCLOUD_ADMIN_PASS`` the password for the Nextcloud admin user
* ``MYSQL_PASSWORD`` your :manual_anchor:`MySQL Password <database-mysql.html#login-credentials>`

.. code-block:: console
  :emphasize-lines: 1-3

  [isabell@stardust html]$ NEXTCLOUD_ADMIN_USER='MyUserName'
  [isabell@stardust html]$ NEXTCLOUD_ADMIN_PASS='MySuperSecretAdminPassword'
  [isabell@stardust html]$ MYSQL_PASSWORD='MySuperSecretMySQLPassword'
  [isabell@stardust html]$ php occ maintenance:install --admin-user="${NEXTCLOUD_ADMIN_USER}" --admin-pass="${NEXTCLOUD_ADMIN_PASS}" --database='mysql' --database-name="${USER}_nextcloud"  --database-user="${USER}" --database-pass="${MYSQL_PASSWORD}" --data-dir="${HOME}/nextcloud_data"
  Nextcloud was successfully installed
  [isabell@stardust html]$

Set the "trusted" domain
^^^^^^^^^^^^^^^^^^^^^^^^

Set the :manual:`domain name <web-domains>` that your Nextcloud will be accessed with as "trusted":

.. code-block:: console
  :emphasize-lines: 1,3

  [isabell@stardust html]$ php occ config:system:set trusted_domains 0 --value="isabell.uber.space"
  System config value trusted_domains => 0 set to string isabell.uber.space
  [isabell@stardust html]$ php occ config:system:set overwrite.cli.url --value="https://isabell.uber.space"
  System config value overwrite.cli.url set to string https://isabell.uber.space
  [isabell@stardust html]$

Set links to the log file destinations so you can more easily access them:

.. code-block:: console

  [isabell@stardust html]$ ln --symbolic ~/nextcloud_data/nextcloud.log ~/logs/nextcloud.log
  [isabell@stardust html]$ ln --symbolic ~/nextcloud_data/updater.log ~/logs/nextcloud-updater.log
  [isabell@stardust html]$

You can now logon your Nextcloud using the domain you just configured as trusted. But before you use it, go to the next chapter and finish the configuration to enable sending mails, optimize performance and setup a housekeeping job.

Configuration
=============

Currently your Nextcloud installation is not capable of sending mail, e.g.  for notifications or password resets. You can do this by executing the commands in the following block or by editing the ``~/html/config/config.php`` with your favorite editor. If you want to keep things simple, use sendmail. Alternatively log in with your admin user, go to settings > Administration > Basic settings and  configure the email-server.

Sendmail Settings
-----------------

| For the basic system mail configuration just run the following commands.
| You can also change the `mail_from_adress` or the `mail_domain` if you have :manual:`set up additional mail domains <mail-domains>`

.. code-block:: console

  [isabell@stardust html]$ php occ config:system:set mail_domain --value="uber.space"
  System config value mail_domain set to string uber.space
  [isabell@stardust html]$ php occ config:system:set mail_from_address --value="$USER"
  System config value mail_from_address set to string isabell
  [isabell@stardust html]$ php occ config:system:set mail_smtpmode --value="sendmail"
  System config value mail_smtpmode set to string sendmail
  [isabell@stardust html]$ php occ config:system:set mail_sendmailmode --value="pipe"
  System config value mail_sendmailmode set to string pipe
  [isabell@stardust html]$

.. note:: | If you prefer an advanced configuration read the `Nextcloud admin manual for email`_.
 | You can also set all settings via the web based admin interface.

Tuning
======

URL rewriting
-------------

If you prefer prettier URLs without ``index.php`` run the following two commands.

.. code-block:: console

  [isabell@stardust html]$ php occ config:system:set htaccess.RewriteBase --value='/'
  System config value htaccess.RewriteBase set to string /
  [isabell@stardust html]$ php occ maintenance:update:htaccess
  .htaccess has been updated
  [isabell@stardust html]$

cronjob
-------

For better performance, Nextcloud suggests to add a local cronjob.

Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

 */5  *  *  *  * sleep $(( 1 + $RANDOM \% 60 )) ; php -f $HOME/html/cron.php > $HOME/logs/nextcloud-cron.log 2>&1

.. note:: The actual cronjob is preceded by a random sleep of maximum one minute to prevent load peaks every 5 minutes due to simultaneous execution of all cronjobs.

Configure Nextcloud to rely on the configured cronjob:

::

  [isabell@stardust html]$ php occ background:cron
  Set mode for background jobs to 'cron'


Memcaching
----------

To further enhance performance, enable Memcaching.

APCu caching
^^^^^^^^^^^^

To enable Memcaching (APCu), execute the following commands:

.. code-block:: console

  [isabell@stardust html]$ php occ config:system:set memcache.local --value='\OC\Memcache\APCu'
  System config value memcache.local set to string \OC\Memcache\APCu
  [isabell@stardust html]$

Redis caching
^^^^^^^^^^^^^

To reduce load on the mysql server and also improve transactional file locking you may follow the :lab:`redis guide <guide_redis>` on the lab and then execute the following commands:

.. code-block:: console

  [isabell@stardust html]$ php occ config:system:set redis host --value="${HOME}/.redis/sock"
  System config value redis => host set to string /home/isabell/.redis/sock
  [isabell@stardust html]$ php occ config:system:set redis port --value=0
  System config value redis => port set to string 0
  [isabell@stardust html]$ php occ config:system:set redis timeout --value=1.5
  System config value redis => timeout set to string 1.5
  [isabell@stardust html]$ php occ config:system:set filelocking.enabled --value='true'
  System config value filelocking.enabled set to string true
  [isabell@stardust html]$ php occ config:system:set memcache.locking --value='\OC\Memcache\Redis'
  System config value memcache.locking set to string \OC\Memcache\Redis
  [isabell@stardust html]$ php occ config:system:set memcache.distributed --value='\OC\Memcache\Redis'
  System config value memcache.distributed set to string \OC\Memcache\Redis
  [isabell@stardust html]$

In the Nextcloud admin manual you can find more Information about `memory caching <https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html#memory-caching>`_ and `transactional file locking <https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/files_locking_transactional.html>`_.

default phone region
^^^^^^^^^^^^^^^^^^^^

| This sets the default phone region for phone numbers to allow users to add phone numbers to their profile without the country calling code.
| Nextcloud will then automatically add the default country calling code (e.g. +49 for Germany).
| Change the value for this setting according to your `ISO 3166-1 country code <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements>`_ like ``DE`` in this case.

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust html]$ php occ config:system:set default_phone_region --value='DE'
  System config value default_phone_region set to string DE
  [isabell@stardust html]$

Client Push
-----------

To prevent clients from regularly asking the server for updates in short periods of time you can use the service: :lab:`Client Push <guide_notify_push>`.

Database maintenance
--------------------

To adapt some database configs to make Nextcloud run smoother execute these commands:

.. code-block:: console

  [isabell@stardust ~]$ cd html
  [isabell@stardust html]$ php occ db:add-missing-indices --no-interaction
  [isabell@stardust html]$ php occ db:add-missing-columns --no-interaction
  [isabell@stardust html]$ php occ db:add-missing-primary-keys --no-interaction
  [isabell@stardust html]$ php occ db:convert-filecache-bigint --no-interaction
  [isabell@stardust html]$

Apps
----

Nextcloud Talk
^^^^^^^^^^^^^^

To enable video/audio calls in your instance, install and enable the "Talk" app in the admin interface.
If the web installation fails, install the app manually in your shell:

.. code-block:: console

  [isabell@stardust html]$ cd apps
  [isabell@stardust apps]$ curl -L https://github.com/nextcloud/spreed/releases/download/v8.0.7/spreed-8.0.7.tar.gz | tar -xvzf -
  [isabell@stardust apps]$

Reload the page and press the talk icon in the top menu bar.

Updates
=======

.. note:: Check the `changelog <https://nextcloud.com/changelog/>`_ regularly or subscribe to the project's `Github release feed <https://github.com/nextcloud/server/releases.atom/>`_ with your favorite feed reader to stay informed about new updates and releases.

The easiest way to update Nextcloud is to use the web updater provided in the admin section of the Web Interface.

Updating via console command is also a comfortable way to perform upgrades. While new major releases of Nextcloud also introduce new features the updater might ask you to run some commands e.g. for database optimization.
The release cycle of Nextcloud is very short. A prepared script with some common checks would ensure you don't need to run them.

.. warning:: Before updating to the next major release, such as version 19.x.x to 20.x.x, make sure your apps are compatible or there exists updates. Otherwise the incompatible apps will get disabled. If the web based admin overview displays an available update it also checks if there are any incompatible apps. You can also check for compatible versions in the `Nextcloud App Store`_.

Create ``~/bin/nextcloud-update`` with the following content:

.. code-block:: bash

 #!/usr/bin/env bash
 ## Updater automatically works in maintenance:mode.
 ## Use the Uberspace backup system for files and database if you need to roll back.
 ## The Nextcloud updater creates backups only to safe base and app code data and config files
 ## so it takes ressources you might need for your productive data.
 ## Deactivate NC-updater Backups with --no-backup (works from 19.0.4, 18.0.10 and 17.0.10)
 php ~/html/updater/updater.phar -vv --no-backup --no-interaction

 ## database optimisations
 php ~/html/occ db:add-missing-primary-keys --no-interaction
 php ~/html/occ db:add-missing-columns --no-interaction
 php ~/html/occ db:add-missing-indices --no-interaction
 php ~/html/occ db:convert-filecache-bigint --no-interaction

 php ~/html/occ app:update --all
 /usr/sbin/restorecon -R ~/html

 ## FYI: If that file exist...
 if test -f ~/etc/services.d/notify_push.ini
 then supervisorctl restart notify_push
 fi

Make the script executable:

.. code-block:: console

  [isabell@stardust ~]$ chmod +x ~/bin/nextcloud-update
  [isabell@stardust ~]$

Then you can run the script whenever you need it to perform the update.

.. code-block:: console

  [isabell@stardust ~]$ nextcloud-update
  [...]
  [isabell@stardust ~]$

.. tip:: You can automate this script as a :manual:`cronjob <daemons-cron>`.

 | ``@daily $HOME/bin/nextcloud-update`` output as email
 | ``@daily $HOME/bin/nextcloud-update > $HOME/logs/nextcloud-update.log 2>&1`` latest output as logfile

Troubleshooting
===============

403 errors
----------

If you have installed Nextcloud on a subdomain it can happen that the update fails: Access to the UI is not possible and HTTP 403 errors are thrown.
In most cases this happens due to wrong `SELinux labels`_ which can be fixed with finishing the update via console and setting the labels according the loaded SELinux policy.

.. code-block:: console

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ php occ upgrade
 [isabell@stardust html]$ restorecon -R .
 [isabell@stardust html]$ php occ maintenance:mode --off
 [isabell@stardust html]$

missing files
-------------

If files are missing like if you move files or restore backups on the machine and not via web you can perform a scan.

.. code-block:: console

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ php occ files:scan --all
 [isabell@stardust html]$ php occ files:scan-app-data
 [isabell@stardust html]$

memory limit after migration from U6
------------------------------------

If you still see an error in the web UI, edit ``~/etc/php.d/php.ini`` with the following content:

.. code-block:: ini

 memory_limit=512M

storage capacity problems
-------------------------

| If you use large apps like onlyoffice, your backups can get very large in relation to your storage capacity. Nextcloud always keeps the last 3 backups and deletes the older ones.
| Depending on your storage quota you may run into issues so you may want to delete some backups. The Updater will store the backups in a folder with a generated suffix ``updater-XXXXX`` inside the data directory.

| e.g. according to the recommended data location:
|  ``/home/isabell/nextcloud_data/updater_XXXXX/backups``
| if you did't change the default setting:
|  ``/home/isabell/html/data/updater_XXXXX/backups``

Here is an example you probably don't want to keep on your Uberspace. To get rid of the old version navigate to that path and run: ``rm --recursive nextcloud-19.*``
::

  ncdu 1.15.1 ~ Use the arrow keys to navigate, press ? for help
  --- /home/isabell/nextcloud-data/updater-ocRANDOMg5/backups ----
                         /..
    1,8 GiB [##########] /nextcloud-20.0.0.9-1603717139
    1,6 GiB [########  ] /nextcloud-19.0.3.1
    1,6 GiB [########  ] /nextcloud-19.0.4.0-1601738662

  Total disk usage:   4,9 GiB  Apparent size:   4,7 GiB  Items: 132481

PHP fatal error
---------------

The update to Nextcloud 21.0.1 may fail with the following error message:

.. code-block:: console

  /PHP Fatal error:  Allowed memory size of XXXXXX bytes exhausted (tried to allocate XXXXXXX
  bytes) in /var/www/virtual/isabell/html/lib/private/AppFramework/Utility/
  SimpleContainer.php on line 133/

To solve the issue, apply the ``apc.enable_cli=1`` step above to your installation.

Contacts app hangs
------------------

When your instance is hanging when you open the contacts app you might be affected by `Nextcloud issue #33048 <https://github.com/nextcloud/server/issues/33048>`_

As a workaround you can remove or override ``ErrorDocument`` entries in the ``.htaccess`` file:

.. code-block:: bash

 ErrorDocument 403 "Forbidden"
 ErrorDocument 404 "Not found"

You need to reapply these changes after you installed Nextcloud updates or after you executed the ``maintenance:update:htaccess`` command.

.. _ownCloud: https://owncloud.org
.. _Nextcloud: https://nextcloud.com
.. _`system requirements`: https://docs.nextcloud.com/server/latest/admin_manual/installation/system_requirements.html
.. _`Nextcloud admin manual for email`: https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/email_configuration.html#email
.. _`Nextcloud App Store`: https://apps.nextcloud.com
.. _SELinux labels: https://wiki.gentoo.org/wiki/SELinux/Labels#Introduction


----

Tested with Nextcloud 25.0.1, Uberspace 7.14, PHP 8.1

.. author_list::
