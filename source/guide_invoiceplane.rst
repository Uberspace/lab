.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web
.. tag:: business

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

We’re using :manual:`PHP <lang-php>` in the stable version 7.2. Since new Uberspaces are currently setup with PHP 7.1 by default you need to set this version manually:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install InvoicePlane we download the current version from the official website. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the zip file will be under your ``html``.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://www.invoiceplane.org/download/v1.5.10
 [isabell@stardust html]$ unzip v1.5.10
 [isabell@stardust html]$ rm v1.5.10
 [isabell@stardust html]$ 

Configuration
=============

Create the database, copy the configuration template, rename the ``htaccess`` file and add your URL ``https://isabell.uber.space`` in the ``ipconfig.php`` file under ``IP_URL``.

.. code-block:: console

 [isabell@stardust html]$ mysql -e "CREATE DATABASE ${USER}_ip"
 [isabell@stardust html]$ cp ipconfig.php.example ipconfig.php
 [isabell@stardust html]$ mv htaccess .htaccess
 [isabell@stardust html]$

After the installation you need to open https://isabell.uber.space/index.php/setup in your browser to finish your setup.

Fill out your system settings, admin user and edit the following database settings:
 * Username: ``isabell``
 * Password from your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * Database: ``isabell_ip``

::

Best practices
==============

Security
--------

If you want to secure your installation, you may disable the setup for now. To do so, replace the line DISABLE_SETUP=false with DISABLE_SETUP=true in your ``ipconfig.php`` file.


Updates
=======

Check InvoicePlane's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation.

Backup your ``ipconfig.php`` file, delete everything else in your ``html`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp ipconfig.php ~
 [isabell@stardust html]$ rm -rf * .*

Proceed with the installation steps from here and move back your config file.

 [isabell@stardust html]$ mv ~/ipconfig.php ./
 [isabell@stardust html]$

Finish the update by open https://isabell.uber.space/index.php/setup in your browser.

.. _InvoicePlane: https://www.invoiceplane.com/
.. _stable releases: https://www.invoiceplane.com/downloads

----

Tested with osTicket 1.5.10 and Uberspace 7.4

.. author_list::
