.. author:: Putzwasser <26040044+putzwasser@users.noreply.github.com>

.. tag:: web
.. tag:: lang-php
.. tag:: audience-business
.. tag:: customer-management
.. tag:: mail

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/mautic.svg
      :align: center


######
Mautic
######

.. tag_list::

Mautic is an open-source marketing automation platform that enables businesses to create, manage, and track personalized digital marketing campaigns across multiple channels and is very suitable to build an email newsletter.

This guide will show you how to install Mautic 4 on your Uberspace using the Composer installation method.

----

.. error::

  This guide seems to be **broken** for the current versions of PHP, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1692

Prerequisites
=============

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`cronjobs <daemons-cron>`

Domain
------

You can use the domains that are currently configured:

.. include:: includes/web-domain-list.rst

You can also setup :manual:`additional` (sub) domains for use with your Uberspace account.

MySQL credentials
-----------------

.. include:: includes/my-print-defaults.rst

Create the database
-------------------

Create a new MySQL database for Mautic.

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_mautic;"
  [isabell@stardust ~]$


Installation
============

Change to Apache's :manual:`DocumentRoot <web-documentroot>` directory:

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$

Step 1: Download Mautic
-----------------------

Download your Mautic instance into it's own subdirectory:

.. code-block:: console

  [isabell@stardust isabell]$ composer create-project mautic/recommended-project:^4 mautic --no-interaction
  Creating a "mautic/recommended-project:^4" project at "./mautic"
  Installing mautic/recommended-project (4.4.7)
    - Installing mautic/recommended-project (4.4.7): Extracting archive
    [...]
  Congratulations, you’ve installed the Mautic codebase
  from the mautic/recommended-project template!

  Next steps:
    * Install Mautic
    * Read the user guide
    * [...]
  [isabell@stardust isabell]$


Step 2: Create a symbolic link
------------------------------

Create a symbolic link pointing to Mautic's ``docroot`` folder to let Apache serve Mautic's pages.
You need to delete Apache's root directory (``/var/www/virtual/isabel/html``) for that.
Make sure not to delete important files.

.. code-block:: console

  [isabell@stardust isabell]$ rm -f html/nocontent.html
  [isabell@stardust isabell]$ rmdir html
  [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/mautic/docroot/ /var/www/virtual/$USER/html

This will result in the following structure:

.. code-block:: console

  [isabell@stardust isabell]$ tree -L 2
  .
  ├── html -> /var/www/virtual/isabell/mautic/docroot/
  └── mautic
      ├── app
      ├── autoload.php
      ├── bin
      ├── composer.json
      ├── composer.lock
      ├── docroot
      ├── Gruntfile.js
      ├── package.json
      ├── package-lock.json
      ├── README.md
      └── vendor


Finishing installation
======================

Now you can access the Mautic's web interface on ``https://isabell.uber.space`` and use the installation wizard to complete your setup.

You retrieved your MySQL username and password in the *Prerequisites* section and set the database name there (e.g. ``isabell_mautic``).
Use these values for the wizard.

Set up Mautic's cronjobs
------------------------

Mautic requires a few `cron jobs <https://docs.mautic.org/en/setup/cron-jobs>`_ to handle some maintenance tasks such as updating contacts
or campaigns, executing campaign actions, sending emails, and more.

.. hint::
  The cron jobs here are staggered as recommended in Mautic's documentation.
  If you want to edit the schedules you could use `crontab.guru <https://crontab.guru/>`_, which is a quick and simple editor for cron schedule expressions.

Logging
~~~~~~~

Create a folder to save the outputs of the cronjob commands to distinct log files:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/logs/mautic
  [isabell@stardust ~]$

If you don't want to keep logs, remove the part after ``>>`` in the following cronjobs.


Basic maintenance cronjobs
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add these cronjobs to your crontab like described in the :manual:`cron jobs to your server<daemons-cron>`.

.. code-block:: console

  # Update segments
  0,15,30,45 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:segments:update >> /home/$USER/logs/mautic/segments 2>&1

  # Update campaings
  5,20,35,50 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:campaigns:update >> /home/$USER/logs/mautic/campaigns 2>&1

  # Update trigger campaign events
  10,25,40,55 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:campaigns:trigger >> /home/$USER/logs/mautic/campaigns 2>&1

  # Send broadcasts every fifteen minutes
  12,27,42,57 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:broadcasts:send >> /home/$USER/logs/mautic/broadcasts 2>&1


Purge old data
~~~~~~~~~~~~~~

Use this cronjob to remove old data due to privacy reasons and following GDRP regulations.

.. code-block:: console

  # Purge old data every friday
  0 0 * * FRI php /var/www/virtual/isabell/mautic/bin/console mautic:maintenance:cleanup -g -n --days-old=365


Send queued emails
~~~~~~~~~~~~~~~~~~

You need this if you use the `email queue <https://docs.mautic.org/en/contacts/message-queue>`_.

.. code-block:: console

  # Send out queued emails every 2nd minute
  */2 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:emails:send  >> /home/$USER/logs/mautic/emails 2>&1


Fetch mail bounces
~~~~~~~~~~~~~~~~~~

You need this to get your `bounces <https://docs.mautic.org/en/channels/emails/bounce-management>`_ from somewhere.

.. code-block:: console

  # Fetch bounces
  3,33 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:email:fetch >> /home/$USER/logs/mautic/emails 2>&1

.. hint::
  This guide made sure that everything important is reflected in the cron jobs.

  Mautic might get busy if you have many contacts and do some heavy sending/lifting.
  This might lead to commands that overlap / run simultaneously. You can adjust your
  cronjobs in timing and limits to adapt any of those problems afterwards.

  Most of the commands do have a ``--[message|time-]limit=[LIMIT]`` option you can leverage.


Configuration
=============

Suppressing security header for external origins
------------------------------------------------

If you embed mautic forms on another website (domain) you will need to `suppress <https://manual.uberspace.de/web-headers/#removing-security-headers>`_
the default Uberspace security header that only accepts data from the same origin:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web header suppress mautic.mysite.com X-Frame-Options
  Suppressing header "X-Frame-Options" for mautic.mysite.com
  [isabell@stardust ~]$

----

Tested with Mautic 4.4.7, Uberspace 7.15

.. author_list::
