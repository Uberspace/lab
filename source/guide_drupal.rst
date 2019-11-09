.. author:: Florian Latzel <https://netzaffe.de>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/Drupal-wordmark.svg
      :align: center

######
Drupal
######

.. tag_list::

Drupal_ is a free, web-based Open Source Content Management System (CMS) and Framework written in PHP and distributed under the GPL 2.0 or later licence.

According to  W3Techs (2011-07-15), at least 2.3% of all websites worldwide are running with Drupal.

As of Drupal 8, it is based on Symfony_, a popular high performance PHP framework for web development. 

Drupal was released for the first time in 2000 by Dries Buytaert. Since then it has been continuously developed and it is actively maintained by various contributors.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * Composer_


Prerequisites
=============


PHP 7.2
-------

We are using PHP_ in the stable version ``7.2``:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

Database credentials
--------------------

.. include:: includes/my-print-defaults.rst

Domain
------

Your :manual_anchor:`website domain <web-domains.html#setup>` needs to be set up:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.example
 isabell.uber.space
 [isabell@stardust ~]$

Create Database
---------------

Create an :manual_anchor:`additional <database-mysql.html#additional-databases>` database, for example: ``isabell_drupal``.


Installation
============

Since Drupal installation via Composer_ uses the subdirectory ``web/`` as web root of your website you should **not** install Drupal in your default Uberspace :manual:`DocumentRoot <web-documentroot>`. Instead, we install it next to that and then use a symlink to make it accessible to the web.

``cd`` into the directory above your document root ``/var/www/virtual/$USER/``

:: 
 
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/

Composer
--------

.. note:: The given Composer_ command uses the  `Drupal Composer Template`_  and  command always installs the latest stable release. 
   
  You might replace target parameter, here drupal with something more suitable.


.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust isabell]$ composer create-project drupal-composer/drupal-project:8.x-dev drupal --no-interaction
   - Installing drupal-composer/drupal-project (8.x-dev bdaa8fd): Cloning bdaa8fd53b from cache
 Created project in drupal
 > DrupalProject\composer\ScriptHandler::checkComposerVersion
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 [...]
 > DrupalProject\composer\ScriptHandler::createRequiredFiles
 Created a sites/default/settings.php file with chmod 0666
 Created a sites/default/files directory with chmod 0777
 [isabell@stardust isabell]$ 


Symlinks 
--------

tbd

install.php
-----------
 

Configuration
=============

tbd


Updates
=======

tbd



.. _Drupal: https://drupal.org/
.. _Symfony: https://symfony.com/
.. _PHP: http://www.php.net/
.. _Composer: https://getcomposer.org/
.. _Drupal Composer Template: https://github.com/drupal-composer/drupal-project
.. _News: https://www.drupal.org/news
.. _Planet Drupal: https://www.drupal.org/planet
.. _Security advisories: https://www.drupal.org/security
.. _download: https://www.drupal.org/download
.. _Git: https://git-scm.com/

----

Tested with Drupal 8.7.9 and Uberspace 7.3.7.0

.. author_list::
