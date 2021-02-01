.. highlight:: console

.. author:: Till Deeke <hallo@tilldeeke.de>
.. author:: Daniel Weber <https://github.com/DaniW42>

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

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We will be installing Invoice Ninja using the latest stable version.
Download the release file, unzip it using ``unzip`` and copy the contents to your :manual:`DocumentRoot <web-documentroot>`:

.. code-block:: console

 [isabell@stardust ~]$ wget https://download.invoiceninja.com -O ninja.zip
 Resolving download.invoiceninja.com (download.invoiceninja.com)...
 Saving to: ‘ninja.zip’
 […]
 [isabell@stardust ~]$ unzip -q ninja.zip
 [isabell@stardust ~]$ mv ninja/* html/
 [isabell@stardust ~]$ rm -rf ninja*

Edit ``html/.htaccess`` to hide ``/public`` (example.com/public) from your url and force https:

::

 # Redirect HTTP to HTTPS:
 RewriteCond %{ENV:HTTPS} !=on
 RewriteRule ^(.*) https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

 # Hide /public from url:
 RewriteBase /
 RewriteRule ^(.*)$ public/$1 [L]

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

 0 8 * * * /usr/bin/php /var/www/virtual/$USER/html/artisan ninja:send-invoices
 0 8 * * * /usr/bin/php /var/www/virtual/$USER/html/artisan ninja:send-reminders

You can learn more about cronjobs in the :manual:`uberspace manual cron article <daemons-cron>`.


Sending emails in the background
--------------------------------

Invoice Ninja sends emails in the current request by default, which can lead to slow response times. You can add a background service that takes care of sending the emails:

Add this to the ``.env`` file in the application directory:

::

 QUEUE_DRIVER=database

After that you can :manual_anchor:`add a new supervisord service <daemons-supervisord.html#create-a-service>` with

::

 /usr/bin/php /var/www/virtual/$USER/artisan queue:work --daemon

as the command.

Attaching PDF invoices to emails
--------------------------------

If you want to attach a PDF file of an invoice to the email a client is receiving, you will need ``phantomjs`` to generate the PDF. We are going to install phantomjs globally using the binary from http://phantomjs.org/download.html. Download the Linux 64-bit archive and unzip it using ``tar``:

.. code-block:: console

 [isabell@stardust ~]$ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
 […]
 [isabell@stardust ~]$ tar xfvj phantomjs-2.1.1-linux-x86_64.tar.bz2 phantomjs-2.1.1-linux-x86_64/bin/phantomjs
 [isabell@stardust ~]$ mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs ~/bin/
 [isabell@stardust ~]$ rm -rf phantomjs-2.1.1-linux-x86_64*
 [isabell@stardust ~]$ phantomjs --version
 2.1.1
 [isabell@stardust ~]$ 

After phantomjs is installed you need to change some settings in the application. Edit the ``.env`` file in the root of the application folder (``/var/www/virtual/$USER/.env``). Replace these lines:

::

 PHANTOMJS_CLOUD_KEY=a-demo-key-with-low-quota-per-ip-address
 PHANTOMJS_SECRET=<someRandomString>

with this:

::

 PHANTOMJS_BIN_PATH=/home/$USER/bin/phantomjs

Now you only have to enable the correct option in the admin panel (``https://isabell.uber.space/settings/email_settings``)

Using the mobile apps
---------------------

If you want to use the mobile apps for Invoice Ninja, you will need to add a secret key to the configuration file in the application directory (``/var/www/virtual/$USER/.env``).

You can generate the secret key with this command:

::

 [isabell@stardust ~]$ pwgen 32 1
 <randomSecret>
 [isabell@stardust ~]$

And add it like this to the configuration file:

::

 API_SECRET=<randomSecret>

Updates
=======

.. note:: Check the Releases_ on Github regularly to stay informed about the newest version.

To update `Invoice Ninja`_ you can run the internal self updater. It should perform all the necessary tasks to bring your app up to the latest version.
For convenience please check the official Updating_ Guide.

.. _Invoice Ninja: https://www.invoiceninja.org/
.. _AAL License: https://opensource.org/licenses/AAL
.. _LICENSE: https://github.com/invoiceninja/invoiceninja/blob/master/LICENSE
.. _Self-Hosting Terms of Service: https://www.invoiceninja.com/self-hosting-terms-service/
.. _Self-Hosting Data Privacy Addendum: https://www.invoiceninja.com/self-hosting-privacy-data-control/
.. _Releases: https://github.com/invoiceninja/invoiceninja/releases
.. _Updating: https://invoiceninja.github.io/selfhost.html#shared-hosting-zip-builds


----

Tested with Invoice Ninja v4.5.31, Uberspace 7.9.0

.. author_list::
