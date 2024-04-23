.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: board
.. tag:: forum

.. sidebar:: Logo

  .. image:: _static/images/phpbb.svg
      :align: center

#####
phpBB
#####

.. tag_list::

phpBB_ is a free flat-forum bulletin board software solution that can be used to stay in touch with a group of people.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`mail <mail-access>`

License
=======

phpBB_ is released under the `GPLv2 License`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use your phpBB board with your own domain, you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Create Database
===============

phpBB saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_phpbb``) instead of the default database.

.. code-block:: console

 [isabell@stardust ~]$ mysql --verbose --execute="CREATE DATABASE ${USER}_phpbb"
 --------------
 CREATE DATABASE isabell_phpbb
 --------------
 [isabell@stardust ~]$

Installation
============

Download
--------

Go to the phpBB download_ website and copy the URL of the latest ``bz2`` release package, e.g. ``https://download.phpbb.com/pub/release/3.3/3.3.8/phpBB-3.3.8.tar.bz2``.

Then, ``cd`` to your :manual:`document root <web-documentroot>` and download the latest release of phpBB and extract it:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ curl -L https://download.phpbb.com/pub/release/3.3/3.3.8/phpBB-3.3.8.tar.bz2 -o phpbb.tar.bz2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 25565    0 25565    0     0  22942      0 --:--:--  0:00:01 --:--:-- 22948
  100 5138k  100 5138k    0     0   769k      0  0:00:06  0:00:06 --:--:-- 1108k
 [isabell@stardust html]$ tar --strip-components 1 -xf phpbb.tar.bz2
 [isabell@stardust html]$ rm phpbb.tar.bz2
 [isabell@stardust html]$

Install
-------

Now point your browser to your uberspace URL ``https://isabell.uber.space`` and follow the instructions of the Installer Assistant.
Click on the Tab "Install" to start the installation.

You will need to enter the following information:

  * Administrator username and password: choose a username (maybe not *admin*) and a strong password for the admin user
  * your MySQL hostname, username, password and database name: the hostname is ``localhost``. Check the beginning of the guide for your :manual_anchor:`database credentials <database-mysql.html#login-credentials>`. You can leave the Database server port empty. As database name insert the name of the created additional database, e.g. ``isabell_phpbb``.

When the installer is finished, click on the link ``Take me to the ACP``. On the start page of the Admin Control Panel (ACP), you should disable the "Send statistical information" and the "VigLink" extension and submit your choices.

Also, the board is only usable when you have deleted the ``install`` folder:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ rm install/ -rf
 [isabell@stardust html]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Go to the phpBB.com download_ page and copy the link to the latest ``bz2`` release package, e.g. ``https://download.phpbb.com/pub/release/3.3/3.3.8/phpBB-3.3.8.tar.bz2``.

Then, create a new folder for the update in your home folder and download the release package and extract it:

::

 [isabell@stardust ~]$ mkdir phpbb_update
 [isabell@stardust ~]$ cd phpbb_update
 [isabell@stardust phpbb_update]$ curl -L https://download.phpbb.com/pub/release/3.3/3.3.8/phpBB-3.3.8.tar.bz2 -o phpbb.tar.bz2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 25565    0 25565    0     0  22942      0 --:--:--  0:00:01 --:--:-- 22948
  100 5138k  100 5138k    0     0   769k      0  0:00:06  0:00:06 --:--:-- 1108k
 [isabell@stardust phpbb_update]$ tar --strip-components 1 -xf phpbb.tar.bz2

Now, some files are removed from the downloaded package, as they are not needed. After that, the new files are copied over your existing installation files.

::

 [isabell@stardust phpbb_update]$ rm phpbb.tar.bz2 config.php images/ store/ files/ -rf
 [isabell@stardust phpbb_update]$ rm ~/html/vendor/ ~/html/cache/ -rf
 [isabell@stardust phpbb_update]$ cp -r . ~/html/
 [isabell@stardust phpbb_update]$ cd ..
 [isabell@stardust ~]$ rm phpbb_update -rf
 [isabell@stardust ~]$

Now Navigate to the database updater, e.g. ``https://isabell.uber.space/install/app.php/update`` and start the database update.

When the update is done, delete the ``install`` folder:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ rm install/ -rf
 [isabell@stardust html]$

Backup
======

Backup the following directories:

  * ``~/html/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_phpbb | xz - > ~/isabell_phpbb.sql.xz

Debugging
=========

Logs
----
Enable the Uberspace PHP and Apache error logs:

::

  [isabell@stardust ~]$ uberspace web log php_error enable
  php error log is enabled
  [isabell@stardust ~]$ uberspace web log apache_error enable
  apache error log is enabled
  [isabell@stardust ~]$

The PHP errors will be written to the file ``~/logs/error_log_php``, the Apache logs to the file ``~/logs/webserver/error_log_apache``.

Debug Mode
----------
phpBB offers a debug functionality. To enable it, edit the file ``~/html/config/production/config.yml`` and add the following section:

::

 parameters:
     debug.load_time: true
     debug.sql_explain: true
     debug.memory: true
     debug.show_errors: true
     debug.exceptions: true

After that, purge the cache at the phpBB ACP. Under the "General" tab, there will be a button on the right side of the page that says "Purge Cache".

.. _phpBB: https://www.phpbb.com/
.. _download: https://www.phpbb.com/downloads/
.. _feed: https://github.com/phpbb/phpbb/releases.atom
.. _GPLv2 License: https://github.com/phpbb/phpbb/blob/master/LICENSE

----

Tested with phpBB 3.3.8, PHP 8.1 and Uberspace 7.13.0

.. author_list::
