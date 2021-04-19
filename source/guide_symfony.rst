.. highlight:: console

.. author:: Sascha Groetzner <https://groetzner.net>

.. tag:: web
.. tag:: lang-php

.. sidebar:: Logo

  .. image:: _static/images/symfony.svg
      :align: center

##########
Symfony
##########

.. tag_list::

`Symfony <https://symfony.com/what-is-symfony>`_ is a set of PHP Components, a Web Application framework, a Philosophy, and a Community — all working together in harmony.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`PHP <lang-php>`

License
=======

Symfony Source Code is published under the terms of the MIT License

  * `<https://symfony.com/license>`_

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.0'
 [isabell@stardust ~]$

Your symfony URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install symfony cli
-------------------

::

 [isabell@stardust ~]$ wget https://get.symfony.com/cli/installer -O - | bash -s -- --install-dir $HOME/bin

Modify ``~/.bash_profile`` to use symfony directly

.. code-block:: ini

 ...
 # User specific environment and startup programs

 PATH=$HOME/.local/bin:$HOME/bin:$PATH
 PATH="$HOME/.symfony/bin:$PATH"
 export PATH


Create symfony project
----------------------

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/
 [isabell@stardust isabell]$ symfony new my_project
 * Creating a new Symfony project with Composer
   (running /usr/local/bin/composer create-project symfony/skeleton /var/www/virtual/isabell/my_project  --no-interaction)
 * Setting up the project under Git version control
   (running git init /var/www/virtual/isabell/my_project)
 [OK] Your project is now ready in /var/www/virtual/isabell/my_project

Adding Rewrite Rules

::

 [isabell@stardust isabell]$ composer require symfony/apache-pack
 -  WARNING  symfony/apache-pack (>=1.0): From github.com/symfony/recipes-contrib:master
    The recipe for this package comes from the "contrib" repository, which is open to community contributions.
    Review the recipe at https://github.com/symfony/recipes-contrib/tree/master/symfony/apache-pack/1.0

    Do you want to execute this recipe?
    [y] Yes
    [n] No
    [a] Yes for all packages, only for the current installation session
    [p] Yes permanently, never ask again for this project
    (defaults to n): y
  - Configuring symfony/apache-pack (>=1.0): From github.com/symfony/recipes-contrib:master
 Executing script cache:clear [OK]
 Executing script assets:install public [OK]

 Some files may have been created or updated to configure your new packages.
 Please review, edit and commit them: these files are yours.

 Nothing to unpack

Configuration
=============

Configure the web server
------------------------

We connect our symfony public folder to our web server

::

 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/my_project/public /var/www/virtual/isabell/html/

Finishing installation
======================

Point your browser to URL and build up your project.

Best practices
==============

Security
--------

Per default you are in DEV-mode, so please restrict public-access or switch to PROD-mode.
Modify ``/var/www/virtual/isabell/my_project/.env`` and replace ``APP_ENV=dev`` with ``APP_ENV=prod``

To enable debugging only for your developer ip, use the ``SetEnvIf`` in the ``/var/www/virtual/isabell/my_project/public/.htaccess``
For example we are using a subnet 123.456.789.0/24 for debugging:

.. code-block:: ini

 SetEnvIf Remote_Addr "^123.456.789.*" APP_ENV dev

Logging
-------

We can use Monolog to log all of our messages

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/my_project
 [isabell@stardust my_project]$ composer require symfony/monolog-bundle

Now you can configure your logging as needed: `Symfony Logging <https://symfony.com/doc/current/logging.html>`_


Debug
=====

Install the debug-package within our dev-environment

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/my_project
 [isabell@stardust my_project]$ composer require --dev debug-pack

To see the Debugger we have to disable the uberspace-error-page

::

 [isabell@stardust ~]$ uberspace web errorpage 500 disable
 Error page for HTTP 500 is disabled.

Updates
=======

symfony check:security

.. note:: Check the update `Releases <https://symfony.com/blog/category/releases>`_ regularly to stay informed about the newest version.

Check whether your project’s dependencies contain any known security vulnerability:

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/my_project
 [isabell@stardust my_project]$ symfony check:security
 Symfony Security Check Report
 =============================

 No packages have known vulnerabilities.

 Note that this checker can only detect vulnerabilities that are referenced in the security advisories database.
 Execute this command regularly to check the newly discovered vulnerabilities.

----

Tested with Symfony 5.2.6, Uberspace 7.10.0

.. author_list::
