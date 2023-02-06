.. highlight:: console

.. author:: Malte Krupa <http://nafn.de>

.. tag:: lang-go
.. tag:: monitoring
.. tag:: audience-admins

.. sidebar:: About

  .. image:: _static/images/grafana.svg
      :align: center

#######
Grafana
#######

.. tag_list::

The leading open source software for time series analytics.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

License
=======

grafana_ is licensed under the Apache License 2.0.

All relevant legal information can be found here

  * https://github.com/grafana/grafana/blob/master/LICENSE

Prerequisites
=============

We need to prepare a couple of directories and create a database which is used by grafana.

Directory for storing the static files and default configuration:

::

 [isabell@stardust ~]$ mkdir -p usr/share/grafana
 [isabell@stardust ~]$

Directory for storing the custom configuration files:

::

 [isabell@stardust ~]$ mkdir -p etc/grafana
 [isabell@stardust ~]$

Directory for storing the log files:

::

 [isabell@stardust ~]$ mkdir -p var/log/grafana
 [isabell@stardust ~]$

Finally, create the mysql database for grafana:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE isabell_grafana"
 [isabell@stardust ~]$

Installation
============

Find the latest version of grafana_ for the platform ``linux`` from the `download page <https://grafana.com/grafana/download?platform=linux>`_, download and extract it and enter the extracted directory:

::

 [isabell@stardust ~]$ wget https://dl.grafana.com/oss/release/grafana-6.7.3.linux-amd64.tar.gz
 [isabell@stardust ~]$ tar xvzf grafana-6.7.3.linux-amd64.tar.gz
 [isabell@stardust ~]$ cd grafana-6.7.3
 [isabell@stardust grafana-6.7.3]$

Move the binary to ``~/bin`` and the default configuration and html files to ``~/usr/share/grafana``.

::

 [isabell@stardust grafana-6.7.3]$ mv bin/grafana-server ~/bin/
 [isabell@stardust grafana-6.7.3]$ mv conf public ~/usr/share/grafana
 [isabell@stardust grafana-6.7.3]$

Configuration
=============

Configure web server
--------------------

.. note::

    grafana is running on port 3000.

.. include:: includes/web-backend.rst

Setup grafana
-------------

Create the file ``~/etc/grafana/grafana.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 4,5,7,13,14

  [database]
  type = mysql
  host = 127.0.0.1:3306
  name = isabell_grafana
  user = isabell
  # If the password contains # or ; you have to wrap it with triple quotes. Ex """#password;"""
  password = "<mysql-password>"

  [analytics]
  reporting_enabled = false
  check_for_updates = true
  [security]
  admin_user = admin
  admin_password = password123

.. note:: The ``admin_password`` MUST later be changed via the web interface when grafana is running.

Setup daemon
------------

Create the file ``~/etc/services.d/grafana.ini`` with the following content:

.. code-block:: ini

  [program:grafana]
  command=grafana-server
    -config %(ENV_HOME)s/etc/grafana/grafana.ini
    -homepath %(ENV_HOME)s/usr/share/grafana
    cfg:default.paths.logs=%(ENV_HOME)s/var/log/grafana
  autostart=yes
  autorestart=yes

What the arguments for grafana_ mean:

  * ``--config``: The location of the custom configuration file we created.
  * ``--homepath``: The location of the default configuration and the static files.
  * ``cfg:default.paths.logs``: The location of the log files created by grafana.

Finishing installation
======================

Start grafana
-------------

.. include:: includes/supervisord.rst

Now point your browser at your uberspace and you should see the grafana web interface.

.. _grafana: https://grafana.com

Best practices
==============

Security
--------

Change the default password which we configured in the configuration file ``~/etc/grafana/grafana.ini``!

----

Tested with grafana_ 6.7.3, Uberspace 7.6.1.2

.. author_list::
