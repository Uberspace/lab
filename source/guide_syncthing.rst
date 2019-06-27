.. author:: stunkymonkey <http://stunkymonkey.de>

.. tag:: lang-go
.. tag:: sync

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/syncthing.png
      :align: center

#########
Syncthing
#########

.. tag_list::

Syncthing_ replaces proprietary sync and cloud services with something open, trustworthy and decentralized. Your data is your data alone and you deserve to choose where it is stored, if it is shared with some third party and how it's transmitted over the Internet.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Your syncthing URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Like a lot of Go software, Syncthing is distributed as a single binary. Download Syncthing's latests release_,
verify the checksum specified in the respective ``.sha256`` file and finally extract the files.

::

  [isabell@stardust ~]$ mkdir ~/syncthing
  [isabell@stardust ~]$ wget -O syncthing/syncthing.tar.gz https://github.com/syncthing/syncthing/releases/download/v1.1.4/syncthing-linux-amd64-v1.1.4.tar.gz
  --2019-05-30 19:16:10--  https://github.com/syncthing/syncthing/releases/download/v1.1.3/syncthing-linux-amd64-v1.1.3.tar.gz
  Resolving github.com (github.com)... 140.82.118.3
  Connecting to github.com (github.com)|140.82.118.3|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: https://github-production-release-asset-2e65be.s3.amazonaws.com/14712850/0ea39200-71b9-11e9-8b63-1c457246edfa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20190530%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190530T171610Z&X-Amz-Expires=300&X-Amz-Signature=d579bd937f01b31321b38a436e2ea22ef5838fa4f821e4e6a66648f3d4631710&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3Dsyncthing-linux-amd64-v1.1.3.tar.gz&response-content-type=application%2Foctet-stream [following]
  --2019-05-30 19:16:10--  https://github-production-release-asset-2e65be.s3.amazonaws.com/14712850/0ea39200-71b9-11e9-8b63-1c457246edfa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20190530%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190530T171610Z&X-Amz-Expires=300&X-Amz-Signature=d579bd937f01b31321b38a436e2ea22ef5838fa4f821e4e6a66648f3d4631710&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3Dsyncthing-linux-amd64-v1.1.3.tar.gz&response-content-type=application%2Foctet-stream
  Resolving github-production-release-asset-2e65be.s3.amazonaws.com (github-production-release-asset-2e65be.s3.amazonaws.com)... 52.216.162.59
  Connecting to github-production-release-asset-2e65be.s3.amazonaws.com (github-production-release-asset-2e65be.s3.amazonaws.com)|52.216.162.59|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 8690658 (8.3M) [application/octet-stream]
  Saving to: ‘syncthing/syncthing.tar.gz’

  100%[=======================================================================================================================================>] 8,690,658   8.17MB/s   in 1.0s

  2019-05-30 19:16:12 (8.17 MB/s) - ‘syncthing/syncthing.tar.gz’ saved [8690658/8690658]
  [isabell@stardust ~]$ sha256sum syncthing/syncthing.tar.gz
  bb27b94d236276aac87088c554ec30fbecf2478a05f54d4ac23f801144583445 gitea/gitea
  [isabell@stardust ~]$ tar --strip-components=1 -xzf syncthing/syncthing.tar.gz -C syncthing/
  [isabell@stardust ~]$ rm syncthing/syncthing.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Generate the configuration
--------------------------

generate a config start syncthing via

.. code-block:: bash

  [isabell@stardust ~]$ ./syncthing/syncthing -generate=~/.config/syncthing/
  22:56:57 INFO: Device ID: L3M5WQB-ZST2GT2-7OUBKYZ-7XSWWIV-G7MKB54-5OQNXJU-FJP567H-4YUL3QP
  22:56:57 INFO: Default folder created and/or linked to new config
  [isabell@stardust ~]$

Change the configuration
------------------------

Syncthing needs to listen to all interfaces therefore you have to edit ``~/.config/syncthing/config.xml``. Find the following block

.. code-block:: xml

  <gui enabled="true" tls="false" debugging="false">
      <address>127.0.0.1:8384</address>
      <apikey>ruPy5mvncF9J5jixzxUPoioGRtZyoVtY</apikey>
      <theme>default</theme>
  </gui>


and change it to 

.. code-block:: xml
  :emphasize-lines: 2

  <gui enabled="true" tls="false" debugging="false">
      <address>0.0.0.0:8384</address>
      <apikey>ruPy5mvncF9J5jixzxUPoioGRtZyoVtY</apikey>
      <theme>default</theme>
  </gui>

.. note::

  Syncthing provides many other configuration options. Take a look at the Documentation_ to learn more.

Configure web server
--------------------

.. note::

    Syncthing is running on port 8384.

.. include:: includes/web-backend.rst

Setup daemon
------------

To start syncthing automatically and run it in the background, create ``~/etc/services.d/syncthing.ini`` with the following content:

.. code-block:: ini

  [program:syncthing]
  command=%(ENV_HOME)s/syncthing/syncthing

Then, tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 syncthing: available
 [isabell@stardust ~]$ supervisorctl update
 syncthing: added process group
 [isabell@stardust ~]$ supervisorctl status
 syncthing                        RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

.. note::

  If syncthing is not ``RUNNING``, check your configuration and the logs using ``supervisorctl maintail``.

Finishing installation
======================

Add password
------------

.. warning:: Without password everybody in the internet can load files from and to your uberspace account!

To protect the access to your syncthing instance, visit your domain and set a username and password.

Best practice
=============

right now the server will sync with your devices only via a relay-server, wich is not super fast. To improve performance, you can connect directly by opening a port in the firewall

::

 [isabell@stardust ~]$ uberspace port add
 Port 40200 will be open for TCP and UDP treffic in a few minutes.
 [isabell@stardust ~]$

remember this port.

then open ``~/.config/syncthing/config.xml``, find the following block and change it to:

.. code-block:: xml
  :emphasize-lines: 2

  ...
  <options>
      <listenAddress>tcp://:$yourport$</listenAddress>
      <globalAnnounceServer>default</globalAnnounceServer>
      <globalAnnounceEnabled>true</globalAnnounceEnabled>
      <localAnnounceEnabled>true</localAnnounceEnabled>
      <localAnnouncePort>21027</localAnnouncePort>
      <localAnnounceMCAddr>[ff12::8384]:21027</localAnnounceMCAddr>
  ...


Updates
=======

.. note:: Syncthing is updating automatically.

.. _Syncthing: https://syncthing.net/
.. _Documentation: https://docs.syncthing.net/
.. _release: https://github.com/syncthing/syncthing/releases/latest

----

Tested with Syncthing 1.1.3, Uberspace 7.2.14.0

.. author_list::
