.. author:: jo-mei

.. tag:: STUN
.. tag:: TURN
.. tag:: webRTC

.. highlight:: console

########
coturn
########

.. tag_list::

The `TURN Server <https://github.com/coturn/coturn>`_ is a VoIP media traffic NAT traversal server and gateway. It can be used as a general-purpose network traffic TURN server and gateway, too.
On-line management interface (over telnet or over HTTPS) for the TURN server is available.
The implementation also includes some extra experimental features.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`firewall ports <basics-ports>`

Installation
============

Download, configure, compile and install coturn to your uberspace home directory.
Use the following options for ``./configure``:

  * ``--prefix=$HOME/opt/turnserver/``: Install to separate folder in your personal uberspace

.. note::
  Coturn supports sqlite, mysql, postgresql, mongodb and redis as database backends.
  Sqlite and mysql work out of the box.
  If you want the others you must install them before and set ``CPATH`` and ``LIBRARY_PATH`` accoringly.

::

 [isabell@stardust ~]$ mkdir -p $HOME/src/
 [isabell@stardust ~]$ cd $HOME/src/
 [isabell@stardust src]$ curl -O https://coturn.net/turnserver/v4.5.0.8/turnserver-4.5.0.8.tar.gz
 [isabell@stardust src]$ tar -xvzf turnserver-4.5.0.8.tar.gz
 [isabell@stardust src]$ cd turnserver-4.5.0.8/
 [isabell@stardust turnserver-4.5.0.8]$ ./configure --prefix=$HOME/opt/turnserver
 [isabell@stardust turnserver-4.5.0.8]$ make
 [isabell@stardust turnserver-4.5.0.8]$ make install

Make the binaries and man pages available through ``.bash_profile``:

.. code-block:: bash

 # Turnserver Environment
 export PATH=$HOME/opt/turnserver/bin:$PATH
 export MANPATH=${MANPATH:+${MANPATH}:}$HOME/opt/turnserver/man

Configuration
=============

Open Firewall Ports
-------------------
Coturn needs at least 2 open ports, plus some additional sucessive ports as port range for udp connections.
So lets open 5 ports.

.. include:: includes/open-port.rst


Create a configuration
----------------------
The default configuration can be found at ``$HOME/opt/turnserver/etc/turnserver.conf.default``.
So have a look there or at the documantation_ for all options.

For some ciphers we need a DH-file:.

::

  [isabell@stardust ~]$ mkdir -p $HOME/etc/coturn
  [isabell@stardust ~]$ cd $HOME/etc/coturn
  [isabell@stardust coturn]$ openssl dhparam -out dhparam-2066.pem 2066

Create a new config file at ``$HOME/etc/coturn/turnserver.conf``
Replace values in brackets ``<value>`` with your values.

::

 listening-port=<port-1>
 tls-listening-port=<port-1>
 alt-listening-port=<port-2>
 alt-tls-listening-port=<port-2>
 listening-ip=::
 listening-ip=0.0.0.0
 relay-ip=::
 relay-ip=0.0.0.0
 min-port=<port-3>
 max-port=<port-5>
 fingerprint
 lt-cred-mech
 use-auth-secret
 static-auth-secret=<YOUR_SUPER_LONG_SUPER_SECRET_STATIC_PASSPHRASE>
 realm=isabell.uber.space
 total-quota=100
 bps-capacity=0
 stale-nonce
 cert=/home/isabell/etc/certificates/isabell.uber.space.crt
 pkey=/home/isabell/etc/certificates/isabell.uber.space.key
 dh-file=/home/isabell/etc/coturn/dhparam-2066.pem
 cipher-list="ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AES:RSA+3DES:!ADH:!AECDH:!MD5"
 no-cli
 no-loopback-peers
 no-multicast-peers

Setup daemon
------------

Create ``~/etc/services.d/coturn.ini`` with the following content:

.. code-block:: ini

  [program:coturn]
  command=%(ENV_HOME)s/opt/turnserver/bin/turnserver -c %(ENV_HOME)s/etc/coturn/turnserver.conf

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

There are a multiple applications that can use your turnserver.

Nextcloud Talk
--------------
If you are using :lab:`Nextcloud<guide_nextcloud>`, the Talk app can use coturn as STUN and TURN server.
Therefore in Nextcloud go to ``Settings`` and select the ``Talk`` Tab.

  * Add ``isabell.uber.space:<port-1>`` as STUN Server.
  * Add ``isabell.uber.space:<port-1>`` with ``<YOUR_SUPER_LONG_SUPER_SECRET_STATIC_PASSPHRASE>`` as TURN Server for ``UDP and TCP``
  * Test your server (the little heart beat symbol next to it)

The test should result in a checkmark symbol. If not check your Nextcloud and coturn logs.

Synapse
-------
The :lab:`Synapse<guide_synapse>` homeserver can be configured to offer your coturn server for webRTC calls.
Therefore edit your ``homeserver.yaml`` config:

.. code-block:: yaml
  :emphasize-lines: 5-8,11

  ## TURN ##

  # The public URIs of the TURN server to give to clients
  turn_uris:
    - "turns:isabell.uber.space:<port-1>?transport=udp"
    - "turns:isabell.uber.space:<port-1>?transport=tcp"
    - "turn:isabell.uber.space:<port-1>?transport=udp"
    - "turn:isabell.uber.space:<port-1>?transport=tcp"

  # The shared secret used to compute passwords for the TURN server
  turn_shared_secret: "<YOUR_SUPER_LONG_SUPER_SECRET_STATIC_PASSPHRASE>"


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check coturn's `releases <https://github.com/coturn/coturn/releases>`_ for the latest version. If a newer
version is available, stop daemon with ``supervisorctl stop coturn`` and repeat the "Installation" step followed by ``supervisorctl start coturn`` to restart coturn.

.. _documantation: https://github.com/coturn/coturn/wiki/turnserver
.. _feed: https://github.com/coturn/coturn/releases.atom

----

Tested with coturn 4.5.1.1 and Uberspace 7.5.1

.. author_list::
