.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/nextcloud.png 
      :align: center

#########
Nextcloud
#########

Nextcloud_ is an open source cloud solution written in PHP and distributed unter the AGPLv3 licence.

Nextcloud was initially released in 2016 as a fork of ownCloud_ and is maintained by Nextcloud GmbH.

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
 [isabell@stardust html]$ curl https://download.nextcloud.com/server/releases/latest.tar.bz2 | tar -xjf - --strip-components=1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust html]$

Now point your browser to your uberspace URL and follow the instructions.

You will need to enter the following information:
  
  * Administrator username and password: Insert the credentials you want to use for the admin user
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Nextcloud database name: we suggest you use an additional_ database. For example: isabell_nextcloud

Tuning
======

cronjob
-------

For better performance, Nextcloud suggests to add a local cronjob.

Add the following cronjob to your crontab_:

::

 *  *  *  *  * php -f $HOME/html/cron.php

Memcaching
----------

To further enhance perfomance, enable Memcaching.

To enable Memcaching (APCu), add the following line to your /var/www/virtual/$USER/html/config/config.php:

.. code-block:: console
 :emphasize-lines: 5

 [...]
    'dbuser' => 'isabell',
    'dbpassword' => 'eeCae1ahx6angai',
    'installed' => true,
    'memcache.local' => '\OC\Memcache\APCu',
  );

opcache
-------

Enable opcache to further optimise perfomance.

To do that, add the following lines to $HOME/etc/php.d/opcache.ini

::

 opcache.enable=1
 opcache.enable_cli=1
 opcache.interned_strings_buffer=8
 opcache.max_accelerated_files=10000
 opcache.memory_consumption=128
 opcache.save_comments=1
 opcache.revalidate_freq=1

After that you need to reload your PHP configuration:

::

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$

HSTS
----

NextCloud will complain about your HSTS settings in the admin interface.

At the moment it is not possible to change the HSTS settings, as mentioned in the `manual <https://manual.uberspace.de/en/web-security.html>`_.

Updates
=======

The easiest way to update Nextcloud is to use the web updater provided in the admin section of the Web Interface.

.. note:: Check the `changelog <https://nextcloud.com/changelog/>`_ regularly to stay informed about new updates and releases.


.. _ownCloud: https://owncloud.org
.. _Nextcloud: https://nextcloud.com
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _cronjobs: https://manual.uberspace.de/en/daemons-cron.html
.. _crontab: https://manual.uberspace.de/en/daemons-cron.html


----

Tested with Nextcloud 13.0.1, Uberspace 7.1.3
