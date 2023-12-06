.. highlight:: console

.. author:: Franz Wimmer <https://codefoundry.de>

.. tag:: lang-go
.. tag:: monitoring
.. tag:: metrics
.. tag:: grafana
.. tag:: prometheus
.. tag:: observability
.. tag:: audience-admins

.. sidebar:: About

  .. image:: _static/images/mimir.png
      :align: center

#############
Grafana Mimir
#############

.. tag_list::

Mimir is a long term storage for metrics, scraped by various agents like the Prometheus or Grafana Agent. It can optionally be distributed among several nodes.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :lab:`Grafana <guide_grafana>`
  * :lab:`MinIO <guide_minio>`

License
=======

Mimir is licensed under the GNU Affero General Public License (AGPL).

All relevant legal information can be found here:

  * https://github.com/grafana/mimir/blob/main/LICENSE

Prerequisites
=============

Mimir is capable of using AWS S3 as backend storage. To get a local S3 compatible storage, install :lab:`MinIO <guide_minio>` on your uberspace. Afterwards, create three MinIO buckets for Mimir:

::

  # replace mcli by the name you gave the MinIO client

  [isabell@stardust ~]$ $ mcli mb mimir/mimir-blocks
  Bucket created successfully `mimir/mimir-blocks`.

  [isabell@stardust ~]$ $ mcli mb mimir/mimir-alertmanager
  Bucket created successfully `mimir/mimir-alertmanager`.

  [isabell@stardust ~]$ $ mcli mb mimir/mimir-ruler
  Bucket created successfully `mimir/mimir-ruler`.


We need to configure two distinct network routes for Mimir:

  * We will connect a Grafana instance or local scraping agents via localhost.
  * We will connect a Grafana instance on another machine or remote scraping agents via the Apache webserver.

If you need help running Grafana on your uberspace, please have a look at this great uberlab article: :lab:`Grafana <guide_grafana>`

We need to prepare a couple of directories used by Mimir.

Directory for storing the Mimir database:

::

  [isabell@stardust ~]$ mkdir -p ~/mimir
  [isabell@stardust ~]$

Directory for storing the custom configuration files:

::

  [isabell@stardust ~]$ mkdir -p ~/etc/mimir
  [isabell@stardust ~]$


Mimir installation
=================

Find the latest version of `Mimir <mimir_download_>`_ at GitHub and download the latest Linux binary (`mimir-linux-amd64`):

::

  [isabell@stardust ~]$ wget https://github.com/grafana/mimir/releases/download/mimir-2.10.0/mimir-linux-amd6
  [isabell@stardust ~]$ mv mimir-linux-amd64 ~/bin/mimir
  [isabell@stardust ~]$ chmod 755 ~/bin/mimir
  [isabell@stardust ~]$


Mimir Configuration
------------------

Create the file ``~/etc/mimir/mimir.yaml`` with the following content:

.. code-block:: yaml
  :emphasize-lines: 9,20,22,33,36,65

  target: all,overrides-exporter

  common:
    storage:
      backend: s3
      s3:
        endpoint: 127.0.0.1:9000
        access_key_id: mimir
        secret_access_key: <password>
        insecure: true

  limits:
    # Delete from storage metrics data older than 14 days.
    compactor_blocks_retention_period: 14d

  blocks_storage:
    s3:
      bucket_name: mimir-blocks
    tsdb:
      dir: /home/<username>/mimir/tsdb
    bucket_store:
      sync_dir: /home/<username>/mimir/bucket_store_sync

  alertmanager_storage:
    s3:
      bucket_name: mimir-alertmanager

  ruler_storage:
    s3:
      bucket_name: mimir-ruler

  ruler:
    rule_path: /home/<username>/mimir/rules

  compactor:
    data_dir: /home/<username>/mimir/compactor
    sharding_ring:
      kvstore:
        store: memberlist

  distributor:
    ring:
      instance_addr: 127.0.0.1
      kvstore:
        store: memberlist

  ingester:
    ring:
      instance_addr: 127.0.0.1
      kvstore:
        store: memberlist
      replication_factor: 1

  server:
    log_level: info
    http_listen_port: 9009

  store_gateway:
    sharding_ring:
      replication_factor: 1

  activity_tracker:
    # File where ongoing activities are stored. If empty, activity tracking is
    # disabled.
    filepath: /home/<username>/var/log/mimir/metrics-activity.log

  usage_stats:
    enabled: false

.. note::

  Replace `<username>` with your own uberspace user.
  Replace `<password>` with the secret access key of your MinIO instance.

Setup daemon
------------

Create the file ``~/etc/services.d/mimir.ini`` with the following content:

.. code-block:: ini

  [program:mimir]
  command=mimir
    -config.file %(ENV_HOME)s/etc/mimir/mimir.yaml
  autostart=yes
  autorestart=yes
  # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
  startsecs=30

What the arguments for mimir mean:

  * ``-config.file``: The location of the custom configuration file we created.

Connecting Grafana to Mimir
--------------------------

.. note:: At that point, you already should have installed :lab:`Grafana <guide_grafana>`.

Go to the main page of your Grafana installation and navigate to Configuration / Data sources.

Mimir exposes a Prometheus-compatible API.
Click "Add data source" and select "Prometheus". Choose a name you like and add ``http://localhost:9009/prometheus`` as HTTP URL.

Add a custom HTTP header ``X-Scope-OrgID`` and set the value to e.g. ``1``.
Under the heading "Type and version" choose "Mimir" and version > 2.3.x.

Grafana Agent
=============

We will use Grafana Agent to scrape metrics of various systems. You can install it on other systems, too!
Please note that you can also use other tools, e.g. Prometheus, to scrape and send metrics to Mimir.

Grafana Agent installation
--------------------------

Find the latest version of `Grafana Agent <grafana_agent_download_>`_ at GitHub.

::

  [isabell@stardust ~]$ wget https://github.com/grafana/agent/releases/download/v0.36.2/grafana-agent-linux-amd64.zip
  [isabell@stardust ~]$ unzip grafana-agent-linux-amd64.zip
  [isabell@stardust ~]$ mv grafana-agent-linux-amd64 ~/bin/grafana-agent
  [isabell@stardust ~]$ rm grafana-agent-linux-amd64.zip
  [isabell@stardust ~]$


Grafana Agent configuration
----------------------

Grafana Agent uses the "River" format for configuration files. You can find documentation about this format `here <river_documentation_>`_.
Create the file ``~/etc/grafana-agent/grafana-agent.river`` with the following basic configuration:

.. code-block:: yaml
  :emphasize-lines: 25

  logging {
      level  = "info"
      format = "logfmt"
  }

  prometheus.exporter.unix {
      include_exporter_metrics = true
      disable_collectors       = ["mdadm"]
  }

  prometheus.scrape "default" {
      targets = concat(
          prometheus.exporter.unix.targets,
      )

      forward_to = [
          prometheus.relabel.node_exporter.receiver,
      ]
  }

  prometheus.relabel "node_exporter" {
      rule {
          action          = "replace"
          target_label    = "instance"
          replacement     = "<host label>"
      }

      forward_to = [
          prometheus.remote_write.mimir.receiver,
      ]
  }

  prometheus.remote_write "mimir" {
      endpoint {
          url = "http://localhost:9009/api/v1/push"
          headers = {
              "X-Scope-OrgID" = "1",
          }
      }
  }

.. note::

  Replace `<host label>` with the label you want to use for the metrics scraped from this instance.

Setup daemon
------------

Create the file ``~/etc/services.d/grafana-agent.ini`` with the following content:

.. code-block:: ini

  [program:grafana-agent]
  directory=%(ENV_HOME)s/etc/grafana-agent
  command=grafana-agent
      run
      %(ENV_HOME)s/etc/grafana-agent/grafana-agent.river
      --storage.path=$HOME/tmp/grafana-agent
  environment=AGENT_MODE="flow"
  autostart=yes
  autorestart=yes
  # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
  startsecs=30


Finishing installation
======================

Start Mimir and Grafana Agent
-----------------------

.. include:: includes/supervisord.rst

Best practices
==============

Security
--------

If you want to expose Mimir on the internet in order do pass metrics from other systems, see :manual:`web backends <web-backends>`.
When exposing Mimir to other systems, you should add basic auth to the system.

----

Tested with `Grafana <grafana_>`_ 10.1.2, `Mimir <mimir_>`_ 2.10.0, `Grafana Agent <grafana_agent_>`_ 0.36.2, Uberspace 7.15.6

.. author_list::

.. _grafana: https://grafana.com
.. _mimir: https://grafana.com/oss/mimir/
.. _mimir_download: https://github.com/grafana/mimir/releases
.. _grafana_agent: https://grafana.com/docs/agent/latest/
.. _grafana_agent_download: https://github.com/grafana/agent/releases
.. _river_documentation: https://grafana.com/docs/agent/latest/flow/config-language/
