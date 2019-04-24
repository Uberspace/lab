.. highlight:: console

.. author:: Daniel Kratz <uberlab@danielkratz.com>

.. sidebar:: Logo

  .. image:: _static/images/october.svg
      :align: center

##########
OctoberCMS
##########

October_ is a free, open-source, self-hosted CMS platform based on the Laravel_ PHP Framework. It is especially known for its simplicity, flexibility and modern design.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

The OctoberCMS platform is released under the `MIT License`_. All relevant information can be found in the LICENSE_ file in the repository of the project. Please also review the `Marketplace terms`_ if you plan to use plugins or themes from the official Marketplace.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We will install October using the official command-line interface (CLI). To do this simply ``cd`` into your :manual:`DocumentRoot <web-documentroot>` and use the the following command to download the install script using cURL and execute it with PHP.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust isabell]$ curl -s https://octobercms.com/api/installer | php
 All settings correct for installing OctoberCMS
 Downloading OctoberCMS...
 OctoberCMS successfully installed to: /var/www/virtual/$USER/html
 [isabell@stardust ~]$

The installer script will download all necessary files including the CLI so you can directly continue with the configuation of your October installation afterwards.

Configuration
=============

During the setup process you will be asked for database credentials. We use MySQL and suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for October to save your data. You have to create this database first using the following command.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_october"
 [isabell@stardust ~]$

To start the CLI that will guide you trough the setup use the ``october:install`` command.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ php artisan october:install
 [...]
 [isabell@stardust ~]$

The following list contains information on what you need to enter in the CLI setup:

    #. Database type: ``MySQL``
    #. MySQL host: ``localhost`` (default)
    #. MySQL port: ``3306`` (default)
    #. Database name: ``isabell_october`` (the name of the database you just created)
    #. MySQL login: ``isabell`` (your username)
    #. MySQL password: your MySQL password that you've got from ``my_print_defaults client``
    #. First name, Last name, Email adress: your account information
    #. Admin login: your admin username (to follow security best practices please don't use ``admin`` here)
    #. Admin password: your admin password (please choose a strong, secure password to prevent hacking of your installation)
    #. Confirm that the entered information is correct
    #. Application URL: the domain of your uberspace e.g. ``https://isabell.uber.space``
    #. Configure advanced options?: select no

With the confirmation of the last step October will setup your database and install a demo package.

You can now visit your domain and you will see the frontend of the installed demo package. To log in to the admin panel append ``/backend`` to your URL (e.g. ``https://isabell.uber.space/backend``).

Best practices
==============

You can use the October CLI which we used to setup your instace also to e.g. install plugins. See the `Console command list`_ to explore all possibilities.

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
.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE: https://github.com/octobercms/october/blob/master/LICENSE
.. _Marketplace terms: https://octobercms.com/help/terms/marketplace
.. _Console command list: https://octobercms.com/docs/console/commands

----

Tested with OctoberCMS 1.0.443, Uberspace 7.1.14

.. author_list::
