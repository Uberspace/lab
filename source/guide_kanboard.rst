.. highlight:: console

.. author:: stratmaster <https://github.com/stratmaster>

.. sidebar:: Logo

  .. image:: _static/images/kanboard.svg
      :align: center

#######
Kanboard
#######

Kanboard_ is a free and open source Kanban project management software.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * domains_
  * PHP_
  * cron_

License
=======

The software is licensed under `MIT License`_. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

The domain you want to use must be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Clone the Kanboard code from GitHub_:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ git clone https://github.com/kanboard/kanboard ~/html
 Cloning into '/home/isabell/html'...
 remote: Enumerating objects: 76, done.
 remote: Counting objects: 100% (76/76), done.
 remote: Compressing objects: 100% (52/52), done.
 remote: Total 57743 (delta 28), reused 42 (delta 22), pack-reused 57667
 Receiving objects: 100% (57743/57743), 65.28 MiB | 11.89 MiB/s, done.
 Resolving deltas: 100% (37070/37070), done.
 [isabell@stardust ~]$



Configuration
=============

Setup your database
-------------------

We recommend setting up a new MySQL database for Kanboard.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE <username>_kanboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;;"

Configuration
-------------

Copy the ``config.default.php`` to ``config.php``:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust isabell]$ cd html
 [isabell@stardust html]$ cp config.default.php config.php
 [isabell@stardust html]$

Now edit ``config.php`` file, change the Database driver to ``mysql`` and provide your MySQL credentials.

.. code-block:: ini
 :emphasize-lines: 2,5,8,11,14

 // Database driver: sqlite, mysql or postgres (sqlite by default)
 define('DB_DRIVER', 'mysql');

 // Mysql/Postgres username
 define('DB_USERNAME', 'isabell');

 // Mysql/Postgres password
 define('DB_PASSWORD', 'MySuperSecretPassword');

 // Mysql/Postgres hostname
 define('DB_HOSTNAME', 'localhost');

 // Mysql/Postgres database name
 define('DB_NAME', 'isabell_kanboard');

Now, go to ``isabell.uber.space`` and log in to your installation with the default login ``admin`` and password ``admin``.

.. warning:: Do not forget to change the default user/password!

Check out the official `Kanboard documentation`_ for explanation of further configuration parameters.

Cron job
========

To work properly, Kanboard requires that a `background job`_ run on a daily basis. Edit your cron tab using the ``crontab -e`` command and insert this cron job to execute the daily cronjob at 8am. Make sure to replace ``isabell`` with your own user name.

::

  0 8 * * * cd /var/www/virtual/isabell/html && ./cli cronjob >/dev/null 2>&1

Tuning
=======

Plugins
-------

Get an overview of all available Plugins_ for Kanboard and install them from the user interface. More (unofficial) plugins may also be available, just browse GitHub.


Email Notifications
-------------------
To receive `email notifications`_, users of Kanboard `must have`_:

* Activated notifications in their profile
* Have a valid email address in their profile
* Be a member of the project that will trigger notifications

Set the email address used for the "From" header by changing the values in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2

 // E-mail address used for the "From" header (notifications)
 define('MAIL_FROM', 'isabell@uber.space');

Specify the URL of your Kanboard installation in your Application Settings to display a link to the task in notifications: ``http://isabell.uber.space/``. By default, nothing is defined, so no links will be displayed in notifications.

.. note:: Don’t forget the ending slash ``/``.

Debugging
---------

Enable debug mode by setting the following two values in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2

 // Enable/Disable debug
 define('DEBUG', true);

 // Available log drivers: syslog, stderr, stdout, system or file
 define('LOG_DRIVER', 'file');

The file ``debug.log`` will be found in the ``data`` folder of your Kanboard directory.


Updates
=======

You can regularly check the GitHub's Atom Feed_ for any new Kanboard releases. If a new version is available, ``cd`` to your Kanboard folder and do a simple ``git pull origin master``:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ git pull origin master
 Already up to date.
 [isabell@stardust html]$


.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _cron: https://manual.uberspace.de/en/daemons-cron.html
.. _DocumentRoot: https://manual.uberspace.de/en/web-documentroot.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _Kanboard: https://kanboard.org/
.. _MIT License: https://github.com/kanboard/kanboard/blob/master/LICENSE
.. _Kanboard documentation: https://docs.kanboard.org/en/latest/admin_guide/config_file.html
.. _background job: https://docs.kanboard.org/en/latest/admin_guide/cronjob.html
.. _Github: https://github.com/kanboard/kanboard
.. _Feed: https://github.com/kanboard/kanboard/releases.atom
.. _Plugins: https://kanboard.org/#plugins
.. _email notifications: https://docs.kanboard.org/en/latest/admin_guide/email.html
.. _must have: https://docs.kanboard.org/en/latest/user_guide/notifications.html
----

Tested with Kanboard 1.2.6, Uberspace 7.1.13.0

.. authors::
