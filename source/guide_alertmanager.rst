.. highlight:: console

.. author:: Malte Krupa <http://nafn.de>

.. tag:: lang-go
.. tag:: monitoring
.. tag:: audience-admins

############
Alertmanager
############

.. tag_list::

The alertmanager handles alerts sent by client applications such as the Prometheus server. It takes care of deduplicating, grouping, and routing them to the correct receiver integrations such as email, PagerDuty, or OpsGenie. It also takes care of silencing and inhibition of alerts.

----

.. note:: The alertmanager is one of the tools that grew out of the prometheus_ project. Without prometheus_ you'll need a very specific use-case to make use of the alertmanager.

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :lab:`prometheus <guide_prometheus>`

License
=======

alertmanager_ is licensed under the Apache License 2.0.

All relevant legal information can be found here

  * https://github.com/prometheus/alertmanager/blob/master/LICENSE

Prerequisites
=============

We need to prepare a couple of directories.

The first directory is for storing the notification log and the alert silences:

::

 [isabell@stardust ~]$ mkdir -p ~/var/lib/alertmanager
 [isabell@stardust ~]$

The second directory is for storing the configuration files:

::

 [isabell@stardust ~]$ mkdir ~/etc/alertmanager
 [isabell@stardust ~]$


Installation
============

Find the latest version of alertmanager_ for the operating system ``linux`` and the architecture ``amd64`` from the `download page <https://prometheus.io/download>`_, download and extract it and enter the extracted directory:

::

 [isabell@stardust ~]$ wget https://github.com/prometheus/alertmanager/releases/download/v0.20.0/alertmanager-0.20.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ tar xvzf alertmanager-0.20.0.linux-amd64.tar.gz
 [isabell@stardust ~]$ cd alertmanager-0.20.0.linux-amd64
 [isabell@stardust alertmanager-0.20.0.linux-amd64]$

Move the binary to ``~/bin`` and the configuration file to ``~/etc/alertmanager``.

::

 [isabell@stardust alertmanager-0.20.0.linux-amd64]$ mv alertmanager ~/bin/
 [isabell@stardust alertmanager-0.20.0.linux-amd64]$ mv alertmanager.yml ~/etc/alertmanager
 [isabell@stardust alertmanager-0.20.0.linux-amd64]$

Configuration
=============

Setup daemon
------------

Create the file ``~/etc/services.d/alertmanager.ini`` with the following content:

.. code-block:: ini

  [program:alertmanager]
  command=alertmanager
    --web.listen-address="127.0.0.1:9093"
    --config.file=%(ENV_HOME)s/etc/alertmanager/alertmanager.yml
    --storage.path=%(ENV_HOME)s/var/lib/alertmanager/
  autostart=yes
  autorestart=yes

What the arguments for alertmanager_ mean:

  * ``--web.listen-address``: The IP address and port alertmanager_ listens on.
  * ``--config.file``: The full path to the alertmanager_ configuration file.
  * ``--storage.path``: The path where alertmanager_ stores the notification log and the alert silences.

Finishing installation
======================

Start alertmanager
------------------

.. include:: includes/supervisord.rst

Now point your alert creating tool or your prometheus_ service to the configured alertmanager port and you should receive alerts sent out via the alertmanager.

Best practices
==============

Security
--------

We did not configure a web backend because the alertmanager web interface should not be reachable from the public internet.

Everyone with access to the web interface is able to create and silence alarms.

Accessing the webinterface
--------------------------

One option to access the web interface is via a SSH tunnel:

::

 [isabell@localhost ~]$ ssh -L 8080:localhost:9093 isabell@stardust.uberspace.de
 [isabell@stardust ~]$

Now you can access the web interface via ``http://localhost:8080`` on your workstation.

.. _Prometheus: https://prometheus.io/
.. _alertmanager: https://github.com/prometheus/alertmanager

----

Tested with alertmanager_ 0.20.0, Uberspace 7.6.1.2

.. author_list::
