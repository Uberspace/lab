.. author:: André Jaenisch <https://jaenis.ch>
.. author:: Tobias Quathamer <t.quathamer@mailbox.org>
.. author:: Raphael Fetzer

.. tag:: lang-php
.. tag:: web
.. tag:: fediverse
.. tag:: podcast
.. tag:: ActivityPub

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/castopod.svg
      :align: center

########
Castopod
########

.. tag_list::

Castopod_ is a free and open-source podcast hosting platform.

It forms one part of the Fediverse, an interconnected and
decentralized network of independently operated servers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>` and its package manager :manual_anchor:`composer <lang-php#package-manager>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`Mail <mail-mailboxes>`
  * :manual:`Cron <daemons-cron>`
  * :manual:`Domains <web-domains>`

License
=======

Castopod_ is released under the `GNU Affero General Public License v3.0`_.
All relevant information can be found in the LICENSE.md_ file in the
repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

  [isabell@stardust ~]$ uberspace tools version show php
  Using 'PHP' version: '8.1'
  [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for Castopod:

::

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_castopod"
  [isabell@stardust ~]$

Your castopod URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note::
  Castopod should be installed in a domain of its own (or in a subdomain),
  not in a subdirectory of a domain.

Installation
============

Change to the parent directory of your DocumentRoot and
download the latest version of castopod. At the time of writing, this
is v1.5.2. You'll find all releases_ on their gitlab instance.
Please note that you need to download the "Castopod Package",
not just the source code. The latter is missing some needed
files.

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ wget https://code.castopod.org/adaures/castopod/uploads/55eedf951df971df8e18438a80cb048e/castopod-1.5.2.tar.gz
  [isabell@stardust isabell]$

Unpack and symlink
------------------

Unpack the tarball and remove the downloaded file.

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ tar --extract --auto-compress --file castopod-1.5.2.tar.gz
  [isabell@stardust isabell]$ rm castopod-1.5.2.tar.gz
  [isabell@stardust isabell]$

Remove your empty DocumentRoot and create a symlink to the public
directory of castopod.

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ rm html/nocontent.html; rmdir html
  [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/castopod/public html
  [isabell@stardust isabell]$

Configuration
=============

Create a copy of the file :file:`.env.example` and use :file:`.env` as the new name.

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/castopod
  [isabell@stardust castopod]$ cp .env.example .env
  [isabell@stardust castopod]$

Open the file :file:`.env` in an editor and change the default settings
in the following lines to use your settings.

.. code-block::
  :emphasize-lines: 4,5,13-15,21-24

  #--------------------------------------------------------------------
  # Instance configuration
  #--------------------------------------------------------------------
  app.baseURL="https://isabell.uber.space/"
  media.baseURL="https://isabell.uber.space/"
  admin.gateway="cp-admin"
  auth.gateway="cp-auth"

  #--------------------------------------------------------------------
  # Database configuration
  #--------------------------------------------------------------------
  database.default.hostname="localhost"
  database.default.database="isabell_castopod"
  database.default.username="isabell"
  database.default.password="MySuperSecretPassword"
  database.default.DBPrefix="cp_"

  #--------------------------------------------------------------------
  # Email configuration
  #--------------------------------------------------------------------
  email.fromEmail="isabell@uber.space"
  email.SMTPHost="stardust.uberspace.de"
  email.SMTPUser="isabell@uber.space"
  email.SMTPPass="SuperSecretMailPassword"

Update .htaccess
----------------

Open the file :file:`.htaccess` in the directory :file:`/var/www/virtual/$USER/html`.
The instruction "All" is not supported on Uberspace, so prepend
the line with a hash ("#") to disable it.
Also, the unsupported instruction "FollowSymlinks" has to be replaced
with "SymLinksIfOwnerMatch".
Note: If the installation is done in a subdomain, the ``RewriteBase /`` must be commented out, too.

.. code-block:: none
  :emphasize-lines: 2,11

  # Disable directory browsing
  # Options All -Indexes

  # ----------------------------------------------------------------------
  # Rewrite engine
  # ----------------------------------------------------------------------

  # Turning on the rewrite engine is necessary for the following rules and features.
  # FollowSymLinks must be enabled for this to work.
  <IfModule mod_rewrite.c>
          Options +SymLinksIfOwnerMatch
          RewriteEngine On

Finishing installation
======================

Point your browser to your uberspace URL to finish the setup:
https://isabell.uber.space/cp-install

Most settings should not need changing, as they are taken from
the :file:`.env` file. However, you have to create an admin user.

Cron jobs
---------

Now set up some cron jobs for various background processes.
Depending on your needs, the frequency of these cron jobs can be
adjusted. For a small personal site, it's probably enough to
run them once per hour – or even daily or weekly.

Use :command:`crontab -e` to edit your cronjobs.

::

  0 * * * * php /var/www/virtual/$USER/castopod/spark tasks:run > /dev/null 2>&1

Redis
-----

Optionally, you can enable :lab:`Redis <guide_redis>` for better
cache performance. If you do, edit the file :file:`.env` in
:file:`/var/www/virtual/$USER/castopod` to use the Redis cache system.

Updates
=======

If there is a new release available, move the file :file:`/var/www/virtual/$USER/castopod/.env`
and the directory :file:`/var/www/virtual/$USER/castopod/public/media` outside
the directory :file:`/var/www/virtual/$USER/castopod`.
Then delete all other files there. Follow the installation
instructions from above. Move the files back to their
original place.

Sometimes there are additional update instructions you
have to follow. For example, .sql files containing migrations.

If you picked Redis as caching mechanism, clear the cache.

Enjoy your new version!

.. note:: Check the releases_ regularly to stay informed about the newest version.


.. _Castopod: https://castopod.org/
.. _GNU Affero General Public License v3.0: https://www.gnu.org/licenses/agpl-3.0.en.html
.. _LICENSE.md: https://code.castopod.org/adaures/castopod/-/blob/develop/LICENSE.md
.. _releases: https://code.castopod.org/adaures/castopod/-/releases

Backup
======

This is a list of files you need to restore your
castopod installation:

- A dump of the database
- Configuration file: :file:`/var/www/virtual/$USER/castopod/.env`
- Contents of the directory :file:`/var/www/virtual/$USER/castopod/public/media`

----

Tested with Castopod v1.5.2, Uberspace 7.15.4

.. author_list::
