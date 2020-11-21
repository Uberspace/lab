
.. highlight:: console
.. author:: 927589452

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/partdb.png
      :align: center

#######
Part-DB
#######

.. tag_list::

Part-DB_ is a web-based database for managing electronic components and distributed under the GPL-2.0 License.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`cronjobs <daemons-cron>`
  * composer_

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of Part-DB and extract it:

.. note:: The link to the latest version can be found at the `release page <https://github.com/Part-DB/Part-DB/releases`_.

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ curl --location https://github.com/Part-DB/Part-DB/archive/master.tar.gz | tar -xzf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

To install all needed libraries you run `composer install`:

::

 [isabell@stardust html]$ composer install
 Installing dependencies from lock file (including require-dev)
 Verifying lock file contents can be installed on current platform.
 Package operations: 24 installs, 0 updates, 0 removals
   - Syncing golonka/bbcodeparser (dev-master a19daa7) into cache
   - Syncing tecnickcom/tcpdf (dev-master ca4f9b8) into cache
     0 [>---------------------------]    0 [>---------------------------]  - Installing psr/log (1.1.0): Extracting archive
   - Installing filp/whoops (2.4.1): Extracting archive
   - Installing geertw/ip-anonymizer (v1.1.0): Extracting archive
   - Installing golonka/bbcodeparser (dev-master a19daa7): Cloning a19daa7456 from cache
   - Installing ircmaxell/password-compat (v1.0.4): Extracting archive
   - Installing components/jquery (3.3.1): Extracting archive
   - Installing jquery-form/form (v4.2.2): Extracting archive
   - Installing kartik-v/bootstrap-fileinput (v4.5.3): Extracting archive
   - Installing symfony/polyfill-php72 (v1.11.0): Extracting archive
   - Installing symfony/polyfill-mbstring (v1.11.0): Extracting archive
   - Installing symfony/var-dumper (v4.3.2): Extracting archive
   - Installing maximebf/debugbar (v1.15.0): Extracting archive
   - Installing nnnick/chartjs (v2.7.3): Extracting archive
   - Installing psr/http-message (1.0.1): Extracting archive
   - Installing psr/container (1.0.0): Extracting archive
   - Installing pimple/pimple (v3.2.3): Extracting archive
   - Installing nikic/fast-route (v1.3.0): Extracting archive
   - Installing container-interop/container-interop (1.2.0): Extracting archive
   - Installing slim/slim (3.12.1): Extracting archive
   - Installing smarty-gettext/smarty-gettext (1.5.1): Extracting archive
   - Installing smarty/smarty (v3.1.33): Extracting archive
   - Installing snapappointments/bootstrap-select (v1.13.10): Extracting archive
   - Installing squizlabs/php_codesniffer (3.4.2): Extracting archive
   - Installing tecnickcom/tcpdf (dev-master ca4f9b8): Cloning ca4f9b86c9 from cache
   0/12 [>---------------------------]   0%
   8/12 [==================>---------]  66%
  10/12 [=======================>----]  83%
  11/12 [=========================>--]  91%
  12/12 [============================] 100%Generating autoload files
 [isabell@stardust html]$

You have to create the Part-DB Database before configuring Part-DB like described here :manual_anchor:`additional <database-mysql.html#additional-databases>`:
::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_partdb" && echo "Created database ${USER}_partdb"
 Created database isabell_partdb
 [isabell@stardust ~]$


Now point your browser to your uberspace URL and follow the instructions.

You will need to enter the following information:

  * an initial administrator password: Insert the credentials you want to use for the admin user while installing Part-DB
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Part-DB database name from the previous step

The installation wizard will prompt you to initialize the database and you will have to change the admin password afterwards.

Backup
======

To create a backup of the installation you need the `data` folder and the database.
To backup the `data` directory you copy it into your home:

::

 [isabell@stardust ~]$ cp --recursive ~/html/data ~/data
 [isabell@stardust ~]$

To create a backup of your database you dump it into a file:

::

 [isabell@stardust ~]$ mysqldump ${USER}_partdb > partdb_backup.sql
 [isabell@stardust ~]$

Restore
=======

You restore the database from the backup as follows:

::

 [isabell@stardust ~]$ mysql --database=${USER}_partdb < partdb_backup.sql
 [isabell@stardust ~]$

.. note::
   If you get an error like "ERROR 1049 (42000): Unknown database 'test_partdb'" you have to create the databse as described in the installation instructions.

The `data` directory can just be moved into the documentroot.


Updates
=======

To update Part-DB you create a backup as described above or move the `data` folder away before replacing the installation:

::

 [isabell@stardust ~]$ mv ~/html/data ~/
 [isabell@stardust ~]$

Create an backup of your database:

::

 [isabell@stardust ~]$ mysqldump ${USER}_partdb > partdb_update_backup.sql
 [isabell@stardust ~]$

Remove the old installation:

.. note::
   If the trailing `/` is missing from the command below, the folder will be deleted and you will need to restore it using `mkdir /var/www/virtual/${USER}/html`.

::

 [isabell@stardust ~]$ rm -rf /var/www/virtual/${USER}/html/
 [isabell@stardust ~]$

Follow the installation procedure and restore the data directory
::

 [isabell@stardust ~]$ mv ~/data ~/html/data
 [isabell@stardust ~]$

.. _Part-DB: https://github.com/Part-DB/Part-DB
.. _composer: https://getcomposer.org


----

Tested with Part-DB 0.5.9, Uberspace 7.7.10.0

.. author_list::

Sources:
    * :lab: guide_satis
    * :lab: guide_nextcloud
