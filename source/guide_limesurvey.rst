.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-php
.. tag:: web
.. tag:: survey

.. sidebar:: Logo

  .. image:: _static/images/limesurvey.png
      :align: center

##########
LimeSurvey
##########

.. tag_list::

LimeSurvey_ is a free and open source survey web application.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

LimeSurvey software is licenced under the GPLv2_.

Prerequisites
=============

We're using PHP in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

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
----------------

Visit LimeSurvey's `community downloads`_ page and copy the ``.zip`` download link. Then, ``cd`` to your DocumentRoot and use ``wget`` to download the file. Make sure to replace the dummy URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust html]$ wget -O limesurvey.zip https://download.limesurvey.org/latest-stable-release/limesurvey5.4.10+221107.zip
 [...]
 2022-11-09 12:39:03 (16,1 MB/s) - »limesurvey.zip« saved [84075454/84075454]
 [isabell@stardust html]$


Extract archive
---------------

::

 [isabell@stardust isabell]$ unzip limesurvey.zip
 […]
  inflating: limesurvey/upload/twig/extensions/HelloWorld_Twig_Extension/README.md
  inflating: limesurvey/upload/twig/extensions/README.md
 [isabell@stardust isabell]$

Remove old html directory and rename the extracted directory
------------------------------------------------------------

::

 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ mv limesurvey html
 [isabell@stardust isabell]$

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
 [isabell@stardust html]$ wget -O limesurvey.zip https://download.limesurvey.org/latest-master/limesurvey6.15.23+251110.zip
 [isabell@stardust html]$ unzip -o limesurvey.zip -x "application/config/config.php" -x "upload/*"


.. _LimeSurvey: https://www.limesurvey.org/
.. _feed: https://github.com/LimeSurvey/LimeSurvey/releases.atom
.. _GPLv2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
.. _community downloads: https://community.limesurvey.org/downloads/

----

Tested with LimeSurvey 6.15.23, Uberspace 7.16.9, and PHP 8.3

.. author_list::
