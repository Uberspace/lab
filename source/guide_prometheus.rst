.. highlight:: console

.. spelling::
    prometheus

.. author:: Malte Krupa <http://nafn.de>

.. tag:: lang-go
.. tag:: monitoring
.. tag:: audience-admins

.. sidebar:: About

  .. image:: _static/images/prometheus.svg
      :align: center

##########
prometheus
##########

.. tag_list::

Prometheus_ is an open-source systems monitoring and alerting toolkit originally built at SoundCloud. Since its inception in 2012, many companies and organizations have adopted Prometheus_, and the project has a very active developer and user community. It is now a standalone open source project and maintained independently of any company. To emphasize this, and to clarify the project's governance structure, Prometheus_ joined the Cloud Native Computing Foundation in 2016 as the second hosted project, after Kubernetes.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

License
=======

Prometheus_ is licensed under the Apache License 2.0.

All relevant legal information can be found here

  * https://github.com/Prometheus/Prometheus/blob/master/LICENSE

Prerequisites
=============

We need to prepare a couple of directories.

The first directory is for storing the timeseries database:

::

 [isabell@stardust ~]$ mkdir -p ~/var/lib/prometheus
 [isabell@stardust ~]$

The second directory is for storing the configuration files:

::

 [isabell@stardust ~]$ mkdir -p ~/etc/prometheus
 [isabell@stardust ~]$


Installation
============

Find the latest version of Prometheus_ for the operating system ``linux`` and the architecture ``amd64`` from the `download page <https://prometheus.io/download>`_, download and extract it and enter the extracted directory:

::

 [isabell@stardust ~]$ wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ tar xvzf ~/prometheus-2.45.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ cd ~/prometheus-2.45.0.linux-amd64
 [isabell@stardust prometheus-2.45.0.linux-amd64]$

Move the binary to ``~/bin`` and the configuration file to ``~/etc/prometheus``.

::

 [isabell@stardust prometheus-2.45.0.linux-amd64]$ mv prometheus ~/bin/
 [isabell@stardust prometheus-2.45.0.linux-amd64]$ mv prometheus.yml ~/etc/prometheus
 [isabell@stardust prometheus-2.45.0.linux-amd64]$ cd ~
 [isabell@stardust ~]$

Cleanup
=======

Since we only need the binary and the configuration file we can safely remove the downloaded archive and the extracted directory.

::

 [isabell@stardust ~]$ rm -r ~/prometheus-2.45.0.linux-amd64
 [isabell@stardust ~]$ rm ~/prometheus-2.45.0.linux-amd64.tar.gz

Configuration
=============

Configure web server
--------------------

.. note::

    Prometheus is running on port 9090.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create the file ``~/etc/services.d/prometheus.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 3,7

  [program:prometheus]
  command=prometheus
    --web.listen-address=0.0.0.0:9090
    --config.file=%(ENV_HOME)s/etc/prometheus/prometheus.yml
    --storage.tsdb.path=%(ENV_HOME)s/var/lib/prometheus/
    --storage.tsdb.retention.time=15d
    --web.external-url=https://isabell.uber.space/
    --web.route-prefix=/
  autostart=yes
  autorestart=yes

What the arguments for Prometheus_ mean:

  * ``--web.listen-address``: The IP address and port Prometheus listens on.
  * ``--config.file``: The full path to the Prometheus_ configuration file.
  * ``--storage.tsdb.path``: The path where Prometheus stores the timeseries database.
  * ``--storage.tsdb.retention.time``: The amount of time to keep the datapoints of the timeseries database (in this guide it's set to 15 days).
  * ``--web.external-url``: The URL under which Prometheus is reachable.
  * ``--web.route-prefix``: The path under which Prometheus is reachable.

.. note::
   When using :manual:`web backends <web-backends>`, the address to listen to has to be ``0.0.0.0``, not  127.0.0.1, localhost or ::1.

Finishing installation
======================

Start Prometheus
----------------

.. include:: includes/supervisord.rst

Now point your browser to your uberspace and you should see the Prometheus webinterface.

Best practices
==============

Security
--------

To quote the `Prometheus security documentation <https://prometheus.io/docs/operating/security/#Prometheus>`_:

::

  It's presumed that untrusted users have access to the Prometheus HTTP
  endpoint and logs.

  It is also presumed that only trusted users have the ability to change
  the command line, configuration file, rule files and other aspects of
  the runtime environment of Prometheus and other components.

As stated in the security documentation, it is ok to make Prometheus reachable for everyone as long as only you are able to change the configuration files and the CLI arguments.

If this is something you do not want to do, you could hide it behind a basic auth.

.. _Prometheus: https://prometheus.io/

----

Tested with Prometheus_ 2.18.1, Uberspace 7.6.1.2

.. author_list::
