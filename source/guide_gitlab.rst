.. author:: Michael Strobler <maelstor@posteo.de>

.. tag:: lang-ruby
.. tag:: lang-yaml
.. tag:: audience-developers
.. tag:: continuous-integration
.. tag:: automation

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitlab-logo.png
      :align: center

#############
GitLab
#############

.. tag_list::

`GitLab`_ is a web-based DevOps lifecycle tool that provides a Git-repository
manager providing wiki, issue-tracking and continuous integration and deployment
pipeline features, using an open-source license, developed by GitLab Inc. [#f1]_

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`ssh <basics-ssh>`
  * :manual:`resources <basics-resources>`
  * :manual:`ports <basics-ports>`
  * :manual:`ruby <lang-ruby>`
  * :manual:`nodejs <lang-nodejs>`
  * :manual:`perl <lang-perl>`
  * :manual:`gcc <lang-gcc>`


Prerequisites
=============

Requirements
------------

Before starting to deploy gitlab on uberspace there are some preliminary
conciderations to take.

Since one uberspace account is limited to 1536MB RAM, you will need 2 uberspace
accounts for full functionality without crashes. The gitlab instance will need
around 1,4GB RAM and the sidekiq instance with postgresql intalled will need
around 750MB RAM.  The sidekiq instance doesn't need to be dedicated solely to
sidekiq. I chose to install gitlab runner in parallel for which I would have
needed to create a second account anyways. Just be sure you can spare 5GB of
disk space during the setup of sidekiq and around 2.5GB permanent disk space.

The compilation of the assets most likely won't work on your uberspace host
because the process uses more than the allowed RAM and gets automatically
killed. So you'll need around 5GB disk space left on your home PC and in your
home directory to compile the assets there. In case you want to try compiling
the assets locally before going through the complete guide and noticing it
doesn't work jump to the `Compile assets`_ section.

You should be aware that on the gitlab instance there will be only around 4GB of
disk space left for your repositories.

Adding all up the final gitlab instance can be used by yourself and a small
development team.

If you're finished setting up gitlab you may have noticed that the day is gone,
so be sure you can spare some hours up to a day ;)

This guide is roughly based on the official `GitLab installation from source`_
guide with a lot of adjustments to make it work on uberspace. The main
differences are the lack of root access (this is why to install GitLab from
source and the need to build some software from source), a different user than
the default ``git`` user and the resource limitations, described above.

Finally you'll need a piece of paper or some sort of digital scratchpad to note
things down.

Structure of this guide
-----------------------

Because it is clearer we first setup the ``gitlab`` host and then the
``sidekiq`` host as far it is possible. Setting up the ``sidekiq`` host is in
parts similar to the setup of ``gitlab`` host and once you're done with
``gitlab`` and be warmed up, the ``sidekiq`` host is set up pretty quick. Be
sure you have both accounts created before starting. If not otherwise stated the
commands besides in the `Installation sidekiq`_ section are meant to be run on
the ``gitlab`` host.

Throughout the guide I'm using ``isabell@gitlab`` for the gitlab instance,
``isabell@sidekiq`` for the sidekiq instance and ``isabell@home`` for your home
PC's account. ``isabell`` can't exist on both uberspace hosts but for the sake
of simplicity I'll keep it written that way.

Variables
---------

This guide is pretty long and to refer to created passwords, ips, domain names
etc. in following sections I'll use upper case variable names, which you have to
replace with their values when adviced to do so.

Let's start with the ``SIDEKIQ_FQDN`` and the ``GITLAB_FQDN``. You can get them
with

::

    [isabell@gitlab ~]$ hostname -f
    gitlab.uberspace.de

Do the same on your ``sidekiq`` host and write them down. Your usernames are
referred to as ``SIDEKIQ_USERNAME`` and ``GITLAB_USERNAME``. In our case this
would be ``isabell`` for both of them.

We also need the ``GITLAB_EXTERNAL_FQDN``. That is your external address at
which you want to be gitlab reachable from your browser. It is composed like
that

.. warning:: Replace ``GITLAB_USERNAME``

::

    GITLAB_USERNAME.uber.space

Passwords
---------

A quick word about passwords. The ``REDIS_PASSWORD``,
``POSTGRESQL_GITLAB_PASSWORD`` and ``POSTGRESQL_SUPERUSER_PASSWORD`` need to be
url encoded in some parts of the guide. To avoid the confusion when an when not
to url encode, you can choose to use an alphanumeric password ``[a-zA-Z0-9]``
with a higher length. Something between 64 and 128 characters should provide a
very secure password without the need to go through the url encoding. A 128
character alphanumeric password can easily be created

::

    [isabell@gitlab ~]$ echo -n 'my secret passphrase' | sha512sum | sed 's/[ -]//g'
    1d143ea6fb069e71fa8c90b3f81283cc71bf8d182448fda3e8cc3ae6ee8955b8baa6e616adfa2ffbb436791df91f07fdeac3c8083e1fabfd597398a97801c4a2

For a 96 character password use ``sha384sum`` (64 chars => ``sha256sum`` ...).
If you don't care about a passphrase you can increase the security of your
password

::

    [isabell@gitlab ~]$ head -c 128 /dev/random | sha512sum | sed 's/[ -]//g'

The ``128`` value is chosen by me and you can use anything you want, say from 64
characters onwards to end up with a very secure password. The more characters
the lower the speed of the password creation but the higher the security.

However if you really don't want an alphanumeric password you can url encode it

::

    [isabell@gitlab ~]$ python3
    Python 3.6.8 (default, Apr  2 2020, 13:34:55)
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib.parse as p
    >>> password = '# {my secret password as string or as bytes!}'
    >>> p.quote(password)
    '%23%20%7Bmy%20secret%20password%20as%20string%20or%20as%20bytes%21%7D'


Installation Dependencies
=========================

There are a lot of them and some need to be built from source. I'll just tell
about those which need attention or are not installed by default on uberspace
hosts. You can have a look at all dependencies at `GitLab installation from
source dependencies`_ . The basic working directory is ``$HOME/workspace``. You
can choose a different one if you like. Since we dont' need it anymore when
`GitLab`_ is installed, delete it when you reached the end of the gitlab
installation process to get back some disk space.

Cmake
-----

Check the current available version of ``cmake`` with

::

    [isabell@gitlab ~]$ cmake --version

If it is below ``3.0.0`` than we'll need to install cmake from source. You can
skip the ``test`` if you like to, because it takes a while to complete but to be
sure that your installation will work you should run it.

::

    [isabell@gitlab ~]$ mkdir -p workspace/cmake
    [isabell@gitlab ~]$ cd workspace/cmake
    [isabell@gitlab ~/workspace/cmake]$ wget https://github.com/Kitware/CMake/releases/download/v3.18.3/cmake-3.18.3.tar.gz
    [isabell@gitlab ~/workspace/cmake]$ tar xzf cmake-3.18.3.tar.gz && cd cmake-3.18.3
    [isabell@gitlab ~/workspace/cmake/cmake-3.18.3]$ ./bootstrap --prefix=$HOME/.local --docdir=share --mandir=share
    [isabell@gitlab ~/workspace/cmake/cmake-3.18.3]$ make
    [isabell@gitlab ~/workspace/cmake/cmake-3.18.3]$ make test # this may take a while
    [isabell@gitlab ~/workspace/cmake/cmake-3.18.3]$ make install

and add the ``$HOME/.local/bin`` dir to the PATH

::

    [isabell@gitlab ~]$ echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc
    [isabell@gitlab ~]$ source .bashrc

Check the cmake version

::

    [isabell@gitlab ~]$ cmake --version
    cmake version 3.18.3

    CMake suite maintained and supported by Kitware (kitware.com/cmake).

If your output looks similar you're all set.

Git
---

Check that git has minimum version ``>=2.24.0`` and is compiled with ``libpcre2``.

::

    [isabell@gitlab ~]$ git --version && ldd $(command -v git) | grep pcre2
    git version 2.24.3
        libpcre2-8.so.0 => /lib64/libpcre2-8.so.0 (0x00007fc2bf65c000)

This is normally the case and if the output looks similar then everything's
fine.

Exiftool
--------

GitLab Workhorse needs ``exiftool`` to remove EXIF data from uploaded images.
As of ``Uberspace 7.7.9.0`` it is not available but you can check yourself with

::

    [isabell@gitlab ~]$ command -v exiftool
    [isabell@gitlab ~]$

If this returns an error with no output we'll install it from source into the
``$HOME/.local`` hierarchy

::

    [isabell@gitlab ~]$ mkdir -p workspace/exiftool
    [isabell@gitlab ~]$ cd workspace/exiftool
    [isabell@gitlab ~/workspace/exiftool]$ wget 'https://exiftool.org/Image-ExifTool-12.07.tar.gz'
    [isabell@gitlab ~/workspace/exiftool]$ tar xzf Image-ExifTool-12.07.tar.gz
    [isabell@gitlab ~/workspace/exiftool]$ cd Image-ExifTool-12.07
    [isabell@gitlab ~/workspace/exiftool/Image-ExifTool-12.07]$ perl Makefile.PL INSTALL_BASE="$HOME/.local"
    [isabell@gitlab ~/workspace/exiftool/Image-ExifTool-12.07]$ make test
    [isabell@gitlab ~/workspace/exiftool/Image-ExifTool-12.07]$ make install

The man pages of ``exiftool`` aren't installed into the right location so we
have to fix that:

::

    [isabell@gitlab ~/workspace/exiftool/Image-ExifTool-12.07]$ cd ~/.local
    [isabell@gitlab ~/.local]$ cp -af man/ share/ && rm -rf man/

Optionally add the ``$HOME/.local/share/man`` and ``$HOME/.local/share/info``
paths to MANPATH and INFOPATH in your ``.bashrc``

.. code-block:: bash

    export MANPATH="$HOME/.local/share/man:$MANPATH"
    export INFOPATH="$HOME/.local/share/info:$INFOPATH"

Next add the local perl libraries to the INC path of perl. Edit
``$HOME/.bashrc`` and add

.. code-block:: bash

    export PERL5LIB="$HOME/.local/lib/perl5:$PERL5LIB"

Now source your ``.bashrc``

::

    [isabell@gitlab ~]$ source .bashrc

Check that the INC path includes ``/home/GITLAB_USERNAME/.local/lib/perl5``

::

    [isabell@gitlab ~]$ perl -V
    # ...
    @INC:
        /home/<username>/.local/lib/perl5
        /usr/local/lib64/perl5
        /usr/local/share/perl5
        /usr/lib64/perl5/vendor_perl
        /usr/share/perl5/vendor_perl
        /usr/lib64/perl5
        /usr/share/perl5

At the very bottom of this pretty long output you'll see the INC path where
``<username>`` is your ``GITLAB_USERNAME``.

Ruby
----

We'll need ruby in version ``2.6.x``. Check the current version with

::

    [isabell@gitlab ~]$ ruby --version

If it is below or higher than the required version we'll change to ``2.6``

::

    [isabell@gitlab ~]$ uberspace tools version use ruby 2.6
    Using 'Ruby' version: '2.6'

Bundler is needed in a version ``>=1.5.2, < 2``. Install bundler with

::

    [isabell@gitlab ~]$ gem install bundler --no-document --version '>=1.5.2, < 2'

Re2
---

Usually ``libre2`` isn't installed on uberspace hosts but you can check it
yourself with

::


    [isabell@gitlab ~]$ /sbin/ldconfig -p | grep 'libre2\.so' || echo nope
    nope


So let's install it from source

::

    [isabell@gitlab ~]$ mkdir -p workspace/libre2 && cd workspace
    [isabell@gitlab ~/workspace]$ git clone 'https://github.com/google/re2.git' libre2
    [isabell@gitlab ~/workspace]$ cd libre2
    [isabell@gitlab ~/workspace/libre2]$ make prefix="$HOME/.local"
    [isabell@gitlab ~/workspace/libre2]$ make test prefix="$HOME/.local"
    [isabell@gitlab ~/workspace/libre2]$ make install prefix="$HOME/.local"
    [isabell@gitlab ~/workspace/libre2]$ make testinstall prefix="$HOME/.local"

Make sure that ``LD_LIBRARY_PATH`` is set to include ``$HOME/.local/lib`` in your
``.bashrc``

.. code-block:: bash

    export LD_LIBRARY_PATH="$HOME/.local/lib:$LD_LIBRARY_PATH"

and source your ``.bashrc``

::

    [isabell@gitlab ~]$ source .bashrc

bundler needs to know about the ``libre2`` path too

::

    [isabell@gitlab ~]$ bundler config set --global build.re2 "--with-re2-dir=$HOME/.local"

Runit
-----

Only the ``runit`` binaries are required but since they are not installed on
uberspace we need to compile them ourselves

::

    [isabell@gitlab ~]$ mkdir -p workspace/runit
    [isabell@gitlab ~]$ cd workspace/runit
    [isabell@gitlab ~/workspace/runit]$ wget 'http://smarden.org/runit/runit-2.1.2.tar.gz'
    [isabell@gitlab ~/workspace/runit]$ tar xzpf runit-2.1.2.tar.gz
    [isabell@gitlab ~/workspace/runit]$ cd admin/runit-2.1.2
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ sed -i 's/ -static//g' src/Makefile
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ sed -i 's:/service/:'"$HOME"'/.local/var/service/:g' src/sv.c
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ echo 'gcc' > src/conf-cc
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ echo 'gcc -s' > src/conf-ld
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ make
    [isabell@gitlab ~/workspace/runit/admin/runit-2.1.2]$ for c in (<package/commands); do cp -a "src/$c" "$HOME/.local/bin/$c"; done


If you've not already added ``$HOME/.local/bin`` to your ``PATH`` do it now.

Node
----

nodejs is required with a minimum version of ``>= 10.13.0`` but node ``12.x`` is
faster. Check you're version with

::

    [isabell@gitlab ~]$ node --version

and if necessary change it with

::

    [isabell@gitlab ~]$ uberspace tools version node 12

yarn is needed with a minimum version of ``>=1.10.0`` and is installed on
uberspace but check with

::

    [isabell@gitlab ~]$ yarn --version

PostgreSQL
----------

This is the only supported database by `GitLab`_. We need postgresql installed
on both the ``gitlab`` host for the libraries and on the ``sidekiq`` host for
the functionality.

PostgreSQL Installation
^^^^^^^^^^^^^^^^^^^^^^^

.. note:: To keep things in line start the `PostgreSQL Installation`_ on the
   ``sidekiq`` host and then on the ``gitlab`` host before `Creating the
   Database Cluster`_.

Follow the uberlab guide :lab:`PostgreSQL <guide_postgresql>` until
:lab_anchor:`Step 3 <guide_postgresql.html#step3-environment-settings>`. I
strongly recommend configuring with ``./configure --prefix $HOME/.local`` into
the ``$HOME/.local`` hierarchy because I will refer to this directory structure
in this guide. It also makes sure that your PATH settings don't need to be
adjusted once you've added ``$HOME/.local/bin`` to you're PATH in the
``.bashrc`` like described above.

In your ``$HOME/.bashrc`` adjust the ``LD_LIBRARY_PATH`` to include
``$HOME/.local/lib/postgresql`` and ``PGPASSFILE`` environment variables

.. code-block:: bash

    export LD_LIBRARY_PATH="$HOME/.local/lib/postgresql:$HOME/.local/lib:$LD_LIBRARY_PATH"
    export PGPASSFILE="$HOME/.pgpass"

and source ``$HOME/.bashrc`` to make you're current shell recognize the changes.

Create and edit the ``$HOME/.pgpass`` file with the following content

.. warning:: Replace ``SIDEKIQ_USERNAME``. Replace
   ``POSTGRESQL_SUPERUSER_PASSWORD`` with a secure password. (See the
   `Passwords`_ section)

::

    *:*:*:SIDEKIQ_USERNAME:POSTGRESQL_SUPERUSER_PASSWORD

Change permissions to

::

    [isabell@sidekiq ~]$ chmod 0600 "$HOME/.pgpass"

Creating the Database Cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: We need the database cluster only on the ``sidekiq`` host.

Dump your plain ``POSTGRESQL_SUPERUSER_PASSWORD`` from above into
``$HOME/pgpass.temp``

.. warning:: Replace ``POSTGRESQL_SUPERUSER_PASSWORD``

::

    POSTGRESQL_SUPERUSER_PASSWORD

Create the database cluster and remove the temporary ``$HOME/pgpass.temp`` file.

::

    [isabell@sidekiq ~]$ initdb --pwfile ~/pgpass.temp --auth=scram-sha-256 -E UTF8 -D ~/.local/var/postgresql
    [isabell@sidekiq ~]$ rm "$HOME/pgpass.temp"

Port
^^^^

.. note:: This step is also only needed on the ``sidekiq`` host

We need ``postgresql`` to be available from the outside so the ``gitlab`` host
can communicate with ``postgresql``. On the ``sidekiq`` host execute

::

    [isabell@sidekiq ~]$ uberspace port add
    Port 55555 will be open for TCP and UDP traffic in a few minutes.

Write this port number down, in this case ``55555``. We'll need it in
different places later. I'll refer to it with ``POSTGRESQL_PORT``.

Configuration
^^^^^^^^^^^^^

.. note:: Only on the ``sidekiq`` host if not otherwise noted

Edit the ``$HOME/.local/var/postgresql/postgresql.conf`` configuration file and
adjust the following values:


.. warning:: Replace ``POSTGRESQL_PORT``

::

    listen_addressses = '*'
    port = POSTGRESQL_PORT

In the next step we need the external ip address of our ``gitlab`` host. You
can get the ip address by executing

.. warning:: Replace ``GITLAB_FQDN``

::

    [isabell@sidekiq ~]$ dig GITLAB_FQDN +short
    185.26.156.230

for example on your ``sidekiq`` host. I'll refer to this ip with ``GITLAB_IP``.

To secure the database edit the ``$HOME/.local/var/postgresql/pg_hba.conf``
configuration file on your ``gitlab`` host:

.. warning:: Replace ``GITLAB_IP``

::

    # TYPE  DATABASE        USER            ADDRESS                 METHOD

    # local   all             all                                 scram-sha-256
    host    all             all             127.0.0.1/32        scram-sha-256
    host    all             all             ::1/32              scram-sha-256
    host    gitlab          gitlab          GITLAB_IP/32       scram-sha-256

The ``local`` type sets the connection method for linux ``unix`` sockets, but
postgresql doesn't listen on both tcp and unix sockets, so we comment it out.
``host`` configures ``tcp`` sockets. The last line ensures that you can connect
from your ``gitlab`` host to the ``sidekiq`` host.

Add or adjust the following environment variables in your ``.bashrc``

.. warning:: Replace ``POSTGRESQL_PORT``

.. code-block:: bash

    # PostgreSQL configuration on the sidekiq host

    export PGPASSFILE="$HOME/.pgpass"
    export PGHOST="localhost"
    export PGPORT="POSTGRESQL_PORT"
    export PGDATA="$HOME/.local/var/postgresql"
    export PGUSER="gitlab"
    export PGDATABASE="gitlab"

and source it with ``source $HOME/.bashrc``.

On the ``gitlab`` host add the following to your ``.bashrc``

.. warning:: Replace ``POSTGRESQL_PORT`` and ``SIDEKIQ_FQDN``.

.. code-block:: bash

    # PostgreSQL configuration on the gitlab host
    export PGPASSFILE="$HOME/.pgpass"
    export PGHOST="SIDEKIQ_FQDN"
    export PGPORT="POSTGRESQL_PORT"
    export PGUSER="gitlab"
    export PGDATABASE="gitlab"

and source it.

Setup the supervisor PostgreSQL service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Only on the ``sidekiq`` host

Create ``$HOME/etc/services.d/postgresql.ini`` with the folllowing content:

::

    [program:postgresql]
    command=%(ENV_HOME)s/.local/bin/postgres -D %(ENV_HOME)s/.local/var/postgresql/
    autostart=yes
    autorestart=yes
    redirect_stderr=true
    stdout_logfile=%(ENV_HOME)s/logs/postgresql.log


and start it with

::

    [isabell@sidekiq ~]$ supervisorctl reread
    [isabell@sidekiq ~]$ supervisorctl update postgresql
    [isabell@sidekiq ~]$ supervisorctl status postgresql

Make sure postgresql is listening on the configured port and addresses

::

    [isabell@sidekiq ~]$ netstat -tlpn | grep postgres
    tcp        0      0 0.0.0.0:port           0.0.0.0:*               LISTEN      1786/postgres
    tcp6       0      0 :::port                :::*                    LISTEN      1786/postgres

The output should look similar to the output above with your ``POSTGRESQL_PORT``
as ``port``. The process number in ``1786/postgres`` may differ, too.

Check PostgreSQL connection from sidekiq host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check that you can connect to the database from your ``sidekiq`` host as
superuser.

.. warning:: Replace ``SIDEKIQ_USERNAME``

::

    [isabell@sidekiq ~]$ psql -U SIDEKIQ_USERNAME -d postgres
    psql (12.4)
    Type "help" for help.

    postgres=#

You should see the postgresql command prompt. You can exit with ``CTRL-D`` or by
typing ``\q`` and hitting the ``ENTER`` key. But first list the current database
users and verify that everything's alright

::

    postgres=# \du
                                      List of roles
    Role name |                         Attributes                         | Member of
    ----------+------------------------------------------------------------+-----------
    username  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

where username in the ``Role name`` column should be your ``SIDEKIQ_USERNAME``.
For the next step stay in the prompt.

Create the GitLab Database
^^^^^^^^^^^^^^^^^^^^^^^^^^

Supposed you're still connected as your user to the ``postgres`` database we
now setup the ``gitlab`` database user and database. The actual production
database and user should be different from the superuser to limit its power as
far as possible.

.. warning:: Replace ``POSTGRESQL_GITLAB_PASSWORD`` with a password different from
   the ``POSTGRESQL_SUPERUSER_PASSWORD``. (See the `Passwords`_ section.)

::

    postgres=# \c template1
    template1=# CREATE USER gitlab with password 'POSTGRESQL_GITLAB_PASSWORD' CREATEDB;
    template1=# CREATE EXTENSION IF NOT EXIST pg_trgm;
    template1=# CREATE EXTENSION IF NOT EXIST btree_gist;
    template1=# CREATE DATABASE gitlab OWNER gitlab;
    template1=\q


Now add the password from above to the ``$HOME/.pgpass`` file on the ``sidekiq``
and ``gitlab`` host which should now like like

.. warning:: Replace ``SIDEKIQ_USERNAME``, ``POSTGRESQL_SUPERUSER_PASSWORD`` and
   ``POSTGRESQL_GITLAB_PASSWORD``

::

    *:*:*:SIDEKIQ_USERNAME:POSTGRESQL_SUPERUSER_PASSWORD
    *:*:gitlab:gitlab:POSTGRESQL_GITLAB_PASSWORD

Try to connect to the ``gitlab`` database as ``gitlab`` user and check that
the extensions are enabled

::

    [isabell@sidekiq ~]$ psql -U gitlab -d gitlab
    gitlab=# SELECT true AS enabled
    gitlab=# FROM pg_available_extensions
    gitlab=# WHERE name = 'pg_trgm'
    gitlab=# AND installed_version IS NOT NULL;
     enabled
    ---------
     t
    (1 row)

    gitlab=# SELECT true AS enabled
    gitlab=# FROM pg_available_extensions
    gitlab=# WHERE name = 'btree_gist'
    gitlab=# AND installed_version IS NOT NULL;
     enabled
    ---------
     t
    (1 row)

    gitlab=# \q

The enabled column should contain a row with ``t``. The extensions are required
by `GitLab`_ 13.1+.

Check PostgreSQL from the gitlab host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With all the environment set in the ``.bashrc`` and the database password stored
in ``$HOME/.pgpass`` it's just one command away to connect to the database from
the ``gitlab`` host as gitlab user

::

    [isabell@gitlab ~]$ psql
    psql (12.4)
    Type "help" for help.

    gitlab=> \q


Redis
-----

Redis is installled on uberspace hosts so just quickly check that redis version
is ``>=6.x``

::

    [isabell@gitlab ~]$ redis-server --version

For an in-depth guide see the :lab:`Redis <guide_redis>` lab guide. Here in
short. We need redis to accept outside connections for ``sidekiq`` in addition
to its socket so let's aquire a port for it. I'll refer to it as ``REDIS_PORT``

::

    [isabell@gitlab ~]$ uberspace port add
    Port 66666 will be open for TCP and UDP traffic in a few minutes.

We further need the bind url

::

    [isabell@gitlab ~]$ /sbin/ifconfig | grep -A1 veth
    veth_isabell: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 100.64.4.52  netmask 255.255.255.252  broadcast 0.0.0.0

Look out for the inet key in the last line and write the ip down. The
``veth_isabell`` line will look different from yours and the ip in the case
above would be ``100.64.4.52``. I'll refer to it as ``GITLAB_VETH_IP``

Now create the redis directory

::

    [isabell@gitlab ~]$ mkdir "$HOME/.redis"

and the ``$HOME/.redis/conf`` file in it

.. warning:: Replace ``GITLAB_VETH_IP``, ``REDIS_PORT``, ``GITLAB_USERNAME`` and
   ``REDIS_PASSWORD`` with a secure password. (See `Passwords`_)

::

    bind GITLAB_VETH_IP
    port REDIS_PORT
    unixsocket /home/GITLAB_USERNAME/.redis/sock
    requirepass REDIS_PASSWORD
    daemonize no

Setup the damon and create ``$HOME/etc/services.d/redis.ini`` with the following
content:

::

    [program:redis]
    command=redis-server %(ENV_HOME)s/.redis/conf
    autostart=yes
    autorestart=yes
    redirect_stderr=true
    stdout_logfile=%(ENV_HOME)s/logs/redis.log


Let's start redis

::

    [isabell@gitlab ~]$ supervisorctl reread
    [isabell@gitlab ~]$ supervisorctl update redis
    [isabell@gitlab ~]$ supervisorctl status redis

and eventually check that redis works as expected (you'll end up in a redis
prompt)

.. note:: Do this from your ``sidekiq`` host and ``gitlab`` host. On the
   ``gitlab`` host you don't need to specify the REDIS_PORT and GITLAB_FQDN
   since you can connect via the redis socket. A simple ``$ redis-cli`` will
   do.

.. warning:: Replace ``REDIS_PORT``, ``GITLAB_FQDN`` and ``REDIS_PASSWORD``

::

    [isabell@sidekiq ~]$ redis-cli -p REDIS_PORT -h GITLAB_FQDN
    host:port> ping
    (error) NOAUTH Authentication required.
    host:port> auth REDIS_PASSWORD
    OK
    host:port> ping
    PONG
    host:port> quit

``host`` should match ``GITLAB_FQDN``  and ``port`` the ``REDIS_PORT``. If your
prompt looks like that after typing all commands you're all set. If not you
should go through the `Redis`_ section again.


Installation GitLab
===================

.. note:: This guide is tested with `GitLab`_ 13.4.2.

Pull the source

::

    [isabell@gitlab ~]$ git clone https://gitlab.com/gitlab-org/gitlab-foss.git -b 13-4-stable gitlab
    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ git checkout v13.4.2

Configuration
-------------

Change the current directory

::

    [isabell@gitlab ~/gitlab]$ cd config
    [isabell@gitlab ~/gitlab/config]$


and copy the example files

::

    [isabell@gitlab ~/gitlab/config]$ cp gitlab.yml.example gitlab.yml

    [isabell@gitlab ~/gitlab/config]$ cp secrets.yml.example secrets.yml
    [isabell@gitlab ~/gitlab/config]$ chmod 0600 secrets.yml

    [isabell@gitlab ~/gitlab/config]$ cp puma.rb.example puma.rb

    [isabell@gitlab ~/gitlab/config]$ cp resque.yml.example resque.yml
    [isabell@gitlab ~/gitlab/config]$ chmod 0600 resque.yml

    [isabell@gitlab ~/gitlab/config]$ cp database.yml.example database.yml
    [isabell@gitlab ~/gitlab/config]$ chmod 0600 database.yml

    [isabell@gitlab ~/gitlab/config]$ cp initializers/smtp_settings.rb.sample initializers/smtp_settings.rb
    [isabell@gitlab ~/gitlab/config]$ chmod 0600 initializers/smtp_settings.rb

We need to change all occurences of ``/home/git/`` to your actual home
``/home/GITLAB_USERNAME/``

.. warning:: Replace ``GITLAB_USERNAME``

::

    [isabell@gitlab ~/gitlab/config]$ sed -i 's:/home/git/:/home/GITLAB_USERNAME/:g' gitlab.yml secrets.yml puma.rb resque.yml database.yml


Edit ``gitlab.yml`` to match the following (only required changes are listed)

.. warning:: Replace ``GITLAB_USERNAME``, ``GITLAB_EXTERNAL_FQDN``

   The file is big so you may need to scroll down a lot to get to the configuration key.

::

    production: &base

        # ...

        gitlab:
            host: GITLAB_EXTERNAL_FQDN
            port: 443
            https: true

            # ...

            user: GITLAB_USERNAME

            # ...

            email_enabled: true
            email_from: GITLAB_USERNAME@uber.space
            email_display_name: GitLab
            email_reply_to: GITLAB_USERNAME@uber.space

        # ...

        repositories:
            # ...
            storages:
                default:
                    #
                    gitaly_address: unix:/home/GITLAB_USERNAME/gitlab/tmp/sockets/private/gitaly.socket


Edit ``puma.rb`` to match the following (only required changes are listed)

.. warning:: Replace ``GITLAB_USERNAME``

::

    # ...
    threads 1, 16
    # ...
    bind 'unix:///home/GITLAB_USERNAME/gitlab/tmp/sockets/gitlab.socket'
    workers 1
    # ...
    worker_timeout 100

Setting the ``workers`` count to 1 limits the RAM usage of puma. The main puma
process and one puma worker use up to 600MB each. This sums up to around 1-1.2GB
and leaves some headroom but not enough for another worker.

Edit ``resque.yml`` to match the following (only required changes are listed)

.. warning:: Replace ``GITLAB_USERNAME`` and ``REDIS_PASSWORD``

::

    # ...
    production:
        url: unix:/home/GITLAB_USERNAME/.redis.sock
        password: REDIS_PASSWORD

Edit ``database.yml`` to match the following (only required changes are listed)

.. warning:: Replace ``POSTGRESQL_PORT`` and ``POSTGRESQL_GITLAB_PASSWORD``

::

    production:
        # ...
        database: gitlab
        username: gitlab
        password: POSTGRESQL_GITLAB_PASSWORD
        host: localhost
        port: POSTGRESQL_PORT

    # ...

Edit ``initializers/smtp_settings.rb`` to match the following

.. warning:: Replace ``GITLAB_FQDN``,
   ``GITLAB_USERNAME``, ``GITLAB_EMAIL_PASSWORD`` and ``GITLAB_EXTERNAL_FQDN``

::

    # ...
    if Rails.env.production?
    Rails.application.config.action_mailer.delivery_method = :smtp

    ActionMailer::Base.delivery_method = :smtp
    ActionMailer::Base.smtp_settings = {
      address: "GITLAB_FQDN",
      port: 587,
      user_name: "GITLAB_USERNAME@uber.space",
      password: "GITLAB_EMAIL_PASSWORD",
      domain: "GITLAB_EXTERNAL_FQDN",
      authentication: :plain,
      enable_starttls_auto: true,
      tls: false,
      ssl: false,
      openssl_verify_mode: 'none' # See ActionMailer documentation for other possible options


Directories
-----------

Ensure that the basic directories exist and have the correct permissions

::


    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ chmod -R 0770 log/

    [isabell@gitlab ~/gitlab]$ chmod -R 0770 tmp/
    [isabell@gitlab ~/gitlab]$ chmod -R 0770 tmp/pids/
    [isabell@gitlab ~/gitlab]$ chmod -R 0770 tmp/sockets/
    [isabell@gitlab ~/gitlab]$ chmod 0700 tmp/sockets/private

    [isabell@gitlab ~/gitlab]$ mkdir -p public/uploads
    [isabell@gitlab ~/gitlab]$ chmod -R 0700 public/uploads

    [isabell@gitlab ~/gitlab]$ chmod -R 0770 builds/

    [isabell@gitlab ~/gitlab]$ chmod -R 0770 shared/artifacts
    [isabell@gitlab ~/gitlab]$ chmod -R 0770 shared/pages/

Git
---

Configure git

::

    [isabell@gitlab ~]$ git config --global core.autocrlf input
    [isabell@gitlab ~]$ git config --global gc.auto 0
    [isabell@gitlab ~]$ git config --global repack.writeBitmaps true
    [isabell@gitlab ~]$ git config --global receive.advertisePushOptions true
    [isabell@gitlab ~]$ git config --global core.fsyncObjectFiles true

Install Gems
------------

This step fails if the bundler build configuration hasn't the correct ``re2``
path. Double check the `Ruby`_ section.

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ bundle install --deployment --without development test mysql aws kerberos

Install GitLab Shell
--------------------

::

    [isabell@gitlab ~/gitlab]$ bundle exec rake gitlab:shell:install RAILS_ENV=production

The gitlab-shell configuration is auto generated from the configuration values
above but it doesn't harm to double check. This is what the
``$HOME/gitlab-shell/config.yml`` configuration file should look like

.. warning:: Replace ``GITLAB_USERNAME`` and ``GITLAB_EXTERNAL_FQDN``

::

    ---
    user: GITLAB_USERNAME
    gitlab_url: "https://GITLAB_EXTERNAL_FQDN"
    http_settings:
        ca_path: '/home/GITLAB_USERNAME/etc/certificates'
        self_signed_cert: false
    auth_file: '/home/GITLAB_USERNAME/.ssh/authorized_keys'
    log_level: INFO
    audit_usernames: false


Install GitLab Workhorse
------------------------

Under normal cirumstances the nginx weberver communicates over a socket with
gitlab-workhorse but since we don't have the option to install a nginx
configuration file to set this up and apache doesn't support reverse proxying to
sockets we use a tcp port on the loopback interface. Make sure that the port
8181 isn't occupied by another processes. I'll refer to it as
``GITLAB_WORKHORSE_PORT``.

::

    [isabell@gitlab ~]$ netstat -tulpn | grep '\b8181\b' || echo nope
    nope

If there is a process occupying the port just choose another one that is above
``1024``. Connections only operating on the loopback interface don't need to be
unlocked by the firewall with ``uberspace port add``.

.. warning:: Replace ``GITLAB_USERNAME``

::

    [isabell@gitlab ~/gitlab]$ bundle exec rake "gitlab:workhorse:install[/home/GITLAB_USERNAME/gitlab-workhorse]" RAILS_ENV=production

The gitlab-workhorse needs a supervisor service in
``$HOME/etc/services.d/gitlab-workhorse.ini``


.. warning:: Replace ``GITLAB_USERNAME`` and ``GITLAB_WORKHORSE_PORT``

::


    [program:workhorse]
    directory=%(ENV_HOME)s/gitlab
    command=%(ENV_HOME)s/gitlab-workhorse/gitlab-workhorse -listenUmask 0 -listenNetwork tcp -listenAddr 0.0.0.0:GITLAB_WORKHORSE_PORT -authBackend http://127.0.0.1:9292 -authSocket %(ENV_HOME)s/gitlab/tmp/sockets/gitlab.socket -documentRoot %(ENV_HOME)s/gitlab/public
    environment=PERL5LIB="/home/GITLAB_USERNAME/.local/lib/perl5",LD_LIBRARY_PATH="/opt/rh/devtoolset-9/root/usr/lib64:/opt/rh/devtoolset-9/root/usr/lib:/opt/rh/devtoolset-9/root/usr/lib64/dyninst:/opt/rh/devtoolset-9/root/usr/lib/dyninst:/home/GITLAB_USERNAME/.local/lib:/home/GITLAB_USERNAME/.local/postgresql/lib",PATH="/home/GITLAB_USERNAME/.local/bin:/home/GITLAB_USERNAME/bin:/opt/uberspace/etc/GITLAB_USERNAME/binpaths/ruby:/opt/rh/devtoolset-9/root/usr/bin:/home/GITLAB_USERNAME/.cargo/bin:/home/GITLAB_USERNAME/.luarocks/bin:/home/GITLAB_USERNAME/go/bin:/home/GITLAB_USERNAME/.deno/bin:/home/GITLAB_USERNAME/.config/composer/vendor/bin:/bin:/usr/bin:/usr/ucb:/usr/local/bin:/home/GITLAB_USERNAME/.dotnet/tools"
    redirect_stderr=true
    stdout_logfile=%(ENV_HOME)s/gitlab/log/gitlab-workhorse.log


The ``-authBackend`` settings isn't needed actually because the ``-authSocket``
takes precedence but if you would like to change the method ``gitlab-workhorse``
and ``puma`` communicate then change it to the port number ``puma`` is listening
on. The default is ``9292``.

Reread the supervisor configuration but do NOT start ``gitlab-workhorse`` yet.

::

    [isabell@gitlab ~]$ supervisorctl reread


Install Gitaly
--------------

.. warning:: Replace ``GITLAB_USERNAME``

::

    [isabell@gitlab ~/gitlab]$ bundle exec rake "gitlab:gitaly:install[/home/GITLAB_USERNAME/gitaly,/home/GITLAB_USERNAME/repositories]" RAILS_ENV=production

The ``sidekiq`` host needs to communicate with gitaly and we need another open
port. The last one. I'll refer to it with ``GITALY_PORT``.

::

    [isabell@gitlab ~]$ uberspace port add
    Port 77777 will be open for TCP and UDP traffic in a few minutes.

Now let's check the auto-generated gitaly configuration file
``$HOME/gitaly/config.toml`` and add or change configuration options to match
the following:

.. warning:: Replace ``GITLAB_USERNAME``, ``GITLAB_VETH_IP``, ``GITALY_PORT``
   and ``GITLAB_EXTERNAL_FQDN``

::

    bin_dir = "/home/GITLAB_USERNAME/gitaly"
    internal_socket_dir = "/home/GITLAB_USERNAME/gitaly/internal_sockets"
    socket_path = "/home/GITLAB_USERNAME/gitlab/tmp/sockets/private/gitaly.socket"
    listen_addr = "GITLAB_VETH_IP:GITALY_PORT"
    [gitaly-ruby]
    dir = "/home/GITLAB_USERNAME/gitaly/ruby"
    [gitlab]
    url = "https://GITLAB_EXTERNAL_FQDN"
    [gitlab-shell]
    dir = "/home/GITLAB_USERNAME/gitlab-shell"
    [[storage]]
    name = "default"
    path = "/home/GITLAB_USERNAME/repositories"


Setup the supervisor service in ``$HOME/etc/services.d/gitaly.ini``

.. warning:: Replace ``GITLAB_USERNAME``

::

    [program:gitaly]
    directory=%(ENV_HOME)s/gitlab
    command=nohup %(ENV_HOME)s/gitaly/gitaly %(ENV_HOME)s/gitaly/config.toml
    environment=LD_LIBRARY_PATH="/opt/rh/devtoolset-9/root/usr/lib64:/opt/rh/devtoolset-9/root/usr/lib:/opt/rh/devtoolset-9/root/usr/lib64/dyninst:/opt/rh/devtoolset-9/root/usr/lib/dyninst:/home/GITLAB_USERNAME/.local/lib:/home/GITLAB_USERNAME/.local/postgresql/lib",PATH="/home/GITLAB_USERNAME/.local/bin:/home/GITLAB_USERNAME/bin:/opt/uberspace/etc/GITLAB_USERNAME/binpaths/ruby:/opt/rh/devtoolset-9/root/usr/bin:/home/GITLAB_USERNAME/.cargo/bin:/home/GITLAB_USERNAME/.luarocks/bin:/home/GITLAB_USERNAME/go/bin:/home/GITLAB_USERNAME/.deno/bin:/home/GITLAB_USERNAME/.config/composer/vendor/bin:/bin:/usr/bin:/usr/ucb:/usr/local/bin:/home/GITLAB_USERNAME/.dotnet/tools"
    autostart=yes
    autorestart=yes
    redirect_stderr=true
    stdout_logfile=%(ENV_HOME)s/gitlab/log/gitaly.log


Gitaly must be running for the next section to work

::


    [isabell@gitlab ~]$ supervisorctl reread
    [isabell@gitlab ~]$ supervisorctl update gitaly
    [isabell@gitlab ~]$ supervisorctl status gitaly


Initialize Database
-------------------

.. warning:: The command below with all given flags is destructive! Only use it
   if you need to setup the database the first time or if you know what you're
   doing!

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ bundle exec rake gitlab:setup RAILS_ENV=production DISABLE_DATABASE_ENVIRONMENT_CHECK=1 force=yes

``DISABLE_DATABASE_ENVIRONMENT_CHECK=1`` lets you drop the production database
and ``force=yes`` disables the interactive questions if you really want to do
that.

Post installation steps
-----------------------

Stop the gitaly process for the moment

::

    [isabell@gitlab ~]$ supervisorctl stop gitaly

and check the application status

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ bundle exec rake gitlab:env:info RAILS_ENV=production
    System information
    System:
    Current User:   <username>
    Using RVM:      no
    Ruby Version:   2.6.6p146
    Gem Version:    3.1.4
    Bundler Version:1.17.3
    Rake Version:   12.3.3
    Redis Version:  6.0.8
    Git Version:    2.24.3
    Sidekiq Version:5.2.9
    Go Version:     go1.15.1 linux/amd64

    GitLab information
    Version:        13.4.2
    Revision:       b08b36dccc3
    Directory:      /home/<username>/gitlab
    DB Adapter:     PostgreSQL
    DB Version:     12.4
    URL:            https://<username>.uber.space
    HTTP Clone URL: https://<username>.uber.space/some-group/some-project.git
    SSH Clone URL:  <username>@<username>.uber.space:some-group/some-project.git
    Using LDAP:     no
    Using Omniauth: yes
    Omniauth Providers:

    GitLab Shell
    Version:        13.7.0
    Repository storage paths:
    1. default:      /home/<username>/repositories
    GitLab Shell path:              /home/<username>/gitlab-shell
    Git:            /usr/bin/git

Your output should look similar to this but with ``<username>`` replaced with
your ``GITLAB_USERNAME``.

Compile GetText PO files
------------------------

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ bundle exec rake gettext:compile RAILS_ENV=production

Install yarn packages
---------------------

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ yarn install --production --pure-lockfile

Compile assets
--------------

This step hasn't worked for me on my uberspace host because the ``webpack``
process uses too much RAM and gets killed in the middle. The solution is to
compile the assets locally.

Make sure you have the minimum ``node`` and ``yarn`` versions installed
otherwise install them with your package manager. You'll also need cmake ``>=
3.x`` and the libre2-dev package. The package name may differ depending on your
OS. If something goes wrong this is most likely because you're missing some
dependencies. Check the dependencies section at `GitLab installation from source
dependencies`_. Next we go through some of the steps again to be able to
compile the assets locally. It's not that much anymore like before.


.. warning:: Checkout the same gitlab version on your local host than the one
   on your ``gitlab`` host.

::


    [isabell@home ~]$ mkdir -p workspace/
    [isabell@home ~/workspace]$ cd workspace/
    [isabell@home ~/workspace]$ git clone https://gitlab.com/gitlab-org/gitlab-foss.git -b 13-4-stable gitlab
    [isabell@home ~/workspace]$ cd gitlab
    [isabell@home ~/workspace/gitlab]$ gem install bundler --version '>=1.5.2, < 2'
    [isabell@home ~/workspace/gitlab]$ git checkout v13.4.2
    [isabell@home ~/workspace/gitlab]$ bundle install --deployment --without development test mysql aws kerberos

For the next step to work you'll need some configuration files from your
``gitlab`` host. Download them for example with

.. warning:: Replace ``GITLAB_USERNAME`` and ``GITLAB_FQDN``

::

    [isabell@home ~/workspace/gitlab]$ scp GITLAB_USERNAME@GITLAB_FQDN:'gitlab/config/{database.yml,gitlab.yml}' config


Now compile the assets

::

    [isabell@home ~/workspace/gitlab]$ bundle exec rake gettext:compile RAILS_ENV=production
    [isabell@home ~/workspace/gitlab]$ yarn install --production --pure-lockfile
    [isabell@home ~/workspace/gitlab]$ bundle exec rake gitlab:assets:compile RAILS_ENV=production NODE_ENV=production

This may take a while to complete but in next step we can upload the assets to
the ``gitlab`` host. You can either upload it directly or compress them first
like described here

::

    [isabell@home ~/workspace/gitlab]$ cd public
    [isabell@home ~/workspace/gitlab/public]$ tar czf assets.tar.gz assets/
    [isabell@home ~/workspace/gitlab/public]$ scp assets.tar.gz GITLAB_USERNAME@GITLAB_FQDN:gitlab/public

Next on your ``gitlab`` host

::

    [isabell@gitlab ~]$ cd gitlab/public
    [isabell@gitlab ~/gitlab/public]$ rm -rf assets/ # just needed if you've tried to compile the assets on your gitlab host
    [isabell@gitlab ~/gitlab/public]$ tar xzf assets.tar.gz
    [isabell@gitlab ~/gitlab/public]$ rm assets.tar.gz

and your done.

Installation sidekiq
====================

Prerequisites
-------------

Have your ``POSTGRESQL_PORT``, ``REDIS_PORT`` and ``GITALY_PORT`` ready. You
should also know the ``GITLAB_FQDN``.

We also need the ip address of the ``veth`` interface

::

    [isabell@sidekiq ~]$ /sbin/ifconfig | grep -A1 veth
    veth_isabell: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 100.64.4.53  netmask 255.255.255.252  broadcast 0.0.0.0

Write the ip down (in the case above ``100.64.4.53``). I'll refer to it as
``SIDEKIQ_VETH_IP``.


Install dependencies
--------------------

You'll need go through some of the steps for the ``gitlab`` host again. These
are

#. `Cmake`_
#. `Ruby`_
#. `Re2`_
#. `Runit`_

Don't forget to adjust your ``.bashrc`` on the ``sidekiq`` host to include all
``PATH``'s and the ``LD_LIBRARY_PATH`` adjustments.

Install sidekiq
---------------

The steps are pretty much the same like in the `Installation gitlab`_ section
and mainly differ in the configuration. For details look there, we're going
through all commands quickly here

.. warning:: Checkout the same version like on the ``gitlab`` host

::

    [isabell@sidekiq ~]$ git clone https://gitlab.com/gitlab-org/gitlab-foss.git -b 13-4-stable gitlab
    [isabell@sidekiq ~]$ cd gitlab
    [isabell@sidekiq ~/gitlab]$ git checkout v13.4.2
    [isabell@sidekiq ~/gitlab]$ cd config

    [isabell@sidekiq ~/gitlab/config]$ cp gitlab.yml.example gitlab.yml

    [isabell@sidekiq ~/gitlab/config]$ cp resque.yml.example resque.yml
    [isabell@sidekiq ~/gitlab/config]$ chmod 0600 resque.yml

    [isabell@sidekiq ~/gitlab/config]$ cp database.yml.example database.yml
    [isabell@sidekiq ~/gitlab/config]$ chmod 0600 database.yml

    [isabell@sidekiq ~/gitlab/config]$ cp initializers/smtp_settings.rb.sample initializers/smtp_settings.rb
    [isabell@sidekiq ~/gitlab/config]$ chmod 0600 initializers/smtp_settings.rb

.. note:: We need the ``gitlab/config/secrets.yml`` file from the ``gitlab``
   host. Copy it over with the tool of your choice.

Next change all occurences of ``/home/git/`` to the actual home
``/home/GITLAB_USERNAME/`` of the user on the ``gitlab`` host.

.. warning:: Replace ``GITLAB_USERNAME``

::

    [isabell@sidekiq ~/gitlab/config]$ sed -i 's:/home/git/:/home/GITLAB_USERNAME/:g' gitlab.yml secrets.yml resque.yml database.yml

Edit ``gitlab.yml`` to match the following (only required changes are listed)

.. warning:: Replace ``GITLAB_USERNAME``, ``GITLAB_EXTERNAL_FQDN``,
   ``GITLAB_FQDN`` and ``GITALY_PORT``

::

    production: &base

        # ...

        gitlab:
            host: GITLAB_EXTERNAL_FQDN
            port: 443
            https: true

            # ...

            user: GITLAB_USERNAME

        # ...

        incoming_email:
            enabled: false

        # ...

        dependency_proxy:
            enabled: false

        # ...

        repositories:
            # ...
            storages:
                default:
                    path: /home/GITLAB_USERNAME/repositories/
                    gitaly_address: tcp://GITLAB_FQDN:GITALY_PORT


Edit ``resque.yml`` to match the following (only required changes are listed)


.. warning:: Replace ``REDIS_PASSWORD``, ``GITLAB_FQDN`` and ``REDIS_PORT``

::

    # ...
    production:
        # Redis (single instance)
        url: redis://:REDIS_PASSWORD@GITLAB_FQDN:REDIS_PORT

Edit ``database.yml`` to match the following (only required changes are listed)

.. warning:: Replace ``POSTGRESQL_GITLAB_PASSWORD``, ``SIDEKIQ_FQDN`` and
   ``POSTGRESQL_PORT``

::

    production:
        # ...
        database: gitlab
        username: gitlab
        password: 'POSTGRESQL_GITLAB_PASSWORD'
        host: 'SIDEKIQ_FQDN'
        port: 'POSTGRESQL_PORT'

    # ...

Edit ``initializers/smtp_settings.rb`` to match the following

.. warning:: Replace ``GITLAB_FQDN``,
   ``GITLAB_USERNAME``, ``GITLAB_EMAIL_PASSWORD`` and ``GITLAB_EXTERNAL_FQDN``

::

    # ...
    if Rails.env.production?
    Rails.application.config.action_mailer.delivery_method = :smtp

    ActionMailer::Base.delivery_method = :smtp
    ActionMailer::Base.smtp_settings = {
      address: "GITLAB_FQDN",
      port: 587,
      user_name: "GITLAB_USERNAME@uber.space",
      password: "GITLAB_EMAIL_PASSWORD",
      domain: "GITLAB_EXTERNAL_FQDN",
      authentication: :plain,
      enable_starttls_auto: true,
      tls: false,
      ssl: false,
      openssl_verify_mode: 'none' # See ActionMailer documentation for other possible options

Install Gems (sidekiq)
^^^^^^^^^^^^^^^^^^^^^^

::

    [isabell@sidekiq ~]$ cd gitlab
    [isabell@sidekiq ~/gitlab]$ bundle install --deployment --without development test mysql aws kerberos


Now that installation is done we need a supervisor service for sidekiq in
``$HOME/etc/services.d/sidekiq.ini``

.. warning:: Replace ``GITLAB_USERNAME``

::

    [program:sidekiq]
    directory=%(ENV_HOME)s/gitlab
    command=%(ENV_HOME)s/gitlab/bin/background_jobs start_foreground
    environment=RAILS_ENV="production",SIDEKIQ_WORKERS="1",LD_LIBRARY_PATH="/opt/rh/devtoolset-9/root/usr/lib64:/opt/rh/devtoolset-9/root/usr/lib:/opt/rh/devtoolset-9/root/usr/lib64/dyninst:/opt/rh/devtoolset-9/root/usr/lib/dyninst:/home/SIDEKIQ_USERNAME/.local/lib:/home/SIDEKIQ_USERNAME/.local/postgresql/lib",PATH="/home/SIDEKIQ_USERNAME/.local/bin:/home/SIDEKIQ_USERNAME/bin:/opt/uberspace/etc/SIDEKIQ_USERNAME/binpaths/ruby:/opt/rh/devtoolset-9/root/usr/bin:/home/SIDEKIQ_USERNAME/.cargo/bin:/home/SIDEKIQ_USERNAME/.luarocks/bin:/home/SIDEKIQ_USERNAME/go/bin:/home/SIDEKIQ_USERNAME/.deno/bin:/home/SIDEKIQ_USERNAME/.config/composer/vendor/bin:/bin:/usr/bin:/usr/ucb:/usr/local/bin:/home/SIDEKIQ_USERNAME/.dotnet/tools"
    autostart=yes
    autorestart=yes
    redirect_stderr=yes
    stdout_logfile=%(ENV_HOME)s/gitlab/log/sidekiq.log

The ``SIDEKIQ_WORKERS=1`` setting ensures to run only one worker which uses
around 500-600MB and leaves enough headroom to run another app on the same host,
so your ``sidekiq`` host doesn't need to be dedicated to sidekiq alone.

Final steps
===========

Reread the configuration and start sidekiq

::

    [isabell@sidekiq ~]$ supervisorctl reread
    [isabell@sidekiq ~]$ supervisorctl update sidekiq
    [isabell@sidekiq ~]$ supervisorctl status sidekiq


Now change to your ``gitlab`` host and start all the services

::

    [isabell@sidekiq ~]$ supervisorctl reread
    [isabell@sidekiq ~]$ supervisorctl update
    [isabell@sidekiq ~]$ supervisorctl status

Web Backend
-----------

Configure the web backend to use the ``GITLAB_WORKHORSE_PORT`` on your
``gitlab`` host

.. warning:: Replace ``GITLAB_WORKHORSE_PORT``

::

    [isabell@gitlab ~]$ uberspace web backend set / --remove-prefix --http --port GITLAB_WORKHORSE_PORT

Double check the backend

::

    [isabell@gitlab ~]$ uberspace web backend list
    / http:<port>, --remove-prefix => OK, listening: PID 21435, /home/<username>/gitlab-workhorse/gitlab-workhorse -listenUmask 0 -listenNetwork tcp -listenAddr 0.0.0.0:<port> -authBackend http://127.0.0.1:9292 -authSocket /home/<username>/gitlab/tmp/sockets/gitlab.socket -documentRoot /home/<username>/gitlab/public

your output should look similar to the one above where ``<port>`` is to your
``GITLAB_WORKHORSE_PORT`` and ``<username>`` is your ``GITLAB_USERNAME``.


Double Check the application status
-----------------------------------

Run a thourough check of your ``gitlab`` instance

::

    [isabell@gitlab ~]$ cd gitlab
    [isabell@gitlab ~/gitlab]$ bundle exec rake gitlab:check RAILS_ENV=production
    Checking Incoming Email ...
    Checking GitLab subtasks ...

    Checking GitLab Shell ...

    GitLab Shell: ... GitLab Shell version >= 13.7.0 ? ... OK (13.7.0)
    Running /home/gitls7or/gitlab-shell/bin/check
    Internal API available: OK
    Redis available via internal API: OK
    gitlab-shell self-check successful

    Checking GitLab Shell ... Finished

    Checking Gitaly ...

    Gitaly: ... default ... OK

    Checking Gitaly ... Finished

    Checking Sidekiq ...

    Sidekiq: ... Running? ... no
      Try fixing it:
      sudo -u gitls7or -H RAILS_ENV=production bin/background_jobs start
      For more information see:
      doc/install/installation.md in section "Install Init Script"
      see log/sidekiq.log for possible errors
      Please fix the error above and rerun the checks.

    Checking Sidekiq ... Finished
    Incoming Email: ... Reply by email is disabled in config/gitlab.yml

    Checking Incoming Email ... Finished

    Checking LDAP ...

    LDAP: ... LDAP is disabled in config/gitlab.yml

    Checking LDAP ... Finished

    Checking GitLab App ...

    Git configured correctly? ... yes
    Database config exists? ... yes
    All migrations up? ... yes
    Database contains orphaned GroupMembers? ... no
    GitLab config exists? ... yes
    GitLab config up to date? ... yes
    Log directory writable? ... yes
    Tmp directory writable? ... yes
    Uploads directory exists? ... yes
    Uploads directory has correct permissions? ... yes
    Uploads directory tmp has correct permissions? ... skipped (no tmp uploads folder yet)
    Init script exists? ... no
      Try fixing it:
      Install the init script
      For more information see:
      doc/install/installation.md in section "Install Init Script"
      Please fix the error above and rerun the checks.
    Init script up-to-date? ... can't check because of previous errors
    Projects have namespace: ... skipped (no projects yet)
    Redis version >= 4.0.0? ... yes
    Ruby version >= 2.5.3 ? ... yes (2.6.6)
    Git version >= 2.24.0 ? ... yes (2.24.3)
    Git user has default SSH configuration? ... yes
    Active users: ... 0
    Is authorized keys file accessible? ... yes
    GitLab configured to store new projects in hashed storage? ... yes
    All projects are in hashed storage? ... yes

    Checking GitLab App ... Finished


    Checking GitLab subtasks ... Finished

There should only be two errors presents which we can ignore. ``sidekiq`` isn't
running because we've set it up on a different host and the init script is
replaced by our supervisor services.

Finish it
---------

Point your browser to ``https://GITLAB_EXTERNAL_FQDN``, follow the instructions
and reset the password. You can login with ``root`` as user and your new
password.

Done :)

Cleanup
^^^^^^^

Finally we can cleanup our home a bit to gain some disk space back. Remove the
entire workspace directory and some of the cache. You can do so on both hosts.

::

    [isabell@gitlab ~]$ rm -rfI workspace/
    [isabell@gitlab ~]$ rm -rfI .cache/{yarn,go-build}

Check your quota

::

    [isabell@gitlab ~]$ quota -gsl

you should have left around 4-5GB for your repositories.

.. rubric:: Footnotes

.. [#f1] https://en.wikipedia.org/wiki/GitLab

.. _GitLab: https://gitlab.com
.. _GitLab installation from source: https://docs.gitlab.com/13.4/ee/install/installation.html
.. _GitLab installation from source dependencies: https://docs.gitlab.com/13.4/ee/install/installation.html#1-packages-and-dependencies

----

Tested with GitLab 13.4.2, Uberspace 7.7.9.0

.. author_list:: Michael Strobler
