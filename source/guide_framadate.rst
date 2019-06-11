

.. highlight:: console

.. author:: Marmo

.. categorize your guide! refer to the manual for the current list of tags: https://manual.uberspace.de/tags
.. tag:: lang-php
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/framadate.png
      :align: center

##########
Framadate
##########

.. tag_list::

Framadate is an online service for planning an appointment or making a decision quickly and easily.

This guide is based on `this guide <https://framacloud.org/en/cultivate-your-garden/framadate.html>`_ with some changes to make it work on Uberspace 7.

----

License
=======

Framadate is licensed under the `CeCILL-B License <http://www.cecill.info/>`_. The current license can always be found `here <https://framagit.org/framasoft/framadate/framadate/raw/develop/LICENSE.en.txt>`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

  [isabell@stardust ~]$ uberspace tools version show php
  Using 'PHP' version: '7.1'
  [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

  [isabell@stardust ~]$ my_print_defaults client
  --default-character-set=utf8mb4
  --user=isabell
  --password=MySuperSecretPassword
  [isabell@stardust ~]$

Your Framadate URL needs to be setup:

::

  [isabell@stardust ~]$ uberspace web domain list
  isabell.uber.space
  [isabell@stardust ~]$

Installation
============

Step 1
------

First download the files from the Framadate repository with Git into the folder ``~/html`` and switch to the `latest stable version <https://framagit.org/framasoft/framadate/framadate/tags>`_. Be sure to replace the version ``1.1.10`` with the current version.

::

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust ~]$ git clone https://framagit.org/framasoft/framadate/framadate.git .
  ...
  [isabell@stardust ~]$ git checkout 1.1.10
  ...
  [isabell@stardust ~]$

Step 2
------
Import the necessary libraries with composer:

::

  [isabell@stardust ~]$ composer install
  ...
  [isabell@stardust ~]$

Step 3
------

Create a database for Framadate:

::

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_framadate"
  [isabell@stardust ~]$

Configuration
=============

Configure Framadate
-------------------

Now that the database is ready, you have to configure Framadate to use it.

Go to the page ``https://domain.tld/admin/install.php`` and fill the form with the following string: ``mysql:host=localhost;dbname=<username>_framadate;port=3306``, your database user and your MariaDB-password.

.. warning:: Be sure to replace ``<username>`` with your username!

.. note:: If the page does not appear, check that a folder ``~/html/tpl_c`` has been created with sufficient write permissions.

Upon installation, the database tables and the file ``app/inc/config.php`` are created. The file ``app/inc/config.php`` contains parameters of optional configurations that you can modify.

You are then redirected to the "migration" page which is used to check that the tables and data are in the correct format. For future updates, you will have to go through this page after replacing the files.

Restrict access to Admin area
-----------------------------

Framadate has a management area for all polls in the folder ``admin``

To restrict access, add basic authentication for the admin site by creating ``~/html/admin/.htaccess`` with the following content:

.. warning:: Be sure to replace ``<username>`` with your username!

::

  AuthType Basic
  AuthName "Administration"
  AuthUserFile "/var/www/virtual/<username>/html/admin/.htpasswd"
  Require valid-user
  Order allow,deny
  Allow from all


and create the .htpasswd file containing the authorized user and password:

::

  [isabell@stardust ~]$ htpasswd -bc ~/html/framadate/admin/.htpasswd admin "MySuperSecretPassword"
  [isabell@stardust ~]$

As of writing this text, the ``.htaccess`` and ``.htpasswd`` files are protected from browser access by the default webserver configuration.

URL rewriting
-------------

To enable URL rewriting, to have links in the form ``https://domain.tld/a1b2c3d4e5f6g7h8`` instead of ``https://domain.tld/studs.php?sondage=a1b2c3d4e5f6g7h8`` rename the file ``~/html/framadate/htaccess.txt`` to ``~/html/framadate/.htaccess``:

::

  [isabell@stardust ~]$ mv ~/html/framadate/htaccess.txt ~/html/framadate/.htaccess
  [isabell@stardust ~]$

If you do not do this, you will not be able to access your polls, unless you set ``const URL_PROPRE = false;`` in ``~/html/app/inc/config.php``.

Mail
----
To allow Framadate to send Mails, enter your SMTP Server address/credentials in ``~/html/app/inc/config.php``:

.. code-block:: php

  'smtp_options' => [
          'host' => 'localhost',              // SMTP server (you could add many servers (main and backup for example) : use ";" like separator
          'auth' => false,                    // Enable SMTP authentication
          'username' => '',                   // SMTP username
          'password' => '',                   // SMTP password
          'secure' => '',                     // Enable encryption (false, tls or ssl)
          'port' => 25,                       // TCP port to connect to
      ],

If you do not want to use the mail features, set ``'use_smtp' => false,``.

Tested with Framadate 1.1.10, Uberspace 7.3.0.0

.. author_list::
