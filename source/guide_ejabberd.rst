.. author:: fm0de
.. author:: jo-mei

.. tag:: XMPP
.. tag:: Jabber
.. tag:: Instant Messanging

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ejabberd.png
      :align: center

########
ejabberd
########

.. tag_list::


`ejabberd <https://www.process-one.net/en/ejabberd/>`_ is a distributed, fault-tolerant technology that allows the creation of large-scale instant messaging applications. The server can reliably support thousands of simultaneous users on a single node and has been designed to provide exceptional standards of fault tolerance. As an open source technology, based on industry-standards, ejabberd can be used to build bespoke solutions very cost effectively.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`firewall ports <basics-ports>`
  * :manual:`web backends <web-backends>`

This guide is based on the initial `pull request <https://github.com/Uberspace/lab/pull/444>`_ from `fm0de <https://github.com/fm0de>`_ and the `work from clerie <https://blog.clerie.de/ejabberd-auf-uberspace-installieren/>`_.

Prerequisites
=============

Domain
------

Your ejabberd domain ``isabell.example`` needs to be setup. ejabberd then defaults to the subomains
``upload.isabell.example``, ``conference.isabell.example`` , ``pubsub.isabell.example`` and ``proxy.isabell.example``
::

 [isabell@stardust ~]$ uberspace web domain add isabell.example
 [isabell@stardust ~]$ uberspace web domain add conference.isabell.example
 [isabell@stardust ~]$ uberspace web domain add upload.isabell.example
 [isabell@stardust ~]$ uberspace web domain add pubsub.isabell.example
 [isabell@stardust ~]$ uberspace web domain add proxy.isabell.example

Also we need the SSL Certificates. Visit the domains in a browser or run:
::

 [isabell@stardust ~]$ curl https://isabell.example
 [isabell@stardust ~]$ curl https://conference.isabell.example
 [isabell@stardust ~]$ curl https://upload.isabell.example
 [isabell@stardust ~]$ curl https://pubsub.isabell.example
 [isabell@stardust ~]$ curl https://proxy.isabell.example


Installation
============

Download, configure, compile and install ejabberd.
Use the following options for ``./configure``:

  * ``--prefix=$HOME/opt/ejabberd/``: Install to your personal uberspace
  * ``--enable-user=$USER``: Allow execution of ejabberd as $USER
  * ``--enable-mysql --enable-new-sql-schema``: optionally compile with mysql support
  * ``--enable-sqlite``: optionally compile with sqlite support

Run ``./configure --help`` to see all options.

::

 [isabell@stardust ~]$ mkdir $HOME/src/
 [isabell@stardust ~]$ cd $HOME/src/
 [isabell@stardust src]$ wget https://github.com/processone/ejabberd/archive/20.03.tar.gz
 [isabell@stardust src]$ tar xf 20.03.tar.gz
 [isabell@stardust src]$ cd ejabberd-20.03/
 [isabell@stardust ejabberd-20.03]$ ./autogen.sh
 [isabell@stardust ejabberd-20.03]$ ./configure --enable-user=$USER --prefix=$HOME/opt/ejabberd --enable-mysql --enable-new-sql-schema
 [isabell@stardust ejabberd-20.03]$ make install

Now link the ejabberdctl to $HOME/bin

::
 [isabell@stardust ~]$ ln -s $HOME/opt/ejabberd/sbin/ejabberdctl $HOME/bin/

Configuration
=============

Open Firewall Ports
-------------------
ejabberd needs five open ports: 2 for c2s, 2 for s2s, and 1 for proxy connections. HTTP connections are handled by a web backend.

.. include:: includes/open-port.rst

Add SRV records
---------------
As standard ports cannot be used on uberspace SRV records must be set for c2s and s2s connections. Refer to the `XMPP wiki <https://wiki.xmpp.org/web/SRV_Records>`_ for setup and point them to the corresponding ports.

::

 _xmpp-client._tcp.isabell.example. 86400 IN SRV 5 0 <port-1> isabell.example.
 _xmpps-client._tcp.isabell.example. 86400 IN SRV 4 0 <port-2> isabell.example.
 _xmpp-server._tcp.isabell.example. 86400 IN SRV 5 0 <port-3> isabell.example.
 _xmpps-server._tcp.isabell.example. 86400 IN SRV 4 0 <port-4> isabell.example.

Change the configuration
------------------------

A standard config file is provided at ``~/opt/ejabberd/etc/ejabberd/ejabberd.yml``.
Copy it to ``~/etc/ejabberd/ejabberd.yml`` so it survives updates.
Than adjust it with correct ports, domain and administrator settings:

Change the host configuration to listen for the correct domain:

.. code-block:: ini
 :emphasize-lines: 2

  hosts:
  - "isabell.example"

Provide location of your keys and certificates for TLS transport:

.. code-block:: ini
 :emphasize-lines: 2-11

  certfiles:
    - "/home/isabell/etc/certificates/isabell.example.crt"
    - "/home/isabell/etc/certificates/isabell.example.key"
    - "/home/isabell/etc/certificates/conference.isabell.example.crt"
    - "/home/isabell/etc/certificates/conference.isabell.example.key"
    - "/home/isabell/etc/certificates/upload.isabell.example.crt"
    - "/home/isabell/etc/certificates/upload.isabell.example.key"
    - "/home/isabell/etc/certificates/proxy.isabell.example.crt"
    - "/home/isabell/etc/certificates/proxy.isabell.example.key"
    - "/home/isabell/etc/certificates/pubsub.isabell.example.crt"
    - "/home/isabell/etc/certificates/pubsub.isabell.example.key"


Change the port numbers to your open ports according to your SRV records:

.. code-block:: ini
 :emphasize-lines: 3,11,19,24

  listen:
    - # c2s
      port: <port-1>
      ip: "::"
      module: ejabberd_c2s
      max_stanza_size: 262144
      shaper: c2s_shaper
      access: c2s
      starttls_required: true
    - # 'secure' c2s
      port: <port-2>
      ip: "::"
      module: ejabberd_c2s
      tls: true
      max_stanza_size: 262144
      shaper: c2s_shaper
      access: c2s
    - # s2s
      port: <port-3>
      ip: "::"
      module: ejabberd_s2s_in
      max_stanza_size: 524288
    - # 'secure' s2s
      port: <port-4>
      ip: "::"
      module: ejabberd_s2s_in
      tls: true
      max_stanza_size: 524288

Disable TLS for HTTP as it is going to be provided through web backends and disable the last two listeners:

.. code-block:: ini
 :emphasize-lines: 5,13-23

    -
      port: 5443
      ip: "::"
      module: ejabberd_http
    #  tls: true
      request_handlers:
        "/admin": ejabberd_web_admin
        "/api": mod_http_api
        "/bosh": mod_bosh
        "/captcha": ejabberd_captcha
        "/upload": mod_http_upload
        "/ws": ejabberd_http_ws
    #-
    #  port: 5280
    #  ip: "::"
    #  module: ejabberd_http
    #  request_handlers:
    #    "/admin": ejabberd_web_admin
    #-
    #  port: 1883
    #  ip: "::"
    #  module: mod_mqtt
    #  backlog: 1000

Add your admin user:

.. code-block:: ini
 :emphasize-lines: 2-4

  acl:
    admin:
      user:
        - "admin@isabell.example"
    local:
      user_regexp: ""
    loopback:
      ip:
        - "127.0.0.0/8"
        - "::1/128"

Remove the port from the put_url and provide configuration for mod_http_upload:

.. code-block:: ini
 :emphasize-lines: 2-9

    mod_http_upload:
      put_url: "https://upload.@HOST@/upload"
      file_mode: "0640"
      dir_mode: "2750"
      max_size: 104857600 # 100 MB
      access: local
      thumbnail: false
      docroot: "/home/isabell/ejabberd/upload"
      secret_length: 40

Disable mod_mqtt:

.. code-block:: ini
 :emphasize-lines: 1

    #mod_mqtt: {}

Configure mod_proxy65:

.. code-block:: ini
 :emphasize-lines: 2,4-7

    mod_proxy65:
    #   access: local
      max_connections: 5
      host: "proxy.isabell.example"
      name: "File Transfer Proxy"
      ip: "::"
      port: <port-5>

ejabberd defaults to plain text passwords so the following two lines need to be added to enable scram:

.. code-block:: ini

   auth_method: internal
   auth_password_format: scram


For additional options visit the `ejabberd documentation <https://docs.ejabberd.im/admin/configuration/>`_

Configure web backend
---------------------

.. include:: includes/web-backend.rst

Configure the web backend for the domain ``upload.isabell.example`` to listen on the ejabberd_http port.

.. note::

    ejabberd is listening on  port ``5443``.


Setup daemon
------------

Create ``~/etc/services.d/ejabberd.ini`` with the following content:

.. code-block:: ini

  [program:ejabberd]
  command=%(ENV_HOME)s/opt/ejabberd/sbin/ejabberdctl --config-dir %(ENV_HOME)s/etc/ejabberd foreground
  autostart=yes
  autorestart=yes
  stopasgroup=true
  killasgroup=true
  stopsignal=INT


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Register your administrator user:

.. code-block:: console

   [isabell@stardust ~]$ ejabberdctl register admin isabell.example <password>
   [isabell@stardust ~]$


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check ejabberd's `releases <https://github.com/processone/ejabberd/releases>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop ejabberd`` and repeat the "Installation" step followed by ``supervisorctl start ejabberd`` to restart ejabberd.

.. _Documentation: https://docs.ejabberd.im/
.. _feed: https://github.com/processone/ejabberd/releases.atom

----

Tested with ejabberd 20.03 and Uberspace 7.6.0

.. author_list::
