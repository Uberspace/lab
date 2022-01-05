.. author:: Jonas <https://github.com/jfowl>

.. tag:: lang-rust
.. tag:: chat
.. tag:: matrix

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/conduit.svg
      :align: center

#######
Conduit
#######

.. tag_list::

Conduit_ is a homeserver for the Matrix chat protocol written in :manual:`Rust <lang-rust>`. It is targeted at personal use.

At the time of writing Conduit has not reached a stable 1.0 version yet.
Until then, upgrading it might incur data loss.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

Installation
============

Download the latest development build and mark it as executable:

::

  [isabell@stardust ~]$ wget https://gitlab.com/famedly/conduit/-/jobs/artifacts/master/raw/conduit-x86_64-unknown-linux-musl?job=build:release:cargo:x86_64-unknown-linux-musl -O ~/bin/conduit
  Resolving gitlab.com (gitlab.com)... 172.65.251.78, 2606:4700:90:0:f22e:fbec:5bed:a9b9
  Saving to: ‘conduit’

  100%[=========================================================>] 33.395.624  25,9MB/s   in 1,2s

  2021-07-20 15:17:59 (25,9 MB/s) - ‘conduit’ saved [33395624/33395624]

  [isabell@stardust ~]$ chmod +x ~/bin/conduit
  [isabell@stardust ~]$

Configuration
=============

There are a few things you must decide, if you want to run a Matrix homeserver:

* Do you want to federate with other matrix servers? If not, only users on your server can talk with each other
* Who should be able to register an account? If you don't want other people, you will need to change the settings after creating your account.
* Which domain name do you want to use? This will determine your usernames (e.g. ``@myname:mydomain.tld``).
  This guide assumes you will be using the ``.uber.space`` domain of your Uberspace account.
  If you want to use your own domain, you will need to adjust the commands and configs below accordingly.


Configure Conduit
-----------------

Conduit manages it's own database files. Create a directory for it:

::

  [isabell@stardust ~]$ mkdir -p ~/conduit_data/
  [isabell@stardust ~]$ 

Create ``~/conduit.toml`` with the following content:

.. warning:: Replace all place holders such as ``<username>`` with your actual values!

.. code-block:: toml
 :emphasize-lines: 11,14

 [global]
 # The server_name is the name of this server. It is used as a suffix for user
 # and room ids. Examples: matrix.org, conduit.rs
 # The Conduit server needs to be reachable at https://your.server.name/ on port
 # 443 (client-server) and 8448 (federation) OR you can create /.well-known
 # files to redirect requests. See
 # https://matrix.org/docs/spec/client_server/latest#get-well-known-matrix-client
 # and https://matrix.org/docs/spec/server_server/r0.1.4#get-well-known-matrix-server
 # for more information

 server_name = "<username>.uber.space"

 # This is the only directory where Conduit will save its data
 database_path = "/home/<username>/conduit_data"

 port = 6167

 # Max size for uploads
 max_request_size = 20_000_000 # in bytes

 # Disable registration. No new users will be able to register on this server
 allow_registration = true

 # Disable encryption, so no new encrypted rooms can be created
 # Note: existing rooms will continue to work
 #allow_encryption = false
 allow_federation = true

 # Enable jaeger to support monitoring and troubleshooting through jaeger
 #allow_jaeger = false

 trusted_servers = ["matrix.org"]

 #max_concurrent_requests = 100 # How many requests Conduit sends to other servers at the same time
 #log = "info,state_res=warn,rocket=off,_=off,sled=off"
 #workers = 4 # default: cpu core count * 2

 address = "0.0.0.0" # This makes sure Conduit can only be reached using the reverse proxy

 proxy = "none"

 # The total amount of memory that the database will use.
 db_cache_capacity_mb = 100


Setup daemon
------------

Create ``~/etc/services.d/conduit.ini`` with the following content:

.. code-block:: ini

 [program:conduit]
 command=%(ENV_HOME)s/bin/conduit
 environment=CONDUIT_CONFIG="%(ENV_HOME)s/conduit.toml"
 process_name=%(program_name)s
 autostart=true
 startsecs=5
 startretries=3
 stopwaitsecs=5


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::
  To talk to each other on Matrix, your chat client often needs to know how to talk to users on different servers.
  When a Matrix chat client encounters the user ``@isabell:uberspace.de`` it will look at ``https://uberspace.de/.well-known/matrix/server``,
  which contains information about where to find the actual Matrix server for that domain (``uberspace.de``).

  This is mostly practical for bigger Matrix servers with many users, where you don't want to run the website (uberspace.de) on the same hardware as the matrix server.
  In this guide however, we will just host the Matrix server and your potential website side by side on the same uberspace account.

Create the directory ``~/html/.well-known/matrix/``:

::

  [isabell@stardust ~]$ mkdir -p ~/conduit_data/
  [isabell@stardust ~]$ 

Then create ``~/html/.well-known/matrix/server`` with the following content.
Remember to replace <username> with your actual user name:

.. code-block:: json

  {
    "m.server": "<username>.uber.space:443"
  }

Create ``~/html/.well-known/matrix/client`` with the following content.
Again, remember to replace <username> with your actual user name:

.. code-block:: json

  {
    "m.homeserver": {
      "base_url": "https://<username>.uber.space"
    },
    "m.identity_server": {
      "base_url": "https://<username>.uber.space"
    }
  }


Forward ``/_matrix`` requests to Conduit, but serve ``.well-known/matrix`` from ``~/html``:

::

  [isabell@stardust ~]$ uberspace web backend set /.well-known/matrix --apache
  [isabell@stardust ~]$ uberspace web backend set /_matrix --http --port 6167
  [isabell@stardust ~]$

Usage
=====

Congratulations, you now got your own little Matrix server up and running.

To test if everything is working, you can open https://app.element.io - a matrix web client - and register an account with it.
If everything worked, you should see the "Admin Room" in your chat list.

.. warning:: Remember to set ``allow_registration = false`` in the Conduit config and restart it, if you don't want anyone else to use your server.

Updates
=======

In most cases, you can just overwrite the conduit binary and restart.
If you care about your data, you might want to make a backup first.

::

[isabell@stardust ~]$ supervisorctl stop conduit
[isabell@stardust ~]$ cp -r ~/conduit_data ~/conduit_data_backup
[isabell@stardust ~]$ wget https://gitlab.com/famedly/conduit/-/jobs/artifacts/master/raw/conduit-x86_64-unknown-linux-musl?job=build:release:cargo:x86_64-unknown-linux-musl -O ~/bin/conduit
[isabell@stardust ~]$ chmod +x ~/conduit
[isabell@stardust ~]$ supervisorctl start conduit
[isabell@stardust ~]$

If everything went smoothly, you can remove that backup:

::

[isabell@stardust ~]$ rm -rf ~/conduit_data_backup



----

Tested with Conduit-d07762f5_, Uberspace 7.11.3.0


.. _Conduit: https://conduit.rs
.. _Conduit-d07762f5: https://gitlab.com/famedly/conduit/-/tree/d07762f5962baf0b4e5a50abcefb24cdc210fec1

.. author_list::
