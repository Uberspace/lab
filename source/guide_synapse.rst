.. highlight:: console

.. author:: 927589452
.. author:: luto <http://luto.at>
.. author:: Arian Malek <https://fetziverse.de>

.. tag:: lang-python
.. tag:: chat
.. tag:: matrix

.. sidebar:: Logo

  .. image:: _static/images/matrix-logo.svg
      :align: center

#######
Synapse
#######

.. tag_list::

Synapse_ is the reference implementation of a matrix server.
Matrix_ is federated chat protocol aiming to replace xmpp.
This guide was inspired by Jan Willhaus's guide for Uberspace 6.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here

  * https://github.com/matrix-org/synapse/blob/master/LICENSE
  * https://github.com/matrix-org/sliding-sync/blob/main/LICENSE

Prerequisites
=============

Web domain
----------

.. note:: Keep in mind that since you can't create DNS records for ``.uber.space`` domains, you'll need your own domain like ``example.org``. `Matrix 2.0`_ will increase the support of federation, video and audio calling which recommend a own domain. To understand and setup the domains easier I use the following (recommended) subdomains:

 * ``matrix.example.org``
 * ``syncv3.example.org``

Your domain ``example.org`` and subdomains ``matrix.example.org`` and ``syncv3.example.org`` needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 example.org
 matrix.example.org
 syncv3.example.org
 [isabell@stardust ~]$

Uberspace creates certificates automatically when a domain is first seen by the webserver. Trigger the generation for each one with the following command:

::

 [isabell@stardust ~]$ curl --silent --head https://example.org | head -n 1
 [...]
 [isabell@stardust ~]$ curl --silent --head https://matrix.example.org | head -n 1
 [...]
 [isabell@stardust ~]$ curl --silent --head https://syncv3.example.org | head -n 1
 [...]
 [isabell@stardust ~]$

This will return ``HTTP/1.1 200 OK`` or something similar accordingly your webserver configuration.

Installation
============

We will install synapse using pip, which makes it quite easy:

.. code-block:: console
  :emphasize-lines: 1,2,8,18

  [isabell@stardust ~]$ mkdir -p ~/synapse
  [isabell@stardust ~]$ pip3.9 install --user jinja2
    Collecting jinja2
      Using cached https://files.pythonhosted.org/packages/1d/e7/fd8b501e7a6dfe492a433deb7b9d833d39ca74916fa8bc63dd1a4947a671/Jinja2-2.10.1-py2.py3-none-any.whl
    Requirement already satisfied: MarkupSafe>=0.23 in ./synapse/env/lib/python3.9/site-packages (from jinja2) (1.1.1)
    Installing collected packages: jinja2
    Successfully installed jinja2-2.10.1
  [isabell@stardust ~]$ pip3.9 install --user matrix-synapse
    Collecting matrix-synapse
    Collecting pyasn1-modules>=0.0.7 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/91/f0/b03e00ce9fddf4827c42df1c3ce10c74eadebfb706231e8d6d1c356a4062/pyasn1_modules-0.2.5-py2.py3-none-any.whl
    Collecting Twisted>=18.7.0 (from matrix-synapse)
  (...)
    Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests>=2.1.0->treq>=15.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl
    Installing collected packages: pyasn1, pyasn1-modules, attrs, constantly, idna, hyperlink, zope.interface, six, Automat, PyHamcrest, incremental, Twisted, msgpack, simplejson, frozendict, canonicaljson, sortedcontainers, pyyaml, pycparser, cffi, pynacl, asn1crypto, cryptography, service-identity, unpaddedbase64, signedjson, pillow, daemonize, chardet, certifi, urllib3, requests, treq, bcrypt, pymacaroons, pyopenssl, psutil, pyrsistent, jsonschema, netaddr, phonenumbers, prometheus-client, matrix-synapse
    Successfully installed Automat-0.7.0 PyHamcrest-1.9.0 Twisted-19.2.1 asn1crypto-0.24.0 attrs-19.1.0 bcrypt-3.1.6 canonicaljson-1.1.4 certifi-2019.6.16 cffi-1.12.3 chardet-3.0.4 constantly-15.1.0 cryptography-2.7 daemonize-2.5.0 frozendict-1.2 hyperlink-19.0.0 idna-2.8 incremental-17.5.0 jsonschema-3.0.1 matrix-synapse-1.0.0 msgpack-0.6.1 netaddr-0.7.19 phonenumbers-8.10.13 pillow-6.0.0 prometheus-client-0.3.1 psutil-5.6.3 pyasn1-0.4.5 pyasn1-modules-0.2.5 pycparser-2.19 pymacaroons-0.13.0 pynacl-1.3.0 pyopenssl-19.0.0 pyrsistent-0.15.2 pyyaml-5.1.1 requests-2.22.0 service-identity-18.1.0 signedjson-1.0.0 simplejson-3.16.0 six-1.12.0 sortedcontainers-2.1.0 treq-18.6.0 unpaddedbase64-1.1.0 urllib3-1.25.3 zope.interface-4.6.0
  [isabell@stardust ~]$ pip3.9 install --user psycopg2-binary
    Collecting psycopg2-binary
      Downloading psycopg2_binary-2.9.5-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
         |████████████████████████████████| 3.0 MB 30.0 MB/s
    Installing collected packages: psycopg2-binary
    Successfully installed psycopg2-binary-2.9.5

  [isabell@stardust ~]$

Also we need the latest ``urllib3`` that support OpenSSL 1.0.2 which is provided by Uberspace 7 and cannot be updated due to the base of CentOS 7:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ pip3.9 install --user urllib3==1.26.6
    Collecting urllib3==1.26.6
      Downloading urllib3-1.26.6-py2.py3-none-any.whl (138 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 138.5/138.5 kB 5.2 MB/s eta 0:00:00
    Installing collected packages: urllib3
      Attempting uninstall: urllib3
        Found existing installation: urllib3 2.1.0
        Uninstalling urllib3-2.1.0:
          Successfully uninstalled urllib3-2.1.0
    Successfully installed urllib3-1.26.6
  [isabell@stardust ~]$

.. Rust compilation errors:

.. note:: If you get a compilation error due to missing rust components in the cryptography library for python it may help to run:

.. code-block:: console

  [isabell@stardust ~]$ pip3.9 install --user setuptools_rust
  [isabell@stardust ~]$ python3.9 -m pip install --upgrade  --user pip
  [isabell@stardust ~]$

.. note:: As of `matrix-synapse 1.137.0`_ you also need to symlink `cargo` and `rustc` to workaround `issue #1932`_:

.. code-block:: console

  [isabell@stardust ~]$ ln -s /opt/rust-stable/bin/cargo /home/$USER/bin/cargo
  [isabell@stardust ~]$ ln -s /opt/rust-stable/bin/rustc /home/$USER/bin/rustc
  [isabell@stardust ~]$

Configuration
=============

Generate standard config
------------------------

Generate a config file ``~/synapse/homeserver.yaml`` and replace ``example.org`` with the real domain you want your matrix username to end in.

.. code-block:: console
  :emphasize-lines: 3,6

  [isabell@stardust ~]$ cd ~/synapse
  [isabell@stardust synapse]$  python3.9 -m synapse.app.homeserver \
    --server-name example.org \
    --config-path homeserver.yaml \
    --generate-config \
    --report-stats=[yes|no]
  [isabell@stardust ~]$

Set the Synapse_ to listen for federation and clients on the correct localhost without encryption in the config file ``~/synapse/homeserver.yaml``. To do this, locate the ``listeners:`` section and modify the entry with ``port: 8008``:

.. code-block:: yaml
  :emphasize-lines: 4

      - port: 8008
        type: http
        tls: false
        bind_addresses: ['::','0.0.0.0']
        x_forwarded: true
        resources:
          - names: [client, federation]
            compress: false

And point the ``uberspace web backend`` on ``matrix.example.org`` to the listener on port 8008.

.. include:: includes/web-backend.rst

Announcement
------------

To enable federation as described MatrixFederation_ we need to announce, that we are listening on port 443 (the reverse proxy) via .well-known.

Setup the directory for the next step:

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p /var/www/virtual/$USER/example.org/.well-known/matrix
  [isabell@stardust ~]$

Create the file ``/var/www/virtual/$USER/example.org/.well-known/matrix/server`` with the following content:

.. code-block:: json
  :emphasize-lines: 2

  {
    "m.server": "matrix.example.org:443"
  }

This has to be made available under ``example.org/.well-known/matrix`` via the web backend:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set example.org/.well-known/matrix --apache
  Set backend for /.well-known/matrix to apache.
  [isabell@stardust ~]$

Configure Database Access
-------------------------


Option A: Postgres
^^^^^^^^^^^^^^^^^^

Setup a dedicated postgres user and database for synapse:

.. code-block:: console

  [isabell@stardust ~]$ createuser synapse -P
  Enter password for new role:
  Enter it again:
  [isabell@stardust ~]$ createdb \
    --encoding=UTF8 \
    --lc-collate=C \
    --lc-ctype=C \
    --owner="synapse" \
    --template=template0 \
    synapse
  [isabell@stardust ~]$

You can verify access with:

.. code-block:: console

  [isabell@stardust ~]$ psql synapse synapse


Modify the config file again to give synapse access to the database:

.. code-block:: yaml
  :emphasize-lines: 6,7,8,9

    database:
        # The database engine name
        name: psycopg2
        # Arguments to pass to the engine
        args:
            user: "synapse"
            password: "<my super secure password>"
            database: "synapse"
            host: "/home/isabell/tmp"
            cp_min: 5
            cp_max: 10

Comment out the active sqlite database. If you are using a different port for postgres, add a port property below host.

Option B: Sqlite
^^^^^^^^^^^^^^^^

For the file-based sqlite database, leave the standard config in ``~/synapse/homeserver.yaml``.

Enable user search
------------------

Allow users to be found by enabling the user directory in the config file ``~/synapse/homeserver.yaml``:

.. code-block:: yaml

  user_directory:
    enabled: true

Setup daemon
------------

Create ``~/etc/services.d/synapse.ini`` with the following content:

.. code-block:: ini

 [program:synapse]
 command=python3.9 -m synapse.app.homeserver -c %(ENV_HOME)s/synapse/homeserver.yaml
 autostart=yes
 autorestart=yes
 environment=
        PATH="%(ENV_HOME)s/opt/postgresql/bin/:%(ENV_PATH)s",
        LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%(ENV_HOME)s/opt/postgresql/lib"

.. include:: includes/supervisord.rst

Updates
=======

Watch MatrixRSS_ to be notified of upgrades and if there is a update, use pip to update the installation:

.. note:: If you installed matrix-synapse prior to version 1.137.0, see :ref:`Rust compilation error`.

.. code-block:: console

  [isabell@stardust ~]$ python3.9 -m pip install --user -U matrix-synapse
  [isabell@stardust ~]$

Automate the update process with a bash script called `~/bin/synapse-update` containing:

.. code-block:: bash

  #!/bin/bash
  # update synapse and restart the service

  python3.9 -m pip install --user -U matrix-synapse
  supervisorctl restart synapse

Make it executeable:

.. code-block:: console

  [isabell@stardust ~]$ chmod +x ~/bin/synapse-update
  [isabell@stardust ~]$

.. tip::

  You can automate this script as a :manual:`cronjob <daemons-cron>`.
  ``@weekly $HOME/bin/synapse-update > $HOME/logs/synapse-update.log 2>&1`` update weekly and output to log

Administration
==============

Adding users
------------

Users can be added from the CLI:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/synapse
  [isabell@stardust synape]$ register_new_matrix_user -c homeserver.yaml https://matrix.example.org
  New user localpart [isabell]: USER
  Password:
  Confirm password:
  Make admin [no]: no
  Sending registration request...
  Success!
  [isabell@stardust synapse]$

Password reset
--------------

Passwords can be reset using the cli; first generate the hash of the new password:

.. code-block:: console

  [isabell@stardust ~]$ hash_password
  Password:
  Confirm password:
  $2b$12$yK16TMDMnvj97GFBoxF9QeP2N.U8oadindcjB0Uo9TkSI3CsgwV02
  [isabell@stardust ~]$


Then add it to the USERS table:

.. code-block:: console

  [isabell@stardust ~]$ psql --user synapse
  Password for user synapse:
  psql (9.6.10)
  Type "help" for help.

  synapse=> UPDATE users SET password_hash='$2b$12$yK16TMDMnvj97GFBoxF9QeP2N.U8oadindcjB0Uo9TkSI3CsgwV02' WHERE name='@isabell:example.org';
  UPDATE 1
  synapse=>
  [isabell@stardust ~]$

.. note:: ``SELECT name from users;`` returns a list of all usernames

Check federation
----------------

The Matrix_ project provides a federation checker at MatrixFederationChecker_ .

Sliding-Sync
============

The `Sliding Sync`_ proxy integrated in `Matrix 2.0`_ improves the performance (login and initial sync, launch and incremental sync) especially for group chats. It is also needed for the new Matrix 2.0 clients like Element X.

Prerequisites
-------------

First we clone the repository to ``~/sliding-sync``:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/matrix-org/sliding-sync
    Cloning into 'sliding-sync'...
    remote: Enumerating objects: 12000, done.
    remote: Counting objects: 100% (3685/3685), done.
    remote: Compressing objects: 100% (861/861), done.
    remote: Total 12000 (delta 3029), reused 3321 (delta 2798), pack-reused 8315
    Receiving objects: 100% (12000/12000), 3.76 MiB | 10.90 MiB/s, done.
    Resolving deltas: 100% (8573/8573), done.
  [isabell@stardust ~]$

Generate a secret and compile the proxy:

.. note:: This MUST remain the same throughout the lifetime of the database created above.

.. code-block:: console

  [isabell@stardust ~]$ cd ~/sliding-sync
  [isabell@stardust sliding-sync]$ echo -n "$(openssl rand -hex 32)" > .secret
  [isabell@stardust sliding-sync]$ go build ./cmd/syncv3
  [...]
  [isabell@stardust sliding-sync]$

Create the file ``/var/www/virtual/$USER/example.org/.well-known/matrix/client`` with the following content to announce the sliding sync proxy:

.. code-block:: console
  :emphasize-lines: 3,6

  {
    "m.homeserver": {
        "base_url": "https:/matrix.example.org"
    },
    "org.matrix.msc3575.proxy": {
        "url": "https://syncv3.example.org"
    }
  }

Setup database
--------------

Setup one more dedicated postgres user and database for sliding-sync:

.. code-block:: console
  :emphasize-lines: 2,3

  [isabell@stardust ~]$ createuser syncv3 -P
  Enter password for new role:
  Enter it again:
  [isabell@stardust ~]$ createdb --owner="syncv3" syncv3
  [isabell@stardust ~]$

You can verify access with:

.. code-block:: console

  [isabell@stardust ~]$ psql syncv3 syncv3

Web backend
-----------

Setup ``uberspace web backend`` on ``syncv3.example.org`` to the listener on port 8009.

.. include:: includes/web-backend.rst

Check functionality
-------------------

Make sure to check the functionality. This will make it a lot easier to troubleshoot if something didn't work as expected. Make sure to replace the your domain and your PostgreSQL password:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/sliding-sync
  [isabell@stardust sliding-sync]$ SYNCV3_SECRET=$(cat .secret) SYNCV3_SERVER="https://example.org" SYNCV3_DB="user=syncv3 dbname=syncv3 sslmode=disable password='MySuperSecretPSQLPassword'" SYNCV3_BINDADDR=0.0.0.0:8009 ./syncv3
    Sync v3 [0.99.13] (a8e9c56)
    Debug=false LogLevel= MaxConns=0
    2023/12/10 14:33:36 OK   20230728114555_device_data_drop_id.sql (6.1ms)
    2023/12/10 14:33:36 OK   20230802121023_device_data_jsonb.go (43.74ms)
    2023/12/10 14:33:36 OK   20230814183302_cbor_device_data.go (14.14ms)
    2023/12/10 14:33:36 OK   20230822180807_bogus_snapshot_cleanup.go (7.22ms)
    2023/12/10 14:33:36 OK   20230913120537_events_missing_previous.sql (6.52ms)
    2023/12/10 14:33:36 OK   20231019153023_cleanup_dead_invites.sql (10.87ms)
    14:33:36 INF invalidating users len_invalidate_users=0
    14:33:36 INF invalidating users invalidate_users=[]
    14:33:36 INF reset since tokens num_devices=0
    14:33:36 INF reset invites num_invites=0
    2023/12/10 14:33:36 OK   20231108122539_clear_stuck_invites.go (10ms)
    2023/12/10 14:33:36 goose: successfully migrated database to version: 20231108122539
    14:33:36 INF creating handler
    14:33:36 INF retrieved global snapshot from database
    14:33:36 INF listening on 0.0.0.0:8009
    14:33:36 INF StartV2Pollers num_devices=0 num_fail_decrypt=0
    14:33:36 INF StartV2Pollers finished
  [isabell@stardust sliding-sync]$

You should see some more ``INF`` activity as soon as your client like Element X connects to your account. Otherwise check the configuration again.

Setup daemon
------------

Create ``~/etc/services.d/syncv3.ini`` with the following content. Make sure to replace the secret, your domain and your PostgreSQL password:

.. code-block:: ini

  [program:syncv3]
  Environment=SYNCV3_SECRET=MySuperSecret,SYNCV3_SERVER="https://matrix.example.org",SYNCV3_DB="user=syncv3 dbname=syncv3 sslmode=disable password=MySuperSecretPSQLPassword",SYNCV3_BINDADDR="0.0.0.0:8009"
  command=%(ENV_HOME)s/sliding-sync/syncv3
  autostart=yes
  autorestart=yes
  startsecs=10

.. include:: includes/supervisord.rst

Updates
-------

Stop the service, pull the repo, rebuild it and start the service again.

.. code-block:: console

  [isabell@stardust]$ cd ~/sliding-sync
  [isabell@stardust sliding-sync]$ supervisorctl stop syncv3
    syncv3: stopped
  [isabell@stardust sliding-sync]$ git pull
    remote: Enumerating objects: 86, done.
    remote: Counting objects: 100% (86/86), done.
    remote: Compressing objects: 100% (34/34), done.
    remote: Total 86 (delta 54), reused 71 (delta 49), pack-reused 0
    Unpacking objects: 100% (86/86), 41.61 KiB | 513.00 KiB/s, done.
    From https://github.com/matrix-org/sliding-sync
      62d3798..a8e9c56  main                       -> origin/main
    * [new branch]      dmr/avatars-for-dms-only   -> origin/dmr/avatars-for-dms-only
    * [new branch]      kegan/conn-map-tests       -> origin/kegan/conn-map-tests
    * [new branch]      kegan/log-state-invalidate -> origin/kegan/log-state-invalidate
    * [new tag]         v0.99.13                   -> v0.99.13
    Updating 62d3798..a8e9c56
    Fast-forward
    README.md                |   2 ++
    RELEASING.md             |  11 +++++-----
    cmd/syncv3/main.go       |   2 +-
    sync3/connmap.go         |  30 +++++++++++++++++--------
    sync3/connmap_test.go    | 229 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    sync3/handler/handler.go |  14 ++++++------
    6 files changed, 266 insertions(+), 22 deletions(-)
    create mode 100644 sync3/connmap_test.go
  [isabell@stardust sliding-sync]$ go build ./cmd/syncv3
  [isabell@stardust sliding-sync]$ supervisorctl start syncv3
    syncv3: started
  [isabell@stardust sliding-sync]$

Tested on Uberspace 7.15.6 via riot.im/app on synapse 1.97.0. Sliding Sync tested on version 0.99.13 and Element X 1.4.2.

.. _MatrixFederation: https://github.com/matrix-org/synapse/blob/master/docs/federate.md
.. _MatrixRSS: https://matrix.org/blog/feed
.. _Matrix: https://matrix.org/
.. _Synapse: https://matrix.org/docs/projects/server/synapse
.. _MatrixFederationChecker: https://federationtester.matrix.org/
.. _Sliding Sync: https://github.com/matrix-org/sliding-sync
.. _Matrix 2.0: https://matrix.org/blog/2023/09/matrix-2-0/
.. _matrix-synapse 1.137.0: https://pypi.org/project/matrix-synapse/1.137.0/
.. _issue 1932: https://github.com/Uberspace/lab/issues/1932

----

.. author_list::
