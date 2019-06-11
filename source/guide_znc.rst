.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: irc
.. tag:: bouncer

##########
ZNC
##########

.. tag_list::

ZNC is an advanced IRC bouncer that is left connected so an IRC client can disconnect/reconnect without losing the chat session.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here

  * https://github.com/znc/znc/blob/master/LICENSE

Prerequisites
=============

We'll need an open port:

::

 [isabell@stardust ~]$ uberspace port add
 Port 47680 will be open for TCP and UDP traffic in a few minutes.
 [isabell@stardust ~]$

Installation
============

Step 1
------
Create a new directory, download the lastest version and enter the directory you just created:

::

 [isabell@stardust ~]$ mkdir znc
 [isabell@stardust ~]$ curl https://znc.in/releases/znc-latest.tar.gz | tar -xzvC $HOME/znc --strip-components=1
 [isabell@stardust ~]$ cd znc
 [isabell@stardust ~]$

Step 2
------
Run the comments below:

::

 [isabell@stardust ~]$ ./configure --prefix="$HOME/.local"
 [...]
 [isabell@stardust ~]$ make
 [...]
 [isabell@stardust ~]$ make install
 [...]
 [isabell@stardust ~]$

Configuration
=============

Configure ZNC
-------------------
Run the following command to create a config file:

::

 [isabell@stardust ~]$ /home/isabell/.local/bin/znc --makeconf
 [ .. ] Checking for list of available modules...
 [ ** ]
 [ ** ] -- Global settings --
 [ ** ]
 [ ?? ] Listen on port (1025 to 65534): 47680
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
 [ ** ] /server <znc_server_ip> +47680 myUsername:<pass>
 [ ** ]
 [ ** ] To manage settings, users and networks, point your web browser to
 [ ** ] https://<znc_server_ip>:47680/
 [ ** ]
 [ ?? ] Launch ZNC now? (yes/no) [no]:
 [isabell@stardust ~]$

Setup daemon
------------
Create ``~/etc/services.d/znc.ini`` with the following content:

::

 [program:znc]
 command=/home/isabell/.local/bin/znc --foreground
 autostart=yes
 autorestart=yes

Run the following commands to reread and update the ``supervisord`` configuration:

::

 [isabell@stardust ~]$ supervisorctl reread
 znc: available
 [isabell@stardust ~]$ supervisorctl update
 znc: added process group
 [isabell@stardust ~]$ supervisorctl status
 znc                              RUNNING   pid 20669, uptime 0:00:18
 [isabell@stardust ~]$

If the last command does not return RUNNING, the configuration is probably faulty.

Open webadmin
======================

If ZNC is running, you can find the web interface for further configuration here

  * https://isabell.stardust.uberspace.de:47680

Updates
=======

.. note:: Check https://wiki.znc.in/ZNC regularly to stay informed about the newest version.

----

Tested with ZNC 1.7.3, Uberspace 7.3.0.0

.. author_list::
