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

We're using PHP in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install Kimai we clone the current stable version using Git. ``cd`` to one level above your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will live next to ``html``.

Check the current `stable release`_ and copy the version number which you have to insert in the following ``git clone`` command.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone -b 1.30.11 --depth 1 https://github.com/kimai/kimai.git
 Cloning into 'kimai'...
 […]
 [isabell@stardust ~]$

Install all necessary dependencies using Composer. This can take some time.

::

 [isabell@stardust isabell]$ cd kimai/
 [isabell@stardust kimai]$ composer install --no-dev --optimize-autoloader
 Loading composer repositories with package information
 […]
 [isabell@stardust ~]$


Remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``kimai/public`` directory:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/kimai/public html
 [isabell@stardust ~]$

Configuration
=============

To configure Kimai you need to edit the main configuration file ``/var/www/virtual/$USER/kimai/.env``. Open this file with a text editor of your choice.

Edit the following parts of your configuration file:
 * replace the secret in the line starting with ``APP_SECRET`` by a random string
 * comment in the line starting with ``DATABASE_URL=mysql`` (remove the ``#``)
 * in the same line replace the placeholders ``db_user``, ``db_password`` and ``db_name`` with your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * The finished configuration should look like this ``DATABASE_URL=mysql://isabell:SAFEPASSWORD@127.0.0.1:3306/isabell_kimai``

Save the changed file and start the installation using the Kimai console.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai/
 [isabell@stardust kimai]$ bin/console kimai:install -n
 Kimai installation running ...
 […]
 [isabell@stardust ~]$

Finishing installation
======================

Finish the installation by creating an admin user with the Kimai console. Insert your username and email address in the shell command. You will be prompted to insert a password afterwards.

Please don't use ``admin`` as your username and set yourself a strong password.

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai/
 [isabell@stardust kimai]$ bin/console kimai:user:create <username> <admin@example.com> ROLE_SUPER_ADMIN
 Please enter the password: ****
 […]
 [isabell@stardust ~]$

That's it! You can now visit your website domain and login using your new account.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Kimai's `releases <https://github.com/kimai/kimai/releases>`_ for the latest versions. If a newer
version is available, you should manually update your installation.

To update your installation fetch the new release tags from GitHub and checkout the version you want to update to by using their version number in the ``git checkout`` command. Afterwards update your dependencies with composer.

.. code-block:: console
 :emphasize-lines: 3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/kimai/
 [isabell@stardust kimai]$ git fetch --tags
 [isabell@stardust kimai]$ git checkout 1.30.11
 [isabell@stardust kimai]$ composer install --no-dev --optimize-autoloader
 [isabell@stardust ~]$

Now clear and warmup your cache.

::

 [isabell@stardust kimai]$ bin/console kimai:reload -n
 [isabell@stardust ~]$

And last but not least: upgrade your database (you need to confirm the migration).

.. code-block:: console
 :emphasize-lines: 4

 [isabell@stardust kimai]$ bin/console kimai:update -n
 [isabell@stardust ~]$

.. warning:: It is possible that some version jumps require specific actions. Always check the `UPGRADE guide <https://github.com/kimai/kimai/blob/master/UPGRADING.md>`_ and the release notes before updating your instance.


.. _Kimai: https://www.kimai.org/
.. _feed: https://github.com/kimai/kimai/releases.atom
.. _stable release: https://github.com/kimai/kimai/releases
.. _LICENSE: https://github.com/kimai/kimai/blob/master/LICENSE
.. _MIT License: https://opensource.org/licenses/MIT

----

Tested with Kimai 1.30.11, Uberspace 7.15.0, and PHP 8.1

.. author_list::
