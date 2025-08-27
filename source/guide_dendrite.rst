.. author:: coderkun

.. tag:: chat
.. tag:: matrix
.. tag:: lang-go

.. highlight:: console

########
Dendrite
########

.. tag_list::

`Dendrite <https://element-hq.github.io/dendrite/>`_ is a second-generation
Matrix homeserver written in Go! Following the microservice architecture model,
Dendrite is designed to be efficient, reliable and scalable. Despite being
beta, many Matrix features are already supported.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PostgreSQL <database-postgresql>` in the version 12+.
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

The Matrix protocol uses the subfolder ``isabell.example/_matrix``. That makes
it easy to run Dendrite via HTTPS without affecting your regular website and
without any special DNS setup. Only two ``.well-known`` entries need to be
added.


Installation
============

Clone Dendrite’s git repository into your home directory:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/matrix-org/dendrite.git
  Cloning into 'dendrite'...
  […]
  Resolving deltas: 100% (30826/30826), done.
  [isabell@stardust ~]$

Check out a stable version (replace ``v0.13.5`` with the latest version):

.. code-block:: console

  [isabell@stardust ~]$ cd ~/dendrite/
  [isabell@stardust dendrite]$ git checkout v0.13.5
  Note: switching to 'v0.13.5'.
  […]
  HEAD is now at b7054f42 Version 0.13.5 (#3285)
  [isabell@stardust dendrite]$

Build the application including utility commands with ``go``:

.. code-block:: console

  [isabell@stardust dendrite]$ go build -o bin/ ./cmd/...
  go: downloading github.com/getsentry/sentry-go v0.14.0
  […]
  go: downloading github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd
  go: downloading github.com/modern-go/reflect2 v1.0.2
  [isabell@stardust dendrite]$


Database
--------

Make sure you run PostgreSQL in the required version. Create both a user (role) and a database:

.. code-block:: console

  [isabell@stardust dendrite]$ createuser -P dendrite
  Enter password for new role:
  Enter it again:
  [isabell@stardust dendrite]$ createdb -O dendrite -E UTF-8 dendrite
  [isabell@stardust dendrite]$

Write down the key, you will need it later.

Service
-------

Create a supervisord service by adding the following content to the new file
``~/etc/services.d/dendrite.ini``:

.. code-block:: ini

  [program:dendrite]
  directory=%(ENV_HOME)s/dendrite
  command=%(ENV_HOME)s/dendrite/bin/dendrite -config dendrite.yaml -http-bind-address 0.0.0.0:8008
  startsecs=30

.. include:: includes/supervisord.rst

Web Backend
-----------

To make Dendrite available via HTTPS, create a :manual:`web backend
<web-backends>` for ``/_matrix``:

.. code-block:: console

  [isabell@stardust dendrite]$ uberspace web backend set /_matrix --http --port 8008
  Set backend for /_matrix to port 8008; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust dendrite]$

Please adjust the port ``8008`` if you want to run Dendrite on a different port.

Well-known Delegation
---------------------

To tell both Matrix servers and clients how to find your Dendrite server,
create ``.well-known`` files.

Create a file ``~/html/.well-known/matrix/client`` with the following
content:

.. code-block:: json

    {
      "m.homeserver": {
        "base_url": "https://isabell.example"
      }
    }

Create a file ``~/html/.well-known/matrix/server`` with the following
content:

.. code-block:: json

    {
      "m.server": "isabell.example:443"
    }


Configuration
=============

A sample config file is provided at ``dendrite-sample.yaml``. Copy it to
``dendrite.yaml`` and adjust the following settings.

Domain
------

Configure the domain you use for your Uberspace in the ``global`` section using
the ``server_name`` property:

.. code-block:: yaml
 :emphasize-lines: 2

    global:
      server_name: isabell.example

Signing Keys
------------

Matrix requires a signing key. You can create one using the ``generate-keys``
utility that comes with Dendrite:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/dendrite/
  [isabell@stardust dendrite]$ ./bin/generate-keys --private-key matrix_key.pem
  [isabell@stardust dendrite]$

Add the filename to the configuration using the ``private_key`` property:

.. code-block:: yaml
 :emphasize-lines: 2

    global:
      private_key: matrix_key.pem

If you already have a signing key from an old installation or a Synapse
installation, you can re-use it as described in the `Dendrite manual
<https://matrix-org.github.io/dendrite/installation/manual/signingkeys#old-signing-keys>`_.

Database
--------

Adjust the ``connection_string`` property of the ``database`` section to match
your PostgreSQL setup:

.. code-block:: yaml
 :emphasize-lines: 2

    database:
      connection_string: postgresql://dendrite:key@localhost/dendrite?sslmode=disable

Replace ``key`` with your PostgreSQL database key (see the corresponding
installation step).

Additionally, it is recommended to lower the amount of database connections to
reduce the resource consumption of PostgreSQL:

.. code-block:: yaml
 :emphasize-lines: 3

    database:
      connection_string: postgresql://dendrite:key@localhost/dendrite?sslmode=disable
      max_open_conns: 10

Logging
-------

The log level is set to ``info`` by default. For a production instance reduce
it to ``warn`` or ``error``:

.. code-block:: yaml
 :emphasize-lines: 3,5

    logging:
      - type: std
        level: error
      - type: file
        level: warn
        params:
          path: ./logs

Presence
--------

Presence events are disabled by default. If you want them to be processed,
enabled inbound and outbound:

.. code-block:: yaml
 :emphasize-lines: 3,4

    global:
      presence:
        enable_inbound: true
        enable_outbound: true


Administration
==============

Dendrite comes with several utility commands.

Adding Users
------------

The ``create-account`` utility can be used to create a new user via
commandline:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/dendrite/
  [isabell@stardust dendrite]$ ./bin/create-account -config dendrite.yaml -username myuser
  [isabell@stardust dendrite]$


Maintenance
===========

Backups
-------

To back up the Dendrite database use PostgreSQL’s ``pg_dumpall`` command:

.. code-block:: console

  [isabell@stardust ~]$ pg_dumpall -f ~/pg_backup.sql
  [isabell@stardust ~]$

Updates
-------

To update the code, fetch all git updates and checkout the latest version
(replace ``v0.13.5`` with the latest version):

.. code-block:: console

  [isabell@stardust ~]$ cd ~/dendrite/
  [isabell@stardust dendrite]$ git fetch -p
  [isabell@stardust dendrite]$ git checkout v0.13.5
  [isabell@stardust dendrite]$

Then, stop the Dendrite service, build the new version and start the service
again:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/dendrite/
  [isabell@stardust dendrite]$ supervisorctl stop dendrite
  [isabell@stardust dendrite]$ go build -o bin ./cmd/...
  [isabell@stardust dendrite]$ supervisorctl start dendrite
  [isabell@stardust dendrite]$

.. author_list::
