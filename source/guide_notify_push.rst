.. highlight:: console
.. author:: Marius Bertram <marius@brtrm.de>


.. tag:: lang-rust
.. tag:: web
.. tag:: file-storage
.. tag:: sync

.. sidebar:: Logo

  .. image:: _static/images/nextcloud.svg
      :align: center

###########
notify_push
###########

.. tag_list::

notify_push is a backend service to inform Nextcloud clients on file changes.
The default behavior of the client is to periodically, at short intervals, request changes from the server.
This results in a large proportion of the server load.
With notify_push the requests can be greatly reduced.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`Nextcloud <guide_nextcloud>`
  * :lab:`redis <guide_redis>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

We need a running Nextcloud instance with  version >= 21.
With configured redis.

Installation
============

Install Client Push App in Nextcloud
------------------------------------
We need to install the `Client Push`_ app from the Nextcloud AppStore.

Install the latest release and make it executable:

.. code-block:: console

    [isabell@stardust ~]$ php html/occ app:install notify_push
    notify_push 0.2.2 installed
    notify_push enabled
    [isabell@stardust ~]$ chmod u+x html/apps/notify_push/bin/x86_64/notify_push
    [isabell@stardust ~]$ ln --symbolic --verbose $HOME/html/apps/notify_push/bin/x86_64/notify_push bin/notify_push
    ‘bin/notify_push’ -> ‘/home/isabell/html/apps/notify_push/bin/x86_64/notify_push’
    [isabell@stardust ~]$


Configuration
=============

Setup Supervisord
-----------------

Create the configuration ``${HOME}/etc/services.d/notify_push.ini``:

.. Note:: As argument we need to set the path to our ``config.php`` from our Nextcloud. Adjust the path to your location.

.. code-block:: ini

    [program:notify_push]
    command=notify_push %(ENV_HOME)s/html/config/config.php
    autostart=yes
    autorestart=yes

.. include:: includes/supervisord.rst


Configure the web backend
-------------------------

Create the web backend for notify_push:

.. Note:: The URL for notify_push should be the Nextcloud URL on path /push


.. code-block:: console

    [isabell@stardust ~]$ uberspace web backend set /push --http --port 7867
    Set backend for /push to port 7867; please make sure something is listening!
    You can always check the status of your backend using "uberspace web backend list".
    [isabell@stardust ~]$ uberspace web backend list
    /push http:7867 => OK, listening: PID 28088, notify_push /home/push/html/config/config.php
    / apache (default)
    [isabell@stardust ~]$


Add Uberspace user specific VETH IP to trusted proxies
------------------------------------------------------
We need to get the ip address:

.. code-block:: console
    :emphasize-lines: 2

    [isabell@stardust ~]$ ip route
    100.64.35.0/30 dev veth_isabell proto kernel scope link src 100.64.35.2
    [isabell@stardust ~]$

From the command above we get the ip ``100.64.35.2``

Now we add this ip to the trusted proxies list:

.. code-block:: console

   [isabell@stardust ~]$  php html/occ config:system:set trusted_proxies 0 --value="100.64.35.2"
   System config value trusted_proxies => 0 set to string 100.64.35.2
   [isabell@stardust ~]$


Configure Client Push App with the notify_push backend
------------------------------------------------------

To configure the notify_push app with the notify_push backend, run following command:

.. Note:: Use your URL

.. code-block:: console

    [isabell@stardust ~]$  php occ notify_push:setup https://isabell.uber.space/push
    ✓ redis is configured
    ✓ push server is receiving redis messages
    ✓ push server can load mount info from database
    ✓ push server can connect to the Nextcloud server
    ✓ push server is a trusted proxy
    ✓ push server is running the same version as the app
    configuration saved
    [isabell@stardust ~]$

Updates
=======

The app and the backend have to be on the same version.
After updating the app just restart the service so it runs the latest binary file.

If you are doing your updates with the script you may add the following line or you just run it via console.
.. code-block:: console

 supervisorctl restart notify_push

.. _`Client Push`: https://apps.nextcloud.com/apps/notify_push

----

Tested with Nextcloud 22.1.0,notify_push 0.2.2, Uberspace 7.11.3.0

.. author_list::
