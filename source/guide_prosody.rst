.. highlight:: console
.. author:: fapsi | fenchurch.space <fapsi@fenchurch.space>

.. sidebar:: Logo

  .. image:: _static/images/prosody.svg
      :align: center

#########
Prosody
#########

Prosody_ is a modern XMPP communication server. It aims to be easy to set up and configure, and efficient with system resources. Additionally, for developers it aims to be easy to extend and give a flexible system on which to rapidly develop added functionality, or prototype new protocols.

XMPP is an open and free alternative to commercial messaging and chat providers. Set it up for your company, organisation, or just your family and friends. You are in control, and your communication is private to you. Supporting a wide range of client software for desktop and mobile platforms, you can chat using Prosody from any device.

Prosody is open source software under the permissive MIT/X11 license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * supervisord_
  * mysql_
  * domains_
  * ports_
  * tls_

Prerequisites
=============
Ports
------------

.. include:: includes/open-port.rst

We need three open tcp ports (referred to as: ``CLIENTPORT``, ``SERVERPORT`` and ``FILEPORT``) which should be public accessible.

Domains, DNS
------------
The following domains should be set up:

::
 
 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 groups.isabell.uber.space
 files.isabell.uber.space
 [isabell@stardust ~]$

Additionally to the A-records we need some dns_ SRV-records (adapt the names, ports and change ``stardust`` accordingly in your providers settings):

+---------------------------------------------+-------+-------+-----+----------+--------+--------------+-----------------------+
|  _service._proto.name			      | TTL   | class | SRV | priority | weight | port         | target	               |
+=============================================+=======+=======+=====+==========+========+==============+=======================+
| _xmpp-client._tcp.isabell.uber.space	      | 18000 | IN    | SRV | 0        | 5      | CLIENTPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+-----+----------+--------+--------------+-----------------------+
| _xmpp-server._tcp.isabell.uber.space	      | 18000 | IN    | SRV | 0        | 5      | SERVERPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+-----+----------+--------+--------------+-----------------------+
| _xmpp-server._tcp.groups.isabell.uber.space | 18000 | IN    | SRV | 0        | 5      | SERVERPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+-----+----------+--------+--------------+-----------------------+

TLS
---
For simplicity we use the certificates created via letsencrypt_ for above domains which are already provided on the host.

Lua-dependencies
----------------

Prosody is written in ``lua`` and has some dependencies. In order to install local (per user) packages we have to provide some paths of the ``lua`` package-manager ``luarocks`` via the ``bash_profile`` file (if not already happend):

::

 [isabell@stardust ~]$ grep -qF -- "$(luarocks path)" ~/.bash_profile || \
 echo "$(luarocks path)" >> ~/.bash_profile && source ~/.bash_profile
 [isabell@stardust ~]$

Additionally we need to activate C99-mode as global setting for all packages compiled via luarocks ``~/.luarocks/config-5.1.lua``.
::

 variables = {
 CC= "gcc -std=c99"
 }

.. note:: This is a workaround since luarocks not allowing setting this flag via ``.rockspec``-file.

The following dependencies_ (``luasocket``, ``luaexpat`` and ``luafilesystem``) are _required_:

::

 [isabell@stardust ~]$ luarocks install luasocket --local && \
 luarocks install luaexpat --local EXPAT_BINDIR="/usr/bin" EXPAT_INCDIR="/usr/include/" EXPAT_LIBDIR="/usr/lib64" && \
 luarocks install luafilesystem --local && \
 luarocks install luasec --local OPENSSL_BINDIR="/usr/bin" OPENSSL_INCDIR="/usr/include" OPENSSL_LIBDIR="/usr/lib64"
 [...]
 [isabell@stardust ~]$

.. note:: The variables ``*_BINDIR`` ``*__INCDIR`` and ``*_LIBDIR`` are necessary for correct linking the associated library because CentOS uses a different layout for those files than luarocks expects!

Further _optional_ ones (``luadbi-mysql``, ``lua-zlib`` and ``luaevent``) can be installed with these commands:

::

 [isabell@stardust ~]$ luarocks install luadbi-mysql --local MYSQL_BINDIR="/usr/bin" MYSQL_INCDIR="/usr/include/mysql" MYSQL_LIBDIR="/usr/lib64" && \
 luarocks install lua-zlib --local && \
 luarocks install luaevent --local
 [...]
 [isabell@stardust ~]$

To list the installed packages with their versions use the command ``luarocks list``.

MySQL-database
--------------

Create a separate db for prosody data:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_prosody CHARACTER SET utf8"
 [isabell@stardust ~]$

Installation
============

Install prosody with an (currently unofficial) ``.rockspec``-file:

::

 [isabell@stardust ~]$ luarocks install --tree=fapsi prosody --local
 [...]
 [isabell@stardust ~]$

.. note:: Prosody only provides rockspecs for all modules individually (refer to: _prosodyrockspecs) and I am currently not listed as official maintainer on luarocks.

Adapt the ``.bash_profile`` again :

::

 PROSODY_PATH=$HOME/.luarocks/lib64/luarocks/rocks/prosody/<Version PROSODY>
 export PROSODY_SRCDIR="$HOME/.luarocks/share/lua/<Version LUA>"
 export PROSODY_CFGDIR="$PROSODY_PATH/conf"
 export PROSODY_PLUGINDIR="$PROSODY_PATH/plugins"
 export PROSODY_DATADIR="$HOME/var/prosody/data"

.. note:: Don't forget to replace the correct prosody and lua versions in the paths above.

And create `$PROSODY_DATADIR`:

 mkdir $PROSODY_DATADIR

Configuration
=============

First we have to copy the standard config file to a place outside:

::

 [isabell@stardust ~]$ cp
 TODO
 [isabell@stardust ~]$

Then there are some settings which should be edited accordingly:

.. code-block:: lua

 modules_enabled = {"","","proxy65"}
 modules_disabled = {}
 plugin_paths = {"/home/isabell/var/prosody/prosody-modules-user-build/"}
 data_path = "/home/isabell/var/prosody/data";
 daemonize= false;
 pidfile = "/home/isabell/var/prosody/prosody.pid";
 allow_registration = false
 c2s_require_encryption = true
 s2s_require_encryption = true
 s2s_secure_auth = false
 authentication = "internal_hashed"
 storage = "sql"
 sql = { 
   driver = "MySQL", 
   database = "prosody", 
   username = "prosody", 
   password = "secret", 
   host = "localhost" 
 }
 log = { info = "*console" }
 c2s_ports = { CLIENTPORT }
 s2s_ports = { SERVERPORT }
 proxy65_ports = { FILEPORT }

 certificates = "/home/isabell/etc/prosody/certs"

 VirtualHost "isabell.uber.space"
 
 Component "groups.isabell.uber.space" "muc"
 
 Component "files.isabell.uber.space" "proxy65"

.. warning:: Replace the placeholders ``CLIENTPORT``, ``SERVERPORT`` ``FILEPORT`` with the above obtained ports, adapt the domain-names and the sql settings! Don't delete, obmit or change the ordering of the entries, otherwise some default ports could be spammed. Also don't active modules which including module ``http`` without changing ``http_ports`` and ``https_ports`` . Last but not least be warned that spamming the default ports which could already be in use can lead to fork-spam issues! So be careful and watch your configuration twice and look into the prodoy logs to see whats going on!  

Finally we create a symlink:

Finishing Installation
======================

deamon
-------

Place the file ``prosody.ini`` in ``~/etc/services.d/`` and adaptit accordingly:

.. code-block:: console

 [program:prosody]
 command=/home/isabell/bin/prosody
 autostart=yes
 autorestart=yes


First-Start
-----------

Reread:

::

 [isabell@stardust ~]$ supervisorctl reread
 prosody: available
 [isabell@stardust ~]$

And then start your daemon:

::

 [isabell@stardust ~]$ supervisorctl update
 prosody: added process group
 [isabell@stardust ~]$

Advanced
========

Community modules
-----------------

Backup
------

Tuning
------


Updates
=======

The easiest way to update prosody is via luarocks. Stop the deamon, reinstall updated dependencies and prosody itself. Note: this should also be done on openssl changes.

.. note:: Check the `website <https://prosody.im/>`_ regularly to stay informed about new updates and releases.

.. _prosody: https://prosody.im
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _mysql: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _ports: https://manual.uberspace.de/en/basics-ports.html
.. _tls: https://manual.uberspace.de/en/web-https.html
.. _dns: https://prosody.im/doc/dns
.. _letsencrypt: https://manual.uberspace.de/en/web-security.html#id2
.. _dependencies: https://prosody.im/doc/depends
.. _prosodyrockspecs: https://wiki.uberspace.de/development:lua#mysql



----

Tested with Prosody 0.11.2, Uberspace 7.3.1

.. author_list::
