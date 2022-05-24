.. author:: imntl <max@mntl.de>

.. spelling::
  Uptime
  uptime
  Kuma

.. tag:: audience-admins
.. tag:: lang-nodejs
.. tag:: web
.. tag:: monitoring

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/uptime-kuma.svg
      :align: center

###########
Uptime-Kuma
###########

.. tag_list::

Uptime-Kuma_ provides a very simple web interface to monitor uptime for HTTP(s) / TCP / HTTP(s) Keyword / Ping / DNS Record / Push / Steam Game Server. Notifications can be send via Telegram, Discord, Gotify, Slack, Pushover, Email (SMTP), and `70+ notification services, click here for the full list <https://github.com/louislam/uptime-kuma/tree/master/src/components/notifications>`_. It is published under the MIT License.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Node and npm
------------

We're using :manual:`Node.js <lang-nodejs>` in the stable version 14:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '14'
 [isabell@stardust ~]$

We will need to update the Node Packet Manager npm:

::

  [isabell@stardust ~]$ npm install npm@latest -g
  + npm@8.3.0
  added 169 packages from 86 contributors, removed 157 packages and updated 45 packages in 22.432s
  [isabell@stardust ~]$ hash -r
  [isabell@stardust ~]$ npm --version
  8.3.0
  [isabell@stardust ~]$

This should return a version from ``8.0.0`` upwards.

Domain
------

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First get the Uptime-Kuma source code from Github_:

::

  [isabell@stardust ~]$ git clone https://github.com/louislam/uptime-kuma.git
  git clone https://github.com/louislam/uptime-kuma.git
  Cloning into 'uptime-kuma'...
  remote: Enumerating objects: 11158, done.
  remote: Counting objects: 100% (4844/4844), done.
  remote: Compressing objects: 100% (782/782), done.
  remote: Total 11158 (delta 4387), reused 4320 (delta 4049), pack-reused 6314
  Receiving objects: 100% (11158/11158), 3.14 MiB | 940.00 KiB/s, done.
  Resolving deltas: 100% (7999/7999), done.
  [isabell@stardust ~]$

You have now downloaded the master development branch which is sufficient. Everything else will be done by the setup itself.

.. code-block:: console
  :emphasize-lines: 1,2

  [isabell@stardust ~]$ cd ~/uptime-kuma
  [isabell@stardust uptime-kuma]$ npm run setup
  npm WARN lifecycle The node binary used for scripts is /usr/bin/node but npm is using /opt/nodejs14/bin/node itself. Use the `--scripts-prepend-node-path` option to include the path for the node binary npm was executed with.
      > uptime-kuma@1.11.1 setup /home/isabell/uptime-kuma
  > git checkout 1.11.1 && npm ci --production && npm run download-dist
  […]
  HEAD is now at 8bb8b0a update to 1.11.1
  […]
  [program:uptime-kuma]
  found 0 vulnerabilities
  > uptime-kuma@1.11.1 download-dist
  > node extra/download-dist.js
  Downloading dist
  […]
  Done  
  [isabell@stardust uptime-kuma]$


You maybe got the error that there are vulnerabilities to fix, if so follow the instruction and run ``npm audit fix`` to install the latest package versions:

::

  [isabell@stardust ~]$ cd ~/uptime-kuma
  [isabell@stardust server]$ npm audit fix
  [...]
  found 0 vulnerabilities
  [isabell@stardust server]$

Configuration
=============

Configure web server
--------------------

.. note::

    Uptime-Kuma is running on port 3001.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/uptime-kuma.ini`` with the following content:

.. code-block:: ini

 [program:uptime-kuma]
 directory=%(ENV_HOME)s/uptime-kuma/
 command=node %(ENV_HOME)s/uptime-kuma/server/server.js
 startsecs=60

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Check Website
-------------

Point your browser to your domain for example https://isabell.uber.space

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Update git
----------

Check Uptime-Kuma's `releases <https://github.com/louislam/uptime-kuma/releases>`_ for the latest version and exchange the pseudo version number ``1337.1.3`` here with the latest version number.

.. code-block:: console
  :emphasize-lines: 1,2,3

  [isabell@stardust ~]$ cd ~/uptime-kuma
  [isabell@stardust uptime-kuma]$ git fetch --all
  [isabell@stardust uptime-kuma]$ git checkout 1337.1.3 --force
  [isabell@sturdust uptime-kuma]$

Install dependencies and prebuilt
---------------------------------

.. code-block:: console
  :emphasize-lines: 1,2,3

  [isabell@stardust ~]$ cd ~/uptime-kuma
  [isabell@stardust uptime-kuma]$ npm ci --production
  [isabell@stardust uptime-kuma]$ npm run download-dist


Restart service after update
----------------------------

.. code-block:: console
  :emphasize-lines: 1,4

  [isabell@stardust ~]$ supervisorctl restart uptime-kuma
  uptime-kuma: stopped
  uptime-kuma: started
  [isabell@stardust ~]$ supervisorctl status
  uptime-kuma                            RUNNING   pid 20516, uptime 0:01:14

.. _Uptime-Kuma: https://github.com/louislam/uptime-kuma
.. _Github: https://github.com/louislam/uptime-kuma
.. _feed: https://github.com/louislam/uptime-kuma/releases

----

Tested with Uptime-Kuma 1.15.1 and Uberspace 7.12.2

.. author_list::
