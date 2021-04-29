.. author:: Sven <mail@klomp.eu>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: programming

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/node-red.svg
      :align: center

########
Node-RED
########

.. tag_list::

Node-RED_ is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways.

It provides a browser-based editor that makes it easy to wire together flows using the wide range of nodes in the palette that can be deployed to its runtime in a single-click.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 12:

::

 [isabell@stardust ~]$ uberspace tools version use node 12
 Using 'Node.js' version: '12'
 Selected node version 12
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [eliza@dolittle ~]$

Your domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Use ``npm`` to install ``node-red`` globally.

::

 [isabell@stardust ~]$ npm install -g --unsafe-perm node-red
 [...]
 + node-red@1.3.3
 added xx package in yys


Configuration
=============

Setup daemon
------------

Create ``~/etc/services.d/node-red.ini`` with the following content:

.. code-block:: ini

 [program:node-red]
 command=node-red
 autostart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.


Configure web server
--------------------

Node-RED is listening on port 1880 and cannot be accessed from outside, yet.
To make it accessible, configure a `web backend <webbackend_>`_:

::

  [isabell@stardust ~]$ uberspace web backend set /node-red --http --port 1880 --remove-prefix
  Set backend for /node-red to port 1880; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html



Node-RED can now be accessed via https://isabell.uber.space/node-red.

.. note::
    If you get an error like `Cannot GET /nodered`, you most probably missed the command line parameter ``--remove-prefix`` while setting up the web backend.

Securing
========

.. note::

    By default, Node-RED is accessible by everyone without a password!


At least, an admin and editor password should be set as described in the Node-RED documentation (https://nodered.org/docs/user-guide/runtime/securing-node-red#editor--admin-api-security). The configuration file is located at ``~/.node-red/settings.js``.

After changing the configuration, restart Node-RED to reload configuration:

::

 [isabell@stardust ~]$ supervisorctl restart node-red
 node-red: stopped
 node-red: started
 [isabell@stardust ~]$ supervisorctl status
 node-red                         RUNNING   pid 21665, uptime 0:00:22
 [isabell@stardust ~]$


Updates
=======

To update Node-RED

::

 [isabell@stardust ~]$ npm update -g node-red
 [...]
 + node-red@1.3.4
 updated 7 packages in 29.546s


.. _Node-RED: https://nodered.org/

----

Tested with Node-RED 1.3.4, Uberspace 7.11.0.0

.. author_list::
