.. author:: cblte <https://cbrueggenolte.de>

.. highlight:: console

.. tag:: voip
.. tag:: ports  


.. sidebar:: About

  .. image:: _static/images/teamspeak.svg
      :align: center

##########
Teamspeak
##########

.. tag_list::

TeamSpeak_ is a proprietary voice-over-Internet Protocol (VoIP) application for audio communication between users on a chat channel, much like a telephone conference call. Users typically use headphones with a microphone. The client software connects to a TeamSpeak server of the user's choice, from which the user may join chat channels.

The target audience for TeamSpeak is gamers, who can use the software to communicate with other players on the same team of a multiplayer video game. Communicating by voice gives a competitive advantage by enabling players to keep their hands on the controls.

Teamspeak is an alternativ to Mumble_ and needs a license to run. This can be optained from the the Teamspeak-License_ website and from the ``LICENSE`` file which is part of the downloadable teamspeak file.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Virtual Ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`


License
=======

All relevant legal information can be found here

  * Teamspeak-License_ models


Prerequisites
=============

.. include:: includes/open-port.rst

Run the commmand four times to retrieve four ports. One open port for the ``default_voice_port``, ``filetransfer_port``, ``query_port`` and ``query_ssh_port``.


Installation
============

Step 1
------

Download the Teamspeak Server for Linux. Get the latest download-URL from the Teamspeak-Downloads_ website.

.. code-block:: console

  [isabell@stardust ~]$ mkdir ts3server
  [isabell@stardust ~]$ cd ts3server
  [isabell@stardust ts3server]$ wget https://files.teamspeak-services.com/releases/server/3.11.0/teamspeak3-server_linux_amd64-3.11.0.tar.bz2
  --2020-02-14 21:23:12--  https://files.teamspeak-services.com/releases/server/3.11.0/teamspeak3-server_linux_amd64-3.11.0.tar.bz2
  Auflösen des Hostnamen »files.teamspeak-services.com (files.teamspeak-services.com)«... 151.139.128.10
  Verbindungsaufbau zu files.teamspeak-services.com (files.teamspeak-services.com)|151.139.128.10|:443... verbunden.
  HTTP-Anforderung gesendet, warte auf Antwort... 200 OK
  Länge: 9245357 (8,8M) [application/x-tar]
  In »»teamspeak3-server_linux_amd64-3.11.0.tar.bz2«« speichern.
  
  100%[======================================================================================================>] 9.245.357   32,4MB/s   in 0,3s   
  
  2020-02-14 21:23:12 (32,4 MB/s) - »»teamspeak3-server_linux_amd64-3.11.0.tar.bz2«« gespeichert [9245357/9245357]
  
  [isabell@stardust ts3server]$ 

Step 2
------

Unpack the downloaded archive into the current directory

.. code-block:: console

  [isabell@stardust ts3server]$ tar --extract --bzip2 --strip-components=1 --verbose --file teamspeak3-server_linux_amd64-3.11.0.tar.bz2
  teamspeak3-server_linux_amd64/LICENSE
  [...]
  teamspeak3-server_linux_amd64/CHANGELOG
  [isabell@stardust ts3server]$


Configuration
=============

Step 1: Setup license agreement
-------------------------------

Before starting the server for the first time you should either read the ``LICENSE`` file that is part of the teamspeak server archive you just unpacked or go to the Teamspeak-License_ website. 

If you agree to the license you need to create a file named ``.ts3server_license_accepted`` in the teamspeak server directory. It is enough to create the file. No need to add content. 

Step 2: Create a default config file, admin password and admin token
--------------------------------------------------------------------

To create a configuration file execute the minimal runscript with the ``createinifile=1`` parameter

.. code-block:: console

  [isabell@stardust ts3server]$ ./ts3server_minimal_runscript.sh createinifile=1
  2020-02-14 21:04:49.238119|INFO    |ServerLibPriv |   |TeamSpeak 3 Server 3.11.0 (2020-01-13 08:12:37)
  [...]
  
  ------------------------------------------------------------------
                        I M P O R T A N T                           
  ------------------------------------------------------------------
                 Server Query Admin Account created                 
           loginname= "serveradmin", password= "superSecretPassword"
  ------------------------------------------------------------------
  
  [...]
  
  ------------------------------------------------------------------
                        I M P O R T A N T                           
  ------------------------------------------------------------------
        ServerAdmin privilege key created, please use it to gain 
        serveradmin rights for your virtualserver. please
        also check the doc/privilegekey_guide.txt for details. 
  
         token=MKopgBVlbZm6r+8RLuKZGbiHVuNKPfH5gKcPMk+Y
  ------------------------------------------------------------------
  
  2020-02-14 21:04:50.025184|INFO    |Query         |   |listening for query on 0.0.0.0:10011, [::]:10011
  2020-02-14 21:04:50.025653|INFO    |Query         |   |listening for query ssh on 0.0.0.0:10022, [::]:10022
  2020-02-14 21:04:50.025748|INFO    |Query         |   |creating QUERY_SSH_RSA_HOST_KEY file: ssh_host_rsa_key
  2020-02-14 21:04:59.245200|INFO    |CIDRManager   |   |updated query_ip_whitelist ips: 127.0.0.1/32, ::1/128, 


You can now press **CTRL+C** to kill the server and to continue with the configuration. 

.. note:: Make a copy of **Server Query Admin Account** ``loginname``, ``password`` and **ServerAdmin** ``token``. You vill need this when you connect to your teamspeak server for the first time to gain administrator rights.

Step 3: Edit configuration file
-------------------------------

Now edit the ``ts3server.ini`` and change the following entries. Use the four ports you were assigned by ``uberspace port add`` above.

::
  
  machine_id=0

::
  
  default_voice_port=40132   

::

  filetransfer_port=40133

::

  query_port=40134

::

  license_accepted=1

::

  query_ssh_port=40135


Step 4: Test server start
-------------------------

You can test your configuration by executing the minimal runscript. Use the paramater ``inifile`` with the argument ´´ts3server.ini`` to start the server with your configuration. 

.. code-block:: console

  [isabell@stardust ts3server]$ ./ts3server_minimal_runscript.sh inifile=ts3server.ini
  2020-02-14 21:43:43.659472|INFO    |ServerLibPriv |   |TeamSpeak 3 Server 3.11.0 (2020-01-13 08:12:37)
  [...]
  2020-02-14 22:17:31.884829|INFO    |              |   |Puzzle precompute time: 703
  2020-02-14 22:17:31.885977|INFO    |FileManager   |   |listening on 0.0.0.0:47304, [::]:47304
  2020-02-14 22:17:31.895316|INFO    |VirtualServerBase|1  |listening on 
  2020-02-14 22:17:31.896826|INFO    |Query         |   |listening for query on 0.0.0.0:47305, [::]:47305
  2020-02-14 22:17:31.897214|INFO    |Query         |   |listening for query ssh on 0.0.0.0:47306, [::]:47306
  2020-02-14 22:17:31.897479|INFO    |CIDRManager   |   |updated query_ip_whitelist ips: 127.0.0.1/32, ::1/128,

.. note:: If this does not work right now, it might be, that the ports are not yet open. Try again in a couple minutes. 

If you want, you can also try to connect to the teamspeak server with your local teamspeak client software. Please use the IP address of your server the the default_voice_port (<IPofYourServer>:<default_voice_port>)

Example:

  .. image:: _static/images/teamspeak_client_connect.png
      :align: center


Configure the supervisord service
=================================

Since teamspeak does come with a start-stop script, all we need to do is to create the ``supervisor`` ini-file.

Create supervisord ini (e.g. ``/home/$USER/etc/services.d/ts3server-daemon.ini``):

.. code-block:: ini
  
  [program:ts3server]
  directory=%(ENV_HOME)s/ts3server/
  command=%(ENV_HOME)s/ts3server/ts3server inifile=ts3server.ini
  startsecs=10
  autostart=yes
  autorestart=yes


.. include:: includes/supervisord.rst

If it’s not in state RUNNING after 10 seconds, check your configuration and the log file in ``$HOME/logs/supervisord.log``.

You can read more about the **supervisord** in the :manual:`supervisord <daemons-supervisord>` manual.


Additional Notes
================

Gaining Admin Rights
--------------------

When you connect to your teamspeak server for the first time, you will need the token that got generated on first start of the server. If you have not taken a copy of the *token* and/or the *admin/password* combination, then you can get them from the log files located in the ``logs`` folder of your teamspeak installation. 

Start and Stopping the Server
-----------------------------

To stop and start the teamspeak to perform maintenance tasks, you can use the supervisorctl command which is documented in the :manual:`supervisord <daemons-supervisord>`.

Backup The Server
-----------------

You should make a regular backup of your server. To do this, you need to backup at least the following files and folder: 

  * files/
  * query_ip_blacklist.txt
  * query_ip_whitelist.txt
  * ssh_host_rsa_key
  * ts3server.ini
  * ts3server.sqlitedb


Updating The Server
-------------------

To update the server download the latest linux teamspeak server release from the teamspeak website and unpack the archive into a temporary directory. Then stop the server and replace at least the following files:

  * libts3db_sqlite3.so
  * ts3server
  


---

Tested with Teamspeak 3.11.0 64-bit, Uberspace 7.1.1

.. author_list::


.. _Teamspeak: https://www.teamspeak.com/
.. _Teamspeak-Downloads: https://teamspeak.com/en/downloads/#server
.. _Teamspeak-License: https://support.teamspeak.com/hc/en-us/articles/360002710757-What-license-models-are-available-for-TeamSpeak-3-
.. _Mumble: https://mumble.info/
