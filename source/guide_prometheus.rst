.. highlight:: console

.. author:: Malte Krupa <http://nafn.de>

.. tag:: lang-go
.. tag:: monitoring

.. sidebar:: About

  .. image:: _static/images/prometheus.svg
      :align: center

##########
Prometheus
##########

.. tag_list::

Prometheus_ is an open-source systems monitoring and alerting toolkit originally built at SoundCloud. Since its inception in 2012, many companies and organizations have adopted Prometheus_, and the project has a very active developer and user community. It is now a standalone open source project and maintained independently of any company. To emphasize this, and to clarify the project's governance structure, Prometheus_ joined the Cloud Native Computing Foundation in 2016 as the second hosted project, after Kubernetes.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

License
=======

prometheus_ is licensed under the Apache License 2.0.

All relevant legal information can be found here

  * https://github.com/prometheus/prometheus/blob/master/LICENSE

Prerequisites
=============

We need to prepare a couple of directories.

The first directory is for storing the timeseries database:

::

 [isabell@stardust ~]$ mkdir -p var/lib/prometheus
 [isabell@stardust ~]$

The second directory is for storing the configuration files:

::

 [isabell@stardust ~]$ mkdir etc/prometheus
 [isabell@stardust ~]$


Installation
============

Step 1
------

Find the latest version of prometheus_ for the operating system ``linux`` and the architecture ``amd64`` from the `download page <https://prometheus.io/download>`_, download and extract it and enter the extracted directory:

::

 [isabell@stardust ~]$ wget https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ tar xvzf prometheus-2.10.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ cd prometheus-2.10.0.linux-amd64
 [isabell@stardust prometheus-2.10.0.linux-amd64]$

Step 2
------

Move the binary to ``~/bin`` and the configuration file to ``~/etc/prometheus``.

::

 [isabell@stardust prometheus-2.10.0.linux-amd64]$ mv prometheus ~/bin/
 [isabell@stardust prometheus-2.10.0.linux-amd64]$ mv prometheus.yml ~/etc/prometheus
 [isabell@stardust prometheus-2.10.0.linux-amd64]$

Configuration
=============

Configure web server
--------------------

.. note::

    prometheus is running on port 9090.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create the file ``~/etc/services.d/prometheus.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 3,7

  [program:prometheus]
  command=prometheus
    --web.listen-address=localhost:9090
    --config.file=%(ENV_HOME)s/etc/prometheus/prometheus.yml
    --storage.tsdb.path=%(ENV_HOME)s/var/lib/prometheus/
    --storage.tsdb.retention=15d
    --web.external-url=https://isabell.stardust.uberspace.de/
    --web.route-prefix=/
  autostart=yes
  autorestart=yes

In our example this would be:

.. code-block:: ini

  [program:prometheus]
  command=prometheus
    --web.listen-address=localhost:9000
    --config.file=%(ENV_HOME)s/etc/prometheus/prometheus.yml
    --storage.tsdb.path=%(ENV_HOME)s/var/lib/prometheus/
    --storage.tsdb.retention=15d
    --web.external-url=https://isabell.stardust.uberspace.de/
    --web.route-prefix=/
  autostart=yes
  autorestart=yes

What the arguments for prometheus_ mean:

  * ``--web.listen-address``: The IP address and port prometheus listens on.
  * ``--config.file``: The full path to the prometheus_ configuration file.
  * ``--storage.tsdb.path``: The path where prometheus stores the timeseries database.
  * ``--storage.tsdb.retention``: The amount of time to keep the datapoints of the timeseries database (in this guide it's set to 15 days).
  * ``--web.external-url``: The URL under which prometheus is reachable.
  * ``--web.route-prefix``: The path under which promtheus is reachable.

Finishing installation
======================

Start prometheus
----------------

.. include:: includes/supervisord.rst

Now point your browser to your uberspace and you should see the prometheus webinterface.

Best practices
==============

Security
--------

To quote the `prometheus security documentation <https://prometheus.io/docs/operating/security/#prometheus>`_:

::

  It's presumed that untrusted users have access to the prometheus HTTP
  endpoint and logs.

  It is also presumed that only trusted users have the ability to change
  the command line, configuration file, rule files and other aspects of
  the runtime environment of Prometheus and other components.

As stated in the security documentation, it is ok to make prometheus reachable for everyone as long as only you are able to change the configuration files and the CLI arguments.

If this is something you do not want to do, you could hide it behind a basic auth.

.. _Prometheus: https://prometheus.io/

----

Tested with Prometheus_ 2.10.0, Uberspace 7.3.0.0

.. author_list::
