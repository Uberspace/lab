.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>

.. tag:: lang-php
.. tag:: web
.. tag:: mail
.. tag:: webmail

.. sidebar:: Logo

  .. image:: _static/images/roundcube.svg
      :align: center

#########
Roundcube
#########

.. tag_list::

Roundcube is a browser-based IMAP client with an easy-to-use user interface. It provides full functionality you expect from an email client, including MIME support, address book, folder manipulation, message searching and spell checking.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`
  * :manual:`Mail <mail-access>`

License
=======

Roundcube is released under the GNU General Public License_ version 3 or any later version with exceptions for skins and plugins.


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

If you want to use your Roundcube with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst


.. include:: includes/my-print-defaults.rst
 



Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, download the latest release of Roundcube, extract it and remove the archive afterwards.

.. note:: Check the Roundcube_ website or `Github Repository`_ for the latest stable release and copy the download link to the Complete.tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub/Website.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/roundcube/roundcubemail/releases/download/1.4.3/roundcubemail-1.4.3-complete.tar.gz
 [isabell@stardust html]$ tar xf roundcubemail-*.tar.gz --strip-components=1
 [isabell@stardust html]$ rm -r roundcubemail-*.tar.gz
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
^^^^^^^^^^^^^^^^^^^^^

  * Product name (choose whatever you want, e.g. ``isabell Roundcube``)
  * ``Activate`` the option *ip_check* for greater security. It checks the client’s IP in session authorization.

Database setup
^^^^^^^^^^^^^^

  * Database type (use ``mySQL``)
  * Database server (use ``localhost``)
  * Database name (e.g. ``isabell_roundcube``)
  * MySQL username (equals your Uberspace username, e.g. ``isabell``)
  * MySQL password - you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * db_prefix (e.g. ``rc_``)



IMAP & SMTP Settings
^^^^^^^^^^^^^^^^^^^^

  * default_host (use *ssl://„server“.uberspace.de*, e.g. ``ssl://stardust.uberspace.de``)
  * default_port (use ``993``)
  * username_domain - This is a convenience option for email providers that use a full email address as the username. **This field is optional.** Entering a domain — not the full email — will allow you to login to Roundcube with just your name, before the @, instead of the whole email. For example, ``domain.tld`` in the field will allow ``user@domain.tld`` to log into Roundcube with ``user``.
  
This, however, doesn't restrict access if somebody enters the full email address. If you want to **restrict** the users access to Roundcube to a specific domain have a look at `Restrict Access`_ in the Secuity-Section.

  * Make sure the *auto_create_user* check box is checked. If it’s unchecked, Roundcube won’t create a user in its own database, which will prevent you from logging in.
  * smtp_server (use *tls://„server“.uberspace.de*, e.g. ``tls://stardust.uberspace.de``)
  * smtp_port (use ``587``)
  * junk_mbox (use ``Spam``)

.. warning:: Make sure to add the prefixes (``ssl://`` / ``tls://``) as mentioned above, otherwise you won't be able to receive or sent mails. Uberspace does not support :manual_anchor:`insecure access <mail-access.html#client-settings>`.


  
.. note:: We'll adjust the default setting ``Junk`` to ``Spam`` to refer to the default :manual_anchor:`default Spamfolder <mail-spam.html#configure-spam-folder>`.
 

``Activate`` the option *Use the current IMAP username and password for SMTP authentication*.

Display settings & user prefs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * Enter your desired language for RoundCube under **language**. The code for German is ``de_DE``, English is ``en_US``, the code for French is ``fr_FR`` etc

.. note:: Users can set their own language.

Plugins
^^^^^^^

If you want to add Plugins to your configuration check the corresponding checkboxes.
  
When you're done click *CONTINUE*. The configuration file will be created and stored in ``/var/www/virtual/$USER/html/config``.

Finishing installation
======================

On the last tab *Test config* click on **initialize database** to initialize the database.

.. note:: Optionally you can check your SMTP & IMAP config by entering valid credentials down here, but it's not necessary.

Your done. Point your Browser to your installation URL ``https://isabell.uber.space`` and
admire your shiny new Roundcube!


Best practices
==============

Security
--------

Remove Installer-Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning:: For security reasons, you should remove the installer-directory from the source files.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ rm -r installer/
 [isabell@stardust html]$
 
Restrict Access
^^^^^^^^^^^^^^^

Add the following to your ``~/html/config/config.inc.php``:

.. code-block:: ini

 $rcmail_config['username_domain'] = 'domain.tld';
 $rcmail_config['force_username_domain'] = true;

All domains in the logins will be replaced by the specified domain above.
If you want to specify *multiple domains* you'll have to create an array like the following:

.. code-block:: ini

 $rcmail_config['username_domain'] = array(
   'mail.domain.tld' => 'domain.tld',
   'othermail.domain2.tld' => 'domain2.tld',
 );
 
Login Pattern
-------------

Use your full email address and the corresponding password to login. This works with your ``@uber.space`` address as well as with any addresses using your :manual_anchor:`own domains <mail-domains.html#mail-domains>`.



Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version available, **always make a backup first** including your Roundcube directory and your database.

On the command line
-------------------

Get the latest version
^^^^^^^^^^^^^^^^^^^^^^

``cd`` to your :manual:`home directory <basics-home>` (e.g.``/home/isabell``), download the latest release of Roundcube and extract it.

.. warning:: Make sure to download and extract the tarball to a different location as your active roundcube installation to prevent an accidetalliy override!

.. note:: Check the Roundcube_ website or `Github Repository`_ for the latest stable release and copy the download link to the Complete.tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub/Website.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/roundcube/roundcubemail/releases/download/1.4.3/roundcubemail-1.4.3-complete.tar.gz
 [isabell@stardust isabell]$ tar xf roundcubemail-*.tar.gz
 [isabell@stardust isabell]$
 
Read the ``UPGRADING`` and ``INSTALL`` files and check system requirements of the new version before continuing.
 
Update your existing Roundcube installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``cd`` to the downloaded and extracted roundcube directory and execute the ``installto.sh``-Script bundled with Roundcube to easily update your installation. The script first copies all updated files to the target directory and then runs the update script that will update/migrate your local configuration files and update the database schema if necessary.

.. note:: Make sure to change the directory folloewd by the script-call to your active roundcube directory ``bin/installto.sh ``**<your-existing-roundcube-directory>**````. The Output of the Updatescript can vary depening of your your version and which files have been changed.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/roundcubemail-1.4.3/
 [isabell@stardust roundcubemail-1.4.3]$ bin/installto.sh /var/www/virtual/$USER/html
 ? Upgrading from 1.4.2. Do you want to continue? (y/N)
 ✔ Copying files to target location..../
 ℹ NOTICE: JavaScript dependencies installation skipped.
 ✔ Running update script at target...
 ✔ Executing database schema update.
 ℹ NOTICE: Update dependencies by running `php composer.phar update --no-dev`
 ✔ This instance of Roundcube is up-to-date.
 ✔ Have fun!
 ✔ All done.
 [isabell@stardust roundcubemail-1.4.3]$
 
Finishing updating
^^^^^^^^^^^^^^^^^^

Remove the temporary folder as well as the archive after finishing the update process.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust roundcubemail-1.4.3 ]$ cd /var/www/virtual/$USER/
 [isabell@stardust ]$ rm -r roundcubemail-*
 [isabell@stardust ]$


Via FTP + Installer
-------------------

.. note:: If you prefer to upgrade manually via FTP and the Installer (like described above) refer to the `Upgrade Manual`_ of the official Roundcube Wiki for further instructions.

.. _Upgrade Manual: https://github.com/roundcube/roundcubemail/wiki/Upgrade
.. _Roundcube: https://roundcube.net/download/
.. _feed: https://github.com/roundcube/roundcubemail/releases.atom
.. _GNU General Public License: https://roundcube.net/license/
.. _Github Repository: https://github.com/roundcube/roundcubemail/releases

----

Tested with Roundcube 1.4.3, Uberspace 7.5.0.0

.. author_list::
