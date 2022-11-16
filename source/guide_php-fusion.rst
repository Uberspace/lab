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

.. tag_list::

PHP-Fusion_ is a CMS written in PHP and distributed under the GNU AGPL v3 licence.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

MySQL
-----

.. include:: includes/my-print-defaults.rst

We advise you set up an additional database for PHP Fusion:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_phpfusion"
 [isabell@stardust ~]$


Domain
------

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First get the PHP-Fusion source code from Sourceforge_:

::

  [isabell@stardust ~]$ wget -O phpf9.zip https://sourceforge.net/projects/php-fusion/files/latest/download
  [isabell@stardust ~]$ unzip phpf9.zip
  [isabell@stardust ~]$ mv files/* /var/www/virtual/$USER/html
  [isabell@stardust ~]$ rm -rf files/
  [isabell@stardust ~]$ rm phpf9.zip



Finishing installation
======================

Point your browser to your domain, for example https://isabell.uber.space and follow the installation instructions.

After finishing the installation and logging into PHP-Fusion you will see a red warning box.

To remove the file install.php enter

::

 [isabell@stardust ~]$ rm /var/www/virtual/$USER/html/install.php
 [isabell@stardust ~]$

----

Tested with PHP-Fusion v9.10.30, PHP 8.1 and Uberspace 7.13.0

.. _PHP-Fusion: https://php-fusion.co.uk
.. _Sourceforge: https://sourceforge.net/projects/php-fusion/files/latest/download
.. author_list::
