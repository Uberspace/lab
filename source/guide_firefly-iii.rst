.. author:: Felix Kohlen <https://github.com/FelixKohlen>

.. tag:: lang-php
.. tag:: web
.. tag:: personal-finance

.. sidebar:: Logo

  .. image:: _static/images/firefly-iii.png
      :align: center

###########
Firefly III
###########

.. tag_list::

"Firefly III" is a (self-hosted) manager for your personal finances. It can help you keep track of your expenses and income, so you can spend less and save more.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`mail <mail-access>`
  * :manual:`cron <daemons-cron>`

License
=======

Firefly III is released under the `AGPLv3`_ license. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to the directory one level above your :manual:`document root <web-documentroot>`, then install Firefly III via composer. You can find the latest version on the `release tracker`_, replace the version below with the version number.

.. code-block:: bash
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ mkdir firefly_iii
 [isabell@stardust isabell]$ wget https://github.com/firefly-iii/firefly-iii/releases/download/v6.2.9/FireflyIII-v6.2.9.tar.gz 
 [isabell@stardust isabell]$ tar xvf FireflyIII-v6.2.9.tar.gz -C /var/www/virtual/$USER/firefly_iii
 [...]
 [isabell@stardust isabell]$ rm FireflyIII-v6.2.9.tar.gz
 [isabell@stardust isabell]$

After the installation has finished, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``firefly_iii/public`` directory.

.. code-block:: bash

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/firefly_iii/public html
 [isabell@stardust isabell]$

Configuration
=============

We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for Firefly III to save your data. You have to create this database first.

.. code-block:: bash
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_fireflyiii"
 [isabell@stardust ~]$

``cd`` into your Firefly III directory and create ``.env-file`` from example file.

.. code-block:: bash

 [isabell@stardust isabell]$ cd firefly_iii
 [isabell@stardust isabell]$ cp .env.example .env
 [isabell@stardust firefly_iii]$

Edit the ``.env`` file to change the settings. Change ``DB_HOST`` to  ``localhost`` and change the values of ``DB_DATABASE``, ``DB_USERNAME``, ``DB_PASSWORD`` to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`.
Also edit any other settings like the time zone (``TZ``) or default language (``DEFAULT_LANGUAGE``) while the file is open.
After you have edited all the necessary settings save the file.

Finishing installation
======================
To finish the installation and setup your database run the following commands:

.. code-block:: bash
 :emphasize-lines: 1,2,3

 [isabell@stardust firefly_iii]$ php artisan migrate:refresh --seed
 [isabell@stardust firefly_iii]$ php artisan firefly-iii:upgrade-database
 [isabell@stardust firefly_iii]$ php artisan firefly-iii:correct-database
 [isabell@stardust firefly_iii]$ php artisan firefly-iii:report-integrity
 [isabell@stardust firefly_iii]$ php artisan firefly-iii:laravel-passport-keys
 [isabell@stardust firefly_iii]$

Go to https://isabell.uber.space to access your Firefly III installation.

.. warning:: Please make sure to directly create an account, as the first account will be an admin account.

Tuning
======

Mail
####

To setup Firefly III to be able to send mails, you first have to create a :manual_anchor:`new mailbox user <mail-mailboxes.html#additional-mailboxes>`:

.. code-block:: bash

  [isabell@stardust ~]$ uberspace mail user add firefly_iii
  Enter a password for the mailbox:
  Please confirm your password:
  New mailbox created for user: 'firefly_iii', it will be live in a few minutes...
  [isabell@stardust ~]$

Afterwards navigate to your Firefly III home folder and edit the ``.env`` file. The mail configuration should be setup like this:

.. code-block:: ini

 MAIL_MAILER=smtp
 MAIL_HOST=stardust.uberspace.de
 MAIL_PORT=587
 MAIL_FROM=firefly_iii@isabell.uber.space
 MAIL_USERNAME=firefly_iii@isabell.uber.space
 MAIL_PASSWORD=MySuperSecretPassword
 MAIL_ENCRYPTION=tls

.. note:: Replace ``MySuperSecretPassword`` with the password you just assigned to the mailbox.

Cronjob
########

For Firefly III to be able to create recurring transactions a cronjob needs to be set up. Use the ``crontab -e`` command and add the following line. This will run the job for recurring transactions every night.

.. code-block:: ini
 :emphasize-lines: 2

 # cron job for Firefly III
 0 3 * * * /usr/bin/php /var/www/virtual/$USER/firefly_iii/artisan firefly-iii:cron

Updates
=======

.. warning:: 
 Please make sure to backup your your database and ``storage`` Folder before updating.

Move the old installation
#########################

Move the old installation to a temporary directory, ie firefly_iii_old. Example commands:

.. code-block:: bash

 [isabell@stardust ~]$ mv /var/www/virtual/isabell/firefly_iii /var/www/virtual/isabell/firefly_iii_old
 [isabell@stardust ~]$

Download the latest release
###########################

To update your Firefly III installation, check for the latest version on the Firefly III `release tracker`_, then download the latest release as a tar.gz file from GitHub and unpack that version. Replace the <version> below with the version number.

.. code-block:: bash

 [isabell@stardust ~]$ cd ~/tmp
 [isabell@stardust tmp]$ wget https://github.com/firefly-iii/firefly-iii/releases/download/<version>/FireflyIII-<version>.tar.gz
 [isabell@stardust tmp]$ tar -xvf FireflyIII-<version>.tar.gz -C /var/www/virtual/isabell/firefly_iii --exclude='storage'
 [isabell@stardust tmp]$ rm FireflyIII-<version>.tar.gz
 [isabell@stardust tmp]$ 

.. note::
 When unpacking, make sure you do not overwrite the storage directory. That's why the ``--exclude='storage'`` part is important. It prevents the default storage directory from being extracted. You will overwrite it anyway from the old installation directory.

Copy over files from the old version
####################################

After the installation has finished, we need to copy over our settings located in the ``.env`` file and other data.

.. code-block:: bash

 [isabell@stardust ~]$ cp /var/www/virtual/isabell/firefly_iii_old/.env /var/www/virtual/isabell/firefly_iii/.env
 [isabell@stardust ~]$ cp /var/www/virtual/isabell/firefly_iii_old/storage /var/www/virtual/isabell/firefly_iii
 [isabell@stardust ~]$

Run upgrade commands
####################

Navigate into ``/var/www/virtual/isabell/firefly_iii`` directory and run the following commands to upgrade the database and the application:

.. code-block:: bash

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/firefly_iii
 [isabell@stardust firefly-iii]$ php artisan migrate --seed
 [isabell@stardust firefly-iii]$ php artisan cache:clear
 [isabell@stardust firefly-iii]$ php artisan view:clear
 [isabell@stardust firefly-iii]$ php artisan firefly-iii:upgrade-database
 [isabell@stardust firefly-iii]$ php artisan firefly-iii:laravel-passport-keys
 [isabell@stardust firefly-iii]$

You can now go to https://isabell.uber.space to access your updated Firefly III installation.

Acknowledgements
================
This guide is based on the official `Firefly III setup guide`_ and the official `Firefly III upgrade guide`_.

.. _github: https://github.com/firefly_iii/firefly_iii/
.. _AGPLv3: http://www.gnu.org/licenses/agpl-3.0.en.html
.. _release tracker: https://version.firefly-iii.org/
.. _Firefly III setup guide: https://docs.firefly-iii.org/how-to/firefly-iii/installation/self-managed/
.. _Firefly III upgrade guide: https://docs.firefly-iii.org/how-to/firefly-iii/upgrade/self-managed/

----

Tested with Firefly III 6.2.9, Uberspace 7.16.5, and PHP 8.4

.. author_list::
