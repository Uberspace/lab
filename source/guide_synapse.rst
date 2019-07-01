.. author:: 927589452
.. highlight:: console

.. tag:: python

.. sidebar:: Logo

  .. image:: _static/images/matrix-logo.svg
      :align: center

#######
Synapse
#######

.. tag_list::

Synapse_ is the reference implementation of a matrix server.
Matrix_ is federated chat protocol aiming to replace xmpp.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`Postgresql <guide_postgresql>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here

  * https://github.com/matrix-org/synapse/blob/master/LICENSE

Prerequisites
=============

You need a running :lab:`Postgresql <guide_postgresql>` database server, a dedicated user with a secure password and database for Synapse_.

.. code-block:: console

  [isabell@stardust ~]$ createuser synapse -P
  Enter password for new role:
  Enter it again:
  [isabell@stardust ~]$ createdb \
    --encoding=UTF8 \
    --owner="synapse" \
    --template=template0 \
    synapse
  [isabell@stardust ~]$

Installation
============

We will install synapse using pip, which makes it quite easy:

.. code-block:: console
  :emphasize-lines: 1,2,8,18

  [isabell@stardust ~]$ mkdir -p ~/synapse
  [isabell@stardust ~]$ pip3.6 install --user jinja2
    Collecting jinja2
      Using cached https://files.pythonhosted.org/packages/1d/e7/fd8b501e7a6dfe492a433deb7b9d833d39ca74916fa8bc63dd1a4947a671/Jinja2-2.10.1-py2.py3-none-any.whl
    Requirement already satisfied: MarkupSafe>=0.23 in ./synapse/env/lib/python3.6/site-packages (from jinja2) (1.1.1)
    Installing collected packages: jinja2
    Successfully installed jinja2-2.10.1
  [isabell@stardust ~]$ pip3.6 install --user matrix-synapse
    Collecting matrix-synapse
    Collecting pyasn1-modules>=0.0.7 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/91/f0/b03e00ce9fddf4827c42df1c3ce10c74eadebfb706231e8d6d1c356a4062/pyasn1_modules-0.2.5-py2.py3-none-any.whl
    Collecting Twisted>=18.7.0 (from matrix-synapse)
  (...)
    Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests>=2.1.0->treq>=15.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl
    Installing collected packages: pyasn1, pyasn1-modules, attrs, constantly, idna, hyperlink, zope.interface, six, Automat, PyHamcrest, incremental, Twisted, msgpack, simplejson, frozendict, canonicaljson, sortedcontainers, pyyaml, pycparser, cffi, pynacl, asn1crypto, cryptography, service-identity, unpaddedbase64, signedjson, pillow, daemonize, chardet, certifi, urllib3, requests, treq, bcrypt, pymacaroons, pyopenssl, psutil, pyrsistent, jsonschema, netaddr, phonenumbers, prometheus-client, matrix-synapse
    Successfully installed Automat-0.7.0 PyHamcrest-1.9.0 Twisted-19.2.1 asn1crypto-0.24.0 attrs-19.1.0 bcrypt-3.1.6 canonicaljson-1.1.4 certifi-2019.6.16 cffi-1.12.3 chardet-3.0.4 constantly-15.1.0 cryptography-2.7 daemonize-2.5.0 frozendict-1.2 hyperlink-19.0.0 idna-2.8 incremental-17.5.0 jsonschema-3.0.1 matrix-synapse-1.0.0 msgpack-0.6.1 netaddr-0.7.19 phonenumbers-8.10.13 pillow-6.0.0 prometheus-client-0.3.1 psutil-5.6.3 pyasn1-0.4.5 pyasn1-modules-0.2.5 pycparser-2.19 pymacaroons-0.13.0 pynacl-1.3.0 pyopenssl-19.0.0 pyrsistent-0.15.2 pyyaml-5.1.1 requests-2.22.0 service-identity-18.1.0 signedjson-1.0.0 simplejson-3.16.0 six-1.12.0 sortedcontainers-2.1.0 treq-18.6.0 unpaddedbase64-1.1.0 urllib3-1.25.3 zope.interface-4.6.0
  [isabell@stardust ~]$ pip3.6 install --user psycopg2
    Collecting psycopg2
      Downloading https://files.pythonhosted.org/packages/5c/1c/6997288da181277a0c29bc39a5f9143ff20b8c99f2a7d059cfb55163e165/psycopg2-2.8.3.tar.gz (377kB)
         |████████████████████████████████| 378kB 21.4MB/s
    Building wheels for collected packages: psycopg2
      Building wheel for psycopg2 (setup.py) ... done
      Stored in directory: /home/matrites/.cache/pip/wheels/48/06/67/475967017d99b988421b87bf7ee5fad0dad789dc349561786b
    Successfully built psycopg2
    Installing collected packages: psycopg2
    Successfully installed psycopg2-2.8.3

  [isabell@stardust ~]$


Configuration
=============

Generate standard config
------------------------

Generate a config file ``~/synapse/homeserver.yaml`` and replace my.domain.name with the real domain you want your matrix username to end in.

.. code-block:: console
  :emphasize-lines: 3,6

  [isabell@stardust ~]$ cd ~/synapse
  [isabell@stardust synapse]$  python3.6 -m synapse.app.homeserver \
    --server-name my.domain.name \
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

And point the ``uberspace web backend`` on ``/`` to the listener on port 8008.

.. include:: includes/web-backend.rst

To enable federation as described MatrixFederation_ we need to announce, that we are listening on port 443 (the reverse proxy), either via DNS or via .well-known.

Option A: DNS announcement
--------------------------

.. note:: This is the older method, harder to implement but supporting all servers.

The port can can be announced by setting a DNS record in the following format:

.. code-block:: none

   _matrix._tcp.<yourdomain.com> <ttl> IN SRV <priority> <weight> <port> <synapse.server.name>

For example like this:

.. code-block:: none

  _matrix._tcp.my.domain.name 3600 IN SRV 10 5 443 my.domain.name.

.. note:: this can be checked by running ``dig -t srv _matrix._tcp.my.domain.name``

Option B:.well-known announcement
---------------------------------

.. note:: This is the newer method, easier to implement but not supported on older servers.

Setup the directory for the next step:

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p ~/html/.well-known/matrix
  [isabell@stardust ~]$

The federation port can also be announced via a file ``~/html/.well-known/matrix/server``

.. code-block:: json
  :emphasize-lines: 2

  {
    "m.server": "my.domain.name:443"
  }

This has to be made available under ``/.well-known/matrix`` via the web backend:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set /.well-known/matrix --apache
  Set backend for /.well-known/matrix to apache.
  [isabell@stardust ~]$

Configure Certificates
----------------------

Now you edit the config file ``~/synapse/homeserver.yaml`` to reflect the paths to the letsencrypt certificates:

.. code-block:: yaml
  :emphasize-lines: 1,3,11,13

    tls_certificate_path: "/home/isabell/etc/certificates/my.domain.name.crt"

    tls_private_key_path: "/home/isabell/etc/certificates/my.domain.name.key"

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
 command=python3.6 -m synapse.app.homeserver -c %(ENV_HOME)s/synapse/homeserver.yaml
 autostart=yes
 autorestart=yes
 environment=
        PATH="%(ENV_HOME)s/opt/postgresql/bin/:$PATH",
        LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%(ENV_HOME)s/opt/postgresql/lib",
        PGPASSFILE=%(ENV_HOME)s/.pgpass,
        PGHOST=localhost,
        PGPORT=5432

.. include:: includes/supervisord.rst

Updates
=======

Watch MatrixRSS_ to be notified of upgrades and if there is a update, use pip to update the installation:

.. code-block:: console

  [isabell@stardust ~]$ pip3.6 install --user -U matrix-synapse
  [isabell@stardust ~]$


Administration
==============

Adding users
------------

Users can be added from the CLI:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/synapse
  [isabell@stardust synape]$ register_new_matrix_user -c homeserver.yaml https://my.domain.name:PORT
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

  synapse=> UPDATE users SET password_hash='$2b$12$yK16TMDMnvj97GFBoxF9QeP2N.U8oadindcjB0Uo9TkSI3CsgwV02' WHERE name='@isabell:my.domain.name';
  UPDATE 1
  synapse=>
  [isabell@stardust ~]$

.. note:: ``SELECT name from users;`` returns a list of all usernames

Check federation
----------------

The Matrix_ project provides a federation checker at MatrixFederationChecker_ .



Tested on uberspace 7.3.1.1 via riot.im/app on synapse 1.0.0.

.. _MatrixFederation: https://github.com/matrix-org/synapse/blob/master/docs/federate.md
.. _MatrixRSS: https://matrix.org/blog/feed
.. _Matrix: https://matrix.org/
.. _Synapse: https://matrix.org/docs/projects/server/synapse
.. _MatrixFederationChecker: https://federationtester.matrix.org/

----

.. author_list::

