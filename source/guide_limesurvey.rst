.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. sidebar:: Logo

  .. image:: _static/images/limesurvey.png
      :align: center

##########
LimeSurvey
##########

LimeSurvey_ is a free and open source survey web application.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * MySQL_
  * domains_

License
=======

LimeSurvey software is licenced under the GPLv2_.

Prerequisites
=============

We're using PHP in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

You'll need your MySQL credentials_. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your survey URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Download archive
------

Visit LimeSurvey's `stable release`_ page and copy the ``.tar.gz`` download link. Then, ``cd`` to your DocumentRoot and use ``wget`` to download the file. Make sure to replace the dummy URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2
 
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget -O limesurvey.tar.gz https://www.limesurvey.org/stable-release?download=4711:limesurvey4711%20180926targz
 [...]
 2018-10-02 16:01:50 (10.0 MB/s) - ‘stable-release?download=4711:limesurvey4711%20180926targz’ saved [72359513/72359513]
 [isabell@stardust html]$ 


Extract archive
------

::

 [isabell@stardust html]$ tar -xzf limesurvey.tar.gz --strip-components=1
 [isabell@stardust html]$ 

Configuration
=============

Point your browser to your domain (e.g. ``https://isabell.uber.space``) and use the installer to set up your database and admin user account.

We recommend to use a new database such as ``isabell_limesurvey`` for LimeSurvey.

Edit .htaccess
---------------

The default ``.htaccess`` includes a RewriteCond so that existing directories won't be rewritten, but for some reason it is commented out:

.. code-block:: apacheconf
 
     #RewriteCond %{REQUEST_FILENAME} !-d



Edit the ``.htaccess`` file and uncomment the line above, so the full ``.htaccess`` file should look like this:

.. code-block:: apacheconf
 
 <IfModule mod_rewrite.c>
     RewriteEngine on
 
     # if a directory or a file exists, use it directly
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteCond %{REQUEST_FILENAME} !-d
 
     # otherwise forward it to index.php
     RewriteRule . index.php
 
     # deny access to hidden files and directories except .well-known
     RewriteCond %{REQUEST_URI} !^/\.well-known
     RewriteRule ^(.*/)?\.+ - [F]
 </IfModule>
 
 # deny access to hidden files and directories without mod_rewrite
 RedirectMatch 403 ^/(?!\.well-known/)(.*/)?\.+
 
 # General setting to properly handle LimeSurvey paths
 # AcceptPathInfo on

Best practices
==============

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

When a new version is released, copy the download link and download it as above, but exclude ``/application/config/config.php`` and ``/upload/*`` when extracting the archive.

.. code-block:: console
 :emphasize-lines: 2
 
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget -O limesurvey.tar.gz https://www.limesurvey.org/stable-release?download=4711:limesurvey4711%20180926targz
 [isabell@stardust html]$ tar -xzf limesurvey.tar.gz --strip-components=1 --overwrite  --exclude '/application/config/config.php' --exclude '/upload/*'
 [isabell@stardust html]$ 


.. _LimeSurvey: https://www.limesurvey.org/
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/LimeSurvey/LimeSurvey/releases.atom
.. _GPLv2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
.. _stable release: https://www.limesurvey.org/en/downloads/category/25-latest-stable-release

----

Tested with LimeSurvey 3.14.11+180926, Uberspace 7.1.13.0

.. authors::

