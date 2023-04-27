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

.. _mautic-installation:
######
Mautic
######

.. tag_list::

Mautic is an open-source marketing automation platform that enables businesses to create, manage, and track personalized digital marketing campaigns across multiple channels and is very suitable to build an email newsletter.

----

This guide will show you how to install Mautic 4 on your Uberspace using the Composer installation method.

.. important:: It is bad practice to run your Mautic along your blog on the same server.
  Doing so would expose your users' data along with their email addresses if your blog was victim to a successful hacker attack.
  This would pose a massive GDPR infringement.
  A separate Mautic installation means that Mautic will have its own distinct subdomain, such as ``mautic.mysite.com``.
  Hence, we use ``mautic.mysite.com`` as your domain in this guide, since there is little practical use for Mautic without an accompanying website.
  (Mautic is still reachable via ``isabell.uber.space`` if you follow this guide.)
  If you still prefer to use a subdirectory, you will need to make slight adjustments to this guide.

.. note:: For this guide, you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`DocumentRoot <web-documentroot>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`PHP <lang-php>`

.. note:: This guide is based on the `Mautic Composer installation method <https://docs.mautic.org/en/setup/how-to-install-mautic/install-and-manage-mautic-with-composer>`_.

----

Prerequisites
=============

* You have to :manual:`setup a domain <web-domains>`.
* You have to :manual:`create a MySQL database <database-mysql>`.

Step 1: Set up the subdomain
----------------------------

1. You need to register the subdomain with Uberspace:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web domain add mautic.mysite.com
  The webserver's configuration has been adapted.
  Now you can use the following records for your DNS:
    A -> xxx.26.156.13
    AAAA -> xxxx:d0c0:200:0:6ca2:b2ff:fee6:2c13
  [isabell@stardust ~]$

Once you've set up your domain using the uberspace tool, the tool provides you with the ``A`` and ``AAAA`` records that need to be configured in your registrar's nameserver.

2. Let Apache handle the backend for your added domain.

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set mautic.mysite.com --apache
  Set backend for mautic.mysite.com/ to apache.
  [isabell@stardust ~]$


Step 2: Create the database
---------------------------

.. include:: includes/my-print-defaults.rst

Create a new MySQL database for Mautic.

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_mautic;"
  [isabell@stardust ~]$


Installation (using Composer)
=============================

Change to Apache's :manual:`DocumentRoot <web-documentroot>` directory:

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$

Step 1: Download Mautic
------------------------

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
-------------------------------

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


Step 3: Check your Mautic installation
----------------------------------

Visit ``https://mautic.mysite.com`` (or ``https://isabell.uber.space``) in your browser.
There might be a ``403 forbidden error``.

Fix 403 forbidden error (if applicable)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you encounter a 403 forbidden error, there are two possible causes:

1. You didn't follow this guide and installed Mautic in your ``$HOME`` directory and linked to it. Apache can't access these files. Move it into ``/var/www/virtual/$USER/`` as indicated in this manual.
2. There's an error with Mautic's ``.htaccess`` file.

To fix the second problem, follow these steps:

.. note:: This problem is documented `at the Mautic fourum <https://forum.mautic.org/t/mautic-upgrade-to-4-3-1-produces-403-http-error-unless-htaccess-security-lines-are-removed/24255>`_ and `at GitHub <https://github.com/mautic/mautic/issues/10913>`_.

1. Open the .htaccess file in the ``docroot`` directory of your Mautic installation (``/var/www/virtual/$USER/mautic/docroot/.htaccess``).
2. Comment out the following lines by adding a ``#`` at the beginning of each line:

.. code-block:: apache

     # Apache 2.4+
     <IfModule authz_core_module>
         # Deny access via HTTP requests to all PHP files.
         <FilesMatch "\.php$">
             Require all denied
         </FilesMatch>

         # Deny access via HTTP requests to composer files.
         <FilesMatch "^(composer\.json|composer\.lock)$">
             Require all denied
         </FilesMatch>

         # Except those allowed below.
         <If "%{REQUEST_URI} =~ m#^/(index|index_dev|upgrade/upgrade)\.php#">
             Require all granted
         </If>
     </IfModule>

3. Mautic should now be accessible.

Configuration
=============

If your Mautic installation is separated from your main site or blog (which is how it should be done from a security and data privacy point of view), then you need to configure the :manual:`web header <web-headers>`.

.. note::
  This is necessary, because your uberspace comes with a number of :manual:`security headers <web-security-headers>` set by default.
  In this particular case ``X-Frame-Options: SAMEORIGIN`` is set.
  It causes problems, because it prevents Mautic's forms that are embedded on your main site to receive form result data.
  This leads to an error that the `form keeps hanging on "please wait" <https://forum.mautic.org/t/multisite-wordpress-trouble-mautic-form-iframe-error-refused-to-connect-please-wait-hanging-mautic-form-submission/11092>`_ after it was submitted.

Suppressing `X-Frame-Options: SAMEORIGIN`
-----------------------------------------

.. code-block:: console

  [isabell@stardust ~]$ uberspace web header suppress mautic.mysite.com X-Frame-Options
  Suppressing header "X-Frame-Options" for mautic.mysite.com
  [isabell@stardust ~]$


Finishing installation
======================

Now you can access the Mautic's web interface and the installation wizard to complete your setup.
You retrieved your MySQL username and password in the `Prerequisites` section and set the database name there (e.g. ``isabell_mautic``).
Use these values for the wizard.

Set up Mautic's cronjobs
-----------------------

Mautic requires a few `cron jobs <https://docs.mautic.org/en/setup/cron-jobs>`_ to handle some maintenance tasks such as updating contacts or campaigns, executing campaign actions, sending emails, and more.
You must manually add the required :manual:`cron jobs to your server<daemons-cron>`.

.. hint::
  The cron jobs are staggered as recommended in Mautic's documentation.
  If you want to edit the schedules you could use `crontab.guru <https://crontab.guru/>`_, which is a quick and simple editor for cron schedule expressions.

We save the logs of Mautic's console. If you don't want this remove the part after ``>>`` in your crontab.
If you keep the logs create the directory where the logs will be saved to:

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p /home/$USER/logs/mautic
  [isabell@stardust isabell]$


To create your cron instructions you can use the following commands.
Just execute them and copy the output into your crontab (using `crontab -e` to edit it):

**Update your segments:**

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Update segments every fifteen minutes\n0,15,30,45 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:segments:update >> /home/$USER/logs/mautic/segments 2>&1"
  # Update segments every fifteen minutes
  0,15,30,45 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:segments:update >> /home/isabell/logs/mautic/segments 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at minute 0, 15, 30, and 45` your contacts in smart segments get updated based on new contact data.

**Update your campaigns:**

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Update campaings every fifteen minutes\n5,20,35,50 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:campaigns:update >> /home/$USER/logs/mautic/campaigns 2>&1"
  # Update campaings every fifteen minutes
  5,20,35,50 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:campaigns:update >> /home/isabell/logs/mautic/campaigns 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at minute 5, 20, 35, and 50` your campaigns get rebuilt based on your contact segments.

**Trigger campaing events:**

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Update trigger campaign events every fifteen minutes\n10,25,40,55 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:campaigns:trigger >> /home/$USER/logs/mautic/campaigns 2>&1"
  # Update trigger campaign events every fifteen minutes
  10,25,40,55 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:campaigns:trigger >> /home/isabell/logs/mautic/campaigns 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at minute 10, 25, 40, and 55` your timed events for published campaigns get triggered.

**Send broadcasts:**

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Send broadcasts every fifteen minutes\n12,27,42,57 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:broadcasts:send >> /home/$USER/logs/mautic/broadcasts 2>&1"
  # Send broadcasts every fifteen minutes
  12,27,42,57 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:broadcasts:send >> /home/isabell/logs/mautic/broadcasts 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at minute 12, 27, 42, and 57` your broadcasts get sent.

**Send queued emails:**

You need this if you use the `email queue <https://docs.mautic.org/en/contacts/message-queue>`_ (`Queue documentation <https://docs.mautic.org/en/queue>`_).

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Send emails ever 2nd minute\n*/2 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:emails:send  >> /home/$USER/logs/mautic/emails 2>&1"
  # Send emails ever 2nd minute
  */2 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:emails:send  >> /home/isabell/logs/mautic/emails 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at every 2nd minute` your queue emails get sent.

**Fetch bounces:**

You need this if you get your `bounces <https://docs.mautic.org/en/channels/emails/bounce-management>`_ from somewhere.

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Fetch bounces at minutes 3 and 33\n3,33 * * * * php /var/www/virtual/$USER/mautic/bin/console mautic:email:fetch >> /home/$USER/logs/mautic/emails 2>&1"
  # Send emails ever 2nd minute
  */2 * * * * php /var/www/virtual/isabell/mautic/bin/console mautic:emails:send  >> /home/isabell/logs/mautic/emails 2>&1
  [isabell@stardust ~]$

Explanation:

- `Every hour at minute 3 and 33` monitored emails get fetched and processed to `handle bounces <https://docs.mautic.org/en/channels/emails/bounce-management>`_.

**Purge old data:**

You need this if you are subject to the European GDPR regulation.
If you sure you aren't (*which is highly unlikely given it's architecture*) you could omit this command.
This command simply removes data older than one year, which is probably advisable regardless of the GDPR.

.. code-block:: console

  [isabell@stardust ~]$ echo -e "# Purge old data every friday\n0 0 * * FRI php /var/www/virtual/$USER/mautic/bin/console mautic:maintenance:cleanup -g -n --days-old=365"
  # Purge old data every friday
  0 0 * * FRI php /var/www/virtual/isabell/mautic/bin/console mautic:maintenance:cleanup -g -n --days-old=365
  [isabell@stardust ~]$

Explanation:

- `Every Friday at 00:00 AM (midnight)` data older than 365 days get purged.

.. warning::
  This guide made sure that everything important is reflected in the cron jobs.
  Mautic might get busy if you have many contacts and do some heavy sending/lifting.
  This might lead to commands that overlap / run simultaneously.
  This might have bad side effects. Therefore, you might want to adjust your crontab (later).

  Most of the commands do have a ``--[message|time-]limit=[LIMIT]`` option you can leverage.
  Use it to prevent errors and mistakes.

Additional Steps
================

There might be some steps that are outside of this manual's scope:

- Configure an email provider

----

Tested with Mautic 4.4.7, Uberspace 7.15

.. author_list::
