.. highlight:: console

.. author:: Martin Porsch <martin.pors.ch/martin@pors.ch>

.. sidebar:: About
  
  .. image:: _static/images/resilio.png 
      :align: center

############
Resilio Sync
############

Resilio-Sync_ (formerly BitTorrent Sync) is a private file syncing similar to Dropbox that works with peer to peer cennections between connected devices. 
----

.. note:: For this guide you should be familiar with the basic concepts of 

  * supervisord_
  * domains_

Prerequisites
=============

We need to set up some directories in order to make it work:

::

 [isabell@stardust ~]$ mkdir -p ~/bin/resilio
 [isabell@stardust ~]$ mkdir ~/.sync
 [isabell@stardust ~]$ 

You need a free port that Reslio-Sync can listen to. To generate a currently unoccupied port run:
.. code-block:: none

 [isabell@stardust ~]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9000
 [isabell@stardust ~]$ 

Write the port down. In our example it is 9000. In reality you'll get a free port between 61000 and 65535.

Furthermore, we need a subdomain that we want Resilio-Sync to run on. In our guide we will use ``https://resilio.isabell.uber.space``. Create the corresponding directory as follows:

::

 [isabell@stardust ~]$ mkdir /var/www/virtual/isabell/resilio.isabell.uber.space
 [isabell@stardust ~]$ 


Installation
============

Change into the newly created reslio directory, download and extract the latest version of Resilio-Sync:

::

 [isabell@stardust ~]$ cd ~/bin/resilio
 [isabell@stardust ~]$ wget https://download-cdn.resilio.com/stable/linux-x64/resilio-sync_x64.tar.gz
 [isabell@stardust ~]$ tar -zxf resilio-sync_x64.tar.gz
 [isabell@stardust ~]$ rm resilio-sync_x64.tar.gz
 [isabell@stardust ~]$ 

Setup .htaccess
===============

Create ``/var/www/virtual/isabell/resilio.isabell.uber.space/.htaccess`` with the following content:

.. warning:: Replace ``<PORT>`` with your port!

.. code-block:: .htaccess

 RewriteEngine On
 RewriteRule (.*) http://localhost:<PORT>/$1 [P]
 DirectoryIndex disabled

In our example this would be:

.. code-block:: .htaccess

 RewriteEngine On
 RewriteRule (.*) http://localhost:90000/$1 [P]
 DirectoryIndex disabled

Configure ``supervisord``
=========================

Create ``~/etc/services.d/resilio-sync.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username!
.. warning:: Replace ``<PORT>`` with your port!

.. code-block:: ini

 [program:resilio-sync]
 command=/home/<username>/bin/resilio/rslsync --webui.listen 0.0.0.0:<PORT> --nodaemon --log /home/<username>/logs/resilio-sync.log --storage /home/<username>/.sync

In our example this would be:

.. code-block:: ini

 [program:resilio-sync]
 command=/home/isabell/bin/resilio/rslsync --webui.listen 0.0.0.0:90000 --nodaemon --log /home/isabell/logs/resilio-sync.log --storage /home/isabell/.sync

Start Service
=============

Now you need to load you changes and start your service:

::

 [isabell@stardust ~]$ supervisorctl reread
 [isabell@stardust ~]$ supervisorctl update
 [isabell@stardust ~]$ supervisorctl start resilio-sync

Nor go to ``https://resilio.isabell.uber.space`` and see if it works. Enjoy!

.. _Resilio-Sync: https://www.resilio.com

----

Tested with Resilio-Sync 2.5.12, Uberspace 7.1.4.0
