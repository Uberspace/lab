.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>, Andreas Fuchs <https://anfuchs.de/>, Amin Zoubaa <https://zoubaa.de>

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

We’re using :manual:`PHP <lang-php>` in the stable version 8.3.

::

 [isabell@stardust ~]$ uberspace tools version use php 8.3
 Selected PHP version 8.3
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

Generate your OpenPGP key using headless mode. Add a gpg_batch.conf.

::

 [isabell@stardust ~]$ nano gpg_batch.conf

Copy following content to ``gpg_batch.conf`` and replace ``YOUR_NAME``, ``YOUR_COMMENT`` and ``SERVER_KEY@EMAIL.TEST`` with your mail:

::

 %echo Generating a GPG key
 Key-Type: RSA
 Key-Length: 3072
 Key-Usage: sign
 Subkey-Type: RSA
 Subkey-Length: 3072
 Subkey-Usage: encrypt
 Name-Real: YOUR_NAME
 Name-Comment: YOUR_COMMENT
 Name-Email: SERVER_KEY@EMAIL.TEST
 Expire-Date: 0
 %commit
 %echo done

Save your fingerprint and replace ``SERVER_KEY@EMAIL.TEST`` with your email. ``gpg --batch --gen-key gpg_batch.conf`` will run for multiple minutes. Just wait until it's finished!

::

 [isabell@stardust ~]$ mkdir -p ~/passbolt/config
 [isabell@stardust ~]$ gpg --batch --gen-key gpg_batch.conf
 [isabell@stardust ~]$ gpg --list-keys --fingerprint
 [isabell@stardust ~]$ gpg --armor --export-secret-keys SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey_private.asc
 [isabell@stardust ~]$ gpg --armor --export SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey.asc
 [isabell@stardust ~]$

Install the dependencies:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ wget --output-document=composer.phar https://getcomposer.org/download/latest-2.x/composer.phar
 [isabell@stardust html]$ php -d allow_url_fopen=on composer.phar install --no-dev -n -o
 [isabell@stardust html]$ rm composer.phar
 [isabell@stardust html]$ cp config/passbolt.default.php config/passbolt.php
 [isabell@stardust html]$

Edit following settings in ``config/passbolt.php``:
 * ``fullBaseUrl`` : ``https://isabell.uber.space`` in ``App``
 * ``username``, ``password`` and ``database`` in ``Datasources.default``: :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * ``host`` : ``stardust.uberspace.de``, ``port`` : ``587``, ``tls`` : ``true``, ``username`` : ``isabell`` and ``password`` in ``EmailTransport.default``
 * ``from`` : ``['passbolt@isabell.uber.space' => 'Passbolt']`` in ``Email.default``
 * ``fingerprint`` in ``passbolt.gpg.serverKey``: Insert your gpg fingerprint without spaces (!)
 * ``public`` : ``/home/isabell/passbolt/config/serverkey.asc`` in ``passbolt.gpg.serverKey``
 * ``private`` : ``/home/isabell/passbolt/config/serverkey_private.asc`` in ``passbolt.gpg.serverKey``
 * optional add ``ssl.force`` : ``true`` in ``passbolt``

If you use an additional DocumentRoot for your Passbolt domain, make sure the
Passbolt rewrite rules contain ``RewriteBase /``. Otherwise Apache may run into
an internal redirect loop and return HTTP 500 errors.

Add ``RewriteBase /`` after ``RewriteEngine on`` in ``.htaccess``:

::

 <IfModule mod_rewrite.c>
     RewriteEngine on
     RewriteBase /
     RewriteRule    ^(\.well-known/.*)$ $1 [L]
     RewriteRule    ^$    webroot/    [L]
     RewriteRule    (.*) webroot/$1    [L]
 </IfModule>

Also add ``RewriteBase /`` after ``RewriteEngine On`` in ``webroot/.htaccess``:

::

 <IfModule mod_rewrite.c>
     RewriteEngine On
     RewriteBase /
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteRule ^ index.php [L]
 </IfModule>


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

Check Passbolt's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation. The update process varies between patch, minor or major update. Read Passbolt's `update from source documentation`_ before updating.

Before updating, check the current requirements. Passbolt 5 requires PHP 8.2 or
newer and Composer 2. On Uberspace, you can check and switch the selected PHP
version with:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.3'
 [isabell@stardust ~]$ uberspace tools version use php 8.3
 Selected PHP version 8.3
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Create backups before changing the installation:

::

 [isabell@stardust ~]$ mkdir -p ~/backups
 [isabell@stardust ~]$ mysqldump ${USER}_passbolt > ~/backups/passbolt-$(date +%F).sql
 [isabell@stardust ~]$ tar -czf ~/backups/passbolt-files-$(date +%F).tar.gz ~/html ~/passbolt/config
 [isabell@stardust ~]$

Run a healthcheck before the update:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ ./bin/cake passbolt healthcheck
 [isabell@stardust html]$

Fetch the latest release tags and switch to the release you want to install.
Replace ``vX.Y.Z`` with the current stable release tag:

::

 [isabell@stardust html]$ git fetch --tags origin
 [isabell@stardust html]$ git checkout tags/vX.Y.Z
 [isabell@stardust html]$

Update the PHP dependencies with Composer 2:

::

 [isabell@stardust html]$ wget --output-document=composer.phar https://getcomposer.org/download/latest-2.x/composer.phar
 [isabell@stardust html]$ php -d allow_url_fopen=on composer.phar install --no-dev -n -o
 [isabell@stardust html]$ rm composer.phar
 [isabell@stardust html]$

Run the database migrations and clear the cache:

::

 [isabell@stardust html]$ ./bin/cake passbolt migrate --backup
 [isabell@stardust html]$ ./bin/cake cache clear_all
 [isabell@stardust html]$

Compare your configuration with the new default configuration after major
updates, but do not overwrite your production configuration. It contains your
database, email and OpenPGP settings.

::

 [isabell@stardust html]$ diff -u config/passbolt.default.php config/passbolt.php | less
 [isabell@stardust html]$

Run the cleanup dry-run and the healthcheck afterwards:

::

 [isabell@stardust html]$ ./bin/cake passbolt cleanup --dry-run
 (...)
 No issue found, data looks squeaky clean!
 [isabell@stardust html]$ ./bin/cake passbolt healthcheck
 [isabell@stardust html]$

If the cleanup dry-run reports data integrity issues, make sure your backups are
available and re-run the cleanup without ``--dry-run`` as described in the
Passbolt update documentation.

On Uberspace, the healthcheck may report that the system clock is not
synchronized because users cannot manage the system NTP service themselves. If
the server time is wrong, contact the Uberspace support.


.. _Passbolt: https://www.passbolt.com/
.. _feed: https://github.com/passbolt/passbolt_api/releases.atom
.. _AGPL-3.0 license: https://opensource.org/licenses/agpl-3.0
.. _stable releases: https://github.com/passbolt/passbolt_api/releases
.. _update from source documentation: https://www.passbolt.com/docs/hosting/update/from-source/

----

Tested with Passbolt 5.11.0 and Uberspace 7.17.3

.. author_list::
