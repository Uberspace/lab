.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-php
.. tag:: mail
.. tag:: web
.. tag:: webmail

.. sidebar:: Logo

  .. image:: _static/images/snappymail.png
      :align: center

##########
SnappyMail
##########

.. tag_list::

SnappyMail_ is a simple, modern, lightweight and fast web-based open source email client. It is a fork of the email client RainLoop, but with massive changes to be compatible with (mobile) browsers of 2020 and newer.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Mail <mail-access>`

License
=======

All relevant legal information can be found here:

  * https://github.com/the-djmaze/snappymail/blob/master/LICENSE

Prerequisites
=============

Make sure to use :manual:`PHP <lang-php>` version 8.3:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use php 8.3
 Selected PHP version 8.3
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Installation
============

Enter your DocumentRoot directory, download the latest version, unpack the archive and then delete it (as well as the file ``nocontent.html`` if it still exists).

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ wget https://snappymail.eu/repository/latest.tar.gz
 [isabell@stardust html]$ tar -xzf latest.tar.gz
 [isabell@stardust html]$ rm latest.tar.gz nocontent.html
 [isabell@stardust html]$

For security reasons, it is a good idea to move the ``data`` directory from the DocumentRoot to a directory that cannot be accessed by the web server. The home directory is suitable for this purpose. Move the directory ``data`` and rename it ``snappymail-data`` at the same time, so that you know later it is a part of SnappyMail.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ mv data ~/snappymail-data
 [isabell@stardust html]$

Configuration
=============

Configure SnappyMail
--------------------

You must tell SnappyMail about the moved data directory. To do this, enter the new path in the file ``~/html/_include.php`` as the value of the constant ``APP_DATA_FOLDER_PATH``. To achieve this, add the following line:

.. warning:: Replace ``isabell`` with your username!

::

 define('APP_DATA_FOLDER_PATH', '/home/isabell/snappymail-data/');

Afterwards you have to rename the file ``_include.php`` to ``include.php``.

.. code-block:: console

 [isabell@stardust html]$ mv _include.php include.php
 [isabell@stardust html]$

Access the admin page
---------------------

Open the admin panel, which can now be found here:

.. warning:: Replace ``isabell`` with your username!

* https://isabell.uber.space/?admin

When you access this page for the first time, the file ``~/snappymail-data/_data_/_default_/admin_password.txt`` is created with the initial password for the user ``admin``. Use this to log in and then change your password in the "Security" menu item. The file with the password will now be deleted automatically.

Configure your domains
----------------------

You may now want to configure your own domains for email access. You can do this in the admin panel in the menu item "Domains".

Be aware that an entry for ``<your_hostname>.uberspace.de`` (in addition to the correct entries for Gmail and Hotmail) has already been created there automatically. However, this one is incorrect so you need to edit it. You can find the correct settings for IMAP and SMTP here: :manual:`Accessing Your Mails <mail-access>`

Best practices
==============

Security
--------

Keep the software up to date.

You can protect your admin account from unauthorized access by using two-factor authentication in addition to a strong password. You can activate this in the admin panel by clicking on the "Generate" button in the "Security" menu item. Please note that you must also enter your current password in order to be able to save it. Now scan the QR code with an app for two-factor authentication. If you don't have one yet, take a look at 2FAS_ or `Ente Auth`_.

Updates
=======

.. note:: Check the `GitHub release page`_ regularly to stay informed about the newest version.

The `official documentation`_ describes in a separate section ("Upgrade") how to install a new version.

.. _SnappyMail: https://snappymail.eu
.. _2FAS: https://2fas.com
.. _Ente Auth: https://ente.io/auth/
.. _GitHub release page: https://github.com/the-djmaze/snappymail/releases
.. _official documentation: https://github.com/the-djmaze/snappymail/wiki/Installation-instructions#upgrade

----

Tested with SnappyMail 2.38.2, Uberspace 7.16.2

.. author_list::
