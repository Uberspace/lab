.. highlight:: console

.. author:: Martin Porsch <https://github.com/kubiac/>

.. sidebar:: About
  
  .. image:: _static/images/resilio.png 
      :align: center

############
Resilio Sync
############

Resilio_ (formerly BitTorrent Sync) is a proprietary file syncing service similar to Dropbox that works with private peer-to-peer connections between connected devices. The peer-to-peer technology is based on the BitTorrent protocol. Resilio Inc., the company behind Resilio Sync, uses a freemium business model with a free tier called "Sync Home".

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * supervisord_
  * domains_

License
=======

All relevant legal information can be found here 

  * http://www.resilio.com/legal/privacy
  * http://www.resilio.com/legal/terms-of-use
  * http://www.resilio.com/legal/eula

Prerequisites
=============

We need a free port that Resilio Sync can listen to. To discover a currently unoccupied port run:

.. include:: includes/generate-port.rst

Installation
============

Change into the ``~/bin`` directory, download and extract the latest version of Resilio Sync:

::

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget https://download-cdn.resilio.com/stable/linux-x64/resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ tar --gzip --extract --file resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ rm resilio-sync_x64.tar.gz
 [isabell@stardust bin]$ 

Setup .htaccess
===============

Create ``~/html/.htaccess`` with the following content:

.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: .htaccess

 RewriteEngine On
 RewriteRule (.*) http://localhost:<yourport>/$1 [P]
 DirectoryIndex disabled

In our example this would be:

.. code-block:: .htaccess

 RewriteEngine On
 RewriteRule (.*) http://localhost:9000/$1 [P]
 DirectoryIndex disabled

Configure ``supervisord``
=========================

Create ``~/etc/services.d/resilio-sync.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! Replace ``<yourport>`` with your port!

.. code-block:: ini

 [program:resilio-sync]
 command=/home/<username>/bin/rslsync --webui.listen 0.0.0.0:<yourport> --nodaemon --storage /home/<username>/.sync

In our example this would be:

.. code-block:: ini

 [program:resilio-sync]
 command=/home/isabell/bin/rslsync --webui.listen 0.0.0.0:9000 --nodaemon --storage /home/isabell/.sync

Start Service
=============

Now you need to load the changes and start your service:

::

 [isabell@stardust ~]$ supervisorctl reread
 [isabell@stardust ~]$ supervisorctl update
 [isabell@stardust ~]$ 

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
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html

----

Tested with Resilio Sync 2.5.12, Uberspace 7.1.4.0
