.. highlight:: console

.. author:: revilowaldow <oliver@warlow.engineer>
.. author:: Glumbosch <glumbosch.home.blog>

.. tag:: multiplayer
.. tag:: tabletop
.. tag:: RPG

.. sidebar:: Logo

  .. image:: _static/images/foundryvtt.png
      :align: center

############
Foundry VTT
############

.. tag_list::

`Foundry Virtual Tabletop <https://foundryvtt.com/>`_ is an alternative to Roll20 and many other platforms that enable you to play tabletop role playing games online.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :manual:`Domains <web-domains>`

License
=======

Foundry Virtual Tabletop is not free software, but you can host it on your own server.

Prerequisites
==============

You need to purchase a `license key <https://foundryvtt.com/purchase/>`_ to run your own version of Foundry Virtual Tabletop.

Foundry requires the use of :manual:`Node.js <lang-nodejs>` 14.

::

 [isabell@stardust ~]$ uberspace tools version use node 14
 Using 'Node.js' version: '14'
 Selected node version 14
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Set up your domain:

.. include:: includes/web-domain-list.rst

Installation
============

Prepare installation folders
----------------------------

Create the required directories:

::

  [isabell@stardust ~]$ mkdir ~/foundryvtt
  [isabell@stardust ~]$ mkdir ~/foundrydata
  [isabell@stardust ~]$

Download and unpack the archive
-------------------------------

You will need to get your link from the Foundry VTT website, the link expires after a few minutes. Use the following command to download Foundry, replace ``<yourlink>`` with your personal link to the archive, choose the linux version.

::

  [isabell@stardust ~]$ cd ~/foundryvtt
  [isabell@stardust foundryvtt]$ wget -O foundryvtt.zip "<yourlink>"
  [isabell@stardust foundryvtt]$

After the download has completed, extract the archive with the following command:

::

  [isabell@stardust foundryvtt]$ unzip foundryvtt.zip
  Archive:  foundryvtt.zip
  [isabell@stardust foundryvtt]$


Configuration
=============

Configure web server
--------------------

.. note::

    Foundry is running on port 30000.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/foundry.ini`` with the following content:

.. code-block:: ini

 [program:foundry]
 command=node %(ENV_HOME)s/foundryvtt/resources/app/main.js --dataPath=%(ENV_HOME)s/foundrydata
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your installation (https://isabell.uber.space) and follow the instructions.

Best practices
==============

Security
--------

  * Change the default admin password in the config tab **immediately** after installation.
  * When you create a new world in Foundry it does not have a password by default. Keep in mind to setup a password after world creation.

----

Tested with Foundry 0.8.7, Uberspace 7.1.1

.. author_list::
