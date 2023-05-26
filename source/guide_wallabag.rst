.. author:: ezra <ezra@posteo.de> FM <git.fm@mmw9.de>

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
==============================

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
* ``mailer_user:`` <username>@uber.space - *replace <username> with your uberspace username*.
* ``mailer_password:`` <mail-password> - *you need to set a mail password for your uberspace first*.
* ``mailer_port:`` 587 - *we need to serve the special* :manual_anchor:`smtp port <mail-access.html#smtp>` *here*.
* ``mailer_encryption:`` ssl - The parameter for the encryption.
* ``mailer_auth_mode:`` login - The authenication mode.
* ``secret:`` Type in any random string here, minimum 32 characters and do not keep the default string!
* ``twofactor_sender:`` Choose an email address to be used as sender.
* ``fosuser_registration:`` false - Set this to false, otherwise anyone can register at your wallabag instance
* ``from_email:`` Choose an email address to be used as sender (can be the same as above).

.. code-block:: console
  :emphasize-lines: 6,7,8,13,14,16,17,19,20,21,23,25,26,30
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
    mailer_transport: smtp
    mailer_user: isabell@uber.space
    mailer_password: 'MySuperSecretPassword'
    mailer_host: 127.0.0.1
    mailer_port: 587
    mailer_encryption: ssl
    mailer_auth_mode: login
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

.. note:: You can change all the settings afterwards inside the ``~/html/app/config/parameters.yml`` file. In case of changes please clear the cache afterwards with:
::

 [isabell@stardust ~]$ php bin/console cache:clear --env=prod
 [isabell@stardust ~]$

3. Jump into the ``~/html`` folder and let start the installation.

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

I had not the pleasure to update Wallabag till today. I will update this manual if a new version is available.

.. _Wallabag: https://wallabag.org
.. _Project: https://github.com/wallabag/wallabag
.. _feed: https://github.com/wallabag/wallabag/releases.atom
.. _Firefox Pocket: https://support.mozilla.org/en-US/kb/save-web-pages-later-pocket-firefox

----

Tested with Wallabag 2.5.4 and Uberspace 7.15.1

.. author_list::
