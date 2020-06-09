.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. sidebar:: Logo

  .. image:: _static/images/eqdkp-plus.svg
      :align: center

##########
EQdkp Plus
##########

.. tag_list::

EQdkp-Plus_ is an open source Content Management System (CMS) and Guild Management System in PHP and distributed under the AGPLv3 licence.
It is focused on supporting guilds and clans playing online games, especially MMORPGs. Therefore it brings tools for planning raids or distributing loot or points like DKP (Dragon Kill Points).

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

If you want to use your EQdkp Plus with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of EQdkp Plus and extract it:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ curl -L https://eqdkp-plus.eu/repository/download/latestcore -o eqdkp-plus.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 25565    0 25565    0     0  22942      0 --:--:--  0:00:01 --:--:-- 22948
  100 5138k  100 5138k    0     0   769k      0  0:00:06  0:00:06 --:--:-- 1108k
 [isabell@stardust html]$ unzip eqdkp-plus.zip && rm eqdkp-plus.zip
 [isabell@stardust html]$

Now point your browser to your uberspace URL and follow the instructions of the Installer Assistant.

You will need to enter the following information:
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your EQdkp Plus database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_eqdkp
  * an encryption key: choose a strong encryption key, as sensitive data is encrypted using this key. You can generate a strong key using ``openssl``:

  ::

   [isabell@stardust html]$ openssl rand -base64 32
   SuperSecretPassword
   [isabell@stardust html]$

  * Make additional settings like setting first day of week etc. The script path setting is automatically detected and only needs to be changed if the detection will fail. The script path is the subfolder of your domain. If you follow this tutorial, it is ``/``.
  * Administrator username and password: choose a username (maybe not *admin*) and a strong password for the admin user


Updates
=======

The easiest way to update EQdkp Plus is to use the web updater provided in the admin section of the Web Interface.

.. note:: Check the `news <https://eqdkp-plus.eu/>`_ regularly to stay informed about new updates and releases.

.. _EQdkp-Plus: https://eqdkp-plus.eu

----

Tested with EQdkp Plus 2.3.0.26, Uberspace 7.1.3

.. author_list::
