.. author:: Lukas Herzog <hallo@lukasherzog.de>

.. tag:: lang-php
.. tag:: web
.. tag:: calendar
.. tag:: scheduler


.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/easyappointments.png
      :align: center

######################
Easy Appointments
######################

.. tag_list::

`Easy Appointments`_ is an open source web application for booking / scheduling appointments. It allows many customization options and use-cases and provides optional sync to Google Calendar.

Easy Appointments was first released 2016 and is maintained by Alex Tselegidis. It is distributed under GPL 3.0.



----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Easy Appointments works fine with any current (> 7.0) version of PHP.

.. include:: includes/my-print-defaults.rst

We suggest using an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. Create one with:

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_ea"

Your domain needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

``cd`` into your :manual:`document root <web-documentroot>` and download the latest build, unzip and remove the zip file:

.. code-block:: console
 :emphasize-lines: 1,2,3,4

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/alextselegidis/easyappointments/releases/download/1.3.2/easyappointments_1.3.2.zip
 [isabell@stardust html]$ unzip easyappointments_1.3.2.zip
 [isabell@stardust html]$ rm easyappointments_1.3.2.zip

Configuration
=============

To get started set some basic configuration variables. Edit ``/var/www/virtual/$USER/html/config.php``

In here you need to enter your :manual_anchor:`MySQL credentials <database-mysql.html#login-credentials>` database connection parameters and the name of your database (e.g. ``isabell_ea``).

.. code-block:: ini
 :emphasize-lines: 4,12,13,14,15

 // GENERAL SETTINGS
 // ------------------------------------------------------------------------

 const BASE_URL      = 'isabell.uber.space';
 const LANGUAGE      = 'english';
 const DEBUG_MODE    = FALSE;

 // ------------------------------------------------------------------------
 // DATABASE SETTINGS
 // ------------------------------------------------------------------------

 const DB_HOST       = 'localhost';
 const DB_NAME       = 'isabell_app';
 const DB_USERNAME   = 'isabell';
 const DB_PASSWORD   = 'MySuperSecretPassword';

Finishing installation
======================

Point your browser to your domain, ``https://isabell.uber.space/`` in this example, to start the installation process. Here you will

 * Choose a Site title
 * Set a administrative account and password

Your site is now ready to use.


Updates
=======

missing

.. note:: Check the update _feed regularly to stay informed about the newest version.




.. _`Easy Appointments`: https://easyappointments.org/
.. _PHP: http://www.php.net/
.. _feed: https://github.com/alextselegidis/easyappointments/releases/


----

Tested with Easy Appointments 1.3.2, Uberspace 7.7.7

.. author_list::
