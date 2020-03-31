.. highlight:: console

.. author:: Daniel Kratz <https://danielkratz.com>

.. tag:: lang-php
.. tag:: web
.. tag:: audience-business
.. tag:: accounting
.. tag:: time-tracking

.. sidebar:: Logo

  .. image:: _static/images/kimai.png
      :align: center

#########
Kimai
#########

.. tag_list::

Kimai_ is a free, open source time-tracking software written in PHP and designed for small businesses and freelancers.

The times tracked in the software can be directly priced, aggregated, invoiced and integrated in automated processes utilizing the RESTful API.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

Kimai is released under the `MIT License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2. Since new Uberspaces are currently setup with PHP 7.1 by default you need to set this version manually:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install Kimai we clone the current stable version using Git. ``cd`` to one level above your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will live next to ``html``.

Check the current `stable release`_ and copy the version number which you have to insert in the following ``git clone`` command.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone -b 1.8 --depth 1 https://github.com/kevinpapst/kimai2.git
 Cloning into 'kimai2'...
 […]
 [isabell@stardust ~]$

Install all neccessary dependencies using Composer. This can take some time.

::

 [isabell@stardust isabell]$ cd kimai2/
 [isabell@stardust kimai2]$ composer install --no-dev --optimize-autoloader
 Loading composer repositories with package information
 […]
 [isabell@stardust ~]$


Remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``kimai2/public`` directory:

.. warning:: Please make sure your DocumentRoot is empty before removing it. This step will delete all contained files if any.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -rf html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/kimai2/public html
 [isabell@stardust ~]$

Configuration
=============

To configure Kimai you need to edit the main configuration file ``/var/www/virtual/$USER/kimai2/.env``. Open this file with a text editor of your choice.

Edit the following parts of your configuration file:
 * replace the secret in the line starting with ``APP_SECRET`` by a random string
 * comment out the line starting with ``DATABASE_URL=sqlite`` (prefix the line with a ``#``)
 * comment in the line starting with ``DATABASE_URL=mysql`` (remove the ``#``)
 * in the same line replace the placeholders ``db_user``, ``db_password`` and ``db_name`` with your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * The finished configuration should look like this ``DATABASE_URL=mysql://isabell:SAFEPASSWORD@127.0.0.1:3306/isabell_kimai``

Save the changed file and start the installation using the Kimai console.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai2/
 [isabell@stardust kimai2]$ bin/console kimai:install -n
 Kimai installation running ...
 […]
 [isabell@stardust ~]$

Finishing installation
======================

Finish the installation by creating an admin user with the Kimai console. Insert your username and email adress in the shell command. You will be prompted to insert a password afterwards.

Please don't use ``admin`` as your username and set yourself a strong password.

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai2/
 [isabell@stardust kimai2]$ bin/console kimai:create-user <username> <admin@example.com> ROLE_SUPER_ADMIN
 Please enter the password: ****
 […]
 [isabell@stardust ~]$

That's it! You can now visit your website domain and login using your new account.

Best practices
==============

Security
--------

By default Kimai allows any visitor of your domain to register a new user account. You might want to diable that to prevent strangers in your Kimai instance. After disabling the anonymous registration you can still create new user accounts using the console.

Create a new configuration file called ``local.yml`` in ``config/packages/`` and insert the following configuration:

.. code-block:: yaml

 kimai:
    user:
        registration: false

Save the new file and clear the cache so the changes become active.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai2/
 [isabell@stardust kimai2]$ bin/console cache:clear --env=prod
 [isabell@stardust kimai2]$ bin/console cache:warmup --env=prod
 [isabell@stardust ~]$

To be sure if everything works check if the registration link is gone from your login page.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Kimai's `releases <https://github.com/kevinpapst/kimai2/releases>`_ for the latest versions. If a newer
version is available, you should manually update your installation.

To update your installation fetch the new release tags from GitHub and checkout the version you want to update to by using their version number in the ``git checkout`` command. Afterwards update your dependencies with composer.

.. code-block:: console
 :emphasize-lines: 3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai2/
 [isabell@stardust kimai2]$ git fetch --tags
 [isabell@stardust kimai2]$ git checkout 1.8
 [isabell@stardust kimai2]$ composer install --no-dev --optimize-autoloader
 [isabell@stardust ~]$

Now clear and warmup your cache.

::

 [isabell@stardust kimai2]$ bin/console cache:clear --env=prod
 [isabell@stardust kimai2]$ bin/console cache:warmup --env=prod
 [isabell@stardust ~]$

And last but not least: upgrade your database (you need to confirm the migration).

.. code-block:: console
 :emphasize-lines: 4

 [isabell@stardust kimai2]$ bin/console doctrine:migrations:migrate
 Application Migrations
 WARNING! You are about to execute a database migration that could result in schema changes and data loss.
 Are you sure you wish to continue? (y/n)
 [isabell@stardust ~]$

.. warning:: It is possible that some version jumps require specific actions. Always check the `UPGRADE guide <https://github.com/kevinpapst/kimai2/blob/master/UPGRADING.md>`_ and the release notes before updating your instance.


.. _Kimai: https://www.kimai.org/
.. _feed: https://github.com/kevinpapst/kimai2/releases.atom
.. _MIT License: https://opensource.org/licenses/MIT
.. _stable release: https://github.com/kevinpapst/kimai2/releases
.. _LICENSE: https://github.com/kevinpapst/kimai2/blob/master/LICENSE

----

Tested with Kimai 1.8 and Uberspace 7.5.0

.. author_list::
