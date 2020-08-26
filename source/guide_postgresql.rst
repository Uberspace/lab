.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: lang-c
.. tag:: database

##########
PostgreSQL
##########

.. tag_list::

PostgreSQL_ is a free and object-relational database system. It is also compatible to the familiar SQL standard. More details are available in the Wikipedia_.

Some projects (e.g. Miniflux2) require PostgreSQL and many others support it as an alternative to MySQL.

License
=======

PostgreSQL is released under the `PostgreSQL License`_, a liberal Open Source license, similar to the BSD or MIT licenses.

Installation
============

Step 1 - Download and Extract the Source Code
---------------------------------------------

Create a working directory.

::

 [isabell@stardust ~]$ mkdir ~/postgres/
 [isabell@stardust ~]$ cd ~/postgres/
 [isabell@stardust ~]$

Download version 9.6.10. A list of supported major and beta releases can be found on the PostgreSQL `download server`_.

::

 [isabell@stardust ~]$ curl -O https://download.postgresql.org/pub/source/v12.4/postgresql-12.4.tar.gz
 [isabell@stardust ~]$

To extract the tar archive, use the following options:

 * ``-x``: To extract files and directories.
 * ``-v``: To have a verbose output.
 * ``-z``: To consider gzip.
 * ``-f``: And as last option the file to extract.

::

 [isabell@stardust ~]$ tar -xvzf ~/postgres/postgresql-12.4.tar.gz
 [isabell@stardust ~]$


Step 2 - Source Code Configuration, Compiling and Installation
--------------------------------------------------------------

Before we start, we have to consider some aspects, e.g. Python support, and corresponding settings, regarding to a shared hosting environment like Uberspace:

 * ``--prefix=$HOME/opt/postgresql/``: New installation target for your personal Uberspace.
 * ``--with-python PYTHON=/usr/bin/python2``: Compiling with Python 2.x support. Alternatively you can choose ``/usr/bin/python3``. Both are links to the actual supported Python versions.
 * ``--without-readline``: In case of problems, regarding missing Readline support, you can exclude Readline with this option.

Other options can be found in the PostgreSQL documentation_.

Now configure and compile the source code and finally install it.

::

 [isabell@stardust ~]$ configure
 [isabell@stardust ~]$ make
 [isabell@stardust ~]$ make install

.. note:: Please use single steps instead of combining all three in one process to see and identify possible errors.

.. important:: For future usage with projects like Miniflux2, ejabberd, Matrix etc. it is recommended to consider everything like docs and especially additional modules by PostgreSQL. This is the reason to use the supported option ``world`` for ``make`` and ``make install``.

::

 [isabell@stardust ~]$ cd ~/postgres/postgresql-12.4
 [isabell@stardust ~]$ ./configure --prefix=$HOME/opt/postgresql/ --with-python PYTHON=/usr/bin/python2 --without-readline
 [isabell@stardust ~]$ make world
 [isabell@stardust ~]$ make install-world
 [isabell@stardust ~]$


Step 3 - Environment Settings
-----------------------------

Please add the following lines to your ``~/.bash_profile``:

.. code-block:: bash

 # Postgresql Environment

 export PATH=$HOME/opt/postgresql/bin/:$PATH
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/opt/postgresql/lib
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


Step 4 - The Database Cluster
-----------------------------

A database cluster is the base for all new single databases. We will define the location for the cluster and the user password. The user name for the cluster is automatically predefined to be your Uberspace name.

To reduce the effort for the database cluster administration, we will define at first the password and save it to the file *.pgpass*.

Create a ``~/.pgpass`` file with the following content:

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

The temporary password file is no longer necessary:

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

Edit ``~/opt/postgresql/data/postgresql.conf`` and set the key values ``listen_adresses``, ``port`` and ``unix_socket_directories``:

.. warning:: Please replace ``<username>`` with your username!

.. code-block:: postgres
 :emphasize-lines: 7,14

 #------------------------------------------------------------------------------
 # CONNECTIONS AND AUTHENTICATION
 #------------------------------------------------------------------------------

 # - Connection Settings -

 listen_addresses = '*'         # what IP address(es) to listen on;
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


Setup Daemon
------------

Create ``~/etc/services.d/postgresql.ini`` with the following content:

.. code-block:: ini

 [program:postgresql]
 command=%(ENV_HOME)s/opt/postgresql/bin/postgres -D %(ENV_HOME)s/opt/postgresql/data/
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

.. warning:: Please replace ``<username>`` with your user name!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createuser <username> -P
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

.. warning:: Please replace ``<username>`` with your user name, created in step 1!

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=<username> --template=template0 synapse
 [isabell@stardust ~]$


Best Practices
==============

To configure your project with the PostgreSQL details, you should have the database name, user name and password, localhost as server address and your port number.

.. _PostgreSQL: https://www.postgresql.org
.. _Wikipedia: https://en.wikipedia.org/wiki/PostgreSQL
.. _PostgreSQL License: https://www.postgresql.org/about/licence/
.. _documentation: https://www.postgresql.org/docs/9.6/static/install-procedure.html
.. _download server: https://download.postgresql.org/pub/source/

----

Tested with Uberspace 7.1.15 and PostgreSQL 12.4

.. author_list::
