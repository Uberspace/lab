.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. version:: 1.0

##########
PostgreSQL
##########

PostgreSQL is a free and object relational database system. Also compatible to the familiar SQL-Standard. More details are available at Wikipedia:

* https://en.wikipedia.org/wiki/PostgreSQL

PostgreSQL is quiet intesting, because some projects (e.g. Miniflux2) supports only PostgreSQL and will be suported by many other projects as alternative to MySQL.

License
=======

PostgreSQL is released under the PostgreSQL License, a liberal Open Source license, similar to the BSD or MIT licenses.

All relevant legal information can be found here: 

  * https://www.postgresql.org/about/licence/

Prerequisites
=============

No prerequisites at the moment.

Installation
============

Step 1 - Source Code Download and Extracting
--------------------------------------------

I prefer to download all installation packages to a special work directory. In my case 'filebase'.

::

 [isabell@stardust ~]$ mkdir ~/filebase/
 [isabell@stardust ~]$ cd ~/filebase/
 [isabell@stardust ~]$

In this installation, i prefer to download the version 9.6.10. A list of supported major and beta releases can be found here:

 * https://download.postgresql.org/pub/source/ 

::

 [isabell@stardust ~]$ curl -O https://download.postgresql.org/pub/source/v9.6.10/postgresql-9.6.10.tar.gz
 [isabell@stardust ~]$

To extract the complete tar container, i consider the following options:

 * ``-x``: To extract files and directories.
 * ``-v``: To have a verbose output.
 * ``-z``: To consider gzip.
 * ``-f``: And as last option the file to extract.

::

 [isabell@stardust ~]$ tar -xvzf ~/filebase/postgresql-9.6.10.tar.gz
 [isabell@stardust ~]$


Step 2 - Source Code Configuration, Compiling and Installation
--------------------------------------------------------------

Here we use the clasic way to configure and compile the source code with *configure* and *make* and finaly to install with *make install*.

.. note:: Please use single steps instead to combine all three in one process to see and identify possible errors.

But before we start, we have to consider some aspects (e.g. Python support) and correponding settings, regarding to a shared hosting like by Uberspace:

 * ``--prefix=$HOME/opt/postgresql/``: New installation target for your personal Uberspace.
 * ``--with-python PYTHON=/usr/bin/python2``: Compiling with Python 2.x support. Alternative you can choose */usr/bin/python3*. Both are links to the actual supported Python versions.
 * ``--without-readline``: In case of problems, regarding missing Readline support, you can exclude this.

Other options can be found under (here in this case for version 9.6.10, but direct links are available for other versions too):

 * https://www.postgresql.org/docs/9.6/static/install-procedure.html

.. important:: For a future usage with projects like Miniflux, ejabberd, Matrix etc. it is recommend to consider everthing like docs and especialy additional modules by PostgreSQL. This is the reason to use the supported option *world* for *make* and *make install*.

::

 [isabell@stardust ~]$ cd ~/filebase/postgresql-9.6.10
 [isabell@stardust ~]$ ./configure --prefix=$HOME/opt/postgresql/ --with-python PYTHON=/usr/bin/python2 --without-readline
 [isabell@stardust ~]$ make world
 [isabell@stardust ~]$ make install-world
 [isabell@stardust ~]$


Step 3 - Environment Settings
-----------------------------

Some environment settings are necessary, that PostgreSQL tools are available without any problems.

Here as example for a bash shell setting, please add the following lines to ~/.bash_profile:

.. code-block:: .bash_profile

 # Postgresql Environment

 export PATH=$HOME/opt/postgresql/bin/:$PATH
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/opt/postgresql/lib
 export PGPASSFILE='$HOME/.pgpass'

Reload the .bash_profile with:

::

 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

And let show the installed PostgreSQL version as first test:

::

 [isabell@stardust ~]$ psql --version
 psql (PostgreSQL) 9.6.10
 [isabell@stardust ~]$


Step 4 - The Database Cluster
-----------------------------

A database cluster is the base for all new single data bases. We will define the location for the cluster and the user password. The user name for the cluster is automaticaly predefined with your Uberspace name.

To reduce the effort for the database cluster administration, we will define at first the password and safe it into the file *.pgpass*.  

Create ``~/*.pgpass`` with the following content:

.. warning:: Replace ``<username>`` with your Uberspace name!

.. code-block:: .pgpass

 #hostname:port:database:username:password (min 64 characters)
 *:*:*:<username>:1234567890123456789012345678901234567890123456789012345678901234

In our example this would be:

.. code-block:: .pgpass

 #hostname:port:database:username:password (min 64 characters)
 *:*:*:isabell:1234567890123456789012345678901234567890123456789012345678901234

And change the permissions with:

::

 [isabell@stardust ~]$ chmod 0600 ~/.pgpass
 [isabell@stardust ~]$

To use the pure password for the database cluster creation, we will create temporaly a password file, based on the *.pgpass* file with:

::

 [isabell@stardust ~]$ cp ~/.pgpass ~/pgpass.temp
 [isabell@stardust ~]$

Delete all additional text in your *~/pgpass.temp* file that you have only your password and check the content:

::

 [isabell@stardust ~]$ cat ~/pgpass.temp
 1234567890123456789012345678901234567890123456789012345678901234
 [isabell@stardust ~]$

Now we will create the database cluster with:

.. warning:: Replace ``<username>`` with your Uberspace name!

::

 [isabell@stardust ~]$ initdb --pwfile="/home/<username>/pgpass.temp" --auth=md5 -E UTF8 -D ~/opt/postgresql/data/
 The files belonging to this database system will be owned by user "".
 This user must also own the server process.
 The database cluster will be initialized with locale "de_DE.UTF-8".
 The default text search configuration will be set to "german".
 Data page checksums are disabled.
 creating directory /home/<username>/opt/postgresql/data ... ok
 creating subdirectories ... ok
 selecting default max_connections ... 100
 selecting default shared_buffers ... 128MB
 selecting dynamic shared memory implementation ... posix
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

.. warning:: The password above is only an example and must be replaced with your own strong password.


Configuration
=============

After the installation of PostgreSQL, it is necessary to configure the network invironment. This installation consider both, the loopback interface together with the access over the unix domain socket. The access over the unix domain socket alone is not supported by every project.


Step 1 - Configure Port
-----------------------

The standard port by PostgreSQL will not be supported by Uberspace. Here we must identify a free port number at first:

::

 [isabell@stardust ~]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9000
 [isabell@stardust ~]$

Write down your new port number. In this example it is 9000, but in reality you’ll get a free port number between 61000 and 65535.


Step 2 - Configure the Unix Domain Socket
-----------------------------------------

The unix domain socket will be configured to the standard port. You mast set the environment varables with your new port:

Open the file ``~/*.bashrc`` and add the following content:

.. code-block::

 export PGHOST=localhost
 export PGPORT=9000

.. warning:: Please use your own selected port number, instead 9000 like in this example.


Step 3 - Maintain the PostgreSQL-Configuration
----------------------------------------------

Open the configuration file ``~/opt/postgresql/data/postgresql.conf`` and select the connections section to maintain the lines like below for the key values *listen_adresses*, *port* and *unix_socket_directories*:

.. warning:: Please use your own selected port number, instead 9000 like in this example. And replace ``<username>`` with your username!

.. code-block:: postgresql.conf
 :emphasize-lines: 7,11

 #------------------------------------------------------------------------------
 # CONNECTIONS AND AUTHENTICATION
 #------------------------------------------------------------------------------
 
 # - Connection Settings -
 
 listen_addresses = 'localhost'         # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
                                        # (change requires restart)
 port = 9000                            # (change requires restart)
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


Step 4 - Setup Daemon
---------------------

Create ``~/etc/services.d/postgresql.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

 [program:postgresql]
 command=/home/<username>/opt/postgresql/bin/postgres -D /home/<username>/opt/postgresql/data/
 autostart=yes
 autorestart=yes

In our example this would be:

.. code-block:: ini

 [program:postgresql]
 command=/home/isabell/opt/postgresql/bin/postgres -D /home/isabell/opt/postgresql/data/
 autostart=yes
 autorestart=yes

The supervisor must be informed about the new service:

::

 [isabell@stardust ~]$ supervisorctl reread
 postgresql: available
 [isabell@stardust ~]$

 The first run will be initialized with:

::

 [isabell@stardust ~]$ supervisorctl update
 [isabell@stardust ~]$

To stop and start the daemon due to maintenance tasks, you can use the following entries:

::

 [isabell@stardust ~]$ supervisorctl stop postgresql
 postgresql: stopped
 [isabell@stardust ~]$

::

 [isabell@stardust ~]$ supervisorctl start postgresql
 postgresql: started
 [isabell@stardust ~]$

You can find more details to the supervisor at:

  * https://manual.uberspace.de/en/daemons-supervisord.html


Database and User Management
============================

It is highly recommend to use for every single usage (project) a separate user together with a strong password. Please don't use the database cluster user, it is like a root user.

The following example consider a database and new user for Synapse, the Matrix (https://matrix.org) reference server. You can use this example for other projects as well.

.. info:: Please start your PostgreSQL daemon, before you maintain anything.


Step 1 - New User
-----------------

To create a new database user, i consider the following option:

 * ``-P``: To get a username and password dialogue.

.. warning:: Please replace ``synapse`` with your preferred name!

::

 [isabell@stardust ~]$ createuser synapse -P
 Enter password for new role: 
 Enter it again: 
 [isabell@stardust ~]$


Step 2 - New Database
---------------------

 The following options will be use to create the new database:

 * ``--encoding``: Set of UTF8 encoding
 * ``--owner``: The owner of the new database. In this example the new user of step 1.
 * ``--template``: PostgreSQL supports standard templates to create the database structure.
 * ``database name``: And as last option the name of the database.

.. warning:: Please replace ``synapse`` with your preferred names!

::

 [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=synapse --template=template0 synapse
 [isabell@stardust ~]$


Best practices
==============

To configure your project with the PostgreSQL details, you should have the database name, user name and password, localhost as server address and your port number.

----

Tested with Uberspace 7.1.15 and PostgreSQL 9.6.10

.. authors:: FM
