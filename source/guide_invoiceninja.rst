.. highlight:: console

.. author:: Till Deeke <hallo@tilldeeke.de>

.. tag:: lang-php
.. tag:: accounting
.. tag:: customer-management
.. tag:: audience-business
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/invoiceninja.png
      :align: center

#############
Invoice Ninja
#############

.. tag_list::

`Invoice Ninja`_ is a free, open-source, self-hosted invoicing software with built-in support for recurring invoices, time-tracking and online payments.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`cron <daemons-cron>`

License
=======

`Invoice Ninja`_ is released under the `AAL License`_. All relevant information can be found in the LICENSE_ file in the repository of the project. Please also review the `Self-Hosting Terms of Service`_ and `Self-Hosting Data Privacy Addendum`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We will be installing Invoice Ninja using composer.
``cd`` to your :manual:`DocumentRoot <web-documentroot>`, download the latest release, and install the dependencies using ``composer``:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone https://github.com/invoiceninja/invoiceninja
 Cloning into 'invoiceninja'...
 remote: Enumerating objects: 71, done.
 […]
 [isabell@stardust isabell]$ cd invoiceninja
 [isabell@stardust invoiceninja]$ composer install
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 […]
 [isabell@stardust ~]$

Remove your empty :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``invoiceninja/public`` directory.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/invoiceninja/public html
 [isabell@stardust ~]$


Configuration
=============

During the setup process you will be asked for database credentials. We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for Invoice Ninja to save your data. You have to create this database first using the following command.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_invoiceninja"
 [isabell@stardust ~]$

To finish the installation you need to point your browser to your domain (e.g. ``https://isabell.uber.space``) and enter a few settings:

Application Settings

    #. URL: ``https://isabell.uber.space`` (default)
    #. HTTPS: Check ``Require`` to always generate https:// URLs

Database Connection

    #. Host: ``localhost`` (default)
    #. Database: ``isabell_invoiceninja`` (the name of the database you created)
    #. Username: ``isabell`` (your username)
    #. Password: your MySQL password from ``my_print_defaults client``

Email Settings

    #. Driver: ``Mail`` (to send emails directly via the ``mail`` function in php)
    #. From Name: The "from"-name on emails sent by Invoice Ninja (e.g. ``Invoice Ninja``)
    #. From Address: The email-address from which Invoice Ninja sends emails (e.g. ``ninja@isabell.uber.space``)

    If you select the ``Mail`` driver, you can ignore the Username, Host, Port, Encryption and Password fields.

User Details

    #. First Name: your first name
    #. Last Name: your last name
    #. Email: the email address for the initial administrator account
    #. Password: the password for the administrator account


After you save the settings, you will be redirected to the login for the admin panel.

Tuning
======

Sending recurring invoices and reminders
----------------------------------------

To automatically send recurring invoices and reminders we need to setup some cronjobs.

::

 0 8 * * * /usr/bin/php /var/www/virtual/$USER/invoiceninja/artisan ninja:send-invoices
 0 8 * * * /usr/bin/php /var/www/virtual/$USER/invoiceninja/artisan ninja:send-reminders

You can learn more about cronjobs in the :manual:`uberspace manual cron article <daemons-cron>`.


Sending emails in the background
--------------------------------

Invoice Ninja sends emails in the current request by default, which can lead to slow response times. You can add a background service that takes care of sending the emails:

Add this to the ``.env`` file in the application directory:

::

 QUEUE_DRIVER=database

After that you can :manual_anchor:`add a new supervisord service <daemons-supervisord.html#create-a-service>` with

::

 /usr/bin/php /var/www/virtual/$USER/invoiceninja/artisan queue:work --daemon

as the command.

Attaching PDF invoices to emails
--------------------------------

If you want to attach a PDF file of an invoice to the email a client is receiving, you will need ``phantomjs`` to generate the PDF. We are going to install phantomjs globally via npm:

.. code-block:: console

 [isabell@stardust ~]$ npm install -g phantomjs-prebuilt
 […]
 [isabell@stardust ~]$

After phantomjs is installed you need to change some settings in the application. Edit the ``.env`` file in the root of the application folder (``/var/www/virtual/$USER/invoiceninja/.env``). Replace these lines:

::

 PHANTOMJS_CLOUD_KEY=a-demo-key-with-low-quota-per-ip-address
 PHANTOMJS_SECRET=<someRandomString>

with this:

::

 PHANTOMJS_BIN_PATH=/home/$USER/bin/phantomjs

Now you only have to enable the correct option in the admin panel (``https://isabell.uber.space/settings/email_settings``)

Using the mobile apps
---------------------

If you want to use the mobile apps for Invoice Ninja, you will need to add a secret key to the configuration file in the application directory (``/var/www/virtual/$USER/invoiceninja/.env``).

You can generate the secret key with this command:

::

 [isabell@stardust ~] pwgen 32 1
 <randomSecret>
 [isabell@stardust ~]$

And add it like this to the configuration file:

::

 API_SECRET=<randomSecret>

Updates
=======

.. note:: Check the Releases_ on Github regularly to stay informed about the newest version.

To update `Invoice Ninja`_ you can run the following commands in the root directory of the application.
The ``--force`` arguments are needed to prevent warnings about the application running in production mode.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/invoiceninja
 [isabell@stardust invoiceninja]$ git pull
 [isabell@stardust invoiceninja]$ composer install
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 […]
 [isabell@stardust invoiceninja]$ php artisan optimize --force
 Generating optimized class loader
 The compiled services file has been removed.
 [isabell@stardust invoiceninja]$ php artisan migrate --force
 […]
 [isabell@stardust invoiceninja]$ php artisan db:seed --class=UpdateSeeder --force
 Running UpdateSeeder...
 Seeding: CountriesSeeder
 […]
 [isabell@stardust ~]$


.. _Invoice Ninja: https://www.invoiceninja.org/
.. _AAL License: https://opensource.org/licenses/AAL
.. _LICENSE: https://github.com/invoiceninja/invoiceninja/blob/master/LICENSE
.. _Self-Hosting Terms of Service: https://www.invoiceninja.com/self-hosting-terms-service/
.. _Self-Hosting Data Privacy Addendum: https://www.invoiceninja.com/self-hosting-privacy-data-control/
.. _Releases: https://github.com/invoiceninja/invoiceninja/releases


----

Tested with Invoice Ninja v4.5.12, Uberspace 7.2.10.0

.. author_list::
