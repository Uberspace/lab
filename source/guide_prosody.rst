.. highlight:: console
.. author:: Arian Malek <https://fetziverse.de>
.. author:: fapsi

.. tag:: Instant Messaging
.. tag:: Jabber
.. tag:: XMPP

.. sidebar:: Logo

  .. image:: _static/images/prosody.svg
      :align: center

#######
Prosody
#######

.. tag_list::

Prosody_ is a modern XMPP communication server. It aims to be easy to set up and configure, and efficient with system resources. Additionally, for developers it aims to be easy to extend and give a flexible system on which to rapidly develop added functionality, or prototype new protocols.

XMPP is an open and free alternative to commercial messaging and chat providers. Set it up for your company, organization, or just your family and friends. You are in control, and your communication is private to you. Supporting a wide range of client software for desktop and mobile platforms, you can chat using Prosody from any device.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`HTTPS <web-https>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`

This guide is based on the initial `pull request`_ from fapsi_.

License
=======

Prosody is open source software under the permissive MIT/X11 license.

Prerequisites
=============

Web domain
----------

.. note:: Keep in mind that since you can't create DNS records for ``.uber.space`` domains, you'll need your own domain like ``example.org``. To understand and setup the domains easier I use the following (recommended) subdomains:

 * ``xmpp.example.org``
 * ``conference.example.org``
 * ``upload.example.org``

Your domain ``example.org`` and subdomains ``conference.example.org``, ``upload.example.org`` and ``xmpp.example.org`` needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 example.org
 conference.example.org
 upload.example.org
 xmpp.example.org
 [isabell@stardust ~]$

Uberspace creates certificates automatically when a domain is first seen by the webserver. Trigger the generation for each one with the following command:

::

 [isabell@stardust ~]$ curl --silent --head https://example.org | head -n 1
 [...]
 [isabell@stardust ~]$ curl --silent --head https://conference.example.org | head -n 1
 [...]
 [isabell@stardust ~]$ curl --silent --head https://upload.example.org | head -n 1
 [...]
 [isabell@stardust ~]$ curl --silent --head https://xmpp.example.org | head -n 1
 [...]
 [isabell@stardust ~]$

This will return ``HTTP/1.1 200 OK`` or something similar accordingly your webserver configuration.

Ports
-----

.. note:: You need to open ports for the following connections. For the next steps I use the highlighted shortcuts:

 * ``C2S``: client to server
 * ``S2S``: server to server
 * ``FILEUPLOAD``: file upload over the module **http_upload**

.. include:: includes/open-port.rst

Configure DNS records
---------------------

Your DNS needs to be setup with the following values:

+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|                    name                  |   ttl  | class |   type | priority | weight |    port  |       target     |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|                 example.org              |   3600 |    IN |    A   |          |        |          | 192.0.2.42       |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|                 example.org              |   3600 |    IN |   AAAA |          |        |          | 2001:db8::42:42  |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|          conference.example.org          |   3600 |    IN | CNAME  |          |        |          |     example.org  |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|             upload.example.org           |   3600 |    IN | CNAME  |          |        |          |     example.org  |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|              xmpp.example.org            |   3600 |    IN |    A   |          |        |          | 192.0.2.42       |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|              xmpp.example.org            |   3600 |    IN |  AAAA  |          |        |          | 2001:db8::42:42  |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|        _xmpp-client._tcp.example.org     | 18000  |    IN |   SRV  |      0   |     5  | C2S-PORT | xmpp.example.org |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
|        _xmpp-server._tcp.example.org     | 18000  |    IN |   SRV  |      0   |     5  | S2S-PORT | xmpp.example.org |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
| _xmpp-server._tcp.conference.example.org | 18000  |    IN |   SRV  |      0   |     5  | S2S-PORT | xmpp.example.org |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+
| _xmpp-server._tcp.upload.example.org     | 18000  |    IN |   SRV  |      0   |     5  | S2S-PORT | xmpp.example.org |
+------------------------------------------+--------+-------+--------+----------+--------+----------+------------------+

Configure luarocks
------------------

Prosody is written in ``lua`` and has some runtime dependencies which we install with the package manager ``luarocks``. In order to run the installed packages we have to adapt the path-variable in ``~/.bash_profile``:

::

 PATH=$HOME/.luarocks/bin:$PATH

 export PATH

Additionally we need to provide the paths ``LUA_PATH`` as well as ``LUA_CPATH`` and have to reload to use ``luarocks`` accordingly:

::

 [isabell@stardust ~]$ echo 'eval "$(luarocks path)"' >> ~/.bash_profile
 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

Install runtime lua-dependencies
--------------------------------

.. note:: We are using ``luaexpat`` in the version ``1.3.0-1`` due of an `known issue`_ with the newer versions.

The following dependencies_ (``luasocket``, ``luaexpat``, ``luafilesystem`` and ``luasec``) are required:

::

 [isabell@stardust ~]$ luarocks install luasocket --local
 luasocket [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luaexpat 1.3.0-1 --local
 luaexpat [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luafilesystem --local
 luafilesystem [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luasec --local
 luasec [...] is now built and installed in [...]
 [isabell@stardust ~]$

Further optional ones (``luadbi-mysql``, ``luabitop`` and ``luaevent``) can be installed with these commands:

::

 [isabell@stardust ~]$ luarocks install luadbi-mysql --local MYSQL_BINDIR="/usr/bin" MYSQL_INCDIR="/usr/include/mysql" MYSQL_LIBDIR="/usr/lib64"
 luadbi [...] is now built and installed in [...]
 luadbi-mysql [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luabitop --local
 luabitop [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luaevent --local
 luaevent [...] is now built and installed in [...]
 [isabell@stardust ~]$

.. note:: The variables ``*_BINDIR`` ``*__INCDIR`` and ``*_LIBDIR`` are necessary for correct linking the associated library because CentOS uses a different layout for those files than luarocks expects!

To list the installed packages with their versions use the command ``luarocks list``.

MySQL
-----

.. include:: includes/my-print-defaults.rst

Create a database for prosody:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_prosody"
 [isabell@stardust ~]$

Installation
============

.. note:: Check out the latest stable release on https://prosody.im/downloads/source/. We'll set a temporary environment variable for this session to handle it more easier with the version number in the files and directories.

Download and extract the latest stable release from source into ``~/var/lib/prosody/``:

::

 [isabell@stardust ~]$ VERSION=0.11.5
 [isabell@stardust ~]$ wget https://prosody.im/downloads/source/prosody-$VERSION.tar.gz --directory-prefix=$HOME/var/lib/prosody
 [...]
 [isabell@stardust ~]$ tar --extract --gzip --file=$HOME/var/lib/prosody/prosody-$VERSION.tar.gz --directory=$HOME/var/lib/prosody
 [isabell@stardust ~]$ rm ~/var/lib/prosody/prosody-$VERSION.tar.gz
 [isabell@stardust ~]$

Configure, build and install prosody:

::

 [isabell@stardust ~]$ cd ~/var/lib/prosody/prosody-$VERSION
 [isabell@stardust prosody-0.11.5]$ ./configure --ostype=linux --prefix=$HOME --with-lua-include=/usr/include
 Lua version detected: 5.1
 Lua interpreter found: /usr/bin/lua...
 Checking Lua includes... lua.h found in /usr/include/lua.h
 Checking if Lua header version matches that of the interpreter... yes
 Writing configuration...

 Installation prefix: /home/isabell
 Prosody configuration directory: /home/isabell/etc/prosody
 Using Lua from: /usr

 Done. You can now run 'make' to build.

 [isabell@stardust prosody-0.11.5]$ make
 [...]
 [isabell@stardust prosody-0.11.5]$ make install
 [...]
 [isabell@stardust prosody-0.11.5]$

Configuration
=============

Generate SSL dhparam file
-------------------------

.. note:: This is going to take a long time! You can start configuring the server while it runs, but don't start it yet.

To improve the security you can generate a Diffie–Hellman parameter file with ``openssl``:

::

 [isabell@stardust ~]$ openssl dhparam -out ~/etc/prosody/certs/dhparam-4096.pem 4096
 [...]
 [isabell@stardust ~]$

Install modules
---------------

Create the directory ``~/var/lib/prosody/http_upload``  for the module ``http_upload`` which let clients upload files over HTTP. Additionally download the latest available community plugins:

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/var/lib/prosody/http_upload
 [isabell@stardust ~]$ hg clone https://hg.prosody.im/prosody-modules/ ~/var/lib/prosody/prosody-modules
 [isabell@stardust ~]$

Configure prosody
-----------------

Then there are many settings which should be edited accordingly in ``~/etc/prosody/prosody.cfg.lua``. You'll find a explanation of the config file under the `example configuration file`_ from Prosody.

Additionally I recommend the ssl ciphers and options to reach a high security score. You can check it over the `IM Observatory`_.

.. note:: Make sure to adapt ``VirtualHost "localhost"`` with your domain.

Uncomment the modules ``mam`` and ``csi_simple``. Also add / adapt the following lines in your ``prosody.cfg.lua``:

.. code-block:: lua

 ---------- Server-wide settings ----------
 admins = { "isabell@example.org" }
 plugin_paths = { "/home/isabell/var/lib/prosody/prosody-modules" }
 modules_enabled = {
   "mam"; -- Store messages in an archive and allow users to access it
   "csi_simple"; -- Simple Mobile optimizations
 c2s_ports = { C2S-PORT }
 s2s_secure_auth = true
 s2s_ports = { S2S-PORT }
 s2s_timeout = 300
 ssl = {
   dhparam = "/home/isabell/etc/prosody/certs/dhparam-4096.pem";
   cafile = "/etc/pki/tls/certs/ca-bundle.trust.crt";
   ciphers = "EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA384:EECDH+ECDSA+SHA256:EECDH+aRSA+SHA384:EECDH+aRSA+SHA256:EECDH:EDH+aRSA:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS:!RC4:!SEED:!AES128:!CAMELLIA128";
   options = { "no_sslv2", "no_sslv3", "no_tlsv1"; "no_ticket", "no_compression", "cipher_server_preference", "single_dh_use", "single_ecdh_use" };
 }
 pidfile = "/home/isabell/var/lib/prosody/prosody.pid";
 daemonize = false;
 storage = "sql"
 sql = {
   driver = "MySQL",
   database = "isabell_prosody",
   username = "isabell",
   password = "MySuperSecretPassword",
   host = "localhost"
 }
 log = { info = "*console" }
 certificates = "/home/isabell/etc/certificates/"
 https_certificate = "/home/isabell/etc/certificates/upload.example.org.crt"
 http_ports = { }
 https_ports = { FILEUPLOAD-PORT }

 ----------- Virtual hosts -----------
 VirtualHost "example.org"
 Component "conference.example.org" "muc"
   modules_enabled = { "muc_mam", "vcard_muc" }
 Component "upload.example.org" "http_upload"
   http_upload_file_size_limit = 10485760
   http_upload_expire_after = 2419200

.. warning:: Replace the placeholders ``C2S-PORT``, ``S2S-PORT`` and ``FILEUPLOAD-PORT`` with the above obtained ports, adapt the domain-names, sql settings (inclusive username and password) and paths! Don't delete, omit or change the ordering of the entries, otherwise some default ports could be spammed. Also don't active modules which including module ``http`` without changing ``http_ports`` and ``https_ports`` . Last but not least be warned that spamming the default ports which could already be in use can lead to fork-spam issues! So be careful and watch your configuration twice and look into the prosody logs afterwards to verify whats going on after starting prosody!

Setup daemon
============

Place the file ``prosody.ini`` in ``~/etc/services.d/`` and adapt it accordingly:

.. code-block:: ini

 [program:prosody]
 command=/bin/bash -c "source %(ENV_HOME)s/.bash_profile && prosody"
 autostart=yes
 autorestart=yes
 startretries=1
 stopasgroup=true
 killasgroup=true
 stopsignal=INT

.. include:: includes/supervisord.rst

Finishing installation
======================

Create your first user:

.. code-block:: console
 :emphasize-lines: 1-3

 [isabell@stardust ~]$ prosodyctl adduser isabell@example.org
 Enter new password:
 Retype new password:
 [isabell@stardust ~]$

Voice/Video calls
=================

In order to enable voice/video calls a TURN and STUN server for NAT traversal is required. coturn_ is supported by prosody.

First install coturn according to `coturn lab guide`_ and note listening port ``<port-1>`` as well as ``static-auth-secret``.

To enable coturn, it must be configured as `external service`_ in ``prosody.cfg.lua``:

.. code-block:: lua
 :emphasize-lines: 11,16,17

 modules_enabled = {
     -- other modules ...
     "external_services"
 }

 external_services = {
     {
         type = "stun",
         transport = "udp",
         host = "isabell.uber.space",
         port = <port-1>
     }, {
         type = "turn",
         transport = "udp",
         host = "isabell.uber.space",
         port = <port-1>,
         secret = "<YOUR_SUPER_LONG_SUPER_SECRET_STATIC_PASSPHRASE>"
     }
 }


Updates
=======

.. note:: Check the `update feed`_ regularly to stay informed about the newest version.

For updates simply repeat the steps described in the Installation_ part:

::

 [isabell@stardust ~]$ VERSION=X.XX.X
 [isabell@stardust ~]$ wget https://prosody.im/downloads/source/prosody-$VERSION.tar.gz --directory-prefix=$HOME/var/lib/prosody
 [...]
 [isabell@stardust ~]$ tar --extract --gzip --file=$HOME/var/lib/prosody/prosody-$VERSION.tar.gz --directory=$HOME/var/lib/prosody
 [isabell@stardust ~]$ rm ~/var/lib/prosody/prosody-$VERSION.tar.gz
 [isabell@stardust ~]$ cd ~/var/lib/prosody/prosody-$VERSION
 [isabell@stardust prosody-X.XX.X]$ ./configure --ostype=linux --prefix=$HOME --with-lua-include=/usr/include
 Lua version detected: 5.1
 Lua interpreter found: /usr/bin/lua...
 Checking Lua includes... lua.h found in /usr/include/lua.h
 Checking if Lua header version matches that of the interpreter... yes
 Writing configuration...

 Installation prefix: /home/isabell
 Prosody configuration directory: /home/isabell/etc/prosody
 Using Lua from: /usr

 Done. You can now run 'make' to build.

 [isabell@stardust prosody-X.XX.X]$ make
 [...]
 [isabell@stardust prosody-X.XX.X]$ make install
 [...]
 [isabell@stardust prosody-X.XX.X]$ supervisorctl restart prosody
 [isabell@stardust prosody-X.XX.X]$

Update the community prosody modules:

::

 [isabell@stardust ~]$ cd ~/var/lib/prosody/prosody-modules
 [isabell@stardust prosody-modules]$ hg pull --update
 pulling from https://hg.prosody.im/prosody-modules/
 [...]
 [isabell@stardust prosody-modules]$

XMPP Clients
============

As a personal note I want to recommend following XMPP clients:

* Gajim_ for Linux / Windows.
* Conversations_ for Android.
* Siskin_ for iOS.

----

Tested with Prosody 0.11.5, Uberspace 7.7.1.2

.. _prosody: https://prosody.im
.. _pull request: https://github.com/Uberspace/lab/pull/435
.. _fapsi: https://github.com/fapsi
.. _dns: https://prosody.im/doc/dns
.. _known issue: https://issues.prosody.im/1375
.. _dependencies: https://prosody.im/doc/depends
.. _IM Observatory: https://xmpp.net
.. _example configuration file: https://prosody.im/doc/example_config
.. _update feed: https://blog.prosody.im/index.xml
.. _coturn: https://prosody.im/doc/coturn
.. _`coturn lab guide`: https://lab.uberspace.de/guide_coturn.html
.. _`external service`: https://prosody.im/doc/modules/mod_external_services
.. _Gajim: https://gajim.org
.. _Conversations: https://conversations.im
.. _Siskin: https://siskin.im

.. author_list::
