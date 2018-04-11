.. highlight:: console

########
Wallabag
########

Wallabag_ is a read later solution like `Firefox Pocket`_ to save and organize articles between devices and make them available offline. This is the server-side application, it will fetch articles and save the content and images on the server when a link is provided. There is also client software for browsers and mobile devices available which can be used to download and read the fetched articles and add new articles to the server.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * MySQL_
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Also, the domain you want to use for Lychee must be set up as well:

.. include:: includes/web-domain-list.rst

Installation & Configuration
==============================

First get the Wallabag source code from GitHub_:

::

  [isabell@stardust ~]$ git clone https://github.com/wallabag/wallabag.git ~/html
  Cloning into '/home/isabell/wallabag'...
  remote: Counting objects: 46655, done.
  remote: Compressing objects: 100% (23/23), done.
  remote: Total 46655 (delta 10), reused 20 (delta 9), pack-reused 46620
  Receiving objects: 100% (46655/46655), 58.15 MiB | 20.81 MiB/s, done.
  Resolving deltas: 100% (26623/26623), done.
  [isabell@stardust ~]$

Change to that folder and run ``make install``. During the installation process, you will be asked for a lot of configuration settings. But you only need to set up the following information:

* ``database_name:`` <username>_wallabag - *replace <username> with the MySQL username*
* ``database_user:`` put in the MySQL username that you looked up in the prerequisites
* ``database_password:`` that is the MySQL password that you looked up in the prerequisites
* ``mailer_host``: 127.0.0.1:587 - *we need to serve the special* |smtpport|_ *here*
* ``mailer_user``: <username>@uber.space - *replace <username> with your uberspace username*
* ``mailer_password``: <mail-password> - *you need to set a mail password for your uberspace first*
* ``domain_name:`` put in here your domain or subdomain like https://yourdomain
* ``secret:`` type in any random string here, do not keep the defaul string!
* ``twofactor_sender:`` choose an email address to be used as sender
* ``fosuser_registration:`` set this to false, otherwise anyone can register at your wallabag instance
* ``from_email:`` choose an email address to be used as sender (can be the same as above)

* ``Would you like to create a new admin user (recommended)?:`` yes
* ``Username:`` admin *- or you can also choose any other name, that could increase security*
* ``Password:`` *choose a good password here*
* ``Email:`` set in a mailadress to use with this admin account

.. code-block:: console
 :emphasize-lines: 1,2,10,11,12,17,23,25,26,28,30,31,32,33

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ make install
  [...]
  Creating the "app/config/parameters.yml" file
  Some parameters are missing. Please provide them.
  database_driver (pdo_mysql): 
  database_driver_class (null): 
  database_host (127.0.0.1): 
  database_port (null): 
  database_name (wallabag): isabell_wallabag
  database_user (root): isabell
  database_password (null): MySuperSecretPassword
  database_path (null): 
  database_table_prefix (wallabag_):  
  database_socket (null): 
  database_charset (utf8mb4):  
  domain_name ('https://your-wallabag-url-instance.com'): https://isabell.uber.space
  mailer_transport (smtp): 
  mailer_host (127.0.0.1): 127.0.0.1:587
  mailer_user (null): isabell@uber.space
  mailer_password (null): MySuperSecretPassword
  locale (en):  
  secret (ovmpmAWXRCabNlMgzlzFXDYmCFfzGv): *!!set.random.string!!*
  twofactor_auth (true):
  twofactor_sender (no-reply@wallabag.org): isabell@uber.space
  fosuser_registration (true): false
  fosuser_confirmation (true):
  from_email (no-reply@wallabag.org): isabell@uber.space
  [...]
  * Would you like to create a new admin user (recommended)? (yes/no) [yes]: yes
  * Username [wallabag]: admin
  * Password [wallabag]: [hidden] *!!choose.your.own!!*
  * Email []: isabell@uber.space
  [...]
  Config successfully setup.
  [OK] Wallabag has been successfully installed.
  [OK] You can now configure your web server, see https://doc.wallabag.org
  [isabell@stardust html]$

.. note:: You just need to set the highlighted values (as explained above), for the others just accept the default values with *enter*. You can change all the settings afterwards inside the ``~/html/app/config/parameters.yml``

You still need to forward your document root to the ``/web`` folder where the public content is located. Therefore create a ``.htaccess`` file inside the ``~/html`` folder with the following content:

::

  RewriteEngine On
  RewriteBase /
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteRule ^(.*)$ /web/$1 [QSA,L]

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version available, you can get the code using git:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ git pull origin master
  From https://github.com/wallabag/wallabag
   * branch              master     -> FETCH_HEAD
  Already up to date.
  [isabell@stardust html]$


.. _Wallabag: https://wallabag.org
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _GitHub: https://github.com/wallabag/wallabag
.. _feed: https://github.com/wallabag/wallabag/releases.atom
.. _Firefox Pocket: https://support.mozilla.org/en-US/kb/save-web-pages-later-pocket-firefox
.. _smtpport: https://manual.uberspace.de/en/mail-access.html#smtp
.. |smtpport| replace:: *smtp port*

----

Tested with Wallabag 2.3.2 and Uberspace 7.1.2
