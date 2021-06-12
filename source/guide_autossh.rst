.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

.. tag:: lang-c
.. tag:: console
.. tag:: automation

#######
autossh
#######

.. tag_list::

.. abstract::
  autossh_ is a program to start an SSH session and monitor it, restarting it as necessary should it die or stop passing traffic.

  When following best practices laid out by Uberspace (every service should use its own Uberspace account), it can sometimes be necessary to connect two Uberspace hosts with each other privately. For example, this is  the case if you are running an OpenLDAP installation on host A and want to use it for authentication for a Nextcloud installation on host B. autossh_ allows you to set up an automatically monitored tunnel between hosts to use for port forwarding.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * SSH port forwarding
  * SSH public key authentication
  * :manual:`supervisord <daemons-supervisord>`

License
=======

autossh_ was written by `Carson Harding <http://www.harding.motd.ca/>`_ and released as freeware. It uses no known licensing model.


Installation
============

Download the latest version of autossh_ from the website http://www.harding.motd.ca/autossh/index.html, extract it and enter the directory:

::

 [isabell@stardust ~] wget https://www.harding.motd.ca/autossh/autossh-1.4g.tgz
 [isabell@stardust ~] tar zxf autossh-1.4g.tgz
 [isabell@stardust ~] cd autossh-1.4g
 [isabell@stardust autossh-1.4g]

Run ``configure``, ``make`` and ``make install`` (the ``--prefix`` options tells make to install to your home directory):

::

 [isabell@stardust autossh-1.4g] ./configure --prefix=$HOME
 [...]
 [isabell@stardust autossh-1.4g] make
 [...]
 [isabell@stardust autossh-1.4g] make install
 [...]

After running ``make install``, ``which autossh`` should return ``~/bin/autossh``. If not, check the output of the respective commands for errors.


Configuration and Usage
=======================

SSH Tunnel
----------

In order to use autossh_ comfortably, you need to define a connection in your ``~/.ssh/config`` - for the sake of the example, let's assume the following connection in ``~/.ssh/config``:

::

 Host service-tunnel
  HostName tsudrats.uberspace.de
  User llebasi
  IdentityFile ~/.ssh/servicetunnel
  LocalForward 9000 localhost:9000


This configuration will forward the local port ``9000`` to the remote port ``9000``. It could be opened manually by calling ``ssh service-tunnel``.

To ensure that the remote host and it's key fingerprint are trusted, either add them manually to your ``~/.ssh/known_hosts`` or connect to the host once, check the fingerprint and then answer ``yes`` when prompted.

::

 [isabell@stardust ~] ssh llebasi@tsudrats.uberspace.de exit
 The authenticity of host 'tsudrats.uberspace.de (185.26.156.254)' can't be established.
 ED25519 key fingerprint is SHA256:taekOiAJ0efuyKpBtDKuE9c04LXJqJhVNcP1ltr798E.
 ED25519 key fingerprint is MD5:dc:df:0a:f7:2c:cd:62:8a:7e:a3:d7:a1:43:56:0c:36:0.
 Are you sure you want to continue connecting (yes/no)? yes
 Warning: Permanently added 'tsudrats.uberspace.de,185.26.156.254' (ED25519) to the list of known hosts.

.. note:: This guide assumes that you have set up public key authentication (see ``IdentityFile`` parameter in ``~/.ssh/config``). This is required as otherwise you will always be prompted for your password when trying to open the tunnel. See :manual_anchor:`the Uberspace manual <basics-ssh.html#working-with-keys>` for setting up public key authentication if you don't know how.

Daemon Setup
------------

With the information from the earlier step, it is time to configure :manual:`supervisord <daemons-supervisord>` to handle our autossh process. Create the file ``~/etc/services.d/autossh.ini`` with the following content:

::

 [program:autossh]
 command=autossh -M 0 service-tunnel -T -N
 autostart=true
 autorestart=false

This will make sure that autossh_ is automatically started if the host reboots but ignore termination of autossh (which will only happen if there are repeated errors with the connection). ``-M 0`` will cause autossh not to send dummy data through the connection, ``-T -N`` will launch a non-interactive ssh connection.

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, something went wrong.

That's it, you have successfully configured an automatically launching port forwarding tunnel between to hosts!


.. _autossh: http://www.harding.motd.ca/autossh/

.. author_list::
