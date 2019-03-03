.. author:: Willi Mutschler <willi@mutschler.eu>
.. highlight:: console
.. sidebar:: Logo

  .. image:: _static/images/joomla.png
      :align: center

#########
Joomla!
#########

Joomla_ is a free and open-source content management system (CMS) for publishing web content, developed by Open Source Matters, Inc. It is built on a model–view–controller web application framework that can be used independently of the CMS. Joomla_ is distributed under the GPLv2 license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use Joomla! with your own domain you need to setup your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of *Joomla!* and extract it:

.. note:: The link to the lastest version can be found at Joomla!'s `download page <https://downloads.joomla.org/>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://downloads.joomla.org/cms/joomla3/3-8-12/Joomla_3-8-12-Stable-Full_Package.zip
 [isabell@stardust html]$ unzip Joomla_3-8-12-Stable-Full_Package.zip

Now point your browser to your uberspace URL or domain and follow the instructions.

You will (at least) need to enter the following information:

Page 1 - Configuration:
  * Site Name: Enter the name of your website, e.g. ``isabell.uber.space``
  * Email: Enter the email address of the website administrator, e.g. ``isabell@uber.space``
  * Username: Set the user name of the administrator account, e.g. ``admin``
  * Password and Confirm Administrator Password: Set the password of the administrator account, e.g. ``superstrongadminpassword``

Page 2 - Database Configuration:
  * Database Type: Set it to ``MySQLi``
  * Host Name: ``localhost``
  * Username: ``isabell`` 
  * Password: ``yourMySQLPassword`` (you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now; if you don't, start reading again at the top.)
  * Database Name: your Joomla! database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: ``isabell_joomla``
  * Table Prefix: just stick to the randomly generated one
  * Old Database Process: ``Backup`` to be sure

Page 3 - Finalization
  * Install Sample Data: up to you...
  * Email Configuration: up to you...
  * Check that all Pre-Installation Checks are fullfilled (a green ``Yes``)
  * Check that all Recommended Settings are fullfilled (for me the only difference was ``Output Buffering`` which is recommended to *off*, but is *on* in my case -- it does not matter, Joomla! will still operate)
  
Hit ``Install``!
You should see a message ``Congratulations! Joomla! is now installed``
You can also install optionally extra languages by clicking on ``Extra steps: Install languages``

*Important*: Click ``Remove installation folder``. You will not be able to proceed beyond this point until the installation folder has been removed. This is a security feature of Joomla!

Tuning [under construction]
===========================

  * Check the Post-installation Messages for any hints and errors
  * ...

Updates
=======

The easiest way to update Joomla! is to use the web updater provided in the admin section of your website, e.g. ``isabell.uber.space/administrator``

.. _Joomla: https://www.joomla.org/

----

Tested with Joomla! 3.8.12, Uberspace 7.1.12

.. authors::
