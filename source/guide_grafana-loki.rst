.. highlight:: console

.. author:: Franz Wimmer <https://codefoundry.de>

.. tag:: lang-go
.. tag:: monitoring
.. tag:: logs
.. tag:: logshipper
.. tag:: observability
.. tag:: audience-admins

.. sidebar:: About

  .. image:: _static/images/loki.png
      :align: center

############
Grafana Loki
############

.. tag_list::

Loki is a log aggregation system designed to store and query logs from all your applications and infrastructure.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :lab:`Grafana <guide_grafana>`

License
=======

Loki is licensed under the GNU Affero General Public License (AGPL).

All relevant legal information can be found here

  * https://github.com/grafana/loki/blob/main/LICENSE

Prerequisites
=============

We need to prepare a couple of directories used by loki.

Directory for storing the loki database:

::

 [isabell@stardust ~]$ mkdir -p ~/loki
 [isabell@stardust ~]$

Directory for storing the custom configuration files:

::

 [isabell@stardust ~]$ mkdir -p ~/etc/loki
 [isabell@stardust ~]$

Directory for storing the log files:

::

 [isabell@stardust ~]$ mkdir -p ~/var/log/grafana
 [isabell@stardust ~]$

Loki Installation
=================

Find the [latest version of Loki at GitHub](https://github.com/grafana/loki/releases) (`loki-linux-amd64.zip`) and download the latest Linux binary:

::

  [isabell@stardust ~]$ wget https://github.com/grafana/loki/releases/download/v2.7.1/loki-linux-amd64.zip
  [isabell@stardust ~]$ unzip loki-linux-amd64.zip
  [isabell@stardust ~]$ mv loki-linux-amd64 ~/bin/loki


Loki Configuration
------------------


Create the file ``~/etc/loki/loki.yaml`` with the following content:

.. code-block:: yaml
  :emphasize-lines: 4,5,7,13,14

  auth_enabled: false

  server:
    http_listen_address: isabell.local.uberspace.de
    http_listen_port: 3100
    grpc_listen_port: 9096

  common:
    path_prefix: /home/isabell/tmp/loki
    storage:
      filesystem:
        chunks_directory: /home/isabell/tmp/loki/chunks
        rules_directory: /home/isabell/tmp/loki/rules
    replication_factor: 1
    ring:
      instance_addr: 127.0.0.1
      kvstore:
        store: inmemory

  schema_config:
    configs:
      - from: 2020-10-24
        store: boltdb-shipper
        object_store: filesystem
        schema: v11
        index:
          prefix: index_
          period: 24h

  ruler:
    alertmanager_url: http://localhost:9093

.. note:: The ``http_listen_address`` must be configured to listen on the local network interface of your uberspace account, so that other applications like Pronmtail (see below) can access Loki via HTTP.

Setup daemon
------------

Create the file ``~/etc/services.d/loki.ini`` with the following content:

.. code-block:: ini

  [program:loki]
  command=loki
    -config.file %(ENV_HOME)s/etc/loki/loki.yaml
  autostart=yes
  autorestart=yes

What the arguments for loki mean:

  * ``-config.file``: The location of the custom configuration file we created.

Connecting Grafana to loki
--------------------------

.. note:: At that point, you already should have installed :lab:`Grafana <guide_grafana>`.

Go to the main page of your Grafana installation and navigate to Configuration / Data sources.

Click "Add data source" and select "Loki". Choose a name you like and add ``http://localhost:3100`` as HTTP URL.

Promtail
========

Promtail is the logshipper in the Grafana ecosystem. It scrapes logs periodically and sends them to loki.

Install Promtail
----------------

::

  [isabell@stardust ~]$ mkdir -p ~/etc/promtail
  [isabell@stardust ~]$ wget https://github.com/grafana/loki/releases/download/v2.4.2/promtail-linux-amd64.zip
  [isabell@stardust ~]$ unzip promtail-linux-amd64.zip
  [isabell@stardust ~]$ mv promtail-linux-amd64 ~/bin/promtail


Promtail configuration
----------------------

::

Create the file ``~/etc/promtail/promtail.yaml`` with the following content:

::

  server:
    http_listen_port: 0
    grpc_listen_port: 0

  positions:
    filename: /home/isabell/tmp/positions.yaml

  clients:
    - url: "http://<ip_address>:3100/loki/api/v1/push"

  scrape_configs:
    - job_name: "apache access logs"
      static_configs:
        - labels:
            host: orous
            app: apache
            type: access_log
            __path__: /home/isabell/logs/webserver/access_log
      pipeline_stages:
        - regex:
            expression: >-
              ^(?P<endpoint>\S*) (?P<ip>\S*) (?P<identd>\S*) (?P<user>\S*) \[(?P<timestamp>.*)\] "(?P<request>.*)" (?P<status>\d*) (?P<size>\S*) "(?P<url>\S*)" "(?P<browser>.*)"$
        - timestamp:
            source: timestamp
            format: "02/Jan/2006:15:04:05 -0700"


    - job_name: "apache error logs"
      static_configs:
        - labels:
            host: orous
            app: apache
            type: error_log
            __path__: /home/isabell/logs/webserver/error_log_apache

      pipeline_stages:
        - regex:
            expression: >-
              ^\[(?P<timestamp>.*)\] \[(?P<type>\w*)\] \[pid (?P<pid>\d*)\] (?P<module>.*): \[client (?P<client>.*)\] (?P<errorid>\w*): (?P<message>.*)$
        - timestamp:
            source: timestamp
            format: "Mon Jan 06 15:04:05 2006"

.. note:: Replace ``<ip_address>`` with the IP address of your local network adapter.

Setup daemon
------------

Create the file ``~/etc/services.d/promtail.ini`` with the following content:

.. code-block:: ini

  [program:promtail]
  command=promtail
    -config.file %(ENV_HOME)s/etc/promtail/promtail.yaml
  autostart=yes
  autorestart=yes

What the arguments for promtail mean:

  * ``-config.file``: The location of the custom configuration file we created.

Finishing installation
======================

Start loki and promtail
-----------------------

.. include:: includes/supervisord.rst

Now point your browser at your uberspace and you should see the grafana web interface.

.. _grafana: https://grafana.com
.. _loki: https://grafana.com/oss/loki/
.. _promtail: https://grafana.com/docs/loki/latest/clients/promtail/

Best practices
==============

Security
--------

If you want to expose loki in order do pass logs from other systems, see :manual:`web backends <web-backends>`.
When exposing Loki to other systems, you should add basic auth to the system.

----

Tested with grafana_ 8.3.4, loki_ main-07e5eb3, promtail_ 2.4.2, Uberspace 7.13.0

.. author_list::
