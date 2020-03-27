.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>

.. tag:: lang-php
.. tag:: web
.. tag:: mail

.. sidebar:: Logo

  .. image:: _static/images/roundcube.svg
      :align: center

#################
Roundcube Webmail
#################

.. tag_list::

Roundcube webmail is a browser-based IMAP client with an easy-to-use user interface. It provides full functionality you expect from an email client, including MIME support, address book, folder manipulation, message searching and spell checking.

The global Uberspace Webmail-Instance is also based on roundcube. Deploying your own roundcube webmail is ideal if you want to add functionality by plugins or customize the theme etc.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`
  * :manual:`Mail <mail-access>`

License
=======

Roundcube Webmail is released under the GNU General Public License_ version 3 or any later version with exceptions for skins and plugins.


Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.3:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.3
 Selected PHP version 7.3
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.3'
 [isabell@stardust ~]$

If you want to use your Roundcube Webmail with your own domain you need to setup your domain first:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$
 
You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$
 



Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, download the latest release of Roundcube and extract it. Move all containing files up one level and remove the emtpty directory as well as the archive afterwards.

.. note:: Check the Roundcube_ website or `Github Repository`_ for the latest stable release and copy the download link to the Complete.tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub/Website.

.. code-block:: console
 :emphasize-lines: 2,4,5,6,7,8

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/roundcube/roundcubemail/releases/download/1.4.3/roundcubemail-1.4.3-complete.tar.gz
 [isabell@stardust html]$ tar xfz *.tar.gz
 [isabell@stardust html]$ cd roundcubemail-1.4.3
 [isabell@stardust roundcubemail-1.4.3]$ mv * .[a-z]* ../ 
 [isabell@stardust roundcubemail-1.4.3]$ cd ..
 [isabell@stardust html]$ rm -r roundcubemail-1.4.3/
 [isabell@stardust html]$ rm -r roundcubemail-1.4.3-complete.tar.gz
 [isabell@stardust html]$
 

Configuration
=============

Create Database
---------------

Roundcube saves your data in a :manual:`MySQL <database-mysql>` database. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_roundcube``) instead of the default database.

.. note:: You need to create the database **before** you enter the database :manual_anchor:`credentials <database-mysql.html#login-credentials>` in the `Roundcube Installer`_.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_roundcube"
 [isabell@stardust ~]$


Roundcube Installer
-------------------

The final configuration can easily be done in the browser.  Point your Browser to your installation URL ``https://isabell.uber.space/installer/``.

All prerequisite checks should be *OK* - click *NEXT*.

.. note:: You can safely ignore the *NOT AVAILABLE*-Warnings at the SQLite, SQL Server etc Databases, as we'll use the MySQL Database.

Enter the following details at the Tab *CREATE CONFIG*:

General configuration
---------------------

  * Product name (choose whatever you want, e.g. ``isabell Webmail``)

Database setup
--------------

  * Database type (use ``mySQL``)
  * Database server (use ``localhost``)
  * Database name (e.g. ``isabell_roundcube``)
  * MySQL username (equals your Uberspace username, e.g. ``isabell``)
  * MySQL password - you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * db_prefix (e.g. ``rc_``)



IMAP & SMTP Settings
--------------------

  * default_host (use *ssl://„server“.uberspace.de*, e.g. ``ssl://stardust.uberspace.de``)
  * default_port (use ``993``)
  * smtp_server (use *tls://„server“.uberspace.de*, e.g. ``tls://stardust.uberspace.de``)
  * smtp_port (use ``587``)
  * junk_mbox (use ``Spam``)

.. warning:: Make sure to add the prefixes (``ssl://`` / ``tls://``) as mentioned above, otherwise you won't be able to receive or sent mails. Uberspace does not support :manual_anchor:`insecure access <mail-access.html#client-settings>`.
  
.. note:: We'll adjust the default setting ``Junk`` to ``Spam`` to refer to the default :manual_anchor:`default Spamfolder <mail-spam.html#configure-spam-folder>`.
 

``Activate`` the option *Use the current IMAP username and password for SMTP authentication*.

Display settings & user prefs
-----------------------------

Enter your desired language for RoundCube under **language**.
The code for German is ``de_DE``, English is ``en_US``, the code for French is ``fr_FR`` etc

.. note:: Users can set their own language.

Plugins
-------

If you want to add Plugins to your configuration tick the corresponding checkboxes.
  
When you're done click *CONTINUE*. The configuration file will be created and stored in ``/var/www/virtual/$USER/html/config``.

Finishing installation
======================

On the last tab *Test config* click on **initialize database** to initialize the database.

.. note:: Optionally you can check your SMTP & IMAP config by entering valid credentials down here, but it's not necessary.

Your done. Point your Browser to your installation URL ``https://isabell.uber.space`` and
admire your shiny new webmail client!


Best practices
==============

Security
--------

.. warning:: For security reasons, you should remove the installer-directory from the source files.


.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ rm -rv installer/
 [isabell@stardust html]$
 
Login Pattern
-------------

Use your full email address and the corresponding password to login. This works with your ``@uber.space`` address as well as with any addresses using your :manual_anchor:`own domains <mail-domains.html#mail-domains>`.



Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version available, **always make a backup first**.
Refer to the Upgrade_ Manual of the official Roundcube Wiki for further instructions.

.. _Upgrade Manual: https://github.com/roundcube/roundcubemail/wiki/Upgrade
.. _Roundcube: https://roundcube.net/download/
.. _feed: https://github.com/roundcube/roundcubemail/releases.atom
.. _GNU General Public License: https://roundcube.net/license/
.. _Github Repository: https://github.com/roundcube/roundcubemail/releases

----

Tested with Roundcube 1.4.3, Uberspace 7.5.0.0

.. author_list::
