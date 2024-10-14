.. highlight:: console

.. author:: fap <https://github.com/fapdash/>

.. tag:: lang-go
.. tag:: web
.. tag:: inventory
.. tag:: inventory-management

.. sidebar:: Logo

  .. image:: _static/images/homebox.svg
      :align: center


#######
Homebox
#######

.. tag_list::

Homebox_ is an open source inventory and organization system built for the Home User.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

Set up a subdomain and associate the web backend with it
--------------------------------------------------------

First add a new subdomain and then associate the homebox default port with that subdomain:

.. code-block:: console

 [isabell@stardust ~]$ uberspace web domain add homebox.example.com
 The webserver's configuration has been adapted.
 Now you can use the following records for your DNS:
     A -> 35.195.215.42
     AAAA -> 2a00:1450:4005:802::200e
 [isabell@stardust ~]$ uberspace web backend set homebox.example.com --http --port 7745
 [isabell@stardust ~]$

The ``uberspace web domain add`` command will return different instructions / ip addresses
on your system. Be sure to use the output from your command executions and not
from this tutorial.

.. note:: Don't forget to add the subdomain into the DNS record of your DNS provider.

Installation
============

The official documentation_ recommends using Docker, but since Uberspace
doesn't support Docker and the Docker container doesn't do that much
we set up the application as a :manual:`supervisord <daemons-supervisord>` process.

.. _download-latest-release-and-extract:

Download latest release and extract
-----------------------------------

Download the latest release from the GitHub releases_ page:

.. code-block:: console

 [isabell@stardust ~]$ wget https://github.com/hay-kot/homebox/releases/download/v0.10.3/homebox_Linux_x86_64.tar.gz
 [isabell@stardust ~]$ mkdir -p ~/homebox/data
 [isabell@stardust ~]$ tar -xf homebox_Linux_x86_64.tar.gz -C ~/homebox
 [isabell@stardust ~]$

Create supervisord service and start the app
--------------------------------------------

Create the supervisord entry at ``~/etc/services.d/homebox.ini``:

.. code-block:: ini

 [program:homebox]
 directory=%(ENV_HOME)s/homebox
 command=%(ENV_HOME)s/homebox/homebox
 environment=HBOX_MODE="production",HBOX_STORAGE_DATA="%(ENV_HOME)s/homebox/data/",HBOX_STORAGE_SQLITE_URL="%(ENV_HOME)s/homebox/data/homebox.db?_fk=1"
 autostart=true
 autorestart=true
 stderr_logfile = %(ENV_HOME)s/homebox/err.log
 stdout_logfile = %(ENV_HOME)s/homebox/out.log
 startsecs=60

After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 homebox: available
 [isabell@stardust ~]$ supervisorctl update
 homebox: added process group
 [isabell@stardust ~]$

Great, you're done. Your homebox installation should be reachable at https://homebox.example.com now.
There is no default admin account. The application starts with registrations opened.

Closing user registration
=========================

Since the app is now publicly available on the internet it might be a good idea to close
down registration once you have created the accounts that you need.
Create the accounts you want, then close registration by setting ``HBOX_OPTIONS_ALLOW_REGISTRATION`` to ``false`` in the supervisord ini:

.. code-block:: ini
 :emphasize-lines: 4

 [program:homebox]
 directory=%(ENV_HOME)s/homebox
 command=%(ENV_HOME)s/homebox/homebox
 environment=HBOX_MODE="production",HBOX_STORAGE_DATA="%(ENV_HOME)s/homebox/data/",HBOX_STORAGE_SQLITE_URL="%(ENV_HOME)s/homebox/data/homebox.db?_fk=1",HBOX_OPTIONS_ALLOW_REGISTRATION="false"
 autostart=true
 autorestart=true
 stderr_logfile = %(ENV_HOME)s/homebox/err.log
 stdout_logfile = %(ENV_HOME)s/homebox/out.log
 startsecs=60

Then restart the service

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl update
 homebox: stopped
 homebox: updated process group
 [isabell@stardust ~]$

Updates
=======

To update Homebox repeat the steps described in :ref:`download-latest-release-and-extract`.
After updating the binary tell :manual:`supervisord <daemons-supervisord>` to restart the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl restart homebox
 homebox: stopped
 homebox: started
 [isabell@stardust ~]$ supervisorctl status
 homebox                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$


----

Tested with Homebox 0.10.8, Uberspace 7.15.15

..
  ##### Link section #####

.. _Homebox: https://hay-kot.github.io/homebox/
.. _releases: https://github.com/hay-kot/homebox/releases
.. _documentation: https://hay-kot.github.io/homebox/quick-start/

.. author_list::
