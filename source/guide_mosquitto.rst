.. highlight:: console

.. author:: Raphael Höser <raphael@hoeser.info>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-c
.. tag:: mqtt
.. tag:: message-broker

.. sidebar:: About

  .. image:: _static/images/mosquitto.svg
      :align: center

#########
Mosquitto
#########

.. tag_list::

Eclipse Mosquitto_ is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. Mosquitto is lightweight and is suitable for use on all devices from low power single board computers to full servers.

The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe model. This makes it suitable for Internet of Things messaging such as with low power sensors or mobile devices such as phones, embedded computers or microcontrollers.

The Mosquitto project also provides a C library for implementing MQTT clients, and the very popular mosquitto_pub and mosquitto_sub command line MQTT clients.

.. note:: This guide contains some more advanced Linux technics like LD_LIBRARY_PATH and manual RPM extraction. I try to keep it simple, but mosquitto doesn't except to be installed this way.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Eclipse Mosquitto is licensed under EPL/EDL.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download Mosquitto
------------------

Mosquitto can be downloaded from the CentOS7 "epel-release" repo via yumdownloader.

::

 [isabell@stardust ~]$ yumdownloader --resolve mosquitto --destdir=mosquitto/tmp
 --> Running transaction check
 ---> Package mosquitto.x86_64 0:1.6.8-1.el7 will be installed
 --> Processing Dependency: libwebsockets.so.13()(64bit) for package: mosquitto-1.6.8-1.el7.x86_64
 --> Running transaction check
 ---> Package libwebsockets.x86_64 0:3.0.1-2.el7 will be installed
 --> Finished Dependency Resolution
 (1/2): libwebsockets-3.0.1-2.el7.x86_64.rpm                                                                                                                      | 118 kB  00:00:01
 (2/2): mosquitto-1.6.8-1.el7.x86_64.rpm
 [isabell@stardust ~]$

This will download the newest version of mosquitto and libwebsockets to ~/mosquitto_rpms.

Extract the rpms
----------------

Sinze RPMs are not as easy to extract as .tar.gz files.
First we need to convert them to .cpio bundels via rpm2cpio and then extract them via cpio.

rpm2cpio prints the cpio file to stdout, so we can use it to directly convert and extract the rpm.

::

 [isabell@stardust ~]$ cd mosquitto
 [isabell@stardust mosquitto]$ rpm2cpio tmp/libwebsockets* | cpio -idm
 541 blocks
 [isabell@stardust mosquitto]$ rpm2cpio tmp/mosquitto* | cpio -idm
 1475 blocks
 [isabell@stardust mosquitto]$ cd ..
 [isabell@stardust ~]$

Delete the rpms
---------------

We no longer need the rpms, so we'll delete them.

::

 [isabell@stardust ~]$ rm -r mosquitto/tmp
 [isabell@stardust ~]$

Configuring PATH and LD_LIBRARY_PATH
------------------------------------

Please add the following lines to your ``~/.bash_profile``:

.. code-block:: bash

 # Mosquitto Environment
 export PATH=$HOME/mosquitto/usr/bin/:$HOME/mosquitto/usr/sbin/:$PATH
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/mosquitto/usr/lib64

Reload the ``.bash_profile`` with:

::

 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

Run ``mosquitto -h`` to verify the installation so far:

::

 [isabell@stardust ~]$ mosquitto -h
 mosquitto version 1.6.8
 
 mosquitto is an MQTT v3.1.1 broker.
 
 Usage: mosquitto [-c config_file] [-d] [-h] [-p port]
 
  -c : specify the broker config file.
  -d : put the broker into the background after starting.
  -h : display this help.
  -p : start the broker listening on the specified port.
       Not recommended in conjunction with the -c option.
  -v : verbose mode - enable all logging types. This overrides
       any logging options given in the config file.
 
 See http://mosquitto.org/ for more information.

 [isabell@stardust ~]$

Configuration
=============

Create a password file and an initial user
------------------------------------------

By default Mosquitto uses no authentication for it's broker. As this setup shows how to create a public facing broker, I highly recommend setting up credential authorization on it.
I will describe how to setup username:password authentication, but other methods are available (see here: `<https://mosquitto.org/man/mosquitto-conf-5.html>`_).

IMPORTANT: This command is used do initially create the password file. If you rerun it, you'll destroy the existing file!

Run the command below and enter your password twice when asked.

::

 [isabell@stardust ~]$ mosquitto_passwd -c mosquitto/etc/mosquitto/pwfile isabell
 Password:
 Reenter password:
 [isabell@stardust ~]$

Enable password authorization in mosquitto.conf
-----------------------------------------------

Edit the following lines in ~/mosquitto/etc/mosquitto/mosquitto.conf so the part before the "->" becomes the part after the "->".

.. code-block:: ini

 # =================================================================
 # Default listener
 # =================================================================
 ...
 # Port to use for the default listener.
 #port -> port 1883
 ...
 # Choose the protocol to use when listening.
 # This can be either mqtt or websockets.
 # Websockets support is currently disabled by default at compile time.
 # Certificate based TLS may be used with websockets, except that
 # only the cafile, certfile, keyfile and ciphers options are supported.
 #protocol mqtt -> protocol mqtt
 ...
 # =================================================================
 # Extra listeners
 # =================================================================
 ...
 #listener -> listener 9001
 ...
 #protocol -> protocol websockets
 ...
 # -----------------------------------------------------------------
 # Default authentication and topic access control
 # -----------------------------------------------------------------
 ...
 #password_file -> password_file /home/<username>/mosquitto/etc/mosquitto/pwfile

That way you have the normal mqtt listener running on port 1883 and the websocket based one on 9001.

Configure Webserver
-------------------

.. note::

    The Mosquitto server is running on port 1883 for tcp based connections and on 9001 for websocket connections.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ~/etc/services.d/mosquitto.ini with the following content:

.. code-block:: ini

 [program:mosquitto]
 directory=%(ENV_HOME)s/mosquitto
 environment=PATH=%(ENV_HOME)s/mosquitto/usr/bin/:%(ENV_HOME)s/mosquitto/usr/sbin/:%(ENV_PATH)s,LD_LIBRARY_PATH=%(ENV_HOME)s/mosquitto/usr/lib64
 command=mosquitto -c etc/mosquitto/mosquitto.conf

And now start the service:

::

 [isabell@stardust ~] supervisorctl reread
 autossh: available
 [isabell@stardust ~] supervisorctl update
 autossh: added process group
 [isabell@stardust ~] supervisorctl status
 mosquitto                       RUNNING   pid 16184, uptime 0:00:02

Finishing installation
======================

Now you can either try to connect your existing mqtt client, or connect to your broker via websocket and this page: `<http://www.hivemq.com/demos/websocket-client/>`_

User Management
===============

Adding a new user
-----------------

You can add a new user by running the following command. Be aware of the missing -c compared to the initial creation.

::

 [isabell@stardust ~]$ mosquitto_passwd mosquitto/etc/mosquitto/pwfile newUser
 Password:
 Reenter password:
 [isabell@stardust ~]$

Deleting a user
---------------

::

 [isabell@stardust ~]$ mosquitto_passwd -D mosquitto/etc/mosquitto/pwfile newUser
 [isabell@stardust ~]$

Updates
=======

For updating mosquitto, you'll need to 
- save your pwfile (~/mosquitto/etc/mosquitto/pwfile) and your config (~/mosquitto/etc/mosquitto/mosquitto.conf) to a folder outside of ~/mosquitto,
- stop mosquitto via supervisorctl, 
- repeat the download and extract RPMs steps from the installation, 
- restore your pwfile and your config back and 
- start mosquitto again.

----

Tested with Mosquitto 1.6.8, Uberspace 7.6.0.0

.. author_list::
