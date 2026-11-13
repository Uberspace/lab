.. highlight:: console

.. author:: Lomion

.. tag:: VoIP
.. tag:: chat
.. tag:: matrix
.. tag:: synapse

.. sidebar:: Logo

  .. image:: _static/images/matrix-logo.svg
      :align: center

#######
Element Call a.k.a. MatrixRTC
#######

.. tag_list::

Element Call a.k.a. MatrixRTC (https://github.com/element-hq/element-call) is a decentralized and federated video conferencing solution as an extention for the Matrix protocol.
This description is based on the Self-Hosting Guide for Element Call (https://github.com/element-hq/element-call/blob/livekit/docs/self_hosting.md).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`opening ports <basics-ports>`

License
=======

All relevant legal information can be found here

  * https://github.com/element-hq/element-call/blob/livekit/LICENSE-AGPL-3.0
  * https://github.com/livekit/livekit/blob/master/LICENSE
  * https://github.com/element-hq/lk-jwt-service/blob/main/LICENSE

Prerequisites
=============

Web domain
----------

.. note:: Keep in mind that since you can't create DNS records for ``.uber.space`` domains, you'll need your own domain like ``matrixrtc.example.eu``.

 * ``matrixrtc.example.eu``

Web domain
----------

A working Matrix backend e.g. Synapse (see the respetive article in the Uberspace lab) is needed as a prerequisite for this HOWTO.
Changes to the backend configuration is not covered in this article. Look at the self-hosting guide as mentioned above.

External ports
--------------

The WebRTC media is handled directly through externaly accessable ports. For this purpose you need to expose 1 port for TCP connections and several ports for UDP media connections.
In Uberspace (7 ... not 8 yet) you can request up to 20 external ports. The more ports you have the more parallel connections are possible.
Note: In WebRTC usually several ports are used and propagated in the connection setup and then freed if not selected by the clients.

.. code-block:: console
  :emphasize-lines: 1,2,8,18
  
  [isabell@stardust ~]$ uberspace port add
  Port 40130 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$ uberspace port add
  Port 40131 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$ uberspace port add
  Port 40132 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$ uberspace port add
  Port 40133 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$ uberspace port add
  Port 40134 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$ uberspace port add
  Port 40135 will be open for TCP and UDP traffic in a few minutes.  
  [isabell@stardust ~]$  

Installation & Configuration
============================

To install Element call two components will be installed:
 * LiveKit
 * LiveKit JWT Service
 
LiveKit
-------
.. code-block:: console
  :emphasize-lines: 1,2,8,18

  [isabell@stardust ~]$ mkdir -p ~/livekit
  [isabell@stardust ~]$ https://github.com/livekit/livekit/releases/download/v1.13.4/livekit_1.13.4_linux_amd64.tar.gz
  [isabell@stardust ~]$ tar xf livekit_1.13.4_linux_amd64.tar.gz
  [isabell@stardust ~]$ ls
  LICENSE  livekit_1.13.4_linux_amd64.tar.gz  livekit-server
  [isabell@stardust ~]$

Next create a configuration file as ~/livekit/livekit.yaml

.. code-block:: yaml
  :emphasize-lines: 4

  port: 7880
  bind_addresses:
    - "0.0.0.0"
  rtc:
    tcp_port: 40130
    port_range_start: 40131
    port_range_end: 40135
    use_external_ip: true
    advertise_internal_ip: false
  logging:
    level: info
  turn:
    enabled: false
    domain: turn.example.eu 
    tls_port: 5349
    external_tls: true
    relay_range_start: 50180
    relay_range_end: 50200
  keys:
    anygeneratedkey: "anygeneratedsecuresecret"
  room:
    auto_create: false

Finally we create a supervisurd file and start the service

.. code-block:: ini

  [program:livekit]
  command=/home/isabell/livekit/livekit-server --config /home/isabell/livekit/livekit.yaml
  startsecs=15

.. include:: includes/supervisord.rst

LiveKit JWT Service
-------------------
.. code-block:: console
  :emphasize-lines: 1,2,8,18

  [isabell@stardust ~]$ mkdir -p ~/lk-jwt-service
  [isabell@stardust ~]$ https://github.com/element-hq/lk-jwt-service/releases/download/v0.5.0/lk-jwt-service_linux_amd64
  [isabell@stardust ~]$ ls
  lk-jwt-service_linux_amd64
  [isabell@stardust ~]$

The configuration is done by using environment variables.
TODO: Change this to use files.

So we create a supervisurd file and start the service

.. code-block:: ini

  [program:lk-jwt-service]
  command=/home/isabell/lk-jwt-service/lk-jwt-service_linux_amd64
  environment=LIVEKIT_URL="https://matrixrtc.example.eu/livekit/sfu",LIVEKIT_KEY="anygeneratedkey",LIVEKIT_SECRET="anygeneratedsecuresecret",LIVEKIT_FULL_ACCESS_HOMESERVERS="matrix.example.eu"
  startsecs=20

.. include:: includes/supervisord.rst

Web Backend
-----------

Now we have to make our Element Call services accessable from the internet (beside the opened port for media we already opened before) through the web backend.

.. code-block:: console
  :emphasize-lines: 1,2,8,18
  
  [isabell@stardust ~]$ uberspace web backend set matrixrtc.example.eu/livekit/jwt --http -- port 8080 --remove-prefix
  [isabell@stardust ~]$ uberspace web backend set matrixrtc.example.eu/livekit/sfu --http --port 7880 --remove-prefix
  [isabell@stardust ~]$

Note: Don't forget to add the --remove-prefix parameter

Test
====

In order to verify your configuration use the testmatrix tool (https://codeberg.org/spaetz/testmatrix).

.. code-block:: console
  :emphasize-lines: 1,2,8,18
  
  [isabell@stardust ~]$ pip3.14 install testmatrix
  [isabell@stardust ~]$ testmatrix -u myuser -p mytokenreceivedfromaactivematrixsession example.eu
  Testing server matrix.example.eu
    Federation url: https://matrix.example.eu:8448
  ✔ Server well-known exists
  ✔ Client well-known has proper CORS header
    Client url: https://matrix.example.eu
    Adding livekit service URL: https://matrixrtc.example.eu/livekit/jwt
  ✔ Server version: Synapse (1.157.1)
  ✔ Federation API endpoints seem to work fine
  ✔ Client API endpoints seem to work fine
  ✔ Server oauth metadata endpoint exists
  ✔ QR code login is enabled (MSC 4108)
    Public room directory is disabled
  ✔ MatrixRTC SFU configured
    JWTauth healtz url: https://matrixrtc.example.eu/livekit/jwt
  ✔ JWTauth healthz responds
  ✔ jwt /get_token without auth returns 405, good.
  ✔ /get_token succeeded. Use the below information to test your livekit SFU on https://livekit.io/connection-test
    {"url":"https://matrixrtc.example.eu/livekit/sfu","jwt":"verylongjwttoken"}
  ✔ MatrixRTC configured and delayed events work
  ✔ Room summaries (MSC3266) (unstable) support
  ✔ Direct registration and guest access forbidden per se 👍

Note: You have to use the URL of the Matrix backend. Do not use matrixrtc.example.eu here.

Updates
=======

Update the binaries in ~/livekit/ and ~/lk-jwt-service/

Tested on Uberspace 7.17.4 on synapse 1.157.1, Livekit 1.13.4 and Livekit-JWT-Service 0.5.0

----

.. author_list::
