.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web
.. tag:: forum

.. sidebar:: Logo

  .. image:: _static/images/flarum.png
      :align: center

######
Flarum
######

.. tag_list::

Flarum_ is the next-generation forum software that makes online discussion fun. It's simple, fast, and free.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 8.0:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.0'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We create the database and install Flarum using composer.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_flarum"
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project flarum/flarum flarum --stability=beta
 […]
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s flarum/public html
 [isabell@stardust isabell]$

Configuration
=============

After the installation you need to open isabell.uber.space/public in your browser to finish your setup.

Fill out your forum title, admin user and edit the following database settings:
 * MySQL Database: ``isabell_flarum``
 * MySQL Username: ``isabell``
 * MySQL Password from your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`

.. _Flarum: https://flarum.org/

----

Tested with Flarum v0.1.0-beta.13 and Uberspace 7.10.0

.. author_list::
