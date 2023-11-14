.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-php
.. tag:: web
.. tag:: password-manager

.. sidebar:: Logo

  .. image:: _static/images/passbolt.png
      :align: center

#########
Passbolt
#########

.. tag_list::

Passbolt_

The password manager your team was waiting for. Free, open source, self-hosted, extensible, OpenPGP based.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

Passbolt is released under the `AGPL-3.0 license`_.

Prerequisites
=============

Every Uberspace can choose their :manual:`PHP <lang-php>` version manually.
We need PHP version 8.1 or above to use Passbolt.

Check your current version with 
::

  [isabell@stardust ~]$ uberspace tools version show php
  Using 'PHP' version: '7.1'

If you use an older version, change your php version to the latest available version.
::

 [isabell@stardust ~]$ uberspace tools version list php
 - 8.0
 - 8.1
 - 8.2
 [isabell@stardust ~]$ uberspace tools version use php 8.2
 Selected PHP version 8.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Create the database:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_passbolt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
 [isabell@stardust ~]$


Create an email user:

::

 [isabell@stardust ~]$ uberspace mail user add passbolt
 Enter a password for the mailbox: (...)
 Please confirm your password: (...)
 New mailbox created for user: 'passbolt', it will be live in a few minutes...
 [isabell@stardust ~]$

Installation
============

To install Passbolt we clone the current version using Git. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will be under your ``html``.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ git clone https://github.com/passbolt/passbolt_api.git .
 Cloning into '.'...
 (...)
 [isabell@stardust ~]$

Configuration
=============

Generate an OpenPGP key:

.. warning:: Do not set a passphrase or an expiration date.

Save your fingerprint and replace ``SERVER_KEY@EMAIL.TEST`` with your email.

.. code-block:: console
 :emphasize-lines: 4,5

 [isabell@stardust ~]$ mkdir -p ~/passbolt/config
 [isabell@stardust ~]$ gpg --gen-key
 [isabell@stardust ~]$ gpg --list-keys --fingerprint
 [isabell@stardust ~]$ gpg --armor --export-secret-keys SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey_private.asc
 [isabell@stardust ~]$ gpg --armor --export SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey.asc
 [isabell@stardust ~]$

Install the dependencies:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ wget --output-document=composer.phar https://getcomposer.org/composer.phar
 [isabell@stardust html]$ php composer.phar install --no-dev
 [isabell@stardust html]$ rm composer.phar

Create the settings file ``config/passbolt.php``:
::
 [isabell@stardust html]$ touch config/passbolt.php
 [isabell@stardust html]$

Paste and edit following config in ``config/passbolt.php``:

.. code-block:: php

 <?php
 
 # Insert your gpg fingerprint without spaces (!)
 $GPG_FINGERPRINT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';
 # your uberspace name
 $UBERSPACE_USERNAME = 'isabell';
 # set the password from $ my_print_defaults client
 $DB_PASSWORD = 'password';
 # change if you use your own domain
 $APP_URL = "https://$UBERSPACE_USERNAME.uber.space";
 # set the password that you set for the email
 $EMAIL_PASSWORD = 'password';
 # set the username that you set for the email
 $EMAIL_USERNAME = "passbolt@$UBERSPACE_USERNAME.uber.space";

 $DB_NAME = "$UBERSPACE_USERNAME_passbolt";
 $DB_USERNAME = $UBERSPACE_USERNAME;
 
 return [
     'App' => [
         'fullBaseUrl' => $APP_URL,
     ],
     'Datasources' => [
         'default' => [
             'host' => 'localhost',
             'username' => $DB_USERNAME,
             'password' => $DB_PASSWORD,
             'database' => $DB_NAME,
         ],
     ],
     'EmailTransport' => [
         'default' => [
             'host' => 'localhost',
             'port' => 587,
             'username' => $EMAIL_USERNAME,
             'password' => $EMAIL_PASSWORD,
             'tls' => null,
         ],
     ],
     'Email' => [
         'default' => [
             'from' => [
                 $EMAIL_USERNAME => 'Passbolt'
             ],
         ],
     ],
     'passbolt' => [
         'ssl' => [
             'force' => true,
         ],
         'gpg' => [
             'serverKey' => [
                 'fingerprint' => $GPG_FINGERPRINT,
                 'public' => "/home/$UBERSPACE_USERNAME/passbolt/config/serverkey.asc",
                 'private' => "/home/$UBERSPACE_USERNAME/passbolt/config/serverkey_private.asc",
             ],
         ],
     ],
 ];
 
Update .htaccess files

There are two .htaccess files that needs to be modified to work.

1. ``/var/www/virtual/isabell/html/.htaccess`` to ->

.. code-block:: apache

 <IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
  RewriteBase /
  RewriteRule ^(\.well-known/.*)$ $1 [L]
  RewriteRule ^$    webroot/    [L]
  RewriteRule (.*) webroot/$1    [L]
  RewriteRule . /index.php [L]
 </IfModule>

2. ``/var/www/virtual/isabell/html/webroot/.htaccess`` to ->

.. code-block:: apache

 <IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
  RewriteBase /
  RewriteRule ^index\.php$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.php [L]
 </IfModule>


Installation
=============
Finish the installation and fill in your email and name when asked for:

::

 [isabell@stardust html]$ ./bin/cake passbolt install
 [isabell@stardust html]$ ./bin/cake passbolt healthcheck
 (...)
 No error found. Nice one sparky!
 [isabell@stardust html]$

Finally, configure a cronjob so mails get sent automatically: Add the following
line to your crontab using the ``crontab -e`` command:

::

 * * * * * /home/$USER/html/bin/cake EmailQueue.sender >> ~/logs/passbolt_mails.log

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Passbolt's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation. The update process varies between patch, minor or major update. You can easily follow the instructions in the Passbolt`s `update documentation`_.


.. _Passbolt: https://www.passbolt.com/
.. _feed: https://github.com/passbolt/passbolt_api/releases.atom
.. _AGPL-3.0 license: https://opensource.org/licenses/agpl-3.0
.. _stable releases: https://github.com/passbolt/passbolt_api/releases
.. _update documentation: https://help.passbolt.com/hosting/update

----

Tested with Passbolt 3.9.0 and Uberspace 7.15.6

.. author_list::
