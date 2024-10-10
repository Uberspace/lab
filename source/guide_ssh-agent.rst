.. highlight:: console

.. author:: Kai Moschcau <kmoschcau.de>

.. tag:: agent
.. tag:: console
.. tag:: ssh

#########
ssh-agent
#########

.. tag_list::

``ssh-agent`` is part of the `OpenSSH <https://www.openssh.com/>`_ suite of
tools and allows you to use password protected SSH keys, without having to enter
the key's password each time you use them. It already comes pre-installed on
uberspace servers. This guide explains how to use ``ssh-agent`` on these
servers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>` and especially :lab:`Generating keys and adding them to ssh-agent <howto_ssh-keys>`

License
=======

All relevant legal information can be found here

  * https://spdx.org/licenses/SSH-OpenSSH.html

Background
==========

``ssh-agent`` works in conjunction with ``ssh-add``, where the former persists
the unlocked SSH keys and the latter allows you to unlock and add those keys to
the former. The two communicate via a Unix socket, which is created in `/tmp`.
``ssh-add`` expects to be told about this socket's location via the
``$SSH_AUTH_SOCK`` environment variable. ``ssh-agent`` can give you this
information either by echoing it on start or starting a new shell session for
you with the environment variable already set.

Usually you would just execute ``ssh-agent`` in some shell startup script and
also check if an instance is already running. However the permissions on the
uberspace servers are set-up in a way that makes it impossible for you to see
the running ``ssh-agent`` process.

.. CAUTION::
   Take care to not just run ``ssh-agent`` in startup scripts on these servers
   or you will starve your account of resources and will not be able to SSH onto
   the server until staff terminates your running agents.

Because ``ssh-agent`` can only start wrapped commands or echo out its socket
location, it is unsuitable for use with
:manual:`supervisord <daemons-supervisord>`. You would still be able to
terminate the running ``ssh-agent`` this way, but you would have to figure out
the socket location on your own.

A final different possibility is to start the agent in debug-mode, to prevent it
from forking and thus still enabling you to terminate it, like so:

.. code-block:: console

   [isabell@stardust ~]$ ssh-agent -d
   SSH_AUTH_SOCK=/tmp/ssh-9oKXy8hxtdu9/agent.10869; export SSH_AUTH_SOCK;
   echo Agent pid 10869;
   debug2: fd 3 setting O_NONBLOCK

This gives you the socket location and by being a foreground process allows you
to terminate it, but now you either need to use your shell's job control or
start a second shell to be able to do anything.

Because of all the explained downsides, this guide instead uses ``ssh-agent`` to
start a new sub shell.

Prerequisites
=============

You already have an SSH key generated on the uberspace server where you want to
use it, and you are logged into that server with a shell session.

Starting a shell session with ssh-agent
=======================================

Start ``ssh-agent`` with ``$SHELL`` to use your current shell for the new
session, like so:

.. code-block:: console

   [isabell@stardust ~]$ ssh-agent $SHELL
   [isabell@stardust ~]$

Echoing the value of ``$SSH_AUTH_SOCK`` and ``$SSH_AGENT_PID`` should now return
values and ``ssh-add`` should now work in this new session.

.. code-block:: console

   [isabell@stardust ~]$ echo $SSH_AUTH_SOCK
   /tmp/ssh-KbEnRJzBcFzD/agent.19496
   [isabell@stardust ~]$ echo $SSH_AUTH_SOCK
   19497
   [isabell@stardust ~]$ ssh-add
   Enter passphrase for /home/isabell/.ssh/id_rsa:
   Identity added: /home/isabell/.ssh/id_rsa (/home/isabell/.ssh/id_rsa)
   [isabell@stardust ~]$

This key will now be unlocked until you exit the shell session.

Starting a session with a different command
-------------------------------------------

Besides ``$SHELL``, you can also use any other shell on the server. You can get
a list of those by using ``chsh``:

.. code-block:: console

   [isabell@stardust ~]$ chsh --list-shells
   /bin/sh
   /bin/bash
   /usr/bin/sh
   /usr/bin/bash
   /usr/bin/tmux
   /bin/tmux
   /usr/bin/fish
   /bin/ksh
   /bin/rksh
   /bin/zsh
   /bin/tcsh
   /bin/csh
   /usr/bin/pwsh
   [isabell@stardust ~]$

Additionally you can start any other program with ``ssh-agent``, though you
would need to figure out a different way of adding your key in this case.

----

Tested with OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017, Uberspace 7.16.1

.. author_list::
