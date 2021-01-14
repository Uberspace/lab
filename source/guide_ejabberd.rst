.. author:: fm0de
.. author:: jo-mei
.. author:: coderkun

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
  * :manual:`web headers <web-headers>`
  * :manual:`MySQL <database-mysql>`

This guide is based on the initial `pull request <https://github.com/Uberspace/lab/pull/444>`_ from `fm0de <https://github.com/fm0de>`_ and the `work from clerie <https://blog.clerie.de/ejabberd-auf-uberspace-installieren/>`_.


Installation
============

Download, configure, compile and install ejabberd.
Use the following options for ``./configure``:

  * ``--prefix=$HOME/``: Install to your personal uberspace
  * ``--enable-user=$USER``: Allow execution of ejabberd as $USER
  * ``--enable-mysql --enable-new-sql-schema``: optionally compile with mysql support and use the new schema

Run ``./configure --help`` to see all options.

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/processone/ejabberd/archive/20.04.tar.gz
  [isabell@stardust ~]$ tar xf 20.04.tar.gz
  [isabell@stardust ~]$ cd ejabberd-20.04/
  [isabell@stardust ejabberd-20.04]$ ./autogen.sh
  [isabell@stardust ejabberd-20.04]$ ./configure --enable-user=$USER --prefix=$HOME --enable-mysql --enable-new-sql-schema
  [isabell@stardust ejabberd-20.04]$ make
  [isabell@stardust ejabberd-20.04]$ make install

The files will be installed to the following locations:

  * ``~/sbin/``: executables (``ejabberdctl``)
  * ``~/etc/ejabberd/``: configuration files (mainly ``ejabberd.yml``)
  * ``~/var/lib/ejabberd/``: runtime files including internal mnesia database
  * ``~/var/log/ejabberd/``: logfiles


Basic Configuration
===================

A standard config file is provided at ``~/etc/ejabberd/ejabberd.yml``. Adjust
it with correct settings as explained in the next sections.

This section covers only the basic configuration to get ejabberd up and running.
See below for additional security and configuration best practices. Any option
that is not covered here can be found at the `ejabberd documentation <https://docs.ejabberd.im/admin/configuration/>`_.

Domains
-------

Your ejabberd domain ``isabell.example`` needs to be setup. We will additionally
use the following subdomains:

  * ``conference.isabell.example``: Multi-user chat rooms
  * ``proxy.isabell.example``: File transfer proxy
  * ``pubsub.isabell.example``: PubSub
  * ``xmpp.isabell.example``: Web-based features like file uploads and web sockets

Run the following commands to register the domains:

.. code-block:: console

 [isabell@stardust ~]$ uberspace web domain add isabell.example
 [isabell@stardust ~]$ uberspace web domain add conference.isabell.example
 [isabell@stardust ~]$ uberspace web domain add proxy.isabell.example
 [isabell@stardust ~]$ uberspace web domain add pubsub.isabell.example
 [isabell@stardust ~]$ uberspace web domain add xmpp.isabell.example

Change the host configuration to listen for your domain:

.. code-block:: ini
 :emphasize-lines: 2

  hosts:
    - "isabell.example"

TLS Certificates
--------------------

We also need the TLS certificates which are fetched by Uberspace when visiting
the domains, either in a browser or by running the following commands:

.. code-block:: console

 [isabell@stardust ~]$ curl https://isabell.example
 [isabell@stardust ~]$ curl https://conference.isabell.example
 [isabell@stardust ~]$ curl https://proxy.isabell.example
 [isabell@stardust ~]$ curl https://pubsub.isabell.example
 [isabell@stardust ~]$ curl https://xmpp.isabell.example

Provide location of your keys and certificates:

.. code-block:: ini
 :emphasize-lines: 2-11

  certfiles:
    - "/home/isabell/etc/certificates/isabell.example.crt"
    - "/home/isabell/etc/certificates/isabell.example.key"
    - "/home/isabell/etc/certificates/conference.isabell.example.crt"
    - "/home/isabell/etc/certificates/conference.isabell.example.key"
    - "/home/isabell/etc/certificates/proxy.isabell.example.crt"
    - "/home/isabell/etc/certificates/proxy.isabell.example.key"
    - "/home/isabell/etc/certificates/pubsub.isabell.example.crt"
    - "/home/isabell/etc/certificates/pubsub.isabell.example.key"
    - "/home/isabell/etc/certificates/xmpp.isabell.example.crt"
    - "/home/isabell/etc/certificates/xmpp.isabell.example.key"

Disable ACME to avoid ejabberd logging a warning:

.. code-block:: ini

  acme:
    auto: false

Firewall Ports
--------------

In the basic configuration ejabberd needs five open ports: two for
client-to-server (c2s), two for server-to-server (s2s), and one for the file
transfer proxy. HTTP connections are handled by a web backend.

.. include:: includes/open-port.rst

Change the port numbers to the opened ports:

.. code-block:: ini
 :emphasize-lines: 3,8,14,19

  listen:
    - # c2s
      port: <port-1>
      ip: "::"
      module: ejabberd_c2s
      …
    - # 'secure' c2s
      port: <port-2>
      ip: "::"
      module: ejabberd_c2s
      tls: true
      …
    - # s2s
      port: <port-3>
      ip: "::"
      module: ejabberd_s2s_in
      …
    - # 'secure' s2s
      port: <port-4>
      ip: "::"
      module: ejabberd_s2s_in
      tls: true
      …

DNS Records
---------------
Since standard ports cannot be used on Uberspace DNS records must be set for c2s
and s2s connections. Refer to the `XMPP wiki <https://wiki.xmpp.org/web/SRV_Records>`_
for setup and point them to the corresponding ports.

::

 _xmpp-client._tcp.isabell.example. 86400 IN SRV 5 0 <port-1> isabell.example.
 _xmpps-client._tcp.isabell.example. 86400 IN SRV 4 0 <port-2> isabell.example.
 _xmpp-server._tcp.isabell.example. 86400 IN SRV 5 0 <port-3> isabell.example.
 _xmpps-server._tcp.isabell.example. 86400 IN SRV 4 0 <port-4> isabell.example.

File Transfer Proxy
-------------------

Configure ``mod_proxy65`` by setting the ``host`` and ``port`` values:

.. code-block:: ini
  :emphasize-lines: 6,9

  modules:
    …
    mod_proxy65:
      access: local
      max_connections: 5
      host: "proxy.isabell.example"
      name: "File Transfer Proxy"
      ip: "::"
      port: <port-5>
    …

Web-based Features
------------------

For web-based features like file uploads and web sockets adjust the
configuration to listen on port 5443 without TLS:

.. code-block:: ini
  :emphasize-lines: 7

  listen:
    …
    -
      port: 5443
      ip: "::"
      module: ejabberd_http
      #tls: true
      request_handlers:
        "/admin": ejabberd_web_admin
        "/api": mod_http_api
        "/bosh": mod_bosh
        "/captcha": ejabberd_captcha
        "/upload": mod_http_upload
        "/ws": ejabberd_http_ws
    …

Additionally create a web-backend for ``xmpp.isabell.example/`` on port 5443.

.. include:: includes/web-backend.rst

HTTP File Upload
----------------

Configure the ``put_url`` and the ``doc_root`` settings for ``mod_http_upload``
to match the domain and your user folder:

.. code-block:: ini
  :emphasize-lines: 4,10

  modules:
    …
    mod_http_upload:
      put_url: "https://xmpp.@HOST@/upload"
      file_mode: "0640"
      dir_mode: "2750"
      max_size: 104857600 # 100 MB
      access: local
      thumbnail: false
      docroot: "/home/isabell/ejabberd/uploads"
      secret_length: 40
   …

Password Hashing
----------------

ejabberd defaults to plain text passwords so the following two lines need to be
added to enable ``scram``:

.. code-block:: ini

   auth_method: internal
   auth_password_format: scram

Reduce Loglevel
---------------

By default ejabberd does verbose logging. This can be useful for testing
different configuration options. When taking your ejabberd instance to
production you can reduce the logging by setting the loglevel to ``warning``:

.. code-block:: ini

  loglevel: warning

Admin User
----------

Configure your admin user (which will be created later):

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

MQTT
----

Disable MQTT by commenting out the listener for module ``mod_mqtt``:

.. code-block:: ini
  :emphasize-lines: 3-7

  listen:
    …
    #-
    #  port: 1883
    #  ip: "::"
    #  module: mod_mqtt
    #  backlog: 1000
    …

Additionally comment out the module itself:

.. code-block:: ini
  :emphasize-lines: 3

  modules:
    …
    #mod_mqtt: {}
    …

MySQL
-----

For a production server it is recommended to store users, messages and data of
other modules in a MySQL database instead of the mnesia database. To use MySQL
make sure to include the corresponding options during compilation.

.. include:: includes/my-print-defaults.rst

Create an :manual_anchor:`additional database <database-mysql.html#additional-databases>`
with the name ``isabell_ejabberd`` and import the new database schema:

.. code-block:: console

  [isabell@local ~]$ mysql isabell_ejabberd < ~/ejabberd-20.04/sql/mysql.new.sql

Configure ejabberd to use the MySQL database:

.. code-block:: ini

  sql_type: mysql
  sql_server: "localhost"
  sql_database: "isabell_ejabberd"
  sql_username: "isabell"
  sql_password: "MySuperSecretPassword"
  sql_pool_size: 5
  default_db: sql

Additionally adjust the configuration of the proxy65 module:

.. code-block:: ini
  :emphasize-lines: 7

  module:
    …
    mod_proxy65:
      …
      name: "File Transfer Proxy"
      …
      ram_db_type: sql
      …
    …


Compliance Configuration
========================

The following configuration settings are not needed for basic operation but
are required to pass the `Compliance Test <https://compliance.conversations.im/>`_.
It is based on ProcessOne’s blog post
`How to configure ejabberd to get 100% in XMPP compliance test <https://www.process-one.net/blog/how-to-configure-ejabberd-to-get-100-in-xmpp-compliance-test/>`_.

HTTP File Upload: CORS
----------------------

As specified in XEP-0363 the Cross-Origin Request Sharing (CORS) header needs to
be set for HTTP file upload. This can be done by adding the following web
headers:

::

  Access-Control-Allow-Headers: Content-Type
  Access-Control-Allow-Methods: GET,HEAD,PUT,OPTIONS
  Access-Control-Allow-Origin: https://xmpp.isabell.example

Contact Addresses
-----------------

As specified in XEP-0157 configure a contact addresses for abuse of the service:

.. code-block:: ini
  :emphasize-lines: 3-9

  modules:
    …
    mod_disco:
      server_info:
        -
          modules: all
          name: "abuse-addresses"
          urls:
            - "mailto:abuse@isabell.example"
    …

If you like, do the same for the names “support-addresses” and
“admin-addresses”.

Alternative Connection Methods
-----------------------------------

XEP-0156 defines the discovering of alternative XMPP connection methods which
refer to the HTTP-based features BOSH and web sockets. To pass this compliance
test two steps are required.

First, create the following DNS record:

::

  _xmppconnect TXT [ _xmpp-client-websocket=wss://xmpp.isabell.example:443/ws ] 3600

Second, create the file ``~/html/.well-known/host-meta`` with the following
content:

.. code-block:: xml

  <?xml version='1.0' encoding='utf-8'?>
  <XRD xmlns='http://docs.oasis-open.org/ns/xri/xrd-1.0'>
      <Link rel="urn:xmpp:alt-connections:xbosh" href="https://xmpp.isabell.example/bosh" />
      <Link rel="urn:xmpp:alt-connections:websocket" href="wss://xmpp.isabell.example/ws" />
  </XRD>

And create the file ``~/html/.well-known/host-meta.json`` with the following
content:

.. code-block:: json

  {
    "links": [
      {
        "rel": "urn:xmpp:alt-connections:xbosh",
        "href": "https://xmpp.isabell.example/bosh"
      },
      {
        "rel": "urn:xmpp:alt-connections:websocket",
        "href": "wss://xmpp.isabell.example/ws"
      }
    ]
  }

STUN Server
-----------

ejabberd has built-in support for STUN and TURN. First, open two new firewall ports.

.. include:: includes/open-port.rst

Next, add the following DNS records:

::

  _stun._udp SRV 0 <port-6> isabell.example 3600
  _stun._tcp SRV 0 <port-6> isabell.example 3600
  _stuns._tcp SRV 0 <port-7> isabell.example 3600

Finally configure the ``mod_stun_disco`` module:

.. code-block:: ini
  :emphasize-lines: 8,14,20

  modules:
    …
    mod_stun_disco:
      credentials_lifetime: 12h
      services:
        -
          host: "@HOST@"
          port: <port-6>
          transport: udp
          type: stun
          restricted: true
        -
          host: "@HOST@"
          port: <port-6>
          transport: tcp
          type: stun
          restricted: true
        -
          host: "@HOST@"
          port: <port-7>
          transport: tcp
          type: stuns
          restricted: true


Security Configuration
======================

The following configuration settings are not needed for basic operation but
improve the security of your server.

Sensitive Data
--------------

To hide sensitive data like IP addresses from logfiles add the following line
to the configuration file:

.. code-block:: ini

  hide_sensitive_log_data: true

Admin Interface
---------------

By default the the web-based admin interface is publicly available together
with the other web-based features on port 5443. For better security it is
recommended to run it on a separate port that is not exposed to the public.

To do this, comment out the ``/admin`` route on the HTTP listener:

.. code-block:: ini
  :emphasize-lines: 9

  listen:
    …
    -
      port: 5443
      ip: "::"
      module: ejabberd_http
      tls: false
      request_handlers:
        #/admin: ejabberd_web_admin
        /api: mod_http_api
        /bosh: mod_bosh
        /captcha: ejabberd_captcha
        /upload: mod_http_upload
        /ws: ejabberd_http_ws
    …

Add a separate listener on a different port (e.g. 5280):

.. code-block:: ini
  :emphasize-lines: 3-8

  listen:
    …
    -
      port: 5280
      ip: "::"
      module: ejabberd_http
      request_handlers:
        /admin: ejabberd_web_admin
    …

The admin interface can then be accessed from your local machine via SSH port
forward:

.. code-block:: console

  [isabell@local ~]$ ssh -L 5280:localhost:5280 isabell@stardust.uber.space -N

File Upload Quota
-----------------

To limit the size of uploaded files add the module ``mod_http_upload_quote``
to the ``modules`` configuration and set the ``max_days`` parameter to an
appropriate value:

.. code-block:: ini
  :emphasize-lines: 3-4

  modules:
    …
    mod_http_upload_quota:
      max_days: 14
    …

Strong TLS Options
------------------

To disable old TLS versions and to use only strong ciphers add the following
top-level configuration options:

.. code-block:: ini

  c2s_protocol_options:
    - "no_sslv3"
    - "no_tlsv1"
    - "no_tlsv1_1"
    - "cipher_server_preference"
    - "no_compression"
  c2s_ciphers: "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"
  s2s_use_starttls: required
  s2s_protocol_options:
    - "no_sslv3"
    - "no_tlsv1"
    - "no_tlsv1_1"
    - "cipher_server_preference"
    - "no_compression"
  s2s_ciphers: "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"

Additionally enforce StartTLS for he c2s listener:

.. code-block:: ini
 :emphasize-lines: 7-8

  listen:
    …
    - # c2s
      port: <port-1>
      ip: "::"
      module: ejabberd_c2s
      starttls: true
      starttls_required: true
    …

OS Version
----------

To stop ejabberd from exposing details about the Operating System adjust the configuration
of the ``mod_version`` module:

.. code-block:: ini
 :emphasize-lines: 3-4

  modules:
    …
    mod_version:
      show_os: false
    …


Startup
======================

The next step is to bring your ejabberd online and start using it.

Setup Daemon
------------

Create a supervisord service by adding the following content to the new file
``~/etc/services.d/ejabberd.ini``:

.. code-block:: ini

  [program:ejabberd]
  command=%(ENV_HOME)s/sbin/ejabberdctl --config-dir %(ENV_HOME)s/etc/ejabberd foreground
  autostart=yes
  autorestart=yes
  stopasgroup=true
  killasgroup=true
  stopsignal=INT

.. include:: includes/supervisord.rst

Administrator User
------------------

Register your administrator user:

.. code-block:: console

   [isabell@stardust ~]$ ~/sbin/ejabberdctl register admin isabell.example <password>


Maintenance
===========

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Backups
-------

Backup the following directories:

  * ``~/etc/ejabberd/``
  * ``~/var/lib/ejabberd/``
  * ``~/var/log/ejabberd/``

If you use MySQL, additionally backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_ejabberd | xz - > ~/isabell_ejabberd.sql.xz

Updates
-------

Check ejabberd's `releases <https://github.com/processone/ejabberd/releases>`_
for the latest version. If a newer version is available, repeat the
“Installation” step, stop the daemon, merge changes on the configuration file
and start the daemon again:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl stop ejabberd
  [isabell@stardust ~]$ nvim -d ~/etc/ejabberd/ejabberd.yml-new ~/etc/ejabberd/ejabberd.yml
  [isabell@stardust ~]$ supervisorctl start ejabberd

Additionally check the release notes for the new version which you will find at
the `upgrade documentation <https://docs.ejabberd.im/admin/upgrade/>`_. Changes
to the database schema are included there as well.

Logfiles
--------

Regularly check the logfiles at ``~/var/log/ejabberd/``, especially
``error.log``.

----

.. _Documentation: https://docs.ejabberd.im/
.. _feed: https://github.com/processone/ejabberd/releases.atom

Tested with ejabberd 20.04 and Uberspace 7.7.0.

.. author_list::
