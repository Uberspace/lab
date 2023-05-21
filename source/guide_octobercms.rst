.. highlight:: console

.. author:: Daniel Kratz <https://danielkratz.com>

.. tag:: lang-php
.. tag:: web
.. tag:: cms
.. tag:: proprietary

.. sidebar:: Logo

  .. image:: _static/images/october.svg
      :align: center

##########
OctoberCMS
##########

.. tag_list::

October_ is an open-source, self-hosted CMS platform based on the Laravel_ PHP Framework. It is especially known for its simplicity, flexibility and modern design.
However, the CMS is no longer free software. The previous MIT License
has been changed to a proprietary EULA on `16 April 2021`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

The OctoberCMS platform is released under a proprietary EULA. All relevant information can be found in the LICENSE_ file in the repository of the project. Please also review the `Marketplace terms`_ if you plan to use plugins or themes from the official Marketplace.
Although the code is open source, it is not free software.
You're not allowed to modify it and are required to pay a
yearly license fee to continuously receive updates.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

You need to know your MySQL database user and password:

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

During the setup process you will be asked for database credentials. We use MySQL and suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for October to save your data. You have to create this database first using the following command.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_october"
 [isabell@stardust ~]$

We will install October using composer. First, make sure that your DocumentRoot is empty:

.. code-block:: console

 [isabell@stardust ~]$ rm html/nocontent.html
 [isabell@stardust ~]$

Initialize the composer project in your DocumentRoot:

.. code-block:: console

 [isabell@stardust ~]$ composer create-project october/october /var/www/virtual/$USER/html
 [...]
 [isabell@stardust ~]$

Change to your DocumentRoot and then start the installer:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ php artisan october:install


The CLI installer/setup will now ask you for various settings:

    #. Application URL: the domain of your uberspace e.g. ``https://isabell.uber.space``
    #. Backend URI: how you will access your backend, e.g. ``/backend``
    #. Database type: ``MySQL`` (default)
    #. MySQL host: ``localhost`` (default)
    #. MySQL port: ``3306`` (default)
    #. Database name: ``isabell_october`` (the name of the database you created earlier)
    #. MySQL login: ``isabell`` (your username)
    #. MySQL password: your MySQL password that you've got from ``my_print_defaults client``
    #. Include demo content, yes or no?
    #. License Key


Next, you will be asked to run artisan to migrate the database:

.. code-block:: console

 [isabell@stardust html]$ php artisan october:migrate

To finish installation, append the backend URI you set up earlier (e.g. ``https://isabell.uber.space/backend``). Here, you will be asked to set up the admin user.

Best practices
==============

You can use the October CLI which we used to setup your instance also to e.g. install plugins. See the `Console command list`_ to explore all possibilities.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version. You will also be notified in the October backend if Updates are available.

To update October and your installed plugins you can use the ``october:update`` CLI command in the root directory of the application. This will update the core application and plugin files, followed by a database migration.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ php artisan october:update
 Updating October...
 Found 1 new update!
 Downloading application files
 [...]
 [isabell@stardust ~]$


.. _October: https://octobercms.com/
.. _Laravel: https://laravel.com/
.. _feed: https://github.com/octobercms/october/releases.atom
.. _LICENSE: https://github.com/octobercms/october/blob/3.x/LICENSE.md
.. _Marketplace terms: https://octobercms.com/help/terms/marketplace
.. _Console command list: https://octobercms.com/docs/console/commands
.. _16 April 2021: https://github.com/octobercms/october/commit/1f1c0a3b8e2af6db9b8d7ff8f271dda4efec1a32

----

Tested with OctoberCMS 3.1.25, Uberspace 7.13, PHP 8.1

.. author_list::
