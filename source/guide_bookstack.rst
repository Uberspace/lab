.. highlight:: console

.. author:: Daniel Kratz <https://danielkratz.com>

.. tag:: lang-php
.. tag:: web
.. tag:: wiki

.. sidebar:: Logo

  .. image:: _static/images/bookstack.svg
      :align: center

##########
BookStack
##########

.. tag_list::

BookStack_ is a simple, self-hosted, easy-to-use platform for organising and storing information (wiki).

It is specially designed to allow new users with basic word-processing skills to get involved in creating content. However, it offers advanced power features for users who need them.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

BookStack is released under the `MIT License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

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

To install BookStack clone the release branch of the official repository one level above your :manual:`DocumentRoot <web-documentroot>` using Git.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone https://github.com/BookStackApp/BookStack.git --branch release --single-branch
 Cloning into 'BookStack'...
 remote: Enumerating objects: 53, done.
 […]
 [isabell@stardust ~]$

``cd`` into your BookStack directory and install the necessary dependencies using Composer_.

.. code-block:: console

 [isabell@stardust isabell]$ cd BookStack
 [isabell@stardust isabell]$ composer install --no-dev
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 Package operations: 103 installs, 0 updates, 0 removals
 […]
 [isabell@stardust ~]$

Configuration
=============

We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` for BookStack to save your data. You have to create this database first.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_bookstack"
 [isabell@stardust ~]$

Copy the sample configuration file ``.env.example``. Then edit the ``.env`` file and change the values of ``DB_DATABASE``, ``DB_USERNAME``, ``DB_PASSWORD`` to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` and save the file.


.. code-block:: console

 [isabell@stardust BookStack]$ cp .env.example .env
 [isabell@stardust ~]$

.. note:: You can optionally configure BookStack to send emails in the same place.

To make your BookStack installation safe you need to create a unique application key (a random, 32-character string used e.g. to encrypt cookies). Make sure to confirm the command with ``yes``.

.. code-block:: console
 :emphasize-lines: 7

 [isabell@stardust BookStack]$ php artisan key:generate
 **************************************
 *     Application In Production!     *
 **************************************

  Do you really wish to run this command? (yes/no) [no]:
  > yes

 Application key set successfully.
 [isabell@stardust ~]$

Remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``BookStack/public`` directory.

.. warning:: Please make sure your DocumentRoot is empty before removing it. This step will delete all contained files if any. You can also rename the folder to something that's not ``html``.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/BookStack/public html
 [isabell@stardust isabell]$

Now use the following command to create and populate the tables in your database. Confirm the command with ``yes``.

.. code-block:: console
 :emphasize-lines: 7

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/BookStack
 [isabell@stardust BookStack]$ php artisan migrate
 **************************************
 *     Application In Production!     *
 **************************************
 Do you really wish to run this command? (yes/no) [no]:
 > yes
 Migration table created successfully.
 [...]
 [isabell@stardust ~]$

Finishing installation
======================

After the configuration you can now login by visiting your domain and using the default login ``admin@admin.com`` with the password ``password``. Change this standard user directly after your first login.

.. warning:: Change the standard user directly after your first login and use a strong password to prevent others from hacking your instance.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version. Detailed information on releases is posted on the `BookStack blog`_.

To update BookStack you can run the following command in the root directory of the application. This will update your installation via Git, install new dependencies via Composer and migrate your database. It's possible that you need to confirm the steps while updating.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/BookStack
 [isabell@stardust BookStack]$ git pull origin release && composer install --no-dev && php artisan migrate
 From https://github.com/BookStackApp/BookStack
 * branch            release    -> FETCH_HEAD
 [...]
 [isabell@stardust ~]$

After updating your installation you should clean the cache to prevent errors.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/BookStack
 [isabell@stardust BookStack]$ php artisan cache:clear
 Cache cleared successfully.
 [isabell@stardust BookStack]$ php artisan view:clear
 Compiled views cleared!
 [isabell@stardust ~]$

.. _BookStack: https://www.bookstackapp.com
.. _Composer: https://getcomposer.org/
.. _feed: https://github.com/BookStackApp/BookStack/releases.atom
.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE: https://github.com/BookStackApp/BookStack/blob/master/LICENSE
.. _BookStack blog: https://www.bookstackapp.com/tags/releases/

----

Tested with BookStack 0.24.1 Beta, Uberspace 7.1.15

.. author_list::
