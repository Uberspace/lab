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

Altogether we need four open ports (referred to as: ``CLIENTPORT``, ``SERVERPORT`` and ``FILEUPLOADPORT`` ``FILETRANSFERPORT``) which should be public accessible.

Domains, dns
------------
The following domains should be set up (to set up prosody for the domain ``stardust.space``):

::
 
 [isabell@stardust ~]$ uberspace web domain list
 stardust.space
 groupchat.stardust.space
 [isabell@stardust ~]$

Additionally to the dns_ A-records we need the following SRV-records: 

+---------------------------------------------+-------+-------+------+----------+--------+--------------+-----------------------+
|  _service._proto.name			      | ttl   | class | type | priority | weight | port         | target                |
+=============================================+=======+=======+======+==========+========+==============+=======================+
| _xmpp-client._tcp.stardust.space	      | 18000 | IN    | SRV  | 0        | 5      | CLIENTPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+------+----------+--------+--------------+-----------------------+
| _xmpp-server._tcp.stardust.space	      | 18000 | IN    | SRV  | 0        | 5      | SERVERPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+------+----------+--------+--------------+-----------------------+
| _xmpp-server._tcp.groupchat.stardust.space  | 18000 | IN    | SRV  | 0        | 5      | SERVERPORT   | stardust.uber.space   |
+---------------------------------------------+-------+-------+------+----------+--------+--------------+-----------------------+

.. note:: Adapt the port-numbers and change ``stardust`` as well as ``stardust.space`` accordingly in your dns settings of your prefered provider.

TLS
---
For simplicity we use openssl and the certificates created via letsencrypt_ for above domains which are already provided on the host after adding the domains and visiting them.

Configure luarocks
------------------

Prosody is written in ``lua`` and has some dependencies which we install with the package manager ``luarocks``. In order to run the installed packages we have to adapt the path:

::

 PATH=$HOME/.luarocks/bin:$PATH
 
 export $PATH

Additionally we need to provide the paths ``LUA_PATH`` and ``LUA_CPATH`` to use ``luarocks`` accordingly:

::

 [isabell@stardust ~]$ echo "$(luarocks path)" >> ~/.bash_profile \
 && source ~/.bash_profile
 [isabell@stardust ~]$

Install lua-dependencies
------------------------

The following dependencies_ (``luasocket``, ``luaexpat`` and ``luafilesystem``) are required:

::

 [isabell@stardust ~]$ luarocks install luasocket --local && \
 luarocks install luaexpat --local EXPAT_BINDIR="/usr/bin" EXPAT_INCDIR="/usr/include/" EXPAT_LIBDIR="/usr/lib64" && \
 luarocks install luafilesystem --local && \
 luarocks install luasec --local OPENSSL_BINDIR="/usr/bin" OPENSSL_INCDIR="/usr/include" OPENSSL_LIBDIR="/usr/lib64"
 [...]
 luasocket [...] is now built and installed in [...]
 luaexpat [...] is now built and installed in [...]
 luafilesystem [...] is now built and installed in [...]
 luasec [...] is now built and installed in [...]
 [isabell@stardust ~]$

.. note:: The variables ``*_BINDIR`` ``*__INCDIR`` and ``*_LIBDIR`` are necessary for correct linking the associated library because CentOS uses a different layout for those files than luarocks expects!

Further optional ones (``luadbi-mysql``, ``lua-zlib`` and ``luaevent``) can be installed with these commands:

::

 [isabell@stardust ~]$ luarocks install luadbi-mysql --local MYSQL_BINDIR="/usr/bin" MYSQL_INCDIR="/usr/include/mysql" MYSQL_LIBDIR="/usr/lib64" && \
 luarocks install lua-zlib --local && \
 luarocks install luaevent --local
 [...]
 luadbi [...] is now built and installed in [...]
 luadbi-mysql [...] is now built and installed in [...]
 lua-zlib [...] is now built and installed in [...]
 luaevent [...] is now built and installed in [...]
 [isabell@stardust ~]$

To list the installed packages with their versions use the command ``luarocks list``.

Set c99 compilation flag
------------------------
In order to built prosody we have to activate C99-mode as global setting for all packages compiled via luarocks ``~/.luarocks/config-5.1.lua``.

::

 variables = {
 CC= "gcc -std=c99"
 }

.. note:: This is a temporary workaround since luarocks not allowing setting this flag via ``.rockspec``-file.

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

 [isabell@stardust ~]$ luarocks install --server=http://luarocks.org/manifests/fapsi prosody --local
 [...] 
 luabitop [...] is now built and installed in [...]
 cqueues [...] is now built and installed in [...]
 prosody [...] is now built and installed in [...]
 [isabell@stardust ~]$

.. note:: Prosody only provides rockspecs for all modules individually (refer to `prosody rocks <https://packages.prosody.im/rocks>`_ ) and currently there isn't an official up-to-date version on luarocks. Please make sure you want to install the provided unofficial rockspec file by analysing it's content.

Configuration
=============

Adapt the ``.bash_profile`` again :

::

 PROSODY_PATH=$HOME/.luarocks/lib64/luarocks/rocks/prosody/<Version PROSODY>
 export PROSODY_SRCDIR="$HOME/.luarocks/share/lua/<Version LUA>"
 export PROSODY_CFGDIR="$PROSODY_PATH/conf"
 export PROSODY_PLUGINDIR="$PROSODY_PATH/plugins"
 export PROSODY_DATADIR="$HOME/var/prosody/data"

.. note:: Don't forget to replace the correct prosody and lua versions in the paths above.

Now we copy the configuration and plugin files into reasonable locations, download the community plugins and create the prosody-data and http_upload directory:

::

 [isabell@stardust ~]$ cp -R $PROSODY_PATH/conf/ ~/etc/prosody
 [isabell@stardust ~]$ cp -R $PROSODY_PATH/plugins/ ~/var/prosody/plugins
 [isabell@stardust ~]$ mkdir -p ~/var/prosody/data/http_upload
 [isabell@stardust ~]$ hg clone https://hg.prosody.im/prosody-modules/ ~/var/prosody/community-plugins
 [isabell@stardust ~]$

Then there are many settings which should be edited accordingly in ``~/etc/prosody/prosody.cfg.lua``:

.. code-block:: lua

 admins = { "isabell@uber.space" }
 plugin_paths = {"/home/isabell/var/prosody/community-plugins/"}
 -- uncomment/add "proxy65" and "http_upload" in modules_enabled
 allow_registration = false
 c2s_require_encryption = true
 c2s_ports = { CLIENTPORT }
 s2s_require_encryption = true
 s2s_secure_auth = true
 s2s_ports = { SERVERPORT }
 authentication = "internal_hashed"
 pidfile = "/home/isabell/var/prosody/prosody.pid";
 daemonize= false;
 storage = "sql"
 sql = { 
   driver = "MySQL", 
   database = "isabell_prosody", 
   username = "isabell", 
   password = "<Your Password>", 
   host = "localhost" 
 }
 log = { info = "*console" }
 certificates = "/home/isabell/etc/certificates"
 https_certificate = "../certificates/stardust.space.crt"
 http_ports = {}
 https_ports = { FILEUPLOADPORT }
 proxy65_ports = { FILETRANSFERPORT }
 proxy65_address = "stardust.space"
 proxy65_acl = {"stardust.space"}
 VirtualHost "stardust.space" 
 Component "groupchat.stardust.space" "muc"
   modules_enabled = { "muc_mam" } 

.. warning:: Replace the placeholders ``CLIENTPORT``, ``SERVERPORT``, ``FILEUPLOADPORT`` and ``FILETRANSFERPORT`` with the above obtained ports, adapt the domain-names, sql settings (inclusive username and password) and paths! Don't delete, obmit or change the ordering of the entries, otherwise some default ports could be spammed. Also don't active modules which including module ``http`` without changing ``http_ports`` and ``https_ports`` . Last but not least be warned that spamming the default ports which could already be in use can lead to fork-spam issues! So be careful and watch your configuration twice and look into the prodoy logs afterwards to verify whats going on after starting prosody!  

Finishing Installation
======================

supervisord
-----------

Place the file ``prosody.ini`` in ``~/etc/services.d/`` and adapt it accordingly:

.. code-block:: console

 [program:prosody]
 command=/bin/bash -c "source /home/isabell/.bash_profile && prosody"
 autostart=yes
 autorestart=yes
 startretries=1
 stopasgroup=true


First-Start
-----------

Reread:

::

 [isabell@stardust ~]$ supervisorctl reread
 prosody: available
 [isabell@stardust ~]$

And then update and start your new service:

::

 [isabell@stardust ~]$ supervisorctl update
 prosody: added process group
 [isabell@stardust ~]$ supervisorctl start prosody
 prosody: started
 [isabell@stardust ~]$

Best-Practise
=============

Keep an eye on the logs and look at the output of the commands below:

::

 [isabell@stardust ~]$ supervisorctl status
 [...]
 [isabell@stardust ~]$ supervisorctl tail prosody
 [...]
 [isabell@stardust ~]$ prosodyctl about
 [...]
 [isabell@stardust ~]$ prosodyctl check
 [...]
 [isabell@stardust ~]$ prosodyctl status
 [...]
 [isabell@stardust ~]$


Updates
=======

The easiest way to update prosody is via luarocks with the same commands as in the prerequisites and installation step above. 

.. note:: This should also be done on changes to openssl on CentOS. Remember to comment out the C99 setting on problems. Also check the `website <https://prosody.im/>`_ regularly to stay informed about new config updates and releases.

Acknowledgements
================
This guide uses many instructions and ideas of other developers. Refer especially to the guide from alex_ and persons mentioned there as well as the prosody developers for their input on naive questions and with bug fixes for the special uberspace environment.


.. _prosody: https://prosody.im
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _mysql: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _ports: https://manual.uberspace.de/en/basics-ports.html
.. _tls: https://manual.uberspace.de/en/web-https.html
.. _dns: https://prosody.im/doc/dns
.. _letsencrypt: https://manual.uberspace.de/en/web-security.html#id2
.. _dependencies: https://prosody.im/doc/depends
.. _alex: https://plaintext.blog/hosting/Uberspace/prosody.html

----

Tested with Prosody 0.11.2, Uberspace 7.3.2.1

.. author_list::
