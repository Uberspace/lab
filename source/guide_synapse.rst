.. author:: 927589452
.. highlight:: console

.. tag:: python
.. tag:: ports

.. sidebar:: Logo

  .. image:: _static/images/matrix-logo.svg
      :align: center

######
Synapse
######

.. tag_list::

Synapse_ is the reference implementation of a matrix server.
Matrix_ is federated chat protocol aiming to replace xmpp.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PostgreSQL_
  * supervisord_

License
=======

All relevant legal information can be found here

  * https://github.com/matrix-org/synapse/blob/master/LICENSE

Prerequisites
=============

You need a running Postgresql_ database server, a dedicated user with a secure password and database for synape.

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

We will install synapse using pip, which makes it quite easy,
but we start with creating a virtual environment for synapse to run in

.. code-block:: console
  :emphasize-lines: 1,2,8,18.27,37

  [isabell@stardust ~]$ mkdir -p ~/synapse
  [isabell@stardust ~]$ virtualenv -p python3.6 ~/synapse/env
    Running virtualenv with interpreter /usr/bin/python3.6
    Using base prefix '/usr'
    New python executable in /home/matrites/synapse/env/bin/python3.6
    Also creating executable in /home/matrites/synapse/env/bin/python
    Installing setuptools, pip, wheel...done.
  [isabell@stardust ~]$ source ~/synapse/env/bin/activate
  (env) [isabell@stardust ~]$ pip install --upgrade pip
    Cache entry deserialization failed, entry ignored
    Collecting pip
      Using cached https://files.pythonhosted.org/packages/5c/e0/be401c003291b56efc55aeba6a80ab790d3d4cece2778288d65323009420/pip-19.1.1-py2.py3-none-any.whl
    Installing collected packages: pip
      Found existing installation: pip 9.0.1
        Uninstalling pip-9.0.1:
          Successfully uninstalled pip-9.0.1
    Successfully installed pip-19.1.1
  (env) [isabell@stardust ~]$ pip install --upgrade pip
    Cache entry deserialization failed, entry ignored
    Collecting pip
      Using cached https://files.pythonhosted.org/packages/5c/e0/be401c003291b56efc55aeba6a80ab790d3d4cece2778288d65323009420/pip-19.1.1-py2.py3-none-any.whl
    Installing collected packages: pip
      Found existing installation: pip 9.0.1
        Uninstalling pip-9.0.1:
          Successfully uninstalled pip-9.0.1
    Successfully installed pip-19.1.1
  (env) [matrites@clark ~]$ pip install --upgrade setuptools
    Collecting setuptools
      Using cached https://files.pythonhosted.org/packages/ec/51/f45cea425fd5cb0b0380f5b0f048ebc1da5b417e48d304838c02d6288a1e/setuptools-41.0.1-py2.py3-none-any.whl
    Installing collected packages: setuptools
      Found existing installation: setuptools 28.8.0
        Uninstalling setuptools-28.8.0:
          Successfully uninstalled setuptools-28.8.0
    Successfully installed setuptools-41.0.1
  (env) [isabell@stardust ~]$ pip install matrix-synapse
    Collecting matrix-synapse
    Collecting pyasn1-modules>=0.0.7 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/91/f0/b03e00ce9fddf4827c42df1c3ce10c74eadebfb706231e8d6d1c356a4062/pyasn1_modules-0.2.5-py2.py3-none-any.whl
    Collecting Twisted>=18.7.0 (from matrix-synapse)
    Collecting msgpack>=0.5.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/92/7e/ae9e91c1bb8d846efafd1f353476e3fd7309778b582d2fb4cea4cc15b9a2/msgpack-0.6.1-cp36-cp36m-manylinux1_x86_64.whl
    Collecting canonicaljson>=1.1.3 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/59/8d/791b6b9a297a4ff982bb51e5d5248dbd4367215f1eeb5a97da51e70585c7/canonicaljson-1.1.4-py2.py3-none-any.whl
    Collecting six>=1.10 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
    Collecting sortedcontainers>=1.4.4 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/13/f3/cf85f7c3a2dbd1a515d51e1f1676d971abe41bba6f4ab5443240d9a78e5b/sortedcontainers-2.1.0-py2.py3-none-any.whl
    Collecting pyyaml>=3.11 (from matrix-synapse)
    Collecting pynacl>=1.2.1 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/27/15/2cd0a203f318c2240b42cd9dd13c931ddd61067809fee3479f44f086103e/PyNaCl-1.3.0-cp34-abi3-manylinux1_x86_64.whl
    Collecting service-identity>=18.1.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/e9/7c/2195b890023e098f9618d43ebc337d83c8b38d414326685339eb024db2f6/service_identity-18.1.0-py2.py3-none-any.whl
    Collecting signedjson>=1.0.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/fa/af/45b3f7768a7a1640ab7495b645b5f558653a43355dc0e28cc3128257a9b4/signedjson-1.0.0-py2.py3-none-any.whl
    Collecting attrs>=17.4.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/23/96/d828354fa2dbdf216eaa7b7de0db692f12c234f7ef888cc14980ef40d1d2/attrs-19.1.0-py2.py3-none-any.whl
    Collecting frozendict>=1 (from matrix-synapse)
    Collecting unpaddedbase64>=1.1.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/96/da/2ebf30d2fdf0f4dc949b4935e408aaa9cca948963e55ea3c99730b1f74c0/unpaddedbase64-1.1.0-py2.py3-none-any.whl
    Collecting pillow>=4.3.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/d2/c2/f84b1e57416755e967236468dcfb0fad7fd911f707185efc4ba8834a1a94/Pillow-6.0.0-cp36-cp36m-manylinux1_x86_64.whl
    Collecting daemonize>=2.3.1 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/45/ad/1b20db02287afd40d3130a218ac5ce2f7d2ab581cfda29bada5e1c4bee17/daemonize-2.5.0-py2.py3-none-any.whl
    Collecting treq>=15.1 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/77/20/a938853f08d1b2ecb0bc161add2b41173d18a8f1756b3c3236e920a3e200/treq-18.6.0-py2.py3-none-any.whl
    Collecting bcrypt>=3.1.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/d0/79/79a4d167a31cc206117d9b396926615fa9c1fdbd52017bcced80937ac501/bcrypt-3.1.6-cp34-abi3-manylinux1_x86_64.whl
    Collecting pymacaroons>=0.13.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/d8/87/fd9b54258216e3f19671f6e9dd76da1ebc49e93ea0107c986b1071dd3068/pymacaroons-0.13.0-py2.py3-none-any.whl
    Collecting pyasn1>=0.1.9 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/7b/7c/c9386b82a25115cccf1903441bba3cbadcfae7b678a20167347fa8ded34c/pyasn1-0.4.5-py2.py3-none-any.whl
    Collecting idna>=2 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl
    Collecting pyopenssl>=16.0.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/01/c8/ceb170d81bd3941cbeb9940fc6cc2ef2ca4288d0ca8929ea4db5905d904d/pyOpenSSL-19.0.0-py2.py3-none-any.whl
    Collecting psutil>=2.0.0 (from matrix-synapse)
    Collecting jsonschema>=2.5.1 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/aa/69/df679dfbdd051568b53c38ec8152a3ab6bc533434fc7ed11ab034bf5e82f/jsonschema-3.0.1-py2.py3-none-any.whl
    Collecting netaddr>=0.7.18 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/ba/97/ce14451a9fd7bdb5a397abf99b24a1a6bb7a1a440b019bebd2e9a0dbec74/netaddr-0.7.19-py2.py3-none-any.whl
    Collecting phonenumbers>=8.2.0 (from matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/52/9c/f577faea449e12041046ce10b98db65830a192f0ec68e377b1fa270b4781/phonenumbers-8.10.13-py2.py3-none-any.whl
    Collecting prometheus-client<0.4.0,>=0.0.18 (from matrix-synapse)
    Collecting constantly>=15.1 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/b9/65/48c1909d0c0aeae6c10213340ce682db01b48ea900a7d9fce7a7910ff318/constantly-15.1.0-py2.py3-none-any.whl
    Collecting hyperlink>=17.1.1 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/7f/91/e916ca10a2de1cb7101a9b24da546fb90ee14629e23160086cf3361c4fb8/hyperlink-19.0.0-py2.py3-none-any.whl
    Collecting zope.interface>=4.4.2 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/19/17/1d198a6aaa9aa4590862fe3d3a2ed7dd808050cab4eebe8a2f2f813c1376/zope.interface-4.6.0-cp36-cp36m-manylinux1_x86_64.whl
    Collecting Automat>=0.3.0 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/a3/86/14c16bb98a5a3542ed8fed5d74fb064a902de3bdd98d6584b34553353c45/Automat-0.7.0-py2.py3-none-any.whl
    Collecting PyHamcrest>=1.9.0 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/9a/d5/d37fd731b7d0e91afcc84577edeccf4638b4f9b82f5ffe2f8b62e2ddc609/PyHamcrest-1.9.0-py2.py3-none-any.whl
    Collecting incremental>=16.10.1 (from Twisted>=18.7.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/f5/1d/c98a587dc06e107115cf4a58b49de20b19222c83d75335a192052af4c4b7/incremental-17.5.0-py2.py3-none-any.whl
    Collecting simplejson>=3.6.5 (from canonicaljson>=1.1.3->matrix-synapse)
    Collecting cffi>=1.4.1 (from pynacl>=1.2.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/5f/bf/6aa1925384c23ffeb579e97a5569eb9abce41b6310b329352b8252cee1c3/cffi-1.12.3-cp36-cp36m-manylinux1_x86_64.whl
    Collecting cryptography (from service-identity>=18.1.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/97/18/c6557f63a6abde34707196fb2cad1c6dc0dbff25a200d5044922496668a4/cryptography-2.7-cp34-abi3-manylinux1_x86_64.whl
    Collecting requests>=2.1.0 (from treq>=15.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/51/bd/23c926cd341ea6b7dd0b2a00aba99ae0f828be89d72b2190f27c11d4b7fb/requests-2.22.0-py2.py3-none-any.whl
    Collecting pyrsistent>=0.14.0 (from jsonschema>=2.5.1->matrix-synapse)
    Requirement already satisfied: setuptools in ./synapse/env/lib/python3.6/site-packages (from jsonschema>=2.5.1->matrix-synapse) (41.0.1)
    Collecting pycparser (from cffi>=1.4.1->pynacl>=1.2.1->matrix-synapse)
    Collecting asn1crypto>=0.21.0 (from cryptography->service-identity>=18.1.0->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/ea/cd/35485615f45f30a510576f1a56d1e0a7ad7bd8ab5ed7cdc600ef7cd06222/asn1crypto-0.24.0-py2.py3-none-any.whl
    Collecting chardet<3.1.0,>=3.0.2 (from requests>=2.1.0->treq>=15.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl
    Collecting certifi>=2017.4.17 (from requests>=2.1.0->treq>=15.1->matrix-synapse)
      Downloading https://files.pythonhosted.org/packages/69/1b/b853c7a9d4f6a6d00749e94eb6f3a041e342a885b87340b79c1ef73e3a78/certifi-2019.6.16-py2.py3-none-any.whl (157kB)
         |████████████████████████████████| 163kB 17.4MB/s
    Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests>=2.1.0->treq>=15.1->matrix-synapse)
      Using cached https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl
    Installing collected packages: pyasn1, pyasn1-modules, attrs, constantly, idna, hyperlink, zope.interface, six, Automat, PyHamcrest, incremental, Twisted, msgpack, simplejson, frozendict, canonicaljson, sortedcontainers, pyyaml, pycparser, cffi, pynacl, asn1crypto, cryptography, service-identity, unpaddedbase64, signedjson, pillow, daemonize, chardet, certifi, urllib3, requests, treq, bcrypt, pymacaroons, pyopenssl, psutil, pyrsistent, jsonschema, netaddr, phonenumbers, prometheus-client, matrix-synapse
    Successfully installed Automat-0.7.0 PyHamcrest-1.9.0 Twisted-19.2.1 asn1crypto-0.24.0 attrs-19.1.0 bcrypt-3.1.6 canonicaljson-1.1.4 certifi-2019.6.16 cffi-1.12.3 chardet-3.0.4 constantly-15.1.0 cryptography-2.7 daemonize-2.5.0 frozendict-1.2 hyperlink-19.0.0 idna-2.8 incremental-17.5.0 jsonschema-3.0.1 matrix-synapse-1.0.0 msgpack-0.6.1 netaddr-0.7.19 phonenumbers-8.10.13 pillow-6.0.0 prometheus-client-0.3.1 psutil-5.6.3 pyasn1-0.4.5 pyasn1-modules-0.2.5 pycparser-2.19 pymacaroons-0.13.0 pynacl-1.3.0 pyopenssl-19.0.0 pyrsistent-0.15.2 pyyaml-5.1.1 requests-2.22.0 service-identity-18.1.0 signedjson-1.0.0 simplejson-3.16.0 six-1.12.0 sortedcontainers-2.1.0 treq-18.6.0 unpaddedbase64-1.1.0 urllib3-1.25.3 zope.interface-4.6.0
  (env) [isabell@stardust ~]$ pip install jinja2
    Collecting jinja2
      Using cached https://files.pythonhosted.org/packages/1d/e7/fd8b501e7a6dfe492a433deb7b9d833d39ca74916fa8bc63dd1a4947a671/Jinja2-2.10.1-py2.py3-none-any.whl
    Collecting MarkupSafe>=0.23 (from jinja2)
      Using cached https://files.pythonhosted.org/packages/b2/5f/23e0023be6bb885d00ffbefad2942bc51a620328ee910f64abe5a8d18dd1/MarkupSafe-1.1.1-cp36-cp36m-manylinux1_x86_64.whl
    Installing collected packages: MarkupSafe, jinja2
    Successfully installed MarkupSafe-1.1.1 jinja2-2.10.1
  (env) [isabell@stardust ~]$ pip install psycopg2
    Collecting psycopg2
      Downloading https://files.pythonhosted.org/packages/5c/1c/6997288da181277a0c29bc39a5f9143ff20b8c99f2a7d059cfb55163e165/psycopg2-2.8.3.tar.gz (377kB)
         |████████████████████████████████| 378kB 21.4MB/s
    Building wheels for collected packages: psycopg2
      Building wheel for psycopg2 (setup.py) ... done
      Stored in directory: /home/matrites/.cache/pip/wheels/48/06/67/475967017d99b988421b87bf7ee5fad0dad789dc349561786b
    Successfully built psycopg2
    Installing collected packages: psycopg2
    Successfully installed psycopg2-2.8.3

  (env) [isabell@stardust ~]$


Configuration
=============

Generate standard config
------------------------

generate a config file ``~/synapse/homeserver.yaml`` and replace my.domain.name with the real domain you want your matrix username to end in.

.. code-block:: console

  [isabell@stardust ~]$ source ~/synapse/env/bin/activate
  (env) [isabell@stardust ~]$ cd ~/synapse
  (env) [isabell@stardust synapse]$  python -m synapse.app.homeserver \
    --server-name my.domain.name \
    --config-path homeserver.yaml \
    --generate-config \
    --report-stats=[yes|no]
  (env) [isabell@stardust ~]$

Configure port
--------------
Add a port for the homeserver.

.. include:: includes/open-port.rst

and include the generated port in the config file ``~/synapse/homeserver.yaml``.

.. code-block:: yaml

    listeners:
      - port: 40312
        type: http
        tls: true
        bind_addresses: ['::','0.0.0.0']
        resources:
          - names: [client, federation]

      - port: 8008
        type: http
        tls: false
        bind_addresses: ['::','0.0.0.0']
        x_forwarded: true
        resources:
          - names: [client]

for ease of use we will make use of ``uberspace web backend`` and point it to 8008.

.. include:: includes/web-backend.rst


Configure Certificates
----------------------

now you edit the config file ``~/synapse/homeserver.yaml`` to reflect the paths to the letsencrypt certificates:

.. code-block:: yaml

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

allow users to be found by enabling the user directory in the config file ``~/synapse/homeserver.yaml``:

.. code-block:: yaml

  user_directory:
    enabled: true

Setup daemon
------------

Create ``~/etc/services.d/synapse.ini`` with the following content:

.. code-block:: ini

 [program:synapse]
 command=%(ENV_HOME)s/synapse/env/bin/python3.6 -m synapse.app.homeserver -c %(ENV_HOME)s/synapse/homeserver.yaml
 autostart=yes
 autorestart=yes
 environment=
        PATH="/home/matrites/synapse/env/bin:%(ENV_HOME)s/opt/postgresql/bin/:$PATH",
        LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%(ENV_HOME)s/opt/postgresql/lib",
        PGPASSFILE=%(ENV_HOME)s/.pgpass,
        PGHOST=localhost,
        PGPORT=5432


Tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 synapse: available
 [isabell@stardust ~]$ supervisorctl update
 synapse: added process group
 [isabell@stardust ~]$ supervisorctl status
 synapse                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Updates
=======

If there is a update, use pip to update the installation:

.. code-block:: console

  [isabell@stardust ~]$ source ~/synapse/env/bin/activate
  (env) [isabell@stardust ~]$ pip install -U matrix-synapse
  [isabell@stardust ~]$


Administration
==============

Adding users
------------

Users can be added from the CLI:
Adding users
------------

Users can be added from the CLI:

.. code-block:: console

  [isabell@stardust ~]$ source ~/synapse/env/bin/activate
  (env) [isabell@stardust ~]$ cd ~/synapse
  (env) [isabell@stardust synape]$ register_new_matrix_user -c homeserver.yaml https://my.domain.name:PORT
  New user localpart [isabell]: USER
  Password:
  Confirm password:
  Make admin [no]: no
  Sending registration request...
  Success!
  (env) [isabell@stardust synapse]$





Password reset
--------------

Passwords can be reset using the cli; first generate the hash of the new password:

.. code-block:: console

  [isabell@stardust ~]$ ~/synapse/env/bin/hash_password
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


Tested on uberspace 7.3.1.1 via riot.im/app on synapse 1.0.0.

.. _PostgreSQL: https://lab.uberspace.de/guide_postgresql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _Matrix: https://matrix.org/
.. _Synapse: https://matrix.org/docs/projects/server/synapse

----

.. author_list::

