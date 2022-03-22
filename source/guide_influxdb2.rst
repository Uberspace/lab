.. highlight:: console

.. author:: brutus <brutus.dmc@googlemail.com>
.. tag:: database
.. tag:: metrics
.. tag:: prometheus

.. sidebar:: About

  .. image:: _static/images/influxdb.svg
      :align: center

##########
InfluxDB 2
##########

.. tag_list::

InfluxDB_ is an *open source* time series database (TSDB). Or *"a platform for
building and operating time series applications"*. It is developed by
*InfluxData*, written in Go and optimized for fast, high-availability storage
and retrieval of time series data in fields such as operations monitoring,
application metrics, Internet of Things sensor data, and real-time analytics.

It can scrape data from `OpenMetrics`_ endpoints. And has support for
processing a wide assortment of sources via `Telegraf`_. As well as multiple
"officially recognized" `language bindings`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`backends <web-backends>`

License
=======

The *OSS Version* is MIT licensed. Legal information can be found here:

  * https://www.influxdata.com/legal/

Prerequisites
=============

Here's a quick overview of some `key concepts`_ / terminology:

Data is modeled as time series; i.e. data points stored in a *"table-like"*
manner. A *data point* combines a unique *timestamp* with one or more typed
values (*fields*) and optional labels (*tags*). Access is governed by granting
users rights to objects, supporting multiple tenants.

**Organisation**
    *(~ workspace)* groups **buckets** with related objects (e.g. dashboards,
    tasks, alerts) and access management for users.
**Bucket**
    *(~ database)* contains **measurements**, combined with a retention period
    (i.e. how long will this data be stored).
**Measurement**
    *(~ table)* a specific set of time series data, used for grouping
    **points**.
**Point**
    *(~ row)* a single entry, combining a unique timestamp with one or more
    **fields** and optional **tags**.
**Field**
    *(~ column)* a *field name* with a *field value* (typed).
**Tag**
    *(~ labels)* a *tag name* with a *tag value* (string).

Installation
============

We aim to provide the latest stable version of ``influx`` (CLI client) and
``influxd`` (server) for you. So no need to install anything. But you can of
course install other versions yourself, e.g. from
https://github.com/influxdata/influxdb/releases.

Configuration
=============

Configure Influxd
-----------------

Use your favorite editor to create the file ``~/etc/influxd.toml`` with the
following content:

.. code-block:: cfg

    http-bind-address = "0.0.0.0:8086"
    log-level = "error"
    reporting-disabled = true

You might want to review these and other available `options`_.

Setup Service
-------------

Use your favorite editor to create the file ``~/etc/services.d/influxd.ini``
with the following content.

.. code-block:: ini

    [program:influxd]
    startsecs = 60
    startretries = 0
    environment = INFLUXD_CONFIG_PATH=%(ENV_HOME)s/etc/influxd.toml
    command = influxd run

.. include:: includes/supervisord.rst

If it’s not in state RUNNING (after the time set in ``startsecs`` has passed),
check your configuration.

Initial Setup
=============

Before we enable your installation for outside access, we run a quick setup:

.. code-block:: console

    [isabell@stardust ~]$ influx setup

And provide these:

1. Enter a primary **username**.
2. Enter a **password** for your primary user.
3. Confirm your password by entering it again.
4. Enter a name for your primary **organization**.
5. Enter a name for your primary **bucket**.
6. Enter a **retention** period for your primary bucket.
7. Confirm the details for your primary user, organization, and bucket.

Outside Access
==============

.. note::

    InfluxDB is running on port ``8086``, also see ``http-bind-address``
    in your ``~/etc/influxd.toml``.

.. include:: includes/web-backend.rst

Best practice
=============

Schema
------

When designing your schema, think about when to use **fields** and when to use
**tags** for your data:

- Fields aren't indexed, but required.
- Tags are indexed, but optional.

*Queries that filter field values must scan all field values to match query
conditions. As a result, queries on tags are more performant than queries on
fields. So you might want to store commonly queried metadata in tags.*

You should also think about your `series cardinality`_.

Downsampling
------------

To keep memory usage within acceptable limits and performance up, remember to
downsample your data regularly. Here's an intro on how to set up **tasks**, to
do that with **Flux**: https://www.influxdata.com/blog/downsampling-influxdb-v2-0/

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

----

Tested with InfluxDB 2.0.3, Uberspace 7.8.2

.. author_list::

.. _`InfluxDB`: https://github.com/influxdata/influxdb
.. _`documentation`: https://docs.influxdata.com/influxdb/v2.0/
.. _`options`: https://docs.influxdata.com/influxdb/v2.0/reference/config-options/
.. _`key concepts`: https://docs.influxdata.com/influxdb/v2.0/reference/key-concepts/
.. _`series cardinality`: https://docs.influxdata.com/influxdb/v2.0/reference/glossary/#series-cardinality
.. _`language bindings`: https://docs.influxdata.com/influxdb/v2.0/tools/client-libraries/
.. _`feed`: https://github.com/influxdata/influxdb/releases.atom
.. _`OpenMetrics`: https://openmetrics.io/
.. _`Telegraf`: https://www.influxdata.com/time-series-platform/telegraf/
