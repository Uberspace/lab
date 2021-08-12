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
We need to install the client_push_app from the Nextcloud AppStore.

`Client Push`_

Download Binary
---------------
Download the latest release and make it executable:

.. code-block:: console

    [isabell@stardust ~]$ curl -L https://github.com/nextcloud/notify_push/releases/latest/download/notify_push-x86_64-unknown-linux-musl -o ${HOME}/bin/notify_push
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
        100   169  100   169    0     0    401      0 --:--:-- --:--:-- --:--:--   402
    [isabell@stardust ~]$ chmod u+x ${HOME}/bin/notify_push
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
    enviroment=PORT=7867
    autostart=yes
    autorestart=yes

After creating the configuration, tell supervisord to refresh its configuration and start the service:

.. code-block:: console

    [isabell@stardust ~]$ supervisorctl reread
    SERVICE: available
    [isabell@stardust ~]$ supervisorctl update
    SERVICE: added process group
    [isabell@stardust ~]$ supervisorctl status
    notify_push                      RUNNING   pid 28088, uptime 0:00:07
    [isabell@stardust ~]$


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
    :emphasize-lines: 10

    [isabell@stardust ~]$ ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
        valid_lft forever preferred_lft forever
    71: veth_isabell@if72: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 42:2e:5c:a9:10:a6 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 100.64.35.2/30 scope global veth_push
       valid_lft forever preferred_lft forever
    inet6 fd75:6272:7370:23::2/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::402e:5cff:fea9:10a6/64 scope link 
       valid_lft forever preferred_lft forever
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

Updating
--------

The app and the backend have to be on the same version.
After updating the app just stop the service an replace the binary with the newer version.

.. _`Client Push`: https://apps.nextcloud.com/apps/notify_push

----

Tested with Nextcloud 22.1.0, Uberspace 7.11.3.0

.. author_list::
