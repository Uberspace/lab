.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

#######
autossh
#######

autossh_ is a program to start a copy of ssh and monitor it, restarting it as necessary should it die or stop passing traffic.

When following best practices laid out by Uberspace (every service should use its own Uberspace account), it can sometimes become necessary to connect two Uberspace hosts with another privately. This is for example the case, if - for example - you are running an OpenLDAP installation on host A and want to use it for authentication for a nextCloud installation on host B. You wouldn't want the whole world to access your OpenLDAP server, right? autossh_ allows us to set up an automatically monitored tunnel between hosts to use for port forwarding.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * ssh
  * ssh port forwarding
  * ssh public key authentication
  * supervisord_

License
=======

autossh_ was written by `Carson Harding <http://www.harding.motd.ca/>`_ and released as freeware. It uses no known licensing model.


Installation
============

Step 1
------

Download the latest version of autossh_ from the website http://www.harding.motd.ca/autossh/index.html, extract it and enter the directory:

::

 [isabell@stardust ~] wget http://www.harding.motd.ca/autossh/autossh-99.9f.tgz
 [isabell@stardust ~] tar zxf autossh-99.9f.tgz
 [isabell@stardust ~] cd autossh-99.9f
 [isabell@stardust autossh-99.9f] 

Step 2
------

Run ``configure``, ``make`` and ``make install`` (the ``--prefix`` options tells make to install to your home directory):

::

 [isabell@stardust autossh-99.9f] ./configure --prefix=/home/isabell
 [...]
 [isabell@stardust autossh-99.9f] make
 [...]
 [isabell@stardust autossh-99.9f] make install
 [...]

After running ``make install``, ``which autossh`` should return ``~/bin/autossh``. If not, check the output of the respective commands for errors. That's it! Time to configure autossh!


Configuration and Usage
=======================

Step 1
------

In order to use autossh_ comfortably, we need to define a connection in our ``~/.ssh/config`` - for the sake of the example, let's assume the following connection in ``~/.ssh/config``:

::

 Host service-tunnel
  HostName tsudrats.uberspace.de
  User llebasi
  IdentityFile /home/isabell/.ssh/servicetunnel
  LocalForward 9000 localhost:9000


This configuration will forward the local port ``9000`` to the remote port ``9000``. It could be opened manually by calling ``ssh service-tunnel``.

.. note:: This guide assumes that you have set up public key authentication (see ``IdentityFile`` parameter in ``~/.ssh/config``). This is required as otherwise you will always be prompted for your password when trying to open the tunnel. See `the Uberspace manual <https://manual.uberspace.de/en/basics-ssh.html#working-with-keys>`_ for setting up public key authentication if you don't know how.

Step 2
------

With the information from step 1, it is time to configure supervisord_ to handle our autossh process. Create the file ``~/etc/services.d/autossh.ini`` with the following content:

::

 [program:autossh]
 command=%(ENV_HOME)s/bin/autossh -M 0 service-tunnel -T -N
 autostart=true
 autorestart=false

This will make sure that autossh_ is automatically started if the host reboots but ignore termination of autossh (which will only happen if there are repeated errors with the connection). ``-M 0`` will cause autossh to not send dummy data through the connection, ``-T -N`` will launch a non-interactive ssh connection. After you have created the file, update the control daemon:

::

 [isabell@stardust ~] supervisorctl reread
 autossh: available
 [isabell@stardust ~] supervisorctl update
 autossh: added process group

This will then launch autossh.

That's it, you have successfully configured an automatically launching port forwarding tunnel between to hosts!


.. _autossh: http://www.harding.motd.ca/autossh/
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

.. authors::
