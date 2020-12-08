.. highlight:: console
.. author:: Andreas Matschl | SpaceCode <andreas@spacecode.it>

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

  .. image:: _static/images/nextcloud.png
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

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use your cloud with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of the Nextcloud and extract it:

.. note:: The link to the latest version can be found at Nextcloud's `download page <https://nextcloud.com/install/#instructions-server>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ curl https://download.nextcloud.com/server/releases/latest.tar.bz2 | tar -xjf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

Now point your browser to your uberspace URL and follow the instructions.

.. warning:: We strongly recommend you to use the MySQL backend for nextcloud. Do not use the SQLite backend for production. It gives you a better performance and reduces disk load on the host you share.

You will need to enter the following information:

  * Administrator username and password: Insert the credentials you want to use for the admin user
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Nextcloud database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_nextcloud

Additionally, you can choose where Nextcloud is going to store your data files. It is recommended to place them outside of the webserver's DocumentRoot, e.g. at ``/home/isabell/nextcloud_data/``.

Configuration
=============

Currently your Nextcloud installation is not capable of sending mail, e.g.  for notifications or password resets. Log in with your admin user, go to settings > Administration > Basic settings and  configure the email-server. Alternatively you can do this by editing the ``/var/www/virtual/$USER/html/config/config.php`` with your favorite editor. If you want to keep things simple, use the sendmail option. If you prefer saving all messages in a (dedicated) mailbox use the smtp variant.

Sendmail Settings
-----------------

 and enter the following settings:

.. warning:: Make sure to replace the example values.

::

 'mail_domain' => 'uber.space',
 'mail_from_address' => 'isabell',
 'mail_smtpmode' => 'sendmail',
 'mail_sendmailmode' => 'pipe',

SMTP Settings
-------------

.. note:: In our example we assume that Nextcloud will use the user's :manual:`system mailbox <mail-mailboxes>` user to send out mails. If you prefer to use an :manual_anchor:`additional mailbox <mail-mailboxes.html#setup-a-new-mailbox>` just adapt the settings. Refer to the :manual_anchor:`manual <mail-access.html#smtp>` if you don't know your smtp password.

::

 'mail_domain' => 'uber.space',
 'mail_from_address' => 'isabell',
 'mail_smtpmode' => 'smtp',
 'mail_smtpport' => 587,
 'mail_smtphost' => 'stardust.uberspace.de',
 'mail_smtpsecure' => 'tls',
 'mail_smtpauth' => true,
 'mail_smtpauthtype' => 'LOGIN',
 'mail_smtpname' => 'isabell@uber.space',
 'mail_smtppassword' => 'MySSHPasswordIfUsingTheSystemMailbox',


Tuning
======
cronjob
-------

For better performance, Nextcloud suggests to add a local cronjob.

Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

 */15  *  *  *  * php -f /var/www/virtual/$USER/html/cron.php > $HOME/logs/nextcloud-cron.log 2>&1

Memcaching
----------

To further enhance performance, enable Memcaching.

To enable Memcaching (APCu), add the following line to your /var/www/virtual/$USER/html/config/config.php:

.. code-block:: console
 :emphasize-lines: 5

 [...]
    'dbuser' => 'isabell',
    'dbpassword' => 'MySuperSecretPassword',
    'installed' => true,
    'memcache.local' => '\OC\Memcache\APCu',
  );

opcache
-------

Enable opcache to further optimise performance.

To do that, create ``$HOME/etc/php.d/opcache.ini`` with the content:

::

 opcache.enable=1
 opcache.enable_cli=1
 opcache.interned_strings_buffer=8
 opcache.max_accelerated_files=10000
 opcache.memory_consumption=128
 opcache.save_comments=1
 opcache.revalidate_freq=1

PHP Memory
----------

In order to increase the memory limit of php to the recommended value of 512 MB, create ``$HOME/etc/php.d/memory_limit.ini`` with the following content:

::

 memory_limit = 512M

Output Buffering
----------------

Disable output buffering, create ``$HOME/etc/php.d/output_buffering.ini`` with the following content:

::

 output_buffering=0

PHP Reload
----------

After that you need to restart PHP configuration to load the last two changes:

::

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$

Database maintenance
--------------------

To adapt some database configs to make Nextcloud run smoother execute these commands:

::

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ php occ db:add-missing-indices
 [isabell@stardust html]$ php occ db:convert-filecache-bigint

Onlyoffice (Community Edition)
------------------------------
To edit text and spreadsheet documents, you need to install and enable these apps from the admin interface:

* Community Document Server (a light version of the Onlyoffice server)
* Onlyoffice (the connector to the Onlyoffice server)

Both apps can be installed optional during the main install, but the huge document server may fail. Then install it manually from the shell:

::

[isabell@stardust html]$ cd apps
[isabell@stardust apps]$ curl -L https://github.com/nextcloud/documentserver_community/releases/latest/download/documentserver_community.tar.gz | tar -xvzf -

Reload the admin panel and enable the Community Document Server.
A click on a text/spreadsheet document should now start the Onlyoffice Editor.

Nextcloud Talk
--------------

To enable video/audio calls in your instance, install and enable the "Talk" app in the admin interface.
If the web installation fails, install the app manually in your shell:

::

  [isabell@stardust html]$ cd apps
  [isabell@stardust apps]$ curl -L https://github.com/nextcloud/spreed/releases/download/v8.0.7/spreed-8.0.7.tar.gz | tar -xvzf -

Reload the page and press the talk icon in the top menu bar.

Updates
=======

The easiest way to update Nextcloud is to use the web updater provided in the admin section of the Web Interface.

Updating via console command is also a comfortable way to perform upgrades. While new major releases of Nextcloud also introduce new features the updater might ask you to run some commands e.g. for database optimisation.
The release cycle of Nextcloud is very short. A prepared script with some common checks would ensure you don't need to run them.

.. warning:: Before updating to the next major release, such as version 19.x.x to 20.x.x, make sure your apps are compatible or there exists updates. Otherwise the incompatible apps will get disabled. If the web based admin overview displays an available update it also checks if there are any incompatible apps. You can also check for compatible versions in the `Nextcloud App Store`_.

Create `~/bin/nextcloud-update` with the following content:
::

 #!/usr/bin/env bash
 # Updater automatically works in maintenance:mode
 php ~/html/updater/updater.phar --no-interaction

 # re-enable maintenance mode for occ commands
 php ~/html/occ maintenance:mode --on

 ## database optimizations
 ## The following command works from Nextcloud 19.
 ## remove '#' so it is working
 #php ~/html/occ db:add-missing-columns
 php ~/html/occ db:add-missing-indices
 php ~/html/occ db:convert-filecache-bigint

 php ~/html/occ app:update --all
 php ~/html/occ maintenance:mode --off
 restorecon -R ~/html

Make the script executable:
::

 [isabell@stardust ~]$ chmod +x ~/bin/nextcloud-update
 [isabell@stardust ~]$

Then you can run the script whenever you need it to perform the update.
::

 [isabell@stardust ~]$ nextcloud-update
 [...]
 [isabell@stardust ~]$

.. note:: Check the `changelog <https://nextcloud.com/changelog/>`_ regularly or subscribe to the project's `Github release feed <https://github.com/nextcloud/server/releases.atom/>`_ with your favorite feed reader to stay informed about new updates and releases.

Troubleshooting
===============

403 errors
----------

If you have installed Nextcloud on a subdomain it can happen that the update fails: Access to the UI is not possible and HTTP 403 errors are thrown.
In most cases this happens due to wrong `SELinux labels`_ which can be fixed with finishing the update via console and setting the labels according the loaded SELinux policy.
::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ php occ upgrade
 [isabell@stardust html]$ restorecon -R .
 [isabell@stardust html]$ php occ maintenance:mode --off
 [isabell@stardust html]$

missing files
-------------

If files are missing like if you move files or restore backups on the machine and not via web you can perform a scan.
::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ php occ files:scan --all
 [isabell@stardust html]$ php occ files:scan-app-data
 [isabell@stardust html]$

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

.. _ownCloud: https://owncloud.org
.. _Nextcloud: https://nextcloud.com
.. _`Nextcloud App Store`: https://apps.nextcloud.com
.. _SELinux labels: https://wiki.gentoo.org/wiki/SELinux/Labels#Introduction


----

Tested with Nextcloud 20.0.0, Uberspace 7.7.8.0

.. author_list::
