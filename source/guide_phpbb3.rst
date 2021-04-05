.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: board
.. tag:: forum

.. sidebar:: Logo

  .. image:: _static/images/phpbb.svg
      :align: center

######
phpBB3
######

.. tag_list::

phpBB3_ is a free flat-forum bulletin board software solution that can be used to stay in touch with a group of people.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`mail <mail-access>`

License
=======

phpBB3_ is released under the `GPLv2 License`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use your phpBB3 board with your own domain, you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Create Database
===============

phpBB3 saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_phpbb3``) instead of the default database.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_phpbb3"
 [isabell@stardust ~]$

Installation
============

Go to the phpBB3 download_ website and copy the URL of the latest ZIP release, e.g. ``https://download.phpbb.com/pub/release/3.3/3.3.3/phpBB-3.3.3.zip``.

Then, ``cd`` to your :manual:`document root <web-documentroot>` and download the latest release of phpBB3 and extract it:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ curl -L https://download.phpbb.com/pub/release/3.3/3.3.3/phpBB-3.3.3.zip -o phpbb.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 25565    0 25565    0     0  22942      0 --:--:--  0:00:01 --:--:-- 22948
  100 5138k  100 5138k    0     0   769k      0  0:00:06  0:00:06 --:--:-- 1108k
 [isabell@stardust html]$ unzip phpbb.zip
 [isabell@stardust html]$ mv phpBB3/* .
 [isabell@stardust html]$ rm phpbb.zip
 [isabell@stardust html]$ rm phpBB3/ -rf
 [isabell@stardust html]$

Now point your browser to your uberspace URL ``https://isabell.uber.space`` and follow the instructions of the Installer Assistant.
Click on the Tab "Install" to start the installation.

You will need to enter the following information:

  * Administrator username and password: choose a username (maybe not *admin*) and a strong password for the admin user
  * your MySQL hostname, username, password and database name: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top. You can leave the Database server port empty. As database name insert the name of the created additional database.
  * Make additional settings like :manual:`SMTP <mail-access>` for sending E-mails.

When the installer is finished, click on the link ``Take me to the ACP``. On the start page of the Admin Control Panel (ACP), you should disable the "Send statistical information" and the "VigLink" extension and submit your choices.

Also, the board is only usable when you have deleted the ``install`` folder:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ rm install/ -rf
 [isabell@stardust html]$

Updates
=======

Go to the phpBB.com download_ page and copy the link to the latest ZIP release, e.g. ``https://download.phpbb.com/pub/release/3.3/3.3.3/phpBB-3.3.3.zip``.

Then, ``cd`` to your :manual:`document root <web-documentroot>` and download the release package and extract it:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ curl -L https://download.phpbb.com/pub/release/3.3/3.3.3/phpBB-3.3.3.zip -o phpbb_update.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 25565    0 25565    0     0  22942      0 --:--:--  0:00:01 --:--:-- 22948
  100 5138k  100 5138k    0     0   769k      0  0:00:06  0:00:06 --:--:-- 1108k
 [isabell@stardust html]$ unzip phpbb_update.zip -d _update
 [isabell@stardust html]$ rm _update/phpBB3/config.php
 [isabell@stardust html]$ rm _update/phpBB3/files/ -rf
 [isabell@stardust html]$ rm _update/phpBB3/images/ -rf
 [isabell@stardust html]$ rm _update/phpBB3/ext/ -rf
 [isabell@stardust html]$ cp _update/phpBB3/* . -R
 [isabell@stardust html]$ rm _update/ -rf
 [isabell@stardust html]$ rm phpbb_update.zip
 [isabell@stardust html]$

The commands first extracts the archive into an own subfolder ``_update``. After that, some files and folders are removed, as they are not needed. All new files will now the copied over the existing installation. When all finished, the update files are removed.

Now Navigate to the database updater, e.g. ``https://isabell.uber.space/install/app.php/update`` and start the database update.

When the update is done, delete the ``install`` folder:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ rm install/ -rf
 [isabell@stardust html]$

.. note:: Check the update feed_ regularly to stay informed about the newest version.


Backup
======

Backup the following directories:

  * ``~/html/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_phpbb3 | xz - > ~/isabell_phpbb3.sql.xz

.. _phpBB3: https://www.phpbb.com/
.. _download: https://www.phpbb.com/downloads/
.. _feed: https://github.com/phpbb/phpbb/releases.atom
.. _GPLv2 License: https://github.com/phpbb/phpbb/blob/master/LICENSE

----

Tested with phpBB 3.3.3, Uberspace 7.9.0.0

.. author_list::
