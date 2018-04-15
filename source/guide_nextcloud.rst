.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/nextcloud.png 
      :align: center

#########
Nextcloud
#########

Nextcloud_ is an open source cloud solution written in PHP and distributed unter the AGPLv3 licence.

Nextcloud was initially released in 2016 as a fork of ownCloud_ and is maintained by the Nextcloud GmbH.

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * PHP_
  * MySQL_ 
  * domains_
  * cronjobs_

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use your cloud with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your `document root`_, then download the latest release of the Nextcloud and extract it:

.. note:: The link to the lastest version can be found at Nextcloud's `download page <https://nextcloud.com/install/#instructions-server>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ curl https://download.nextcloud.com/server/releases/nextcloud-42.23.1.tar.bz2 | tar -xjf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

Now point your browser to your uberspace URL and follow the instructions.

You will need to enter the following information:
  
  * admin username and password, here you can insert the credentials you want to use for the admin user

If you want to use MySQL insert of SQLite you also need:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Nextcloud database name: we suggest you use an additional_ database. For example: isabell_nextcloud

Tuning
======

cronjob
-------

To get a better performance Nextcloud suggests to add a local cronjob.

Add the following cronjob to your crontab_:

.. warning:: Replace ``<username>`` with your username!

::

 *  *  *  *  * /usr/bin/php -f /var/www/virtual/<username>/html/cron.php

Memcaching
----------

Another thing you can configure to get a better performance is enabling Memcaching.

To enable Memcaching (APCu) you only need to add the following line to your /var/www/virtual/$USER/html/config/config.php:

::

 'memcache.local' => '\OC\Memcache\APCu',


Updates
=======

The easiest way to update Nextcloud is to use the web updater provided in the admin section of the Web Interface.

.. note:: Check the `changelog <https://nextcloud.com/changelog/>`_ regularly to stay informed about new updates and releases.


.. _ownCloud: https://owncloud.org
.. _Nextcloud: https://nextcloud.com
.. _PHP: http://www.php.net/
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _cronjobs: https://manual.uberspace.de/en/daemons-cron.html
.. _crontab: https://manual.uberspace.de/en/daemons-cron.html
