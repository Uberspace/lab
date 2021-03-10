.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: lang-c
.. tag:: database

.. sidebar:: Logo

  .. image:: _static/images/postgresql.png
      :align: center

##########
PostgreSQL
##########

.. tag_list::

PostgreSQL_ is a free and object-relational database system. It is also compatible to the familiar SQL standard. More details are available in the Wikipedia_.

Some projects (e.g. Miniflux2 and Matrix) require PostgreSQL and many others support it as an alternative to MySQL.

License
=======

PostgreSQL is released under the `PostgreSQL License`_, a liberal Open Source license, similar to the BSD or MIT licenses.

Version
=======

At first get an overview which versions are available and will be supported for your project:

::

 [isabell@stardust ~]$ uberspace tools version list postgresql
 - 10
 - 11
 - 12
 - 13
 [isabell@stardust ~]$

Select the desired postgresql version using:

::

 [isabell@stardust ~]$ uberspace tools version use postgresql 12
 Using 'Postgresql' version: '12'
 Selected postgresql version 12
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Initialization
==============

Environment Settings
--------------------

Please add the following lines to your ``~/.bash_profile``:

.. code-block:: bash

 # Postgresql Environment
 export PGPASSFILE=$HOME/.pgpass

Reload the ``.bash_profile`` with:

::

 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

Run ``psql --version`` to verify the installation so far:

::

 [isabell@stardust ~]$ psql --version
 psql (PostgreSQL) 12.4
 [isabell@stardust ~]$


The Database Cluster
--------------------

A database cluster is the base for all new single databases. We will define the location for the cluster and the user password. The user name for the cluster is automatically predefined with your Uberspace name.

To reduce the effort for the database cluster administration, we will define at first the password and save it to the file *.pgpass*.

We will create a random number with openssl (64 characters) and save it direct into the password file:

::

 [isabell@stardust ~]$ openssl rand -hex 32 > ~/.pgpass
 [isabell@stardust ~]$


Edit the file ``~/.pgpass`` file and complete the content:

.. warning:: Replace ``<username>`` with your Uberspace name!

.. warning:: Replace the dummy password with your own!

.. code-block:: console
 :emphasize-lines: 1,2

 #hostname:port:database:username:password (min 64 characters)
 *:*:*:<username>:1234567890123456789012345678901234567890123456789012345678901234

In our example this would be:

.. code-block:: console

 #hostname:port:database:username:password (min 64 characters)
 *:*:*:isabell:1234567890123456789012345678901234567890123456789012345678901234

And change the permissions with:

::

 [isabell@stardust ~]$ chmod 0600 ~/.pgpass
 [isabell@stardust ~]$

To use the pure password for the database cluster creation, create a temporary password file ``~/pgpass.temp``, containing only your password.

In our example this would be:

.. code-block:: console

 1234567890123456789012345678901234567890123456789012345678901234

Now create the database cluster:

.. code-block:: console
 :emphasize-lines: 1

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

The temporary password file is not more necessary:

::

 [isabell@stardust ~]$ rm ~/pgpass.temp
 [isabell@stardust ~]$

Configuration
=============

After the installation of PostgreSQL, it is necessary to configure the network environment. This installation considers the loopback interface as well as access via an Unix socket.  Access via an Unix socket is not supported by every project.

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

Edit ``~/opt/postgresql/data/postgresql.conf`` and set the key values ``listen_adresses``, ``port`` and ``unix_socket_directories``.
Consider using only unix sockets if possible. 

.. warning:: Please replace ``<username>`` with your username!

.. warning:: If you set listen_addresses you might open your postgres installation to the world!

.. code-block:: postgres
 :emphasize-lines: 7,14

 #------------------------------------------------------------------------------
 # CONNECTIONS AND AUTHENTICATION
 #------------------------------------------------------------------------------

 # - Connection Settings -

 listen_addresses = 'localhost'         # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
                                        # (change requires restart)
 port = 5432                            # (change requires restart)
 max_connections = 100                  # (change requires restart)
 #superuser_reserved_connections = 3    # (change requires restart)
 unix_socket_directories = '/home/<username>/tmp'      # comma-separated list of directories
                                        # (change requires restart)
 #unix_socket_group = ''                # (change requires restart)
 #unix_socket_permissions = 0777        # begin with 0 to use octal notation
                                        # (change requires restart)
 #bonjour = off                         # advertise server via Bonjour
                                        # (change requires restart)
 #bonjour_name = ''                     # defaults to the computer name
                                        # (change requires restart)


Later you can see the socket in the filesystem by using ``ls -a ~/tmp``. It is listed as ``.s.PGSQL.5432``.

Setup Daemon
------------

Create ``~/etc/services.d/postgresql.ini`` with the following content:

.. code-block:: ini

 [program:postgresql]
 command=postgres -D %(ENV_HOME)s/opt/postgresql/data/
 autostart=yes
 autorestart=yes

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

It is highly recommended to use a separate user together with a strong password for every single usage (project). Please don't use the database cluster user, it is like a root user.

The following example considers a database and new user for Synapse, the Matrix (https://matrix.org) reference server. You can use this example for other projects as well.

.. note:: Please start your PostgreSQL daemon before you maintain anything.


Step 1 - New User
-----------------

To create a new database user, consider the following option:

 * ``-P``: To get a user name and password dialogue.

.. warning:: Please replace ``<user>`` with your user name of choice!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createuser <user> -P
 Enter password for new role:
 Enter it again:
 [isabell@stardust ~]$


Step 2 - New Database
---------------------

 The following options will be used to create the new database:

 * ``--encoding``: Set of UTF8 encoding
 * ``--owner``: The owner of the new database. In this example the new user of step 1.
 * ``--template``: PostgreSQL supports standard templates to create the database structure.
 * ``database name``: And as last option the name of the database. In this example 'synapse'.

.. warning:: Please replace ``<user>`` with your user name, created in step 1!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=<user> --template=template0 synapse
 [isabell@stardust ~]$


Best Practices
==============

To configure your project with the PostgreSQL details, you should have the database name, user and password, localhost as server address and your port number.


Updates
=======

The update process has some dependencies. Especially the free available space of your Uberspace, because the update process will take temporary ca. the same capacity of your existing data.

Step 1 - Check the Database Volume
----------------------------------

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

Further tools and details are described in the Uberspace manual and section :manual_anchor:`storge <basics-resources#storage>`.

Now you can identify, that you have enough space for the backup. If not, then try to get more space. Otherwise you cannot start the update.

Step 2 - Check the Preconditions
--------------------------------

A PostgreSQL update is in most cases necessary in relation of another software update with new requirements. Check the new software requirements and compare this with existing PostgreSQL versions:

::

 [isabell@stardust ~]$ uberspace tools version list postgresql
 - 10
 - 11
 - 12
 - 13
 [isabell@stardust ~]$

Step 3 - Stop all Daemons with relation to PosgreSQL 
----------------------------------------------------

Check running daemons:

::

 [isabell@stardust ~]$ supervisorctl status
 my-daemon                              RUNNING   pid 16337, uptime 0:00:04
 postgresql                             RUNNING   pid 14711, uptime 0:00:05
 [isabell@stardust ~]$

 And stop all affected daemons:

.. warning:: Please don't stop the PostgreSQL-Daemon.

 [isabell@stardust ~]$ supervisorctl stop my-daemon
 my-daemon: stopped
 [isabell@stardust ~]$

Step 4 - Backup
---------------

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

Step 5 - PostgreSQL-Update
--------------------------

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

For the new database cluster, create the temporary password file. You can copy the existing .pgpass file as base, but finally only the password is necessary.

In our example this would be:

.. code-block:: console

 1234567890123456789012345678901234567890123456789012345678901234

::

 [isabell@stardust ~]$ cp ~/.pgpass ~/pgpass.temp
 [isabell@stardust ~]$

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

Step 6 - Daemon Start
---------------------

Start your Daemons with a relation to PostgreSQL:

::

 [isabell@stardust ~]$ supervisorctl start my-daemon
 my-daemon: started
 [isabell@stardust ~]$

Step 7 - Cleanup
----------------

The backup is not more necessary and can be removed:

::

 [isabell@stardust ~]$ rm -r ~/opt/postgresql/backup
 [isabell@stardust ~]$


.. _PostgreSQL: https://www.postgresql.org
.. _Wikipedia: https://en.wikipedia.org/wiki/PostgreSQL
.. _PostgreSQL License: https://www.postgresql.org/about/licence/
.. _documentation: https://www.postgresql.org/docs/9.6/static/install-procedure.html
.. _download server: https://download.postgresql.org/pub/source/
.. _uberspace_resources: https://manual.uberspace.de/basics-resources/#storage

----

Tested with Uberspace 7.9.0.0 and PostgreSQL 12/13

.. author_list::
