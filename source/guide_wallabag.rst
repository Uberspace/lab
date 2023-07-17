.. author:: ezra <ezra@posteo.de>
.. author:: FM <git.fm@mmw9.de>

.. tag:: lang-php
.. tag:: web
.. tag:: reading-list

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/wallabag.png
      :align: center

########
Wallabag
########

.. tag_list::

Wallabag_ is a read later solution like `Firefox Pocket`_ to save and organize articles between devices and make them available offline. This is the server-side application, it will fetch articles and save the content and images on the server when a link is provided. There is also client software for browsers and mobile devices available which can be used to download and read the fetched articles and add new articles to the server.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.0:

::

  [isabell@stardust ~]$ uberspace tools version show php
  Using 'PHP' version: '8.0'
  [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Also, the domain you want to use for Wallabag must be set up as well:

.. include:: includes/web-domain-list.rst

Remove the placeholder html file from the html folder:

::

  [isabell@stardust ~]$ rm ~/html/nocontent.html
  [isabell@stardust ~]$

Installation & Configuration
============================

1. First get the Wallabag package and let extract this into the target folder ``~/html``:

::

  [isabell@stardust ~]$ wget https://wllbg.org/latest-v2-package && tar xvf latest-v2-package -C ~/html --strip-components=1
  [isabell@stardust ~]$

2. Edit the config file ``~/html/app/config/parameters.yml`` and replace the following information:

* ``database_name:`` <username>_wallabag - *replace <username> with your MySQL username from your credentials above.*
* ``database_user:`` Again your MySQL username.
* ``database_password:`` The MySQL password from your credentials above.
* ``domain_name:`` Put in here your domain or subdomain like https://isabell.uber.space .
* ``server_name:`` Your wallabag instance name.
* ``mailer_dsn:`` Mail authorization to send out mails. Replace the placeholders (user, password, hostname and port) with your information. A good reference is the Uberspace :manual_anchor:`manual <mail-access.html#smtp>`.
* ``secret:`` Type in any random string here, minimum 32 characters and do not keep the default string!
* ``twofactor_sender:`` Choose an email address to be used as sender.
* ``fosuser_registration:`` false - Set this to false, otherwise anyone can register at your wallabag instance
* ``from_email:`` Choose an email address to be used as sender (can be the same as above).

.. code-block:: console
  :emphasize-lines: 6,7,8,13,14,15,17,19,20,24

  # This file is auto-generated during the composer install
  parameters:
    database_driver: pdo_mysql
    database_host: 127.0.0.1
    database_port: null
    database_name: isabell_wallabag
    database_user: isabell
    database_password: 'MySuperSecretPassword'
    database_path: null
    database_table_prefix: wallabag_
    database_socket: null
    database_charset: utf8mb4
    domain_name: 'https://isabell.uber.space'
    server_name: 'Your wallabag instance'
    mailer_dns: smtp://user:password@hostname:port
    locale: en
    secret: CHANGE_ME_TO_SOMETHING_SECRET_AND_RANDOM
    twofactor_auth: true
    twofactor_sender: isabell@uber.space
    fosuser_registration: false
    fosuser_confirmation: true
    fos_oauth_server_access_token_lifetime: 3600
    fos_oauth_server_refresh_token_lifetime: 1209600
    from_email: isabell@uber.space
    rss_limit: 50 rabbitmq_host: localhost
    rabbitmq_port: 5672
    rabbitmq_user: guest
    rabbitmq_password: guest
    rabbitmq_prefetch_count: 10
    redis_scheme: tcp
    redis_host: localhost
    redis_port: 6379
    redis_path: null
    redis_password: null
    sentry_dsn: null

.. note:: You can change all the settings afterwards inside the ``~/html/app/config/parameters.yml`` file. In case of changes please clear the cache with:

::

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust ~]$ php bin/console cache:clear --env=prod
  [isabell@stardust ~]$

3. Start the installation.

::

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust ~]$ php bin/console wallabag:install --env=prod
  [isabell@stardust ~]$

.. note:: In case of problems, please check your config file and clear the cache afterwards.

.. note:: During the installation process you will asking for a new admin username.

4. You still need to forward your document root to the ``/web`` folder where the public content is located.

Therefore create a ``.htaccess`` file inside the ``~/html`` folder with the following content:

::

  RewriteEngine On
  RewriteBase /
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteRule ^(.*)$ /web/$1 [QSA,L]

Updates
=======

The update process is quiet tricky due to the fact there is no update script for shared hosts available. Everthing is to maintain manually.

Plus the update steps could be different from version to version. Sometimes some database changes "and" file updates are necessary, or only file and configuration updates.

.. note:: It is highly recommended to read the Wallabag `upgrade information`_ to consider all necessary changes. And to backup all files before you change anything.

The following is more a common approach to have a general guide line:

1. Backup (move) your existing Wallabag installation.

::

  [isabell@stardust ~]$ mkdir -p ~/wb_backup/wallabag_old/
  [isabell@stardust ~]$

Move all files and directories as backup because only to overwrite an existing installation with a new package will serve problems.

::

  [isabell@stardust ~]$ mv ~/html/* ~/wb_backup/wallabag_old/
  [isabell@stardust ~]$

2. Download the actual package and ectract it to the target directory.

::

  [isabell@stardust ~]$ cd ~/wb_backup/
  [isabell@stardust ~]$ wget https://wllbg.org/latest-v2-package && tar xvf latest-v2-package -C ~/html --strip-components=1
  [isabell@stardust ~]$

3. Backup the new reference config file.

::

  [isabell@stardust ~]$ cp ~/html/app/config/parameters.yml ~/wb_backup/parameters.yml.reference
  [isabell@stardust ~]$

4. Copy your existing config and .htaccess file to the new installation.

::

  [isabell@stardust ~]$ cp ~/wb_backup/wallabag_old/app/config/parameters.yml ~/html/app/config/
  [isabell@stardust ~]$

::

  [isabell@stardust ~]$ cp ~/wb_backup/wallabag_old/.htaccess ~/html/
  [isabell@stardust ~]$


The Wallabag `upgrade information`_ is your first source to get information about possible changes. The reference config file usually shows possible changes as example.

Please consider possible changes in your config file and clear the cache.

::

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust ~]$ php bin/console cache:clear --env=prod
  [isabell@stardust ~]$

6. Database upgrade.

The Wallabag `upgrade information`_ shows also possible hints for a database update.

A good help is the :manual_anchor:`webinterface <database-mysql.html#webinterface>` to consider:

a) A database backup.
b) A console to place SQL statements from the Wallabag upgrade information.

7. Start the upgrade.

.. note:: Please answer the questions on all database topics with no, otherwise you will lose your data. It is also not necessary to create an admin account.

::

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust ~]$ php bin/console wallabag:install --env=prod
  [isabell@stardust ~]$

7. Cleanup.

The wb_backup directory is used to place copies of important files. You can delete this directory but it is recommended to keep it as an information source.

8. Start.

Your Wallabag instance should be available again.

.. _Wallabag: https://wallabag.org
.. _Project: https://github.com/wallabag/wallabag
.. _feed: https://github.com/wallabag/wallabag/releases.atom
.. _Firefox Pocket: https://support.mozilla.org/en-US/kb/save-web-pages-later-pocket-firefox
.. _upgrade information: https://doc.wallabag.org/en/admin/upgrade.html

----

Tested with Wallabag 2.6.1 and Uberspace 7.15.3

.. author_list::
