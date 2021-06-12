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

.. abstract::
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

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project grumpydictator/firefly-iii --no-dev --prefer-dist firefly_iii 5.4.6
 [...]
 [isabell@stardust isabell]$

After the installation has finished, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``firefly_iii/public`` directory.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/firefly_iii/public html
 [isabell@stardust isabell]$

Configuration
=============

We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for Firefly III to save your data. You have to create this database first.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_fireflyiii"
 [isabell@stardust ~]$

``cd`` into your Firefly III directory.

.. code-block:: console

 [isabell@stardust isabell]$ cd firefly_iii
 [isabell@stardust firefly_iii]$

Edit the ``.env`` file to change the settings. Change ``DB_HOST`` to  ``localhost`` and change the values of ``DB_DATABASE``, ``DB_USERNAME``, ``DB_PASSWORD`` to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`.
Also edit any other settings like the time zone (``TZ``) or default language (``DEFAULT_LANGUAGE``) while the file is open.
After you have edited all the necessary settings save the file.

Finishing installation
======================
To finish the installation and setup your database run the following commands:

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust firefly_iii]$ php artisan migrate:refresh --seed
 [isabell@stardust firefly_iii]$ php artisan firefly-iii:upgrade-database
 [isabell@stardust firefly_iii]$ php artisan passport:install
 [isabell@stardust firefly_iii]$

Go to https://isabell.uber.space to access your Firefly III installation.

.. warning:: Please make sure to directly create an account, as the first account will be an admin account.

Tuning
======

Mail
####

To setup Firefly III to be able to send mails, you first have to create a :manual_anchor:`new mailbox user <mail-mailboxes.html#additional-mailboxes>`:

.. code-block:: console

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

.. warning:: Please make sure to backup your data before updating.

To update your Firefly III installation, ``cd`` to the directory one level above your :manual:`document root <web-documentroot>`, then download the new version via composer. Replace <next_version> with the latest version.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project grumpydictator/firefly-iii --no-dev --prefer-dist firefly-iii-updated <next_version>
 [...]
 [isabell@stardust isabell]$


After the installation has finished, we need to copy over our settings located in the ``.env`` file and other data.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust isabell]$ cp firefly_iii/.env firefly-iii-updated/.env
 [isabell@stardust isabell]$ cp firefly_iii/storage/upload/* firefly-iii-updated/storage/upload/
 [isabell@stardust isabell]$ cp firefly_iii/storage/export/* firefly-iii-updated/storage/export/
 [isabell@stardust isabell]$

Navigate into the newly created folder and run the following commands to finish the upgrade:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust isabell]$ cd firefly-iii-updated
 [isabell@stardust firefly-iii-updated]$ rm -rf bootstrap/cache/*
 [isabell@stardust firefly-iii-updated]$ php artisan cache:clear
 [isabell@stardust firefly-iii-updated]$ php artisan migrate --seed
 [isabell@stardust firefly-iii-updated]$ php artisan firefly-iii:upgrade-database
 [isabell@stardust firefly-iii-updated]$ php artisan passport:install
 [isabell@stardust firefly-iii-updated]$ php artisan cache:clear
 [isabell@stardust firefly-iii-updated]$

Move one folder up again and rename the updated folder, so our :manual:`document root <web-documentroot>` points to the updated version.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust firefly-iii-updated]$ cd ..
 [isabell@stardust isabell]$ mv firefly_iii firefly-iii-old
 [isabell@stardust isabell]$ mv firefly-iii-updated firefly_iii
 [isabell@stardust isabell]$

You can now go to https://isabell.uber.space to access your updated Firefly III installation.

Acknowledgements
================
This guide is based on the official `Firefly III setup guide`_.

.. _github: https://github.com/firefly-iii/firefly-iii/
.. _AGPLv3: http://www.gnu.org/licenses/agpl-3.0.en.html
.. _release tracker: https://version.firefly-iii.org/
.. _Firefly III setup guide: https://docs.firefly-iii.org/faq/self_hosted

----

Tested with Firefly III 5.4.6, Uberspace 7.8.0.0.

.. author_list::
