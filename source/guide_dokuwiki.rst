.. highlight:: console

.. spelling::
    superduper

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. tag:: lang-php
.. tag:: web
.. tag:: wiki

.. sidebar:: Logo

  .. image:: _static/images/dokuwiki-logo.png
      :align: center

##########
Dokuwiki
##########

.. tag_list::

DokuWiki_ is a simple to use and highly versatile Open Source wiki_ software that doesn't require a database. It is loved by users for its clean and readable syntax. The ease of maintenance, backup and integration makes it an administrator's favorite. Built in access controls and authentication connectors make DokuWiki especially useful in the enterprise context and the large number of plugins contributed by its vibrant community allow for a broad range of use cases beyond a traditional wiki.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`

License
=======

DokuWiki_ are released under the GNU General Public License (GPL).

All relevant legal information can be found here

  * http://www.gnu.org/licenses/gpl-faq.html
  * https://www.dokuwiki.org/start?id=faq:license

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download and configure DokuWiki_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz
 [isabell@stardust html]$ tar -xzvf dokuwiki-stable.tgz --strip-components=1
 [isabell@stardust html]$ rm dokuwiki-stable.tgz
 [isabell@stardust html]$ cd ~
 [isabell@stardust ~]$


Finishing installation
======================

Now point your Browser to your installation URL ``https://isabell.uber.space/install.php``.
Complete the form and follow the installation instructions.

You will need to enter the following information:

  * your wiki name: The name of your wiki.
  * ACL: It´s recommended that ACL is enable.
  * Superuser: The login name of the admin user.
  * Real Name: Your name, nickname or something else (don´t use superuser name!)
  * E-Mail: The e-mail address of the admin user.
  * Password: The superduper secure password of the admin user.
  * Initial ACL policy: Choose the type of your wiki.
  * Allow users to register themselves: your decision
  * Choose under which license your content will be published

Finally you have to delete the ``install.php``:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ rm install.php
 [isabell@stardust html]$


Tuning
======

For plugins, themes and other stuff go to DokuWiki_.


Nice URLs aka URL-Rewriting
---------------------------

To change default behaviour and rewrite ``https://isabell.uber.space/doku.php?id=dokuwiki-on-uberspace``  to ``https://isabell.uber.space/dokuwiki-on-uberspace`` you need to enable URL rewriting in /var/www/virtual/$USER/html/conf/local.php/ file by appending:

::

  $conf['userewrite'] = 1;
  $conf['useslash'] = 1;

This can also be done in Configuration Settings via Admin page.

Next step is to rename ``/var/www/virtual/$USER/html/.htaccess.dist`` to ``/var/www/virtual/$USER/html/.htaccess`` and edit that file. First uncomment:

::

  #RewriteEngine On

by deleting the # character at the beginning of the line and insert:

::

  RewriteBase /

between ``RewriteEngine On`` and first ``RewriteRule`` directive. Finally uncomment all of the following rewrite rules and save changes.

Before:

::

  ## Uncomment these rules if you want to have nice URLs using
  ## $conf['userewrite'] = 1 - not needed for rewrite mode 2
  #RewriteEngine on
  #
  #RewriteRule ^_media/(.*)              lib/exe/fetch.php?media=$1  [QSA,L]
  #RewriteRule ^_detail/(.*)             lib/exe/detail.php?media=$1  [QSA,L]
  #RewriteRule ^_export/([^/]+)/(.*)     doku.php?do=export_$1&id=$2  [QSA,L]
  #RewriteRule ^$                        doku.php  [L]
  #RewriteCond %{REQUEST_FILENAME}       !-f
  #RewriteCond %{REQUEST_FILENAME}       !-d
  #RewriteRule (.*)                      doku.php?id=$1  [QSA,L]
  #RewriteRule ^index.php$               doku.php
  #

After:

::

  ## Uncomment these rules if you want to have nice URLs using
  ## $conf['userewrite'] = 1 - not needed for rewrite mode 2
  RewriteEngine on
  #
  ## Change RewriteBase to the directory your dokuwiki installation points to
  RewriteBase /
  #
  RewriteRule ^_media/(.*)              lib/exe/fetch.php?media=$1  [QSA,L]
  RewriteRule ^_detail/(.*)             lib/exe/detail.php?media=$1  [QSA,L]
  RewriteRule ^_export/([^/]+)/(.*)     doku.php?do=export_$1&id=$2  [QSA,L]
  RewriteRule ^$                        doku.php  [L]
  RewriteCond %{REQUEST_FILENAME}       !-f
  RewriteCond %{REQUEST_FILENAME}       !-d
  RewriteRule (.*)                      doku.php?id=$1  [QSA,L]
  RewriteRule ^index.php$               doku.php
  #

If something goes wrong, you can set the two values to 0 and delete the ``.htaccess`` file.


Handling Special Characters
---------------------------

Special characters should be handled safe to avoid long or corrupt filenames. Edit ``/var/www/virtual/$USER/html/conf/local.php/`` by appending:

::

  $conf['fnencode'] = 'safe';


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


Your first plugin you have to install, is the upgrade_ plugin. With this plugin you can update directly from the admin interface.



.. _feed: http://feeds.feedburner.com/dokuwiki
.. _wiki: https://en.wikipedia.org/wiki/wiki
.. _DokuWiki: https://www.dokuwiki.org
.. _upgrade: https://www.dokuwiki.org/plugin:upgrade

----

Tested with DokuWiki 2022-07-31a "Igor", Uberspace 7.13, PHP 8.1

.. author_list::
