.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-cpp
.. tag:: irc
.. tag:: bouncer

##########
ZNC
##########

.. tag_list::

ZNC_ is an advanced IRC bouncer that stays connected to the server, so an IRC client can disconnect/reconnect without losing the chat session.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`HTTPS <web-https>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here:

  * https://github.com/znc/znc/blob/master/LICENSE

Prerequisites
=============

.. include:: includes/open-port.rst

Installation
============

Step 1
------
Create a new directory, download the latest version and enter the directory you just created:

::

 [isabell@stardust ~]$ mkdir ~/znc
 [isabell@stardust ~]$ curl https://znc.in/releases/znc-latest.tar.gz | tar -xzvC ~/znc --strip-components=1
 [isabell@stardust ~]$ cd ~/znc
 [isabell@stardust znc]$

Step 2
------

Compile and install ZNC to your home directory:

::

 [isabell@stardust znc]$ ./configure --prefix="$HOME/.local"
 [...]
 [isabell@stardust znc]$ make
 [...]
 [isabell@stardust znc]$ make install
 [...]
 [isabell@stardust znc]$

Configuration
=============

Configure ZNC
-------------
Run the following command to create a config file:

::

 [isabell@stardust ~]$ ~/.local/bin/znc --makeconf
 [ .. ] Checking for list of available modules...
 [ ** ]
 [ ** ] -- Global settings --
 [ ** ]
 [ ?? ] Listen on port (1025 to 65534): 40132
 [ ?? ] Listen using SSL (yes/no) [no]: yes
 [ ?? ] Listen using both IPv4 and IPv6 (yes/no) [yes]:
 [ .. ] Verifying the listener...
 [ ** ] Enabled global modules [webadmin]
 [ ** ]
 [ ** ] -- Admin user settings --
 [ ** ]
 [ ?? ] Username (alphanumeric): myUsername
 [ ?? ] Enter password:
 [ ?? ] Confirm password:
 [ ?? ] Nick [myUsername]: myNick
 [ ?? ] Alternate nick [myNick_]:
 [ ?? ] Ident [myUsername]:
 [ ?? ] Real name (optional):
 [ ?? ] Bind host (optional):
 [ ** ] Enabled user modules [chansaver, controlpanel]
 [ ** ]
 [ ?? ] Set up a network? (yes/no) [yes]: no
 [ ** ]
 [ .. ] Writing config [/home/isabell/.znc/configs/znc.conf]...
 [ ** ]
 [ ** ] To connect to this ZNC you need to connect to it as your IRC server
 [ ** ] using the port that you supplied.  You have to supply your login info
 [ ** ] as the IRC server password like this: user/network:pass.
 [ ** ]
 [ ** ] Try something like this in your IRC client...
 [ ** ] /server <znc_server_ip> +40132 myUsername:<pass>
 [ ** ]
 [ ** ] To manage settings, users and networks, point your web browser to
 [ ** ] https://<znc_server_ip>:40132/
 [ ** ]
 [ ?? ] Launch ZNC now? (yes/no) [no]:
 [isabell@stardust ~]$

Use your own certificate
------------------------
ZNC ships with a self generated certificate which will cause a warning in all modern browsers. To prevent this, we have to use our own certificate. Enter the ``~/.znc/configs`` directory and generate a ``dhparam.pem`` file:

::

  [isabell@stardust ~]$ cd ~/.znc/configs
  [isabell@stardust configs]$ openssl dhparam -out dhparam.pem 2048
  [...]
  [isabell@stardust configs]$

.. warning:: Replace ``isabell`` with your username!

Add the following lines to ``~/.znc/configs/znc.conf`` above the line ``Version = 1.7.3`` (your version number may differ):

::

 SSLCertFile = /home/isabell/etc/certificates/isabell.uber.space.crt
 SSLKeyFile = /home/isabell/etc/certificates/isabell.uber.space.key
 SSLDHParamFile = /home/isabell/.znc/configs/dhparam.pem

Setup daemon
------------
Create ``~/etc/services.d/znc.ini`` with the following content:

::

 [program:znc]
 command=%(ENV_HOME)s/.local/bin/znc --foreground
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Open webadmin
-------------
.. note:: Replace ``isabell`` with your username and ``40132`` with your port!

If ZNC is running, you can find the web interface for further configuration here:

  * https://isabell.uber.space:40132/

Connect your client
-------------------

Add a new server in your local IRC client:

* Hostname: `<username>.uber.space`
* Port: your port
* Username: ZNC nickname
* Password: ZNC password
* Encryption: yes

Updates
=======

.. note:: Check https://wiki.znc.in/ZNC regularly to stay informed about the newest version.

To update an existing installation remove the ``~/znc`` directory (``rm -rf ~/znc``) and repeat the **Installation** steps. Execute ``supervisorctl restart znc`` to start the new version.

.. _ZNC: https://znc.in/

----

Tested with ZNC 1.7.3, Uberspace 7.3.1.1

.. author_list::
