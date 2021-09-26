.. highlight:: console
.. author:: Marius Bertram <marius@brtrm.de>
.. author:: EV21 <uberlab@ev21.de>

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

We need a running Nextcloud instance with  version >= 21 with configured redis.

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
    /push http:7867 => OK, listening: PID 28088, notify_push /home/isabell/html/config/config.php
    / apache (default)
    [isabell@stardust ~]$


Add Uberspace user specific VETH IP to trusted proxies
------------------------------------------------------
We need to get the IP address:

.. code-block:: console
    :emphasize-lines: 2

    [isabell@stardust ~]$ ip route
    10x.xx.xx.x/30 dev veth_isabell proto kernel scope link src 10x.xx.xx.x
    [isabell@stardust ~]$

From the output of the command above we get the IP ``10x.xx.xx.x``

Now we add this IP to the trusted proxies list:

.. code-block:: console

   [isabell@stardust ~]$  php html/occ config:system:set trusted_proxies 0 --value="10x.xx.xx.x"
   System config value trusted_proxies => 0 set to string 10x.xx.xx.x
   [isabell@stardust ~]$


Configure Client Push App with the notify_push backend
------------------------------------------------------

To configure the notify_push app with the notify_push backend, run following command:

.. Note:: Use your URL

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ php html/occ notify_push:setup https://isabell.uber.space/push
    ✓ redis is configured
    ✓ push server is receiving redis messages
    ✓ push server can load mount info from database
    ✓ push server can connect to the Nextcloud server
    ✓ push server is a trusted proxy
    ✓ push server is running the same version as the app
    configuration saved
    [isabell@stardust ~]$

You can test that all clients to a given user (in this case isabell) are receiving push notifications with the following command:

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ php ~/html/occ notification:test-push isabell
    Trying to push to 2 devices

    Language is set to de
    Private user key size: 4242
    Public user key size: 420
    Identified 1 Talk devices and 1 others.

    Device token:4242
    Device public key size: 420
    Data to encrypt is: {"nid":420,"app":"admin_notifications","subject":"Testing push notifications","type":"admin_notifications","id":"6424242a"}
    Signed encrypted push subject
    Push notification sent successfully
    [isabell@stardust ~]$ php ~/html/occ notify_push:metrics
    Active connection count: 2
    Total connection count: 5
    Total database query count: 2
    Events received: 9
    Messages send: 10
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

Tested with Nextcloud 22.1.1, notify_push 0.2.4, Uberspace 7.11.4

.. author_list::
