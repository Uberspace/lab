.. highlight:: console

.. author:: stratmaster <https://github.com/stratmaster>

.. sidebar:: Logo

  .. image:: _static/images/kanboard.svg
      :align: center

########
Kanboard
########

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

Download and extract TAR.GZ archive
-----------------------------------

Check the Kanboard_ website or GitHub_ for the `latest release`_ and copy the download link to the TAR.GZ file. Then ``cd`` to your DocumentRoot_ and use ``wget`` to download it. Replace the URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/kanboard/kanboard/archive/v42.23.1.tar.gz
 […]
 Saving to: ‘v42.23.1.tar.gz’

 100%[========================================================================================================================>] 3,172,029   3.45MB/s   in 0.9s

 2018-10-11 14:48:20 (3.45 MB/s) - 'v42.23.1.tar.gz' saved [3172029]
 [isabell@stardust isabell]$

Untar the archive to the ``html`` folder and then delete it. Replace the version in the file name with the one you downloaded.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust isabell]$ tar -xzf v42.23.1.tar.gz -C html/ --strip-components=1
 [isabell@stardust isabell]$ rm v42.23.1.tar.gz
 [isabell@stardust isabell]$


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

Go to ``https://isabell.uber.space/`` and log in to your installation with the default login ``admin`` and password ``admin``.

.. warning:: Do not forget to change the default user/password!

Check out the official `Kanboard documentation`_ for explanation of further configuration parameters.

Cron job
========

To work properly, Kanboard requires that a `background job`_ runs on a daily basis. Edit your cron tab using the ``crontab -e`` command and insert this cron job to execute the daily cronjob at 8am. Make sure to replace ``isabell`` with your own user name.

::

  0 8 * * * cd /var/www/virtual/isabell/html && ./cli cronjob >/dev/null 2>&1

Best practices
==============

Plugins
-------

Get an overview of all available Plugins_ for Kanboard and install them from the user interface. More (unofficial) plugins may also be available, just browse GitHub.


Email Notifications
-------------------
To receive `email notifications`_, users of Kanboard `must have`_:

* Activated notifications in their profile
* Have a valid email address in their profile
* Be a member of the project that will trigger notifications

Set the email address used for the "From" header by changing the value in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2

 // E-mail address used for the "From" header (notifications)
 define('MAIL_FROM', 'isabell@uber.space');

Specify the URL of your Kanboard installation in your Application Settings to display a link to the task in notifications: ``https://isabell.uber.space/``. By default, nothing is defined, so no links will be displayed in notifications.

.. note:: Don’t forget the ending slash ``/``.

Debugging
---------

Enable debug mode by setting the following two values in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2,5

 // Enable/Disable debug
 define('DEBUG', true);

 // Available log drivers: syslog, stderr, stdout, system or file
 define('LOG_DRIVER', 'file');

The file ``debug.log`` will be found in the ``data`` folder of your Kanboard directory.


Updates
=======

.. note:: Check the update Feed_ regularly to stay informed about the newest version.

Check the GitHub's Atom Feed_ for any new Kanboard releases and copy the link to the ``.tar.gz`` archive. In this example the version is v42.23.2, which of course does not exist. Change the version to the latest one in the highlighted lines.

.. code-block:: console
 :emphasize-lines: 2,3,4,5,6,7

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/kanboard/kanboard/archive/v42.23.2.tar.gz
 [isabell@stardust isabell]$ tar -xzf v42.23.2.tar.gz
 [isabell@stardust isabell]$ mv kanboard-42.23.2/config.php kanboard-42.23.2/config_new.php
 [isabell@stardust isabell]$ cp -r html/data/ html/plugins/ html/config.php kanboard-42.23.2/
 [isabell@stardust isabell]$ cp -r kanboard-42.23.2/* html/
 [isabell@stardust isabell]$ rm -rf kanboard-42.23.2 v42.23.2.tar.gz
 [isabell@stardust isabell]$

Check the `Kanboard documentation`_ if the configuration changed between ``config_new.php`` and your ``config.php`` (happens very rarely). If everything works alright you can delete the ``config_new.php`` file. Also check ``.htaccess`` if further adjustments needed to be made.

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
.. _latest release: https://github.com/kanboard/kanboard/releases/latest
.. _Feed: https://github.com/kanboard/kanboard/releases.atom
.. _Plugins: https://kanboard.org/#plugins
.. _email notifications: https://docs.kanboard.org/en/latest/admin_guide/email.html
.. _must have: https://docs.kanboard.org/en/latest/user_guide/notifications.html

----

Tested with Kanboard 1.2.6, Uberspace 7.1.14.0

.. authors::
