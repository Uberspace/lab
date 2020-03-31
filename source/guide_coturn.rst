.. author:: jo-mei

.. tag:: STUN
.. tag:: TURN
.. tag:: webRTC

.. highlight:: console

########
coturn
########

.. tag_list::

The TURN Server is a VoIP media traffic NAT traversal server and gateway. It can be used as a general-purpose network traffic TURN server and gateway, too.
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
  
.. note:: Coturn supports sqlite, mysql,, postgresql, mongodb and redis as database backends.
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

 # Turnserver Environement
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
-------------------
The default configuration can be found at ``$HOME/opt/turnserver/etc/turnserver.conf.default``.
So have a look there for all options.

Create a new config file at ``$HOME/etc/coturn/turnserver.conf``
For some ciphers we also nee a DH-file. So lets create that as well.

::
 [isabell@stardust ~]$ mkdir -p $HOME/etc/coturn
 [isabell@stardust ~]$ cd $HOME/etc/coturn
 [isabell@stardust coturn]$ openssl dhparam -out dhparam-2066.pem 2066
 [isabell@stardust coturn]$ nano turnserver.conf

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
 static-auth-secret=<YOURSUPERLONGSUPERSECRETSTATICPASSPHRASE>
 realm=isabell.uber.space
 total-quota=100
 bps-capacity=0
 stale-nonce
 cert=/home/isabell/etc/certificates/isabell.uber.space.crt
 key=/home/isabell/etc/certificates/isabell.uber.space.key
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
  command=%(ENV_HOME)s/opt/coturn/bin/turnserver -c %(ENV_HOME)s/etc/coturn/turnserver.conf

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.
