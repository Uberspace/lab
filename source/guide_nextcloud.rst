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

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use your cloud with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of the Nextcloud and extract it:

.. note:: The link to the lastest version can be found at Nextcloud's `download page <https://nextcloud.com/install/#instructions-server>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ curl https://download.nextcloud.com/server/releases/latest.tar.bz2 | tar -xjf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

Now point your browser to your uberspace URL and follow the instructions.

You will need to enter the following information:

  * Administrator username and password: Insert the credentials you want to use for the admin user
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Nextcloud database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_nextcloud

Additionally, you can choose where Nextcloud is going to store your data files. It is recommended to place them outside of the webserver's DocumentRoot, e.g. at ``/home/isabell/nextcloud_data/``.

Tuning
======
Onlyoffice (Community Edition)
-------
To edit text and spreadsheet documents, you need to install and enable these apps from the admin interface: 

* Community Document Server (a light version of the Onlyoffice server)
* Onlyoffice (the connector to the Onlyoffice server)

Both apps can be installed optional during the main install, but the huge document server may fail. Then install it manually from the shell:

::

[isabell@stardust html]$ cd apps
[isabell@stardust apps]$ curl -L https://github.com/nextcloud/documentserver_community/releases/latest/download/documentserver_community.tar.gz | tar -xvzf -

Reload the admin panel and enable the Community Document Server. 
A click on a text/spreadsheet document should now start the Onlyoffice Editor. 

cronjob
-------

For better performance, Nextcloud suggests to add a local cronjob.

Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

 */15  *  *  *  * php -f /var/www/virtual/$USER/html/cron.php > $HOME/logs/nextcloud-cron.log 2>&1

Memcaching
----------

To further enhance perfomance, enable Memcaching.

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

Enable opcache to further optimise perfomance.

To do that, add the following lines to ``$HOME/etc/php.d/opcache.ini``:

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

In order to increase the memory limit of php to the recommended value of 512 MB, go to ``$HOME/etc/php.d/``, create ``memory_limit.ini`` and add the following line:

::

 memory_limit = 512M

PHP Reload
----------

After that you need to restart PHP configuration to load the last two changes:

::

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$

HSTS
----

Nextcloud will complain about your HSTS settings in the admin interface.

At the moment it is not possible to change the HSTS settings, as mentioned in the :manual:`manual <web-security>`.

Updates
=======

The easiest way to update Nextcloud is to use the web updater provided in the admin section of the Web Interface.

If you have installed Nextcloud on a subdomain it can happen that the update fails: Access to the UI is not possible and HTTP 403 errors are thrown.
In most cases this happens due to wrong `SELinux labels`_ which can be fixed with finishing the update via console and setting the labels according the loaded SELinux policy.
::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ php occ upgrade
 [isabell@stardust html]$ restorecon -R .
 [isabell@stardust html]$

.. note:: Check the `changelog <https://nextcloud.com/changelog/>`_ regularly to stay informed about new updates and releases.

.. _ownCloud: https://owncloud.org
.. _Nextcloud: https://nextcloud.com
.. _SELinux labels: https://wiki.gentoo.org/wiki/SELinux/Labels#Introduction


----

Tested with Nextcloud 13.0.1, Uberspace 7.1.3

.. author_list::
