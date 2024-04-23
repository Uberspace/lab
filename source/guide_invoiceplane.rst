.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-php
.. tag:: accounting
.. tag:: web
.. tag:: audience-business

.. sidebar:: Logo

  .. image:: _static/images/invoiceplane.png
      :align: center

############
InvoicePlane
############

.. tag_list::

InvoicePlane_ is a self-hosted open source application for managing your quotes, invoices, clients and payments.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install InvoicePlane we download the current version from the official website. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the zip file will be under your ``html``. After unzipping, we need to move all files one level up, out of the directory ``ip``.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://www.invoiceplane.com/download/v1.6.1
 [isabell@stardust html]$ unzip v1.6.1
 [isabell@stardust html]$ rm v1.6.1
 [isabell@stardust html]$ mv ip/{.,}* .
 [isabell@stardust html]$ rm -rf ip
 [isabell@stardust html]$

Create a database for the application:

::

 [isabell@stardust html]$ mysql -e "CREATE DATABASE ${USER}_invoiceplane"
 [isabell@stardust html]$


Configuration
=============

Enable the URL rewriting rules with the provided htaccess file.

::

 [isabell@stardust html]$ mv htaccess .htaccess
 [isabell@stardust html]$

Now copy the configuration template and open it in an editor.

::

 [isabell@stardust html]$ cp ipconfig.php.example ipconfig.php
 [isabell@stardust html]$

**Important: You must prepend the first line in the file with a
hash sign ("#"), otherwise the application fails to load.**

.. code-block:: php

 # <?php exit('No direct script access allowed'); ?>

Now change the following lines in the configuration file and fill
in your settings:

.. code-block:: php

 IP_URL=https://isabell.uber.space
 REMOVE_INDEXPHP=true
 DB_HOSTNAME=localhost
 DB_USERNAME=isabell
 DB_PASSWORD=MySuperSecretPassword
 DB_DATABASE=isabell_invoiceplane

After the installation you need to open https://isabell.uber.space/setup in your browser to finish your setup.
In that step, the database tables get created and you'll setup an admin user
for your installation.

.. note::

 After completing the web-based setup above,
 you need to disable the setup script.
 To do so, replace the line DISABLE_SETUP=false with
 DISABLE_SETUP=true in your ``ipconfig.php`` file.

Updates
=======

Check InvoicePlane's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation.

Backup your ``ipconfig.php`` file, delete everything else in your ``html`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp ipconfig.php ~
 [isabell@stardust html]$ rm -rf * .*
 [isabell@stardust html]$

Proceed with the installation steps from here and move back your config file.

::

 [isabell@stardust html]$ mv ~/ipconfig.php ./
 [isabell@stardust html]$

Finish the update by opening https://isabell.uber.space/setup in your browser.

.. _InvoicePlane: https://www.invoiceplane.com/
.. _stable releases: https://www.invoiceplane.com/downloads

----

Tested with InvoicePlane 1.6.0 and Uberspace 7.15.1

.. author_list::
