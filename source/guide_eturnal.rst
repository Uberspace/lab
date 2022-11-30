.. author:: this.ven <https://this.ven.uber.space>

.. tag:: STUN
.. tag:: TURN
.. tag:: webRTC
.. tag:: Erlang

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/eturnal.png
      :align: center

#######
eturnal
#######

.. tag_list::

eturnal_ is a modern, straightforward STUN and TURN server written in Erlang. Clients can connect using UDP, TCP, or TLS over IPv4 or IPv6. For authentication, eturnal supports the mechanism described in the `REST API for Access to TURN Services`_ specification.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`firewall ports <basics-ports>`
  * :manual:`cron jobs <daemons-cron>`

License
=======

eturnal is released under the `Apache License, Version 2.0`_.

Prerequisites
=============

Set up your URL:

.. include:: includes/web-domain-list.rst

Installation
============

Check the `latest release`_ and download a precompiled tarball from https://eturnal.net and adapt the download url to the most recent version in the commands below:

.. code-block:: console

  [isabell@stardust ~]$ wget https://eturnal.net/download/linux/eturnal-1.10.1-linux-x64.tar.gz
  [isabell@stardust ~]$ tar xzf eturnal-1.10.1-linux-x64.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Open Firewall Ports
-------------------
eturnal needs 2 listen ports, plus a port range for relaying UDP connections. So lets open 5 ports.

.. include:: includes/open-port.rst

eturnal Config
--------------

Generate a DH-file and a random super long secret (64 characters).

.. code-block:: console

  [isabell@stardust ~]$ openssl dhparam -out $HOME/eturnal/etc/dh-parameters.pem 4096
  Generating DH parameters, 4096 bit long safe prime, generator 2
  This is going to take a long time
  ........+.................................+.....................+..................
  ....................+.....................................+........+...............
  [...]
  [isabell@stardust ~]$ openssl rand -hex 32
  [isabell@stardust ~]$ <super-long-secret>

Backup the standard config: ``mv ~/eturnal/etc/eturnal.yml ~/eturnal/etc/eturnal.yml.bkp``.
Create a new file at ``~/eturnal/etc/eturnal.yml`` and replace values in brackets ``<value>`` with your values.

.. code-block:: yaml
  eturnal:

    secret: "<super-long-secret>"

    listen:
      -
        ip: "::"
        port: <port-1>
        transport: udp
      -
        ip: "::"
        port: <port-1>
        transport: tcp
      -
        ip: "::"
        port: <port-2>
        transport: tls

    tls_crt_file: /home/isabell/etc/certificates/isabell.uber.space.crt
    tls_key_file: /home/isabell/etc/certificates/isabell.uber.space.key
    tls_dh_file: /home/isabell/eturnal/etc/dh-parameters.pem

    relay_min_port: <port-3>
    relay_max_port: <port-5>

    blacklist: 
      - "127.0.0.0/8"
      - "::1"

    log_level: error
    log_rotate_size: 10485760
    log_rotate_count: 10
    log_dir: stdout
  
Find other configuration options in the `reference documentation`_. You can now `first start`_ eturnal as daemon and check it's startup by invoking:

.. code-block:: console

  [isabell@stardust ~]$ ~/eturnal/bin/eturnalctl daemon
  [isabell@stardust ~]$ ~/eturnal/bin/eturnalctl info
  [isabell@stardust ~]$

If it's not running, check your configuration_.

Afterwards you can set up the service by creating a file ``~/etc/services.d/eturnal.ini`` with the following content:

.. code-block:: ini

  [program:eturnal]
  command=%(ENV_HOME)s/eturnal/bin/eturnalctl foreground
  autostart=yes
  autorestart=yes
  startsecs=30

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs.

Finishing installation
======================

There are a multiple applications that can use eturnal as STUN/TURN server.

Nextcloud Talk
--------------

If you are using :lab:`Nextcloud<guide_nextcloud>`, the Talk app can use eturnal in in the `Talk`` Tab of ``Settings``:

  * Add ``isabell.uber.space:<port-1>`` as STUN Server.
  * Add ``isabell.uber.space:<port-1>`` with ``<super-long-secret>`` as TURN and TURNS Server for ``UDP and TCP``
  * Test your server (the little heart beat symbol next to the fields)

The test should result in a checkmark symbol. If not check your Nextcloud and eturnal logs.

Synapse
-------

The :lab:`Synapse<guide_synapse>` homeserver can employ your eturnal server for webRTC calls by editing your ``homeserver.yaml`` config:

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
  turn_shared_secret: "<super-long-secret>"

----

Tested on Uberspace v7.13 with Erlang v24 and eturnal v1.10.1.

.. author_list::

.. _eturnal: https://eturnal.net
.. _`REST API for Access to TURN Services`: https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00
.. _`Apache License, Version 2.0`: https://www.apache.org/licenses/LICENSE-2.0
.. _`latest release`: https://github.com/processone/eturnal/releases/latest
.. _`reference documentation`: https://eturnal.net/documentation/
.. _`first start`: https://eturnal.net/documentation/code/quick-test.html
.. _configuration: #configuration
.. _`cron jobs`: https://manual.uberspace.de/daemons-cron
