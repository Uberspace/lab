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

Drupal_ is a free, web-based Open Source Content Management System (CMS) and Framework 
written in PHP and distributed under the GPL 2.0 (or later) licence.

According to  W3Techs (2011-07-15), at least 2.3% of all websites worldwide are running with Drupal.

Drupal 8 is based on Symfony_, a popular high performance PHP framework for web development. 

Drupal was released for the first time in 2000 by Dries Buytaert. Since then it has been continuously developed and it is actively maintained by various contributors.

----

.. note:: This guide is about installing Drupal 8 via `Drupal Composer Template`_.

.. note::  You should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * Composer_
  * :manual:`Cronjobs <daemons-cron>`


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

Database
--------

Create an :manual_anchor:`additional <database-mysql.html#additional-databases>` database, for example: ``isabell_drupal``.

Composer
--------

.. note:: The given Composer_ command uses the  `Drupal Composer Template`_  and installs the latest stable release. 
   
  You might replace target parameter ``drupal`` with something more suitable.


``cd`` into the directory above your document root ``/var/www/virtual/$USER/`` to run to ``composer`` command:

.. code-block:: console
 :emphasize-lines: 1,2,12

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
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

Since Drupal installation via Composer_ uses the subdirectory ``web/`` 
as web root of your website you should **not** install Drupal in your default Uberspace 
:manual:`DocumentRoot <web-documentroot>`. 
Instead, we install it next to that and then use a symbolic link to make it accessible to the web.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust isabell]$ rmdir  html
 [isabell@stardust isabell]$ ln -s drupal/web/ html
 [isabell@stardust isabell]$ ln -s drupal/web/ isabell.example

RewriteBase
-----------

Edit ``/var/www/virtual/$USER/drupal/web/.htaccess``, search for ``# RewriteBase /`` and remove the leading ``#`` to activate this statement.

::

  RewriteBase /


SCM
---

It is a very good time to initialise a repository within the ``drupal`` directory.
This step is optional but highly recommended ;-D 

drush
-----

In order to make use  of Drupal Composer Template's drush_, 
you will add the path of your Drupal Composer Template's bin directory, 
which contains drush´s executable to the PATH environment variable. 
It will detect *DRUPAL_ROOT*.

Place the following statement to the startup file of your shell, e.g. ``~/.bashrc`` or ``~/.zshrc``:

::

  export PATH=$PATH:/var/www/virtual/$USER/drupal/vendor/bin

Create a configuration file for drush.

::

  mkdir ~/.drush
  cp /var/www/virtual/$USER/drupal/vendor/drush/drush/examples/example.drush.yml ~/.drush/drush.yml

Add *uri* option to your drush configuration.

This is useful for some commands which generate urls, like ``drush uli``. Edit ``~/.drush/drush.yml``, search for ``uri:`` and place the following statement below the matching line.

::

  uri: 'https://isabell.example'

If you use more than one codebase, you will need install drush_launcher_.
  

Installation
============

There are at least two different ways to install Drupal:


Interactive Installer
---------------------

Open a browser and visit the URL of your domain.
It is self-explanatory, for specific steps and screenshots checkout `Running the Interactive Installer`_.


drush site:install
------------------

Do it via Drush at the command line, see `drush site\:install`_ for details.


Configuration
=============

Trusted Host setting
--------------------

For Drupals protection against HTTP HOST Header attacks,
you need to configure `Trusted host security setting`_ in ``settings.php``, which was introduced in Drupal 8.

Insert this configuration for the domains given above:

::

  $settings['trusted_host_patterns'] = [
    '^isabell\.example$',
    '^isabell\.uber\.space$',
  ];


Cronjob
-------

For executing periodical tasks like e.g. updatíng the search index, purging old logs or checking for updates,
you will need to create a cronjob. 

Get your cron url for your site at ``Administration > Configuration > System > Cron (/admin/config/system/cron)``.
We create a cronjob with above url which runs once a day:

::

  [isabell@stardust isabell]$ crontab -e 

::
  
  4 0 * * * wget -O - -q -t 1 https://isabell.example/cron/CsUKMfKtaFI8P3CaFpWy6iMIJPjjAwnm-Svs6wXb_LSrxqLnlbv85qy5us0YSnK3iQpthKoIrQ

Updates
=======

.. note:: For Drupal core and contrib updates, configure ``Reports > Available updates > Settings (/admin/reports/updates/settings)`` within your site
 and subscribe `Security advisories`_ and public service announcements too!

Core Updates
------------

In case of Core updates see the `Updating Drupal Core` section of `Drupal Composer Template`_.

Contrib Updates
---------------

Updates of contributed modules work like this, e.g. for the ``geofield`` contrib:

::
  
  [isabell@stardust drupal]$ composer update drupal/geofield --with-dependencies


.. _Drupal: https://drupal.org/
.. _Symfony: https://symfony.com/
.. _PHP: http://www.php.net/
.. _Composer: https://getcomposer.org/
.. _Vim: https://www.vim.org/
.. _Running the Interactive Installer: https://www.drupal.org/docs/user_guide/en/install-run.html
.. _drush site\:install: https://drushcommands.com/drush-9x/site/site:install/
.. _Trusted host security setting: https://www.drupal.org/docs/8/install/trusted-host-settings
.. _Drupal Composer Template: https://github.com/drupal-composer/drupal-project
.. _Security advisories: https://www.drupal.org/security
.. _Updating Drupal Core: https://github.com/drupal-composer/drupal-project#updating-drupal-core
.. _drush: https://www.drush.org/
.. _drush_launcher: https://github.com/drush-ops/drush-launcher

----

Tested with Drupal 8.7.9 and Uberspace 7.3.7.0

.. author_list::
