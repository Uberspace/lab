.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/phpservermonitor.png
      :align: center

##################
PHP Server Monitor
##################

.. tag_list::

PHP Server Monitor_ is an open source tool to monitor your servers and websites.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2. Since new Uberspaces are currently setup with PHP 7.1 by default you need to set this version manually:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install PHP Server Monitor we download the current version from the github release. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the zip file will be under your ``html``.

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/phpservermon/phpservermon/releases/download/v3.4.5/phpservermon-3.4.5.zip
 [isabell@stardust html]$ unzip phpservermon-3.4.5.zip
 [isabell@stardust html]$ rm phpservermon-3.4.5.zip
 [isabell@stardust html]$ mv phpservermon-3.4.5/* phpservermon-3.4.5/.* ./
 [isabell@stardust html]$ rmdir phpservermon-3.4.5
 [isabell@stardust html]$ 

Configuration
=============

Create the database, copy the configuration template and edit the ``config.php`` file with your SQL credentials.

 [isabell@stardust html]$ mysql -e "CREATE DATABASE ${USER}_psm"
 [isabell@stardust html]$ cp config.php.sample config.php
 [isabell@stardust html]$

After the installation you need to open isabell.uber.space in your browser to finish your setup.

Fill out your system settings, admin user and edit the following database settings:
 * PSM_DB_USER: ``isabell``
 * PSM_DB_PASS from your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * PSM_DB_NAME: ``isabell_psm``

::

Finally, configure a cronjob: Add the following line to your crontab using the crontab -e command:

* * * * * /usr/bin/php /var/www/virtual/isabell/html/cron/status.cron.php

Updates
=======

Check PHP Server Monitor's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation.

Backup your ``config.php`` file, delete everything else in your ``html`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp config.php ~
 [isabell@stardust html]$ rm -rf * .*

Proceed with the installation steps from here and move back your config file.

 [isabell@stardust html]$ mv ~/config.php ./
 [isabell@stardust html]$

Finish the update by open isabell.uber.space in your browser.

.. _PHP Server Monitor: http://www.phpservermonitor.org/
.. _stable releases: https://github.com/phpservermon/phpservermon/releases

----

Tested with PHP Server Monitor v3.4.5 and Uberspace 7.4

.. author_list::
