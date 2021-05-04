.. highlight:: console

.. author:: stratmaster <https://github.com/stratmaster>
.. tag:: lang-go
.. tag:: web
.. tag:: rss

.. sidebar:: Logo

  .. image:: _static/images/miniflux.png
      :align: center

########
Miniflux
########

.. tag_list::

Miniflux_ is a minimalist and opinionated feed reader.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

The software is licensed under `Apache License 2.0`_. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

.. warning:: PostgreSQL has to be setup as shown in this :lab_anchor:`Guide <guide_postgresql.html#database-and-user-management>`! Especially, you'll need to know your PostgreSQL Port ``MyPostgreSQLPort``

You’ll need to create a user and a database in PostgreSQL first.


New PostgreSQL User
-------------------

To create a new database user, we consider the following option:

 * ``-P``: To get a user name and password dialogue.

.. warning:: Please replace ``<username>`` with your user name!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createuser <username> -P
 Enter password for new role:
 Enter it again:
 [isabell@stardust ~]$

New PostgreSQL Database
-----------------------

 The following options will be used to create the new database:

 * ``--encoding``: Set of UTF8 encoding
 * ``--owner``: The owner of the new database. In this example the new user of the previous step.
 * ``--template``: PostgreSQL supports standard templates to create the database structure.
 * ``database name``: And as last option the name of the database (e.g. miniflux2).

.. warning:: Please replace ``<username>`` with your user name!

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ psql -d template1 -c 'create extension hstore;'
 [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=<username> --template=template1 miniflux2
 [isabell@stardust ~]$

Setup domain
------------

The domain you want to use must be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download binary
-----------------------------------

Check the Miniflux_ website or GitHub_ for the `latest release`_ and copy the download link to the binary file named ``miniflux-linux-amd64``. Then ``cd`` to your ``~/bin`` directory and use ``wget`` to download it. Replace the URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd bin/
 [isabell@stardust bin]$ wget https://github.com/miniflux/miniflux/releases/download/42.23.1/miniflux-linux-amd64
 […]
 Saving to: ‘miniflux-linux-amd64’

 100%[======================================>] 11,133,568  7.63MB/s   in 1.4s

 2018-10-11 16:54:43 (7.63 MB/s) - ‘miniflux-linux-amd64’ saved [11133568/11133568]
 [isabell@stardust bin]$

Make the file ``miniflux-linux-amd64`` executable

::

 [isabell@stardust bin]$ chmod +x miniflux-linux-amd64
 [isabell@stardust bin]$


Configuration
=============

Configure web server
--------------------

.. note::

    Miniflux is running on port 9000. To let the installation run somewhere else but your base directory change the '/' to your domain.

.. include:: includes/web-backend.rst

Finishing installation
======================

Setup PostgreSQL database and admin user
----------------------------------------

Define the environment variable ``DATABASE_URL`` first for temporary usage. After that, run the SQL migrations and create an admin user.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ export DATABASE_URL="user=isabell password=MySuperSecretPassword dbname=miniflux2 sslmode=disable host=localhost"
  [isabell@stardust ~]$ miniflux-linux-amd64 -migrate
  Current schema version: 0
  Latest schema version: 16
  Migrating to version: 1
  Migrating to version: 2
  Migrating to version: 3
  [...]
  [isabell@stardust ~]$ miniflux-linux-amd64 -create-admin
  Enter Username: isabell
  Enter Password: ******
  [isabell@stardust ~]$

Setup daemon
------------

Create ``~/etc/services.d/miniflux.ini`` with the following content:

.. code-block:: ini

 [program:miniflux]
 environment =
  LISTEN_ADDR="0.0.0.0:9000",
  BASE_URL="https://isabell.uber.space",
  DATABASE_URL="user=isabell password=MySuperSecretPassword dbname=miniflux2 sslmode=disable host=localhost port=MyPostgreSQLPort"
 command=miniflux-linux-amd64


.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.

Go to ``https://isabell.uber.space/`` and log in to your installation with the login ``isabell`` and password given above.


Best practices
==============

Configuration
-------------

Check the `Miniflux documentation`_ for further environment variables that could be placed in ``~/etc/services.d/miniflux.ini``.


Updates
=======

.. note:: Check the update Feed_ regularly to stay informed about the newest version.

Check the GitHub's Atom Feed_ for any new Miniflux releases and copy the link to the ``miniflux-linux-amd64`` binary. In this example the version is 42.23.2, which of course does not exist. So, change the version to the latest one in the highlighted line. Before that, set the database environment variable, flush all user sessions and stop the service.

.. code-block:: console
 :emphasize-lines: 7

 [isabell@stardust ~]$ export DATABASE_URL="user=isabell password=MySuperSecretPassword dbname=miniflux2 sslmode=disable host=localhost port=MyPostgreSQLPort"
 [isabell@stardust ~]$ miniflux-linux-amd64 -flush-sessions
 Flushing all sessions (disconnect users)
 [isabell@stardust ~]$ supervisorctl stop miniflux
 miniflux: stopped
 [isabell@stardust ~]$ cd bin/
 [isabell@stardust bin]$ wget https://github.com/miniflux/miniflux/releases/download/42.23.2/miniflux-linux-amd64
 […]
 Saving to: ‘miniflux-linux-amd64’

 100%[======================================>] 11,133,568  7.63MB/s   in 1.4s

 2018-10-11 16:54:43 (7.63 MB/s) - ‘miniflux-linux-amd64’ saved [11133568/11133568]
 [isabell@stardust bin]$

Make the binary ``miniflux-linux-amd64`` executable, migrate the database and start the service again.

::

 [isabell@stardust bin]$ chmod +x miniflux-linux-amd64
 [isabell@stardust bin]$ miniflux-linux-amd64 -migrate
 Current schema version: 16
 Latest schema version: 17
 Migrating to version: 1
 Migrating to version: 2
 Migrating to version: 3
 [...]
 [isabell@stardust bin]$ supervisorctl start miniflux
 miniflux: started
 [isabell@stardust bin]$

Check the `Miniflux`_ website for news and/or breaking changes.

.. _Miniflux: https://miniflux.app/
.. _Github: https://github.com/miniflux/miniflux
.. _Apache License 2.0: https://github.com/miniflux/miniflux/blob/master/LICENSE
.. _latest release: https://github.com/miniflux/miniflux/releases/latest
.. _Miniflux documentation: https://miniflux.app/docs/configuration.html
.. _Feed: https://github.com/miniflux/miniflux/releases.atom

----

Tested with Miniflux 2.0.12, Uberspace 7.1.15.0

.. author_list::
