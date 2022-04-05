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

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
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

At least you have to delete or rename the ``install.php``.

Tuning
======

For plugins, themes and other stuff go to DokuWiki_.

Nice URLs
=========

To use nice urls like ``https://isabell.uber.space/dokuwiki-on-uberspace`` instead of ``https://isabell.uber.space/doku.php?id=dokuwiki-on-uberspace`` you need to create a ``.htaccess`` file in the root directory of your dokuwiki installation. You can either copy the existing ``.htaccess.dist`` file and start editing it or paste the following configuration text into a new ``.htaccess`` file.

.. code-block:: ini

  ## You should disable Indexes and MultiViews either here or in the
  ## global config. Symlinks maybe needed for URL rewriting.
  ## +SymLinksIfOwnerMatch is an uberspace requirement as +FollowSymLinks does not work.
  Options -Indexes -MultiViews +SymLinksIfOwnerMatch
  
  ## make sure nobody gets the htaccess, README, COPYING or VERSION files
  <Files ~ "^([\._]ht|README$|VERSION$|COPYING$)">
      <IfModule mod_authz_core.c>
          Require all denied
      </IfModule>
      <IfModule !mod_authz_core.c>
          Order allow,deny
          Deny from all
      </IfModule>
  </Files>

  ## Don't allow access to git directories
  <IfModule alias_module>
      RedirectMatch 404 /\.git
  </IfModule>

  ## Uncomment these rules if you want to have nice URLs using
  ## $conf['userewrite'] = 1 - not needed for rewrite mode 2
  RewriteEngine on
  
  RewriteRule ^_media/(.*)              lib/exe/fetch.php?media=$1  [QSA,L]
  RewriteRule ^_detail/(.*)             lib/exe/detail.php?media=$1  [QSA,L]
  RewriteRule ^_export/([^/]+)/(.*)     doku.php?do=export_$1&id=$2  [QSA,L]
  RewriteRule ^$                        doku.php  [L]
  RewriteCond %{REQUEST_FILENAME}       !-f
  RewriteCond %{REQUEST_FILENAME}       !-d
  RewriteRule (.*)                      doku.php?id=$1  [QSA,L]
  RewriteRule ^index.php$               doku.php
  
  ## Not all installations will require the following line.  If you do,
  ## change "/dokuwiki" to the path to your dokuwiki directory relative
  ## to your document root.
  RewriteBase /
  

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


Your first plugin you have to install, is the upgrade_ plugin. With this plugin you can update directly from the admin interface.



.. _feed: http://feeds.feedburner.com/dokuwiki
.. _wiki: https://en.wikipedia.org/wiki/wiki
.. _DokuWiki: https://www.dokuwiki.org
.. _upgrade: https://www.dokuwiki.org/plugin:upgrade

----

Tested with DokuWiki 2020-07-29 "Hogfather", Uberspace 7.11.1.1, PHP 7.4

.. author_list::
