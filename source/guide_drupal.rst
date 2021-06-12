.. highlight:: console

.. author:: Florian Latzel <https://netzaffe.de>
.. author:: Yannick Ihmels <yannick@ihmels.org>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. sidebar:: Logo

  .. image:: _static/images/Drupal-wordmark.svg
      :align: center

######
Drupal
######

.. tag_list::

.. abstract::
  Drupal_ is a free, web-based Open Source Content Management System (CMS) and Framework
  written in PHP and distributed under the GPL 2.0 (or later) licence.

  According to  W3Techs (2011-07-15), at least 2.3% of all websites worldwide are running with Drupal.

  Drupal 8 is based on Symfony_, a popular high performance PHP framework for web development.

  Drupal was released for the first time in 2000 by Dries Buytaert. Since then it has been
  continuously developed and it is actively maintained by various contributors.

----

.. note::  You should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * Composer_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`Cronjobs <daemons-cron>`


Prerequisites
=============

PHP 7.2
-------

We are using PHP in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

Database credentials
--------------------

.. include:: includes/my-print-defaults.rst

Domain
------

Your :manual_anchor:`website domain <web-domains.html#setup>` needs to be set up:

.. include:: includes/web-domain-list.rst

Database
--------

It's recommended to create an :manual_anchor:`additional database <database-mysql.html#additional-databases>`,
for example: ``isabell_drupal``.

Installation via Composer
-------------------------

``cd`` into the directory above your document root ``/var/www/virtual/$USER/`` and run ``composer``:

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project drupal/recommended-project drupal
 Installing drupal/recommended-project (8.8.4)
   - Installing drupal/recommended-project (8.8.4): Downloading (100%)
 Created project in drupal
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 Package operations: 56 installs, 0 updates, 0 removals
   - Installing drupal/core-composer-scaffold (8.8.4): Downloading (connecting...Downloading (100%)
   - Installing drupal/core-project-message (8.8.4): Downloading (100%)
 [...]

   Congratulations, you’ve installed the Drupal codebase
   from the drupal/recommended-project template!


 Next steps:
   * Install the site: https://www.drupal.org/docs/8/install
   * Read the user guide: https://www.drupal.org/docs/user_guide/en/index.html
   * Get support: https://www.drupal.org/support
   * Get involved with the Drupal community:
       https://www.drupal.org/getting-involved
   * Remove the plugin that prints this message:
       composer remove drupal/core-project-message
   * Homepage: https://www.drupal.org/project/drupal
   * Support:
     * docs: https://www.drupal.org/docs/user_guide/en/index.html
     * chat: https://www.drupal.org/node/314178
 [isabell@stardust isabell]$


Symlinks
--------

Since Drupal installation via Composer_ uses the subdirectory ``web/`` as the
document root of your website, you should **not** install Drupal in your default
:manual:`DocumentRoot <web-documentroot>`. Instead, we install it next to that and then use a
symbolic link to make it accessible to the web.

.. code-block:: console

 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/drupal/web/ html
 [isabell@stardust isabell]$


Installation
============

Open a browser and visit the URL of your domain. It's self-explanatory, for specific steps and
screenshots checkout `Running the Interactive Installer`_.


Configuration
=============

Trusted Host setting
--------------------

For Drupals protection against HTTP HOST Header attacks, you need to configure
`Trusted host security setting`_ in ``settings.php``, which was introduced in Drupal 8.

Add the following configuration to the ``settings.php`` file.

.. code-block:: php

 $settings['trusted_host_patterns'] = [
   '^isabell\.uber\.space$',
 ];


Cronjob
-------

For executing periodical tasks like updating the search index, purging old logs or checking for
updates, etc. you will need to set up a cronjob.

Get your cron URL for your site under Administration → Configuration → System → Cron. We create a
cronjob which runs every hour.

Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

 0 * * * * wget -O - -q -t 1 https://isabell.uber.space/cron/CsUKMfKtaFI8P3CaFpWy6iMIJPjjAwnm-Svs6wXb_LSrxqLnlbv85qy5us0YSnK3iQpthKoIrQ


Updates
=======

.. hint:: Configure update notifications under *Administration* → *Reports* → *Available updates* →
  *Settings* and subscribe to `Security advisories`_ and public service announcements too!

Core Updates
------------

.. note:: Also see section 13.5. `Updating the Core Software`_ of the Drupal User Guide and the
    article `Update core via Composer`_ for up-to-date instructions.

Allow access to ``update.php``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open ``/var/www/virtual/$USER/drupal/sites/default/settings.php``, find the line with the
``$settings['update_free_access']`` variable and set it to ``TRUE``.

Enable maintenance mode
^^^^^^^^^^^^^^^^^^^^^^^

In the Manage administrative menu, navigate to *Configuration* → *Development* → *Maintenance mode*,
enable the *Put site into maintenance mode* option and click on *Save configuration*.

Update via Composer
^^^^^^^^^^^^^^^^^^^

Update the Drupal Core packages with Composer:

.. code-block:: console

 [isabell@stardust isabell]$ cd /var/www/virtual/$USER/drupal
 [isabell@stardust drupal]$ composer update drupal/core --with-dependencies
 [isabell@stardust drupal]$

Run ``update.php``
^^^^^^^^^^^^^^^^^^

Visit ``https://isabel.uber.space/update.php`` and click *Continue* to run the update.

Deny access to ``update.php``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open ``/var/www/virtual/$USER/drupal/sites/default/settings.php``, find the line with the
``$settings['update_free_access']`` variable and set it to ``FALSE``.

Disable maintenance mode
^^^^^^^^^^^^^^^^^^^^^^^^

In the Manage administrative menu, navigate to *Configuration* → *Development* → *Maintenance mode*,
disable the *Put site into maintenance mode* option and click on *Save configuration*.

Clear caches
^^^^^^^^^^^^

In the Manage administrative menu, navigate to *Configuration* → *Development* → *Performance* and
click *Clear all caches*.


.. _Drupal: https://drupal.org
.. _Symfony: https://symfony.com
.. _Composer: https://getcomposer.org
.. _Running the Interactive Installer: https://www.drupal.org/docs/user_guide/en/install-run.html
.. _Trusted host security setting: https://www.drupal.org/docs/8/install/trusted-host-settings
.. _Security advisories: https://www.drupal.org/security
.. _Drush: https://www.drush.org
.. _Update core via Composer: https://www.drupal.org/node/2700999
.. _Updating the Core Software: https://www.drupal.org/docs/user_guide/en/security-update-core.html

----

Tested with Drupal 8.8.4 and Uberspace 7.5.0.0

.. author_list::
