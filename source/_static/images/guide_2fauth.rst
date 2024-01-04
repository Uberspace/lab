.. author:: godmod <godmod@godmod.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: authentication

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/2fauth.png
      :align: center

######
2FAuth
######

.. tag_list::


`2FAuth`_ is a web based self-hosted alternative to One Time Passcode (OTP) generators like Google Authenticator, designed for both mobile and desktop and published under AGPLv3.
If you want to try out 2FAuth without installing it first, visit the `demo-page`_.
A general Installation guide can be found on `Github`_.


----

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Clone 2FAuth code from GitHub, switch to the latest release and install necessary dependencies with composer.

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/
  [isabell@stardust isabell]$ git clone https://github.com/bubka/2fauth.git
  [isabell@stardust isabell]$ cd 2fauth/
  [isabell@stardust 2fauth]$ curl https://api.github.com/repos/Bubka/2FAuth/releases/latest | grep "\"name\"" | grep -Eo 'v[^\"]*' | xargs git checkout
  [isabell@stardust 2fauth]$ composer install --prefer-dist --no-scripts --no-dev
  [isabell@stardust 2fauth]$  

Remove your empty DocumentRoot and link 2FAuth's public folder instead:

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/
  [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
  [isabell@stardust isabell]$ ln -s 2fauth/public html
  [isabell@stardust isabell]$


Configuration
=============

2FAuth saves your data in a MySQL database. We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>`. You need to create this database before you enter the database credentials in the installer.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_2fauth"
 [isabell@stardust ~]$

Now you can start the installation wizard in the 2FAuth installation directory

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/2fauth/
  [isabell@stardust 2fauth]$ php artisan 2fauth:install
  [isabell@stardust 2fauth]$

You will need to enter the following information:

* URL of this 2FAuth instance: your URL including HTTPS protocol, e.g. https://isabell.uber.space
* Type of database: mysql
* Database host: leave empty and just press Enter key
* Database port: leave empty and just press Enter key
* Database name: <username>_2fauth
* Database user: <username>
* Database password: <SQL-Password from above>

The installation wizard will now fill the database with data and present a success message, if the installation was successful.

Now point your browser to your uberspace URL and register a new user at the 2FAuth application. The very first account created is automatically set as an administrator account.


Updates
=======

.. note:: Check the changelog_ regularly to stay informed about the newest changes.

For updating, follow the instructions as described in sections "Installation" and "Configuration", expect the creation of a new MySQL database (it already exists).

.. _`demo-page`: https://demo.2fauth.app/
.. _`2FAuth`: https://docs.2fauth.app/
.. _Github: https://github.com/Bubka/2FAuth
.. _changelog: https://github.com/Bubka/2FAuth/releases

----

Backup
======

Backup the following directories:

  * ``/var/www/virtual/<username>/2fauth/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump ${USER}_2fauth | xz - > ~/${USER}_2fauth.sql.xz

Tested with 2FAuth v4.2.4 and Uberspace v7.15, and PHP 8.1

.. author_list::
