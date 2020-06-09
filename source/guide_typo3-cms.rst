.. author:: Tobias Stahn <hello@tstahn.io>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/typo3.png
      :align: center

#########
TYPO3 CMS
#########

.. tag_list::

`TYPO3 CMS`_ is an Open Source Enterprise Content Management System licensed under `GPL v2`_ and provides the basis for
more than 500.000 websites, intranets and other web applications worldwide.

First released in 1997 by Kasper Skårhøj, a Danish developer, when the term "Content Management" was still widely
unknown, it is represented today by the `TYPO3 Association`_ responsible for coordinating and funding the further
development of the platform.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual_anchor:`composer <lang-php.html#package-manager>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP_ in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

TYPO3 provides the directory ``public`` as web root since version 9.5, so we will install it next to the default :manual:`document root <web-documentroot>` and
use a symlink to make it accessible.

``cd`` into the directory above your document root ``/var/www/virtual/$USER/`` and set up a new project using :manual_anchor:`composer <lang-php.html#package-manager>`.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project "typo3/cms-base-distribution:^10.4" typo3-cms
 Creating a "typo3/cms-base-distribution:^10.4" project at "./typo3-cms"
 Installing typo3/cms-base-distribution (v10.4.1)
   - Installing typo3/cms-base-distribution (v10.4.1): Downloading (100%)
 Created project in /var/www/virtual/tstahn/typo3-cms
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 Package operations: 88 installs, 0 updates, 0 removals
   - Installing typo3/cms-composer-installers (v2.2.4): Downloading (100%)
   - Installing typo3/class-alias-loader (v1.0.2): Downloading (100%)
 [...]
 [isabell@stardust isabell]$

.. warning:: Please make sure your DocumentRoot is empty before removing it. This step will delete all contained files.

Now remove the :manual:`document root <web-documentroot>` and create a symlink to the ``public`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -rf html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/typo3-cms/public html
 [isabell@stardust isabell]$

Configuration
=============

Step 1
------

Point your browser to your website URL and append ``/typo3`` (e.g. isabell.uber.space/typo3). You will be greeted with a
"Thank you for choosing TYPO3" message.

Create an empty file ``FIRST_INSTALL`` (no file extension, all uppercase) inside your document root and reload the page
in your browser. You will be redirected to the TYPO3 Install Tool which will guide you through the remaining steps.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ touch FIRST_INSTALL

.. note:: In case you have any problems in your environment, you will get warnings or hints in this screen. In this case, you should try to fix them.

For the purpose of this guide we assume there are none, so we can proceed with the next step.

Step 2
------

Enter your database :manual_anchor:`credentials <database-mysql.html#login-credentials>`, keep the other settings unchanged, they are correct as they are.

Step 3
------

Create an :manual_anchor:`additional <database-mysql.html#additional-databases>` database - for example: ``isabell_typo3``.

Step 4
------

Enter a username and password for your first TYPO3 admin user (the password will also be configured for the Install Tool).

.. note:: For security reasons it's best to **not** use the name ``admin``.

Enter your email address. This is used in case you forget your password and need to reset it. Additionally it can be used
to notify you by email when somebody logs in from your account.

Choose a "site name" which will identify this installation (in the page tree and browser title).

Step 5
------

Choose whether you want to start with an empty TYPO3 installation (no pages, templates, configuration) or if you want
to have a preconfigured basis to start from.

Next Steps
==========

The basic installation procedure is now complete, TYPO3 will be up and running and the most appropriate settings will
have been made for you. You will get redirected to the TYPO3 Backend and can log in with the admin user account you
created earlier.

If you wish to make changes to your installation at a later stage, use the `Install Tool`_.

For further details, please have a look at the official `installation guide`_.

Updates
=======

.. warning:: Note that TYPO3 and especially any 3rd party packages are **not** updated automatically, you need to take care of that yourself.

To update TYPO3 ``cd`` into the directory you installed it in earlier and update using composer.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/typo3-cms
 [isabell@stardust typo3-cms]$ composer update typo3/cms-core

To update 3rd party packages, find the corresponding composer package name (e.g. from the official `TYPO3 extension repository`_),
and update the package.

In the example below assume ``georgringer/news`` is installed and is to be updated.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/typo3-cms
 [isabell@stardust typo3-cms]$ composer update georgringer/news

Subscribe to the `TYPO3 Announce`_ mailing list to get regular updates regarding new TYPO3 releases and security bulletins.

.. note:: This is a read-only mailing list, so you can neither reply nor post any messages yourself. If you have any questions or want to contribute join the `TYPO3 Slack`_.

You may also refer to the official Twitter account `@typo3_security`_ to stay up-to-date on security advisories.

.. _TYPO3 CMS: https://typo3.org/
.. _TYPO3 extension repository: https://extensions.typo3.org/
.. _GPL v2: https://www.gnu.org/licenses/gpl-2.0.html
.. _TYPO3 Association: https://typo3.org/project/association/
.. _PHP: http://www.php.net/
.. _Composer Helper: https://get.typo3.org/misc/composer/helper
.. _Install Tool: https://docs.typo3.org/typo3cms/InstallationGuide/master/In-depth/TheInstallTool/
.. _installation guide: https://docs.typo3.org/typo3cms/InstallationGuide/master/
.. _TYPO3 Announce: http://lists.typo3.org/cgi-bin/mailman/listinfo/typo3-announce
.. _@typo3_security: https://twitter.com/typo3_security
.. _TYPO3 Slack: https://typo3.slack.com/

----

Tested with TYPO3 10.4 LTS and Uberspace 7.6.0

.. author_list::
