.. highlight:: console

.. author:: Martin Porsch <https://github.com/kubiac/>

.. tag:: web
.. tag:: file-storage
.. tag:: sync

.. sidebar:: About

  .. image:: _static/images/resilio.png
      :align: center

############
Resilio Sync
############

.. tag_list::

Resilio_ (formerly BitTorrent Sync) is a proprietary file syncing service similar to Dropbox that works with private peer-to-peer connections between connected devices. The peer-to-peer technology is based on the BitTorrent protocol. Resilio Inc., the company behind Resilio Sync, uses a freemium business model with a free tier called "Sync Home".

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`ports <basics-ports>`

License
=======

All relevant legal information can be found here

  * http://www.resilio.com/legal/privacy
  * http://www.resilio.com/legal/terms-of-use
  * http://www.resilio.com/legal/eula

Installation
============

Change into the ``~/bin`` directory, download and extract the latest version of Resilio Sync:

::

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget https://download-cdn.resilio.com/stable/linux-x64/resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ tar --gzip --extract --file resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ rm resilio-sync_x64.tar.gz
 [isabell@stardust bin]$

Configure web server
====================

.. note::

    Resilio is running on port 9000.

.. include:: includes/web-backend.rst

Configure firewall port
=======================

Resilio Sync will work without this step, however, all connections will be routed through a relay server, since direct connections are blocked by the firewall.

.. include:: includes/open-port.rst

Configure Resilio Sync
======================

Create a config file ``~/.sync/resilio-sync.conf`` with the follwoing contents:

.. warning:: Replace ``<username>`` with your username and ``<port>`` with the apropiate port number, which was opened in the previous step (would be 40132 in our example).

.. code-block:: text 

 {
   "device_name": "Uberspace",
   "listening_port" : <port>, // 0 - randomize port

    "storage_path" : "/home/<username>/.sync",

    "webui" :
  	{
    	"listen" : "0.0.0.0:9000" // remove field to disable WebUI
	}
 }

Configure ``supervisord``
=========================

Create ``~/etc/services.d/resilio-sync.ini`` with the following content:

.. code-block:: ini

 [program:resilio-sync]
 command=rslsync --nodaemon --config /home/isabell/.sync/resilio-sync.conf

Start Service
=============

.. include:: includes/supervisord.rst

Now go to ``https://<username>.uber.space`` (would be ``https://isabell.uber.space`` in our example) and see if it works. Enjoy!

Update Resilio Sync
===================

The webinterface will notify you when a new version of Resilio Sync is available. To install the update, download the latest binaries, extract them, and restart the service:

::

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget https://download-cdn.resilio.com/stable/linux-x64/resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ supervisorctl stop resilio-sync
 [isabell@stardust bin]$ tar --gzip --extract --overwrite --file resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ rm resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ supervisorctl start resilio-sync
 [isabell@stardust bin]$

.. _Resilio: https://www.resilio.com

----

Tested with Resilio Sync 2.5.12, Uberspace 7.1.4.0

.. author_list::
