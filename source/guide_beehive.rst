.. author:: momoaux <momoaux@koma666.de>

.. tag:: web
.. tag:: agent
.. tag:: lang-go

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/beehive.png
      :align: center

#####
Beehive
#####

.. tag_list::

Beehive is an event and agent system, which allows you to create your own
agents that perform automated tasks triggered by events and filters. It is
modular, flexible and really easy to extend for anyone. It has modules
(we call them *Hives*), so it can interface with, talk to, or retrieve
information from Twitter, Tumblr, Email, IRC, Jabber, RSS, Jenkins, Hue - to
name just a few. Check out the full list of [available Hives](https://github.com/muesli/beehive/wiki/Available-Hives)
in our Wiki.

Connecting those modules with each other lets you create immensly useful agents.
----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Go <lang-go>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :manual:`Domains <web-domains>`

License
=======

Beehive is released under the `AGPL-3.0 License_`.

Prerequisites
=============

Nothing special
.. warning:: But be careful, Beehive has no login and defaults to bind to localhost. So to connect you should use ssh tunnel or use any kind of .htaccess Basic Auth or similar.

::


Installation
============

Install ``Beehive``:

.. code-block:: console

  [isabell@stardust ~]$ mkdir beehive
  [isabell@stardust ~]$ cd beehive
  [isabell@stardust beehive]$ wget https://github.com/muesli/beehive/releases/download/v0.4.0/beehive_0.4.0_Linux_x86_64.tar.gz
  [isabell@stardust beehive]$ tar -xzvf beehive_0.4.0_Linux_x86_64.tar.gz
  [isabell@stardust beehive]$ rm beehive_0.4.0_Linux_x86_64.tar.gz
  

Configuration
=============

Beehive will generate default config on startup

Web Backend Config
------------------

.. warning:: Beehive_ will bind to locahost per default. There is no login. Please make sure to secure it before using it with external interface.

.. include:: includes/web-backend.rst

Supervisord Daemon Setup
------------------------

Create ``~/etc/services.d/beehive.ini`` with the following content:

.. code-block:: ini

  [program:beehive]
  command=%(ENV_HOME)s/beehive/beehive
  autostart=yes
  autorestart=yes

.. warning:: If you want public access then use the following content (be sure to secure your access, beehive will not do this):

.. code-block:: ini 

  [program:beehive]
  command=%(ENV_HOME)s/beehive/beehive -bind "0.0.0.0:8181" -canonicalurl "https://isabell.uber.space"
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

Finishing installation
======================

With internal access go to ``http://localhost:8181``
with external access go to ``https://isabell.uber.space`` 
configure your bees.

I recommend using beehive without external domain. Simply use ssh tunnel for configuration so no auth is needed.

Updates
=======

Update by downloading new binary for x86 64 from https://github.com/muesli/beehive/releases and restarting the service with ``supervisorctl restart beehive``.

.. _Beehive: https://github.com/muesli/beehive
.. _Version 0.4.0: https://github.com/muesli/beehive/releases/tag/v0.4.0
.. _AGPL-3.0 License: https://github.com/muesli/beehive/blob/master/LICENSE

----

Tested on Uberspace U7 with Go v1.15.7, Beehive Version 0.4.0_

.. author_list::
