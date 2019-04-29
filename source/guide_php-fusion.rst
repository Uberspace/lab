.. author:: DwB <dirk@babig.de>
.. highlight:: console

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. sidebar:: Logo

  .. image:: _static/images/php-fusion.png
      :align: center

##########
PHP-Fusion
##########

PHP-Fusion_ is a CMS written in PHP and distributed under the GN AGPL v3 licence.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Domain
------

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First get the PHP-Fusion source code from Github_:

::

  [isabell@stardust ~]$ git clone https://github.com/PHP-Fusion/PHP-Fusion html
  Cloning into 'html'...
  remote: Enumerating objects: 140, done.
  remote: Counting objects: 100% (140/140), done.
  remote: Compressing objects: 100% (121/121), done.
  remote: Total 88715 (delta 54), reused 62 (delta 18), pack-reused 88575
  Receiving objects: 100% (88715/88715), 111.94 MiB | 14.20 MiB/s, done.
  Resolving deltas: 100% (61743/61743), done.
  [isabell@stardust ~]$

  
Finishing installation
======================

Point your browser to your domain for example https://isabell.uber.space
Complete the form and follow the installation instructions.

After finishing the installation and logging into PHP-Fusion you will see a red warning box.

To remove the file install.php enter

::

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ rm install.php
 [isabell@stardust html]$
 
----

Tested with PHP-Fusion v9.10.00 and Uberspace 7.2.8.2

.. authors::
