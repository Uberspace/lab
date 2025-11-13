.. highlight:: console

.. author:: Patric Eckhart <mail@patriceckhart.com>

.. tag:: database
.. tag:: event-sourcing
.. tag:: event-store
.. tag:: event-storming
.. tag:: event-driven
.. tag:: event-driven-architecture
.. tag:: event-driven-design
.. tag:: event-driven-development
.. tag:: event-driven-architecture

#############
Genesis DB CE
#############

Genesis DB is an event sourcing database engine that can be easily deployed on Uberspace. This guide will walk you through the complete setup process for running Genesis DB CE (Community Edition).

----

.. note:: For this guide you should be familiar with the basic concepts of :manual:`supervisord <daemons-supervisord>` and :manual:`web backends <web-backends>`.

Prerequisites
=============

Before setting up Genesis DB, ensure you have the following:

1. Access to your Uberspace account
2. Basic knowledge of command line operations

Installation
============

Step 1: Create Required Directories
-----------------------------------

First, create the necessary directories for Genesis DB:

.. code-block:: bash

 [isabell@stardust ~]$ mkdir -p /home/$USER/bin
 [isabell@stardust ~]$ mkdir -p /home/$USER/data
 [isabell@stardust ~]$ mkdir -p /home/$USER/logs
 [isabell@stardust ~]$

Step 2: Download and Install Genesis DB
---------------------------------------

Download the Genesis DB binary to your bin directory:

.. code-block:: bash

 [isabell@stardust ~]$ cd /home/$USER/bin
 [isabell@stardust bin]$ wget https://releases.genesisdb.io/latest/genesisdb-linux-amd64-ce -O genesisdb-ce-linux-amd64.tar.gz
 [isabell@stardust bin]$ tar -xzf genesisdb-ce-linux-amd64.tar.gz

Configuration
=============

Step 3: Create Supervisord Configuration
-----------------------------------------

Create a configuration file ``~/etc/services.d/genesisdb.ini`` for Genesis DB. Replace ``YOUR_AUTH_TOKEN`` with your actual Genesis DB authentication token. It is recommended to create a secure, strong password: ``pwgen 64 -1``

.. code-block:: bash

 [program:genesisdb]
 command=/home/$USER/bin/genesisdb-ce-1.0.9-linux-amd64/genesisdb
 directory=/home/$USER
 autostart=true
 autorestart=true
 startsecs=2
 stopsignal=TERM
 environment=GENESISDB_AUTH_TOKEN="YOUR_AUTH_TOKEN",GENESISDB_TZ="Europe/Vienna",GENESISDB_PROMETHEUS_METRICS="false",GENESISDB_DATA_DIR="/home/$USER/data"
 stdout_logfile=/home/$USER/logs/genesisdb.out.log
 stderr_logfile=/home/$USER/logs/genesisdb.err.log

Step 4: Start Genesis DB Service
-------------------------------

Reload supervisord configuration and start the Genesis DB service:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl reread
 genesisdb: available
 [isabell@stardust ~]$ supervisorctl update
 genesisdb: added process group
 [isabell@stardust ~]$ supervisorctl start genesisdb
 genesisdb: started
 [isabell@stardust ~]$

Step 5: Configure Web Access
-----------------------------

Find an available port starting from 8081:

.. code-block:: bash

 [isabell@stardust ~]$ ss -tlnp | grep :808
 [isabell@stardust ~]$

If port 8081 is available, use it. Otherwise, try higher port numbers until you find an available one.

Add your custom domain and configure the web backend:

.. code-block:: bash

 [isabell@stardust ~]$ uberspace web domain add genesisdb.domain.tld
 [isabell@stardust ~]$ uberspace web backend set / --http --port 8081 --domain genesisdb.domain.tld
 [isabell@stardust ~]$

Verification
============

Check if Genesis DB is running correctly:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl status genesisdb
 genesisdb                        RUNNING   pid 1234, uptime 0:01:23
 [isabell@stardust ~]$

Check the logs for any issues:

.. code-block:: bash

 [isabell@stardust ~]$ tail -f /home/$USER/logs/genesisdb.out.log
 [isabell@stardust ~]$ tail -f /home/$USER/logs/genesisdb.err.log
 [isabell@stardust ~]$

Your Genesis DB instance should now be accessible via your configured domain.

Configuration Options
=====================

Genesis DB supports various environment variables for configuration:

* ``GENESISDB_AUTH_TOKEN``: Your authentication token (required)
* ``GENESISDB_DATA_DIR``: Data directory path (default: ``/home/$USER/data``)
* ``GENESISDB_TZ``: Timezone setting (default: ``Europe/Vienna``)
* ``GENESISDB_PROMETHEUS_METRICS``: Enable Prometheus metrics (default: ``false``)

Maintenance
===========

Managing the Service
--------------------

To stop Genesis DB:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl stop genesisdb
 [isabell@stardust ~]$

To restart Genesis DB:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl restart genesisdb
 [isabell@stardust ~]$

Log Rotation
------------

Genesis DB logs are automatically rotated by supervisord. You can manually rotate logs if needed:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl signal USR2 genesisdb
 [isabell@stardust ~]$

Troubleshooting
===============

Common Issues
-------------

1. **Service fails to start**: Check the error logs in ``/home/$USER/logs/genesisdb.err.log``
2. **Permission denied**: Ensure the binary has execute permissions: ``chmod +x /home/$USER/bin/genesisdb-1.0.9-linux-amd64/genesisdb``
3. **Port conflicts**: Use ``ss -tlnp | grep :PORT`` to check if a port is already in use
4. **Domain issues**: Verify domain configuration with ``uberspace web domain list``

Getting Help
------------

If you encounter issues:

1. Check the Genesis DB documentation
2. Review the supervisord logs: ``supervisorctl tail genesisdb``
3. Contact Uberspace support for platform-specific issues

----

Tested with Genesis DB CE 1.0.9, Uberspace 7.15.0

.. _Genesis DB: https://genesisdb.io/
.. _Genesis DB Docs: https://docs.genesisdb.io/
