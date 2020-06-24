.. highlight:: console
.. author:: Arian Malek

.. tag:: Instant Messaging
.. tag:: Jabber
.. tag:: XMPP

.. sidebar:: Logo

  .. image:: _static/images/prosody.svg
      :align: center

#########
Prosody
#########

.. tag_list::

Prosody_ is a modern XMPP communication server. It aims to be easy to set up and configure, and efficient with system resources. Additionally, for developers it aims to be easy to extend and give a flexible system on which to rapidly develop added functionality, or prototype new protocols.

XMPP is an open and free alternative to commercial messaging and chat providers. Set it up for your company, organisation, or just your family and friends. You are in control, and your communication is private to you. Supporting a wide range of client software for desktop and mobile platforms, you can chat using Prosody from any device.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`HTTPS <web-https>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

Prosody is open source software under the permissive MIT/X11 license.

Prerequisites
=============

Web domain
----------

.. note:: To understand and setup the domains easier I use the following (recommended) subdomains:

 * ``xmpp.isabell.uber.space``
 * ``conference.isabell.uber.space``
 * ``upload.isabell.uber.space``

Your URL ``xmpp.isabell.uber.space`` and ``upload.isabell.uber.space`` needs to be setup:

.. include:: includes/web-domain-list.rst

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

+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
|                       name                      |  ttl  | class |  type | priority | weight |   port   | target                  |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
|                isabell.uber.space               |  3600 |   IN  |   A   |          |        |          |      35.195.215.42      |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
|                isabell.uber.space               |  3600 |   IN  |  AAAA |          |        |          |            0:           |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
|            upload.isabell.uber.space            |  3600 |   IN  | CNAME |          |        |          | isabell.uber.space      |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
|             xmpp.isabell.uber.space             |  3600 |   IN  | CNAME |          |        |          | isabell.uber.space      |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
| _xmpp-client._tcp.isabell.uber.space            | 18000 | IN    | SRV   | 0        | 5      | C2S-PORT | xmpp.isabell.uber.space |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
| _xmpp-server._tcp.isabell.uber.space            | 18000 | IN    | SRV   | 0        | 5      | S2S-PORT | xmpp.isabell.uber.space |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+
| _xmpp-server._tcp.conference.isabell.uber.space | 18000 | IN    | SRV   | 0        | 5      | S2S-PORT | xmpp.isabell.uber.space |
+-------------------------------------------------+-------+-------+-------+----------+--------+----------+-------------------------+

Configure luarocks
------------------

Prosody is written in ``lua`` and has some runtime dependencies which we install with the package manager ``luarocks``. In order to run the installed packages we have to adapt the path-variable in ``~/.bash_profile``:

::

 PATH=$HOME/.luarocks/bin:$PATH
 
 export PATH

Additionally we need to provide the paths ``LUA_PATH`` as well as ``LUA_CPATH`` and have to reload to use ``luarocks`` accordingly:

::

 [isabell@stardust ~]$ echo "$(luarocks path)" >> ~/.bash_profile
 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

Install runtime lua-dependencies
--------------------------------

The following dependencies_ (``luasocket``, ``luaexpat``, ``luafilesystem`` and ``luasec``) are required:

::

 [isabell@stardust ~]$ luarocks install luasocket --local
 luasocket [...] is now built and installed in [...]
 [isabell@stardust ~]$ luarocks install luaexpat --local
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

Download the latest stable release from source to ``~/prosody/prosody-0.11``:

::

 [isabell@stardust ~]$ hg clone https://hg.prosody.im/0.11/ ~/prosody/prosody-0.11
 requesting all changes
 adding changesets
 adding manifests
 adding file changes
 added 9796 changesets with 11406 changes to 519 files
 updating to bookmark @ on branch 0.11
 357 files updated, 0 files merged, 0 files removed, 0 files unresolved
 [isabell@stardust ~]$

``cd`` to the directory and configure, build and install prosody:

::

 [isabell@stardust ~]$ cd ~/prosody/prosody-0.11
 [isabell@stardust ~]$ ./configure --ostype=linux --prefix=$HOME --with-lua-include=/usr/include
 Lua version detected: 5.1
 Lua interpreter found: /usr/bin/lua...
 Checking Lua includes... lua.h found in /usr/include/lua.h
 Checking if Lua header version matches that of the interpreter... yes
 Writing configuration...

 Installation prefix: /home/isabell
 Prosody configuration directory: /home/isabell/etc/prosody
 Using Lua from: /usr

 Done. You can now run 'make' to build.

 [isabell@stardust ~]$ make
 [...] 
 [isabell@stardust ~]$ make install
 [...] 
 [isabell@stardust ~]$ 

Configuration
=============

Generate SSL dhparam file
-------------------------

.. note:: This is going to take a long time!

To improve the security you can generate a dhparam file with ``openssl``:

::

 [isabell@stardust ~]$ openssl dhparam -out ~/etc/prosody/certs/dhparam-4096.pem 4096
 [...]
 [isabell@stardust ~]$ 

Install modules
---------------

Now we create the http_upload folder and download the community plugins:

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/prosody/http_upload
 [isabell@stardust ~]$ hg clone https://hg.prosody.im/prosody-modules/ ~/prosody/prosody-modules
 [isabell@stardust ~]$

Configure prosody
-----------------

Then there are many settings which should be edited accordingly in ``~/etc/prosody/prosody.cfg.lua``. In this example there are many modules enabled you can check out from the `official page`_.

Additionally I recommended the ssl ciphers and options to reach a high security score on `IM Observatory`_.

.. code-block:: lua
 :emphasize-lines: 1, 2, 7, 10, 13, 19, 24-26, 30, 31, 33-36, 38-41, 44

 admins = { "isabell@uber.space" }
 plugin_paths = {"/home/isabell/prosody/prosody-modules"}
 modules_enabled = {"roster"; "saslauth"; "tls"; "dialback"; "disco"; "carbons"; "pep"; "private"; "blocklist"; "vcard_legacy"; "version"; "uptime"; "time"; "ping"; "register"; "mam"; "admin_adhoc"; "posix"; "smacks"; "smacks_offline"; "csi_simple"; "cloud_notify"; "bookmarks"; }

 allow_registration = false
 c2s_require_encryption = true
 c2s_ports = { C2S-PORT }
 s2s_require_encryption = true
 s2s_secure_auth = true
 s2s_ports = { S2S-PORT }
 s2s_timeout = 300
 ssl = {
   dhparam = "/home/isabell/etc/prosody/certs/dh-4096.pem";         
	 cafile = "/etc/pki/tls/certs/ca-bundle.trust.crt";
	 ciphers = "EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA384:EECDH+ECDSA+SHA256:EECDH+aRSA+SHA384:EECDH+aRSA+SHA256:EECDH:EDH+aRSA:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS:!RC4:!SEED:!AES128:!CAMELLIA128";
	 options = { "no_sslv2", "no_sslv3", "no_ticket", "no_compression", "cipher_server_preference", "single_dh_use", "single_ecdh_use" };
 }
 authentication = "internal_hashed"
 pidfile = "/home/isabell/prosody/prosody.pid";
 daemonize= false;
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
 https_certificate = "/home/isabell/etc/certificates/upload.isabell.uber.space.crt"
 http_ports = { }
 https_ports = { FILEUPLOAD-PORT }
 proxy65_ports = { FILETRANSFER-PORT }
 VirtualHost "isabell.uber.space" 
 Component "conference.isabell.uber.space" "muc"
   modules_enabled = { "muc_mam", "vcard_muc" }
 Component "prosody.isabell.uber.space" "proxy65"
   proxy65_address = "prosody.isabell.uber.space"
   proxy65_acl = { "prosody.isabell.uber.space"  }
 Component "upload.isabell.uber.space" "http_upload" 
   http_upload_file_size_limit = 10485760
   http_upload_expire_after = 2419200
   http_upload_path = "/home/isabell/prosody/http_upload/"

.. warning:: Replace the placeholders ``C2S-PORT``, ``S2S-PORT`` and ``FILEUPLAD-PORT`` with the above obtained ports, adapt the domain-names, sql settings (inclusive username and password) and paths! Don't delete, obmit or change the ordering of the entries, otherwise some default ports could be spammed. Also don't active modules which including module ``http`` without changing ``http_ports`` and ``https_ports`` . Last but not least be warned that spamming the default ports which could already be in use can lead to fork-spam issues! So be careful and watch your configuration twice and look into the prodoy logs afterwards to verify whats going on after starting prosody! 

For a explaination of the configuration check out the `example configuration file`_.

Setup deamon
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
 :emphasize-lines: 2,3 

 [isabell@stardust ~]$ prosodyctl adduser name@isabell.uber.space
 Enter new password:
 Retype new password:
 [isabell@stardust ~]$

Updates
=======

For updates ``cd`` to ``~/prosody/prosody-0.11`` and pull down the latest changes and restart the service:

::

 [isabell@stardust ~]$ cd ~/prosody/prosody-0.11
 [isabell@stardust ~]$ hp pull -u
 [...] 
 [isabell@stardust ~]$ ./configure --ostype=linux --prefix=$HOME --with-lua-include=/usr/include
 Lua version detected: 5.1
 Lua interpreter found: /usr/bin/lua...
 Checking Lua includes... lua.h found in /usr/include/lua.h
 Checking if Lua header version matches that of the interpreter... yes
 Writing configuration...

 Installation prefix: /home/isabell
 Prosody configuration directory: /home/isabell/etc/prosody
 Using Lua from: /usr

 Done. You can now run 'make' to build.

 [isabell@stardust ~]$ make
 [...] 
 [isabell@stardust ~]$ make install
 [...] 
 [isabell@stardust ~]$ supervisorctl restart prosody
 [isabell@stardust ~]$ 
 
----

Tested with Prosody 0.11.5, Uberspace 7.7.1.2

.. _prosody: https://prosody.im
.. _dns: https://prosody.im/doc/dns
.. _dependencies: https://prosody.im/doc/depends
.. _official page: https://modules.prosody.im
.. _IM Observatory: https://xmpp.net
.. _example configuration file: https://prosody.im/doc/example_config

.. author_list::
