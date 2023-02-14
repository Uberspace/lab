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

Loki is a log aggregation system from the Grafana stack designed to store and query logs from all your applications and infrastructure.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :lab:`Grafana <guide_grafana>`

License
=======

Loki is licensed under the GNU Affero General Public License (AGPL).

All relevant legal information can be found here:

  * https://github.com/grafana/loki/blob/main/LICENSE

Prerequisites
=============

In theory, you could expose the Loki UI on the internet.
In my experience, Loki works best as a backend for Grafana, which also provides the better UI.
If you want to run Grafana on your uberspace, please have a look at this great uberlab article: :lab:`Grafana <guide_grafana>`

We need to prepare a couple of directories used by loki.

Directory for storing the loki database:

::

 [isabell@stardust ~]$ mkdir -p ~/loki
 [isabell@stardust ~]$

Directory for storing the custom configuration files:

::

 [isabell@stardust ~]$ mkdir -p ~/etc/loki ~/etc/promtail
 [isabell@stardust ~]$


Loki installation
=================

Find the latest version of `Loki <loki_download_>`_ at GitHub and download the latest Linux binary (`loki-linux-amd64.zip`):

::

  [isabell@stardust ~]$ wget https://github.com/grafana/loki/releases/download/v2.7.1/loki-linux-amd64.zip
  [isabell@stardust ~]$ unzip loki-linux-amd64.zip
  [isabell@stardust ~]$ mv loki-linux-amd64 ~/bin/loki
  [isabell@stardust ~]$ rm loki-linux-amd64.zip # Cleanup
  [isabell@stardust ~]$


Loki Configuration
------------------

Create the file ``~/etc/loki/loki.yaml`` with the following content:

.. code-block:: yaml
  :emphasize-lines: 4,9,12,13

  auth_enabled: false

  server:
    http_listen_address: 127.0.0.1
    http_listen_port: 3100
    grpc_listen_port: 9096

  common:
    path_prefix: /home/<username>/loki
    storage:
      filesystem:
        chunks_directory: /home/<username>/loki/chunks
        rules_directory: /home/<username>/loki/rules
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


.. note::

  Replace `<username>` with your own uberspace user.
  The ``http_listen_address`` must be configured to listen on the local network interface of your uberspace account, so that other applications like Promtail (see below) can access Loki via HTTP.

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

Connecting Grafana to Loki
--------------------------

.. note:: At that point, you already should have installed :lab:`Grafana <guide_grafana>`.

Go to the main page of your Grafana installation and navigate to Configuration / Data sources.

Click "Add data source" and select "Loki". Choose a name you like and add ``http://127.0.0.1:3100`` as HTTP URL (use your own uberspace user).

Promtail
========

Promtail is the logshipper in the Grafana ecosystem. It periodically scrapes log files and sends them to Loki.

Promtail installation
---------------------

Find the latest version of `Promtail <promtail_download_>`_ at GitHub. It's usually located in the latest Loki release (`promtail-linux-amd64.zip`):

::

  [isabell@stardust ~]$ wget https://github.com/grafana/loki/releases/download/v2.7.2/promtail-linux-amd64.zip
  [isabell@stardust ~]$ unzip promtail-linux-amd64.zip
  [isabell@stardust ~]$ mv promtail-linux-amd64 ~/bin/promtail
  [isabell@stardust ~]$ rm promtail-linux-amd64.zip # Cleanup
  [isabell@stardust ~]$


Promtail configuration
----------------------

Create the file ``~/etc/promtail/promtail.yaml`` with the following content:

.. code-block:: yaml
  :emphasize-lines: 6,9,15,18,30,33

  server:
    http_listen_port: 0
    grpc_listen_port: 0

  positions:
    filename: /home/<username>/tmp/positions.yaml

  clients:
    - url: "http://127.0.0.1:3100/loki/api/v1/push"

  scrape_configs:
    - job_name: "apache access logs"
      static_configs:
        - labels:
            host: <username>
            app: apache
            type: access_log
            __path__: /home/<username>/logs/webserver/access_log
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
            host: <username>
            app: apache
            type: error_log
            __path__: /home/<username>/logs/webserver/error_log_apache

      pipeline_stages:
        - regex:
            expression: >-
              ^\[(?P<timestamp>.*)\] \[(?P<type>\w*)\] \[pid (?P<pid>\d*)\] (?P<module>.*): \[client (?P<client>.*)\] (?P<errorid>\w*): (?P<message>.*)$
        - timestamp:
            source: timestamp
            format: "Mon Jan 06 15:04:05 2006"

.. note::

  Replace `<username>` with your own uberspace user.

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

Best practices
==============

Security
--------

If you want to expose Loki on the internet in order do pass logs from other systems, see :manual:`web backends <web-backends>`.
When exposing Loki to other systems, you should add basic auth to the system.

----

Tested with `Grafana <grafana_>`_ 9.3.0, `Loki <loki_>`_ 2.7.2, `Promtail <promtail_>`_ 2.7.2, Uberspace 7.13.0

.. author_list::


.. _grafana: https://grafana.com
.. _loki: https://grafana.com/oss/loki/
.. _loki_download: https://github.com/grafana/loki/releases
.. _promtail: https://grafana.com/docs/loki/latest/clients/promtail/
.. _promtail_download: https://github.com/grafana/loki/releases
