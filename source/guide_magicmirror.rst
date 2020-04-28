.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: smart-mirror

.. sidebar:: Logo

  .. image:: _static/images/magicmirror.png
      :align: center

############
MagicMirror²
############

.. tag_list::

MagicMirror²_ is an open source modular smart mirror platform. With a growing list of installable modules, the MagicMirror² allows you to convert your hallway or bathroom mirror into your personal assistant. MagicMirror² is built by the creator of the original MagicMirror with the incredible help of a growing community of contributors.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Node and npm
------------

We're using :manual:`Node.js <lang-nodejs>` in the latest version:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '12'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We clone the repository to our home directory and install the application.

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/MichMich/MagicMirror
 [isabell@stardust ~]$ cd MagicMirror
 [isabell@stardust MagicMirror]$ npm install
 […]
 [isabell@stardust MagicMirror]$ npm audit fix --force
 […]
 [isabell@stardust MagicMirror]$

Configuration
=============

After the installation you need to setup your config file.

.. code-block:: console

 [isabell@stardust MagicMirror]$ cp config/config.js.sample config/config.js
 [isabell@stardust MagicMirror]$

Change the address from ``localhost`` to ``0.0.0.0``. You may remove the IP addresses in ``ipWhitelist`` to access your MagicMirror² from everywhere.

.. code-block:: javascript
 :emphasize-lines: 1

      address: "0.0.0.0",

Setup daemon
------------

Create ``~/etc/services.d/magicmirror.ini`` with the following content:

.. code-block:: ini

 [program:magicmirror]
 directory=%(ENV_HOME)s/MagicMirror
 command=npm run server
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::

    MagicMirror² running on port 8080.

.. include:: includes/web-backend.rst

Updates
-------

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Stop your service and repeat the installation step.

.. _MagicMirror²: https://magicmirror.builders/
.. _feed: https://github.com/MichMich/MagicMirror/releases

----

Tested with MagicMirror² v2.10.1 and Uberspace 7.5.1

.. author_list::
