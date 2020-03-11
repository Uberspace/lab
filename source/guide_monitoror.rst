.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/monitoror.png
      :align: center

#########
Monitoror
#########

.. tag_list::

Monitoror_ is a wallboard monitoring app to monitor server status; monitor CI builds progress or even display critical values.

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

First we create an installation directory and then we need to configure the `web backend <webbackend_>`_.

.. code-block:: console

  [isabell@stardust ~]$ mkdir monitoror
  [isabell@stardust ~]$ uberspace web backend set / --http --port 8080
  Set backend for / to port 8080; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html

Installation
============

Like a lot of Go software, Monitoror is distributed as a single binary. Download Monitoror's latests `release with the following command.

.. code-block:: console

  [isabell@stardust ~]$ cd monitoror
  [isabell@stardust monitoror]$ curl -sL -o monitoror $(curl -s https://api.github.com/repos/monitoror/monitoror/releases/latest | grep 'browser_download_url.*monitoror-linux-amd64' | cut -d: -f2,3 | tr -d \")
  [isabell@stardust monitoror]$ chmod +x monitoror
  [isabell@stardust monitoror]$

Configuration
=============

Config file
-----------

Documentation for the config file can be found on the Monitoror's documentation_ site.

.. code-block:: console

  [isabell@stardust monitoror]$ touch config.json
  [isabell@stardust monitoror]$

Setup daemon
------------

Create ``~/etc/services.d/monitoror.ini`` with the following content.

.. code-block:: ini

  [program:monitoror]
  command=%(ENV_HOME)s/monitoror/monitoror
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

Finishing installation
======================

Point your webbrowser to: ``https://isabell.uber.space/?configPath=/home/isabell/monitoror/config.json``. You can also host your config file in a webdirectory and change the URL to ``https://isabell.uber.space/?configUrl=https://example.isabell.uber.space/config.json``.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Monitoror's `releases <https://github.com/monitoror/monitoror/releases/>`_ for the latest version. If a newer version is available, stop daemon by ``supervisorctl stop monitoror`` and repeat the "Installation" step followed by ``supervisorctl start monitoror`` to restart Monitoror.

.. _Monitoror: https://monitoror.com/
.. _documentation: https://monitoror.com/documentation/
.. _feed: https://github.com/monitoror/monitoror/releases.atom

----

Tested with Monitoror 3.0.0, Uberspace 7.4.2

.. author_list::
