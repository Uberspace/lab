.. author:: momoaux <momoaux@koma666.de>

.. tag:: web
.. tag:: agent
.. tag:: lang-go

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/beehive.png
      :align: center

#######
Beehive
#######

.. tag_list::

Beehive is an event and agent system, which allows you to create your own
agents that perform automated tasks triggered by events and filters. It is
modular, flexible and really easy to extend for anyone. It has modules
(we call them *Hives*), so it can interface with, talk to, or retrieve
information from Twitter, Tumblr, Email, IRC, Jabber, RSS, Jenkins, Hue - to
name just a few. Check out the full list of `available Hives`_
in our Wiki.

Connecting those modules with each other lets you create immensely useful
agents.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Go <lang-go>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :manual:`Domains <web-domains>`

License
=======

Beehive is released under the `AGPL-3.0 License`_.


Installation
============

Check for the latest version on the Beehive `release page <https://github.com/muesli/beehive/releases>`_, then download
and unpack that version and move the binary to ``~/bin``:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/tmp
  [isabell@stardust beehive]$ wget https://github.com/muesli/beehive/releases/download/v0.4.0/beehive_0.4.0_Linux_x86_64.tar.gz
  [isabell@stardust beehive]$ tar -xzvf beehive_0.4.0_Linux_x86_64.tar.gz
  [isabell@stardust beehive]$ mv beehive ~/bin
  [isabell@stardust beehive]$


Configuration
=============

Beehive will generate default config in the working directory, we will use the ``--config`` flag to store the config
file in ``~/etc/beehive.conf``.

Supervisord Daemon Setup
------------------------

Create ``~/etc/services.d/beehive.ini`` with the following content:

.. code-block:: ini

  [program:beehive]
  command=beehive --config ~/etc/beehive.conf
  autostart=yes
  autorestart=yes
  startsecs=30s

.. include:: includes/supervisord.rst

Finishing installation
======================

Since Beehive does not support any kind of authentication we will not make it public using a web backend but use
`SSH port forwarding`_ to create a secure tunnel from your local device. To do so, execute the following on your
**local device**:

.. code-block:: console

  [you@localhost ~]$ ssh -L 8181:localhost:8181 isabell@stardust.uberspace.de -N -v
  [...]
  debug1: Connection to port 8181 forwarding to localhost port 8181 requested.

Now you can open ``http://localhost:8181`` in your browser and this will forward to the Uberspace and deliver the
Beehive web frontend.

Updates
=======

Update by downloading new binary for x86 64 from https://github.com/muesli/beehive/releases and restarting the service with ``supervisorctl restart beehive``.

.. _Beehive: https://github.com/muesli/beehive
.. _Version 0.4.0: https://github.com/muesli/beehive/releases/tag/v0.4.0
.. _AGPL-3.0 License: https://github.com/muesli/beehive/blob/master/LICENSE
.. _available Hives: https://github.com/muesli/beehive/wiki/Available-Hives
.. _SSH port forwarding: https://www.ssh.com/ssh/tunneling/example

----

Tested on Uberspace U7 with Go v1.15.7, Beehive `Version 0.4.0`_

.. author_list::
