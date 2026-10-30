.. highlight:: console

.. author:: Patric Eckhart <mail@patriceckhart.com>

.. tag:: database
.. tag:: event-sourcing
.. tag:: event-store
.. tag:: event-storming
.. tag:: event-driven
.. tag:: event-driven-architecture
.. tag:: event-driven-design
.. tag:: event-driven-development

#########
GenesisDB
#########

.. tag_list::

GenesisDB_ is an open source event sourcing database engine. It stores events in the CloudEvents format, commits batches atomically with preconditions, chains every event with a SHA-256 hash, and offers live subscriptions and the GDBQL query language over a plain HTTP API. GenesisDB is a single static Go binary without runtime dependencies.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`

License
=======

GenesisDB is released under the `MIT License`_. Every feature is included, there are no editions, license keys or event limits.

Prerequisites
=============

Your GenesisDB URL needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the binary and its checksums from the `latest release`_, verify the binary and make it executable. Replace ``2.0.0`` with the current version:

::

 [isabell@stardust ~]$ mkdir --parents ~/bin
 [isabell@stardust ~]$ wget --output-document ~/bin/genesisdb https://github.com/genesisdb-io/genesisdb/releases/download/v2.0.0/genesisdb-2.0.0-linux-amd64
 [isabell@stardust ~]$ wget --output-document /tmp/genesisdb.sha256 https://github.com/genesisdb-io/genesisdb/releases/download/v2.0.0/SHA256SUMS
 [isabell@stardust ~]$ grep linux-amd64 /tmp/genesisdb.sha256 | awk '{print $1 "  " ENVIRON["HOME"] "/bin/genesisdb"}' | sha256sum --check
 /home/isabell/bin/genesisdb: OK
 [isabell@stardust ~]$ chmod +x ~/bin/genesisdb
 [isabell@stardust ~]$ genesisdb version
 GenesisDB 2.0.0
 [isabell@stardust ~]$

Create the data directory:

::

 [isabell@stardust ~]$ mkdir --parents ~/genesisdb
 [isabell@stardust ~]$

Configuration
=============

Generate a token
----------------

Every request except the health check needs a bearer token of at least 32 bytes. Generate one and keep it safe:

::

 [isabell@stardust ~]$ openssl rand -hex 32
 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
 [isabell@stardust ~]$

Set up the daemon
-----------------

Create ``~/etc/services.d/genesisdb.ini`` with the following content. Replace ``YOUR_AUTH_TOKEN`` with the token you just generated and set ``GENESISDB_TZ`` to your time zone:

.. code-block:: ini

 [program:genesisdb]
 command=%(ENV_HOME)s/bin/genesisdb
 directory=%(ENV_HOME)s
 environment=GENESISDB_AUTH_TOKEN="YOUR_AUTH_TOKEN",GENESISDB_HOST="0.0.0.0",GENESISDB_PORT="8080",GENESISDB_DATA_DIR="%(ENV_HOME)s/genesisdb",GENESISDB_TZ="Europe/Vienna"
 autostart=true
 autorestart=true
 startsecs=60
 stopsignal=TERM
 stopwaitsecs=30

GenesisDB has to listen on ``0.0.0.0`` so the web backend can reach it. ``GENESISDB_HOST`` defaults to ``127.0.0.1`` otherwise.

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs with ``supervisorctl tail genesisdb stderr``.

Configure the web server
------------------------

.. note::

    GenesisDB is running on port 8080.

.. include:: includes/web-backend.rst

Finishing installation
======================

Check that GenesisDB answers. The health check needs no token:

::

 [isabell@stardust ~]$ curl https://isabell.uber.space/api/v2/ping
 Pong
 [isabell@stardust ~]$

Commit your first event and fetch it again. Replace ``YOUR_AUTH_TOKEN`` with your token:

::

 [isabell@stardust ~]$ curl https://isabell.uber.space/api/v2/commit --header "Authorization: Bearer YOUR_AUTH_TOKEN" --header "Content-Type: application/json" --data '{"events":[{"source":"io.genesisdb.app","subject":"/customer","type":"io.genesisdb.app.customer-added","data":{"firstName":"Bruce","lastName":"Wayne"}}]}'
 [isabell@stardust ~]$ curl https://isabell.uber.space/api/v2/fetch --header "Authorization: Bearer YOUR_AUTH_TOKEN" --header "Content-Type: application/json" --data '{"subject":"/customer"}'
 [isabell@stardust ~]$

Official clients for JavaScript and TypeScript, Python, Go, Java, .NET, PHP, Rust and Swift are listed in the `GenesisDB documentation`_.

Best practices
==============

Security
--------

Use a separate token for each purpose. Besides the administrator token, GenesisDB accepts an optional write token (read and commit) and read token (read only). Add them to the ``environment`` line in ``~/etc/services.d/genesisdb.ini``, then run ``supervisorctl update``:

.. code-block:: ini

 GENESISDB_WRITE_TOKEN="ANOTHER_TOKEN",GENESISDB_READ_TOKEN="ONE_MORE_TOKEN"

Give your applications the write or read token and keep the administrator token for administration.

Further settings, such as request limits and Prometheus metrics, are described in the `configuration reference`_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

.. warning:: Back up the data directory before every update. A new version may migrate it on the first start, and the migration is one-way.

Stop GenesisDB, copy the data directory, replace the binary and start it again. Replace ``2.0.1`` with the new version:

::

 [isabell@stardust ~]$ supervisorctl stop genesisdb
 genesisdb: stopped
 [isabell@stardust ~]$ cp --archive ~/genesisdb ~/genesisdb-backup-$(date +%F)
 [isabell@stardust ~]$ wget --output-document ~/bin/genesisdb https://github.com/genesisdb-io/genesisdb/releases/download/v2.0.1/genesisdb-2.0.1-linux-amd64
 [isabell@stardust ~]$ chmod +x ~/bin/genesisdb
 [isabell@stardust ~]$ supervisorctl start genesisdb
 genesisdb: started
 [isabell@stardust ~]$

Upgrading from GenesisDB CE 1.x
-------------------------------

GenesisDB 2 replaces GenesisDB CE 1.x and opens its data directories: the directory is migrated automatically on the first start, and the 1.x API keeps answering under ``/api/v1``. Before the first start of version 2, stop GenesisDB CE and copy the complete data directory, there is no way back to 1.x without that copy. Then install the binary as described above, point ``GENESISDB_DATA_DIR`` to the existing directory and make sure the token has at least 32 bytes. See the `upgrade guide`_ for details.

Debugging
=========

Read the GenesisDB log with ``supervisorctl tail genesisdb stderr``. Check that the web backend points to port 8080 with ``uberspace web backend list``.

If GenesisDB refuses to start, the most common causes are a token shorter than 32 bytes and a data directory that another process already uses.

Backup
======

All data lives in ``~/genesisdb``. Copy it while GenesisDB is stopped, or create a consistent backup of the running instance through the API with the administrator token:

::

 [isabell@stardust ~]$ curl --fail https://isabell.uber.space/api/v2/admin/backup --header "Authorization: Bearer YOUR_AUTH_TOKEN" --output ~/genesisdb-backup.json
 [isabell@stardust ~]$

Commits wait while the backup is collected, so run it in a quiet moment. Restore it into an empty data directory with ``POST /api/v2/admin/restore``.

.. _GenesisDB: https://www.genesisdb.io/
.. _MIT License: https://github.com/genesisdb-io/genesisdb/blob/main/LICENSE
.. _GenesisDB documentation: https://docs.genesisdb.io/
.. _configuration reference: https://docs.genesisdb.io/configuration
.. _upgrade guide: https://docs.genesisdb.io/upgrade
.. _feed: https://github.com/genesisdb-io/genesisdb/releases.atom
.. _latest release: https://github.com/genesisdb-io/genesisdb/releases/latest

----

Tested with GenesisDB 2.0.0, Uberspace 7.16.6

.. author_list::
