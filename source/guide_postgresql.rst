.. highlight:: console

.. author:: FM <git.fm@mmw9.de>
.. author:: CHHEI <chhei@paleoearthlabs.org>

.. tag:: lang-c
.. tag:: database

.. sidebar:: Logo

  .. image:: _static/images/postgresql.png
      :align: center

##########
PostgreSQL
##########

.. tag_list::

PostgreSQL_ is a free and object-relational database system. It is also compatible to the familiar SQL standard. More details are available on Wikipedia_.

Some projects (e.g. Miniflux2 and Matrix) require PostgreSQL and many others support it as an alternative to MySQL.

In addition to basic PostgreSQL functionality, Uberspace provides a number of additional `PostgreSQL Extensions`_ which allow to add functionality to the PostgreSQL_ database, for example using PostGIS_ for geospatial objects.

-----

License
=======

PostgreSQL is released under the `PostgreSQL License`_, a liberal Open Source license, similar to the BSD or MIT licenses.

Version
=======

At first get an overview which versions are available and will be supported for your project::

    [isabell@stardust ~]$ uberspace tools version list postgresql
    - 12
    - 13
    - 14
    - 15
    [isabell@stardust ~]$

Select the desired postgresql version using::

    [isabell@stardust ~]$ uberspace tools version use postgresql 12
    Using 'Postgresql' version: '12'
    Selected postgresql version 12
    The new configuration is adapted immediately. Patch updates will be applied automatically.
    [isabell@stardust ~]$

Run ``psql --version`` to verify the installation so far::

    [isabell@stardust ~]$ psql --version
    psql (PostgreSQL) 12.4
    [isabell@stardust ~]$

Initialization
==============

Environment Settings
--------------------

Please add the following lines to your ``~/.bash_profile``:

.. code-block:: bash

    # Postgresql Environment
    export PGPASSFILE=$HOME/.pgpass

Reload the ``.bash_profile`` with::

    [isabell@stardust ~]$ source ~/.bash_profile
    [isabell@stardust ~]$

And check the results::

    [isabell@stardust ~]$ echo $PGPASSFILE
    /home/isabell/.pgpass
    [isabell@stardust ~]$

The Database Cluster
--------------------

A database cluster is the base for all new single databases. We will define the location for the cluster and the user password. The user name for the cluster is the same as your Uberspace name.

To reduce the effort for the database cluster administration, we will define at first the password and save it to the file *.pgpass*.

We will create a random string with openssl (64 characters) and save it direct to a temporary file (we need that soon) and copy it to the password file::

    [isabell@stardust ~]$ openssl rand -hex 32 > ~/pgpass.temp
    [isabell@stardust ~]$ cp ~/pgpass.temp ~/.pgpass
    [isabell@stardust ~]$

Edit the file ``~/.pgpass`` file and complete the content:

.. warning:: Replace ``<username>`` with your Uberspace name!

.. warning:: Replace the dummy password in both pgpass files with your own!

.. code-block:: console
    :emphasize-lines: 2

    #hostname:port:database:username:password (min 64 characters)
    *:*:*:<username>:1234567890123456789012345678901234567890123456789012345678901234

In our example this would be::

    #hostname:port:database:username:password (min 64 characters)
    *:*:*:isabell:1234567890123456789012345678901234567890123456789012345678901234

And change the permissions with::

    [isabell@stardust ~]$ chmod 0600 ~/.pgpass
    [isabell@stardust ~]$

We now use the temporary password file ``~/pgpass.temp`` (containing only your password), to create the database cluster:

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ initdb --pwfile ~/pgpass.temp --auth=scram-sha-256 -E UTF8 -D ~/opt/postgresql/data/
    The files belonging to this database system will be owned by user "isabell".
    This user must also own the server process.

    The database cluster will be initialized with locale "de_DE.UTF-8".
    The default text search configuration will be set to "german".

    Data page checksums are disabled.

    creating directory /home/isabell/opt/postgresql/data ... ok
    creating subdirectories ... ok
    selecting dynamic shared memory implementation ... posix
    selecting default max_connections ... 100
    selecting default shared_buffers ... 128MB
    selecting default time zone ... Europe/Berlin
    creating configuration files ... ok
    running bootstrap script ... ok
    performing post-bootstrap initialization ... ok
    syncing data to disk ... ok

    Success. You can now start the database server using:

        pg_ctl -D /home/isabell/opt/postgresql/data/ -l logfile start

    [isabell@stardust ~]$

The temporary password file is no longer necessary::

    [isabell@stardust ~]$ rm ~/pgpass.temp
    [isabell@stardust ~]$

Configuration
=============

After the installation of PostgreSQL, it is necessary to configure the network environment. This installation considers the loopback interface as well as access via an Unix socket.  Access via a Unix socket is not supported by every project.

Configure the Unix Socket
-------------------------

The Unix socket will be configured to the standard port. You must set the environment variables with your new port:

Edit your ``~/.bashrc`` and add the following content:

.. code-block:: bash

 export PGHOST=localhost
 export PGPORT=5432

Load the new settings:

.. code-block:: bash

 [isabell@stardust ~] source ~/.bashrc

PostgreSQL Configuration
------------------------

Edit ``~/opt/postgresql/data/postgresql.conf`` and set the ``unix_socket_directories``:

Consider using only unix sockets if possible.

.. warning:: Please replace ``<username>`` with your username and remove the comment mark ``#`` at the start of the line!

.. code-block:: postgres
 :emphasize-lines: 6

 #------------------------------------------------------------------------------
 # CONNECTIONS AND AUTHENTICATION
 #------------------------------------------------------------------------------

 #superuser_reserved_connections = 3    # (change requires restart)
 unix_socket_directories = '/home/<username>/tmp'      # comma-separated list of directories
                                        # (change requires restart)
 #unix_socket_group = ''                # (change requires restart)

Resource Configuration
------------------------

With the default settings PostgreSQL can consume quite a lot of resources.
Especially the number of open file handles can become a problem. To reduce the
resource consumption, the following settings can be lowered:

.. code-block:: ini

  max_files_per_process = 64
  max_worker_processes = 4
  max_parallel_workers = 2

Additionally, the number of connections can be reduced:

.. warning:: If you lower the number of allowed connections, make sure to adjust your client’s connection settings as well. Otherwise, it might fail to start!

.. code-block:: ini

  max_connections = 20

Logging
-------

Postgres writes its logs to ``~/opt/postgresql/data/log/``. To change this, adapt the ``log_directory`` setting in ``postgresql.conf``.

Setup Daemon
------------

Create ``~/etc/services.d/postgresql.ini`` with the following content:

.. code-block:: ini

 [program:postgresql]
 command=postgres -D %(ENV_HOME)s/opt/postgresql/data/
 autostart=yes
 autorestart=yes
 startsecs=15

.. include:: includes/supervisord.rst

To stop and start the daemon to perform maintenance tasks, you can use ``supervisorctl stop`` and ``supervisorctl start``, respectively:

::

 [isabell@stardust ~]$ supervisorctl stop postgresql
 postgresql: stopped
 [isabell@stardust ~]$

::

 [isabell@stardust ~]$ supervisorctl start postgresql
 postgresql: started
 [isabell@stardust ~]$

Check out the :manual:`supervisord manual <daemons-supervisord>` for further details.


Database and User Management
============================

The default setup on Uberspace is that the Uberspace account name is the database cluster user/PostgreSQL superuser
with root-type privileges to administer the database (create/delete new databases and users, install extensions,
run maintenance).

It is highly recommended to use a separate user(s) together with a strong password for every single usage (project).

The following example considers a database and new user for Synapse, the Matrix (https://matrix.org) reference server.
You can use this template setup for other projects as well.

.. note:: Please start your PostgreSQL daemon before you maintain anything.


Create User
-----------

To create a new database user, consider the following option:

 * ``-P``: To get a user name and password dialogue.

.. warning:: Please replace ``<user>`` with your user name of choice!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createuser <user> -P
 Enter password for new role:
 Enter it again:
 [isabell@stardust ~]$

For more options when creating new PostgreSQL users, please refer to the `PostgreSQL manual <https://www.postgresql.org/docs/13/app-createuser.html>`__.

Create Database
---------------

 The following options will be used to create the new database:

 * ``--encoding``: Set of UTF8 encoding
 * ``--owner``: The owner of the new database. In this example the newly created user.
 * ``--template``: PostgreSQL supports standard templates to create the database structure.
 * ``database name``: And as last option the name of the database. In this example ``synapse``.

For more options when creating new PostgreSQL databases, please refer to the `PostgreSQL manual <https://www.postgresql.org/docs/13/app-createdb.html>`__.

.. warning:: Please replace ``<user>`` with the user name, created earlier, and <database name> with the name of the database you want to create!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=<user> --template=template0 <database name>
 [isabell@stardust ~]$

PostgreSQL Extensions
=====================

PostgreSQL `extensions <https://wiki.postgresql.org/wiki/Extensions>`_ allow to extend the functionality and user-visible functions of a database. A number of extensions for PostgreSQL are available (see `list <https://www.postgresql.org/download/products/6-postgresql-extensions/>`_), with the geospatial extension PostGIS_ being one of the most widely used ones.

Available extensions for PostgreSQL on U7 can be found in the ``/usr/pgsql-<MajorVersion>/share/extension`` directory, where ``<MajorVersion>`` refers to the PostgreSQL `Version`_ of your installation.

.. Note:: In order to create extensions, the PostgreSQL user will need to have **"superuser"** rights. These are automatically granted to the database cluster user (your Uberspace account name) and to any database user where the ``--superuser`` flag was used with the ``createuser`` command (see Sections `Create Database` and `Create User`).

The ``select * from pg_roles;`` SQL command allows you to check which roles and privileges exist for the current database (``rolsuper`` needs to be ``t`` (true)):

.. warning:: Please replace <database name> with the name of the database you would like to install extensions in! Commonly ``psql <database name>`` is automatically interpreted by PostgreSQL as ``psql <database name> --username <login account name>``, so here, the "login account name" is automatically taken as your UberSpace name/database cluster user.

.. code-block:: console

 [isabell@stardust ~]$ psql <database name>
 databaseName=# select * from pg_roles;

 test=# select * from pg_roles;
           rolname          | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit | rolpassword | rolvaliduntil | rolbypassrls | rolconfig |  oid
 ---------------------------+----------+------------+---------------+-------------+-------------+----------------+--------------+-------------+---------------+--------------+-----------+-------
 ...
  <db owner>                | f        | t          | f             | f           | t           | f              |           -1 | ********    |               | f            |           | 16386
  <uberspace account name>  | t        | t          | t             | t           | t           | t              |           -1 | ********    |               | t            |           |    10
 ...

PostGIS: Spatially enabling the database using PostGIS
----------------------------------------------------------

PostGIS_ adds support for geographic objects to the database, allowing to run spatial
queries. The PostgreSQL installation on Uberspace comes with pre-compiled versions
of the PostGIS extension saving you from having to compile PostGIS and its FOSS GIS
software stack dependencies (such as `GDAL <https://gdal.org>`_, `PROJ <http://proj.org>`_,
`GEOS <https://trac.osgeo.org/geos/>`_ and `SFCGAL <http://www.sfcgal.org/>`_) from source.

To check whether PostGIS_ exists for the PostgreSQL version do a quick ``ls`` of the ``share``
directory. In this guide we use PostGIS_ version 3.1 with a PostgreSQL major version 12:

.. code-block:: console

 [isabell@stardust ~]$ ls -rtl /usr/pgsql-12/share/extension/postgis--3*.sql
 -rw-r--r--. 1 root root 7.9M May 26 15:59 /usr/pgsql-12/share/extension/postgis--3.1.2.sql

Once you have convinced yourself that the right PostGIS_ extension is available, you need
to enable the extensions. This is done using the interactive ``psql`` shell.

.. note:: Make sure you do this as the database cluster user or a user with "superuser" privileges.

Enter your newly created database (Section `Create Database`_), then issue the SQL statements below to spatially `enable the database <http://postgis.net/docs/postgis_administration.html#create_spatial_db>`_ using  the PostGIS extension.

Note that PostGIS requires the `PL/pgSQL <https://www.postgresql.org/docs/12/plpgsql.html>`_ extension as prerequisite. It should be readily installed when the database is created, however, the ``CREATE EXTENSION IF NOT EXSITS plpgsql`` statement in the code block below provides an additional safety net prior to enabling the PostGIS_ extension.

.. warning:: Please replace ``<database name>`` with the name of the database in which you want to create the PostGIS extension! Keep in mind that PostgreSQL interprets no specified username as the Uberspace account name and hence as database superuser.

.. code-block:: console

 [isabell@stardust ~]$ psql <database name>
 databaseName=# CREATE EXTENSION IF NOT EXISTS plpgsql;
 databaseName=# CREATE EXTENSION postgis;
 databaseName=# CREATE EXTENSION postgis_raster; -- OPTIONAL
 databaseName=# CREATE EXTENSION postgis_topology; -- OPTIONAL

The ``raster`` and ``topology`` functionality of PostGIS_ are optional. Test whether the extensions have been properly installed and can be found by PostgreSQL using the ``\dx`` - you should get output similar to this:

.. code-block:: console

 [isabell@stardust ~]$ psql <database name>
 databaseName=# \dx
                                     List of installed extensions
        Name       | Version |   Schema   |                        Description
 ------------------+---------+------------+------------------------------------------------------------
  plpgsql          | 1.0     | pg_catalog | PL/pgSQL procedural language
  postgis          | 3.1.2   | public     | PostGIS geometry and geography spatial types and functions
  postgis_raster   | 3.1.2   | public     | PostGIS raster types and functions
  postgis_topology | 3.1.2   | topology   | PostGIS topology spatial types and functions

The database should now be spatially enabled, allowing you to load geospatial data with the help of PostGIS_ auxiliary programs such as ``shp2pgsql`` (for `ESRI Shapefiles <https://en.wikipedia.org/wiki/Shapefile>`_).

UUID: Generating UUIDs
----------------------

PostgreSQL provides storage and comparison functions for the standardized `UUID data type <https://www.postgresql.org/docs/12/datatype-uuid.html>`_ (`Universally unique identifier <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_). However, the core database functions cannot generate standard UUIDs. The `uuid-ossp <https://www.postgresql.org/docs/12/uuid-ossp.html>`_ module provides this functionality and can easily be installed as PostgreSQL extension:

.. warning:: Please replace ``<database name>`` with the name of the database in which you want to create the PostGIS extension! Keep in mind that PostgreSQL interprets no specified username as the Uberspace account name and hence as database superuser.

.. code-block:: console

 [isabell@stardust ~]$ psql <database name>
 databaseName=# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

After creating the extension, check whether PostgreSQL can find it using the ``\dx`` command in the interactive ``psql`` shell:

.. code-block:: console

 [isabell@stardust ~]$ psql <database name>
 databaseName=# \dx
                                     List of installed extensions
        Name       | Version |   Schema   |                        Description
 ------------------+---------+------------+------------------------------------------------------------
  uuid-ossp        | 1.1     | public     | generate universally unique identifiers (UUIDs)

Best Practices
==============

To configure your project with the PostgreSQL details, you should have the database name, user and password, localhost as server address and your port number.

Updates
=======

The update process has one dependency, the free available space of your affected Uberspace. Because the update process will take temporary ca. the same capacity of your existing PostgreSQL instance data for a local backup. After the data migration the backup will be deleted and you will have the same capacity situation as before.

Check the Database Volume
-------------------------

A simple check will show the used capacity of your PostgreSQL instance.

::

 [isabell@stardust ~]$ du -sh ~/opt/postgresql/data
 1,0G    /home/isabell/opt/postgresql/data
 [isabell@stardust ~]$

More details about your Uberspace space in total shows the command ``quota``:

::

 [isabell@stardust ~]$ quota -gsl
 Disk quotas for group isabell (gid 1013):
      Filesystem   space   quota   limit   grace   files   quota   limit   grace
       /dev/sda2    713M  10240M  11264M              38       0       0
 [isabell@stardust ~]$

Further tools and details are described in the Uberspace manual and section :manual_anchor:`Storage <basics-resources#storage>`.

Now you can identify, that you have enough space for the backup. If not, then try to get more space. Otherwise you cannot start the update.

Check the Preconditions
-----------------------

A PostgreSQL update is in most cases necessary in relation of another software update with new requirements. Check the new software requirements and compare this with existing PostgreSQL versions:

::

 [isabell@stardust ~]$ uberspace tools version list postgresql
 - 10
 - 11
 - 12
 - 13
 [isabell@stardust ~]$

Stop all Daemons with relation to PosgreSQL
-------------------------------------------

Check running daemons:

::

 [isabell@stardust ~]$ supervisorctl status
 my-daemon                              RUNNING   pid 16337, uptime 0:00:04
 postgresql                             RUNNING   pid 14711, uptime 0:00:05
 [isabell@stardust ~]$

And stop all affected daemons:

.. warning:: Please don't stop the PostgreSQL-Daemon.

::

 [isabell@stardust ~]$ supervisorctl stop my-daemon
 my-daemon: stopped
 [isabell@stardust ~]$

Backup
------

Create the target directory:

::

 [isabell@stardust ~]$ mkdir ~/opt/postgresql/backup
 [isabell@stardust ~]$

Start the backup:

::

 [isabell@stardust ~]$ pg_dumpall -f ~/opt/postgresql/backup/pg_backup.sql
 [isabell@stardust ~]$

And copy the PostgreSQL config file:

::

 [isabell@stardust ~]$ cp ~/opt/postgresql/data/postgresql.conf ~/opt/postgresql/backup
 [isabell@stardust ~]$

.. warning:: If you have further changes in other configuration files, please copy these to the backup directory too.

PostgreSQL-Update
-----------------

Stop the PostgreSQL-Daemon:

::

 [isabell@stardust ~]$ supervisorctl stop postgresql
 postgresql: stopped
 [isabell@stardust ~]$

Delete the existing data directory:

::

 [isabell@stardust ~]$ rm -r ~/opt/postgresql/data
 [isabell@stardust ~]$

Select the new PostgreSQL-Version (e.g. version 13):

::

 [isabell@stardust ~]$ uberspace tools version use postgresql 13
 Selected Postgresql version 13
 The new configuration is adapted immediately. Minor updates will be applied automatically.
 [isabell@stardust ~]$

Check the new version:

::

 [isabell@stardust ~]$ psql --version
 psql (PostgreSQL) 13.2
 [isabell@stardust ~]$

For the new database cluster, create the temporary password file ``~/pgpass.temp``. You can copy the existing ``.pgpass`` file as base, but make sure to delete everything (header, usernames, hostnames, etc.) except the password.

In our example this would be:

.. code-block:: console

 1234567890123456789012345678901234567890123456789012345678901234

Create the new database cluster:

::

 [isabell@stardust ~]$ initdb --pwfile ~/pgpass.temp --auth=scram-sha-256 -E UTF8 -D ~/opt/postgresql/data/

 The files belonging to this database system will be owned by user "<username>".
 This user must also own the server process.

 The database cluster will be initialized with locale "de_DE.UTF-8".
 The default text search configuration will be set to "german".

 Data page checksums are disabled.

 creating directory /home/<username>/opt/postgresql/data ... ok
 creating subdirectories ... ok
 selecting dynamic shared memory implementation ... posix
 selecting default max_connections ... 100
 selecting default shared_buffers ... 128MB
 selecting default time zone ... Europe/Berlin
 creating configuration files ... ok
 running bootstrap script ... ok
 performing post-bootstrap initialization ... ok
 syncing data to disk ... ok

 Success. You can now start the database server using:

    pg_ctl -D /home/<username>/opt/postgresql/data/ -l logfile start

 [isabell@stardust ~]$

Remove the temporary password file:

::

 [isabell@stardust ~]$ rm ~/pgpass.temp
 [isabell@stardust ~]$

Rename the existing new PostgreSQL config file as backup:

::

 [isabell@stardust ~]$ mv ~/opt/postgresql/data/postgresql.conf ~/opt/postgresql/data/postgresql.conf.new
 [isabell@stardust ~]$

And copy your old config file from the backup directory to the new data directory:

::

 [isabell@stardust ~]$ cp ~/opt/postgresql/backup/postgresql.conf ~/opt/postgresql/data
 [isabell@stardust ~]$

Start the PostgreSQL-Daemon:

::

 [isabell@stardust ~]$ supervisorctl start postgresql
 [isabell@stardust ~]$

Check the status:

::

 [isabell@stardust ~]$ supervisorctl status
 postgresql                       RUNNING   pid 26245, uptime 0:23:43
 [isabell@stardust ~]$

In case of problems check the logfile ~/logs/supervisord.log.

Restore the data from your backup file:

::

 [isabell@stardust ~]$ psql -f ~/opt/postgresql/backup/pg_backup.sql postgres
 [isabell@stardust ~]$

Check the cluster, if all databases are available:

::

 [isabell@stardust ~]$ psql -l
                                List of databases
    Name    | Owner  | Encoding |   Collate   |    Ctype    | Access privileges
 -----------+--------+----------+-------------+-------------+-------------------
  my-program| user   | UTF8     | de_DE.UTF-8 | de_DE.UTF-8 |
  postgres  | isabell| UTF8     | de_DE.UTF-8 | de_DE.UTF-8 |
  template0 | isabell| UTF8     | de_DE.UTF-8 | de_DE.UTF-8 |
  template1 | isabell| UTF8     | de_DE.UTF-8 | de_DE.UTF-8 |

 (4 rows)

 [isabell@stardust ~]$

Daemon Start
------------

Start your Daemons with a relation to PostgreSQL:

::

 [isabell@stardust ~]$ supervisorctl start my-daemon
 my-daemon: started
 [isabell@stardust ~]$

Cleanup
-------

The backup is not more necessary and can be removed:

::

 [isabell@stardust ~]$ rm -r ~/opt/postgresql/backup
 [isabell@stardust ~]$

Connecting from outside
=======================

If you want to connect somehow "directly" from a remote host, you can do so by using a SSH tunnel.


.. _postgres-ssh-tunnel-using-linux:

Using Linux, macOS, any other Unix, or Windows 10
-------------------------------------------------

On Linux, macOS and practically every other Unix operating system, as well as Windows 10 since the September 2017 “Fall Creators Update” version, `OpenSSH <https://www.openssh.com/>`_
comes preinstalled so you can use it out of the box.

This is how you can initiate a SSH connection offering a tunnel for port 5432,
your local workstation is represented by a ``[localuser@localhost ~]$`` prompt:

.. code-block:: console

  [localuser@localhost ~]$ ssh -L 5432:127.0.0.1:5432 isabell@stardust.uberspace.de

From now on, you can talk to 127.0.0.1:5432 on your local host to connect to your database.
In fact, it's OpenSSH listening on port 5432 of your local host, tunneling the connection to your uberspace.


.. _PostgreSQL: https://www.postgresql.org
.. _Wikipedia: https://en.wikipedia.org/wiki/PostgreSQL
.. _PostgreSQL License: https://www.postgresql.org/about/licence/
.. _documentation: https://www.postgresql.org/docs/12/static/install-procedure.html
.. _download server: https://download.postgresql.org/pub/source/
.. _uberspace_resources: https://manual.uberspace.de/basics-resources/#storage
.. _PostGIS: https://postgis.net
.. _doc-postgis-extn: http://postgis.net/docs/postgis_administration.html#create_spatial_db


----

Tested on Uberspace 7.11.3, with PostgreSQL 12/13 and PostGIS 3.1.2

.. list-table:: Tested with:
   :widths: 50 25
   :header-rows: 1

   * - Software/Platform
     - Version #
   * - UberSpace
     - 7.11.3
   * - PostgreSQL
     - 12/13
   * - PostGIS
     - 3.1.2



.. author_list::
