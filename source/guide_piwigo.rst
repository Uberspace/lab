.. highlight:: console

.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: gallery
.. tag:: photo

.. sidebar:: Logo

  .. image:: _static/images/piwigo.svg
      :align: center

######
Piwigo
######

.. tag_list::

Piwigo is an open source photo gallery. It allows you to create several galleries and share them with yourself, selected individuals or the world.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`

License
=======

Piwigo is released under the GNU General Public License_ version 2 or any later version.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

If you want to use your Piwigo with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst


.. include:: includes/my-print-defaults.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, download the latest release_ of Piwigo, extract it and remove the archive afterwards.

.. note:: Check the Piwigo_ website or `Github Repository`_ for the latest stable release and copy the download link to the piwigo-2.xx.x.zip file. Then use ``wget`` to download it. Use the latest release_ URL or replace the URL with the one you just got from GitHub.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://piwigo.org/download/dlcounter.php?code=latest -O piwigo.zip
 [isabell@stardust html]$ unzip piwigo.zip
 [isabell@stardust html]$ mv piwigo/* .
 [isabell@stardust html]$ rm piwigo.zip
 [isabell@stardust html]$

Configuration
=============

Create Database
---------------

Piwigo saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_piwigo``) instead of the default database.

.. note:: You need to create the database **before** you enter the database :manual_anchor:`credentials <database-mysql.html#login-credentials>` in the `Piwigo Installer`_.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_piwigo"
 [isabell@stardust ~]$


Piwigo Installer
-------------------

The final configuration can easily be done in the browser. Point your Browser to your installation URL ``https://isabell.uber.space/install.php``.

Enter the following details:

Basic configuration
^^^^^^^^^^^^^^^^^^^

  * ``Default gallery language`` select your desired default language

Database configuration
^^^^^^^^^^^^^^^^^^^^^^

  * ``Host`` use ``localhost``
  * ``User`` equals your Uberspace username, e.g. ``isabell``
  * ``Password`` - you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * ``Database name`` e.g. ``isabell_piwigo``
  * ``Database tables prefix`` e.g. ``piwigo_``

Administration configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * ``Username`` the name of your admin user, e.g. ``isabell``
  * ``Password`` chose a strong password for your user
  * ``Password confirm`` enter your password again
  * ``Email address`` your email address; will be publicly visible
  * ``Options``

    * uncheck the option ``Subscribe to Piwigo Announcements Newsletter`` if you don't want to get Emails from Piwigo
    * uncheck the option ``Send my connection settings by email``, as the email will contain your cleartext password for your user

After that, you are finished with the installation and can now add photos to your gallery.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

The easiest way to update Piwigo is to use the web updater provided in the admin section of the Web Interface: ``Tools > Updates``.

Backup
======

Backup the following directories:

  * ``~/html/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_piwigo | xz - > ~/isabell_piwigo.sql.xz

.. _Upgrade Manual: https://piwigo.org/doc/doku.php?id=user_documentation:learn:upgrade:upgrade_automatic
.. _release: https://piwigo.org/download/dlcounter.php?code=latest
.. _Piwigo: https://piwigo.org/get-piwigo
.. _feed: https://github.com/Piwigo/Piwigo/releases.atom
.. _GNU General Public License: https://github.com/Piwigo/Piwigo/blob/master/COPYING.txt
.. _Github Repository: https://github.com/Piwigo/Piwigo/releases

----

Tested with Piwigo 13.1.0, Uberspace 7.13, PHP 8.1

.. author_list::
