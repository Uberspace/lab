.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: web
.. tag:: lang-go
.. tag:: chat

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/mattermost.svg
      :align: center

##########
Mattermost
##########

.. tag_list::

`Mattermost`_ is an open-source, self-hosted online chat service written in Go and JavaScript.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download the most recent Linux TAR archive from the `Mattermost website`_:

.. code-block:: console

  [isabell@stardust ~]$ wget https://releases.mattermost.com/5.18.0/mattermost-5.18.0-linux-amd64.tar.gz
  --2019-12-23 13:27:01--  https://releases.mattermost.com/5.18.0/mattermost-5.18.0-linux-amd64.tar.gz
  Resolving releases.mattermost.com (releases.mattermost.com)... 99.86.88.55, 99.86.88.121, 99.86.88.31, ...
  Connecting to releases.mattermost.com (releases.mattermost.com)|99.86.88.55|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 155306557 (148M) [application/x-gzip]
  Saving to: ‘mattermost-5.18.0-linux-amd64.tar.gz’

  100%[====================================================================>] 155,306,557 22.5MB/s   in 6.6s

  2019-12-23 13:27:08 (22.6 MB/s) - ‘mattermost-5.18.0-linux-amd64.tar.gz’ saved [155306557/155306557]

  [isabell@stardust ~]$

Extract the archive:

.. code-block:: console

  [isabell@stardust ~]$ tar xfv mattermost-5.18.0-linux-amd64.tar.gz
  […]
  mattermost/prepackaged_plugins/mattermost-plugin-custom-attributes-v1.0.2.tar.gz
  mattermost/prepackaged_plugins/mattermost-plugin-zoom-v1.1.2.tar.gz
  [isabell@stardust ~]$


Configuration
=============

Set up a Database
-----------------

Run the following code to create the database ``<username>_mattermost`` in MySQL:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_mattermost COLLATE utf8mb4_unicode_ci;"
  [isabell@stardust ~]$

Change the configuration
------------------------

You need to set up your URL, and MySQL settings in ``~/mattermost/config/config.json``.

First, set your site URL:

.. code-block:: none

    "SiteURL": "https://isabell.uber.space"

Then find the ``SqlSettings`` block and replace ``mmuser`` with your username, ``mostest`` with your MySQL password and ``mattermost_test`` with the name of the database you created earlier:

.. code-block:: javascript
 :emphasize-lines: 3

    "SqlSettings": {
      "DriverName": "mysql",
      "DataSource": "isabell:MySuperSecretPassword@tcp(localhost:3306)/isabell_mattermost?charset=utf8mb4,utf8\u0026readTimeout=30s\u0026writeTimeout=30s",
      "DataSourceReplicas": [],
      "DataSourceSearchReplicas": [],
      "MaxIdleConns": 20,
      "ConnMaxLifetimeMilliseconds": 3600000,
      "MaxOpenConns": 300,
      "Trace": false,
      "AtRestEncryptKey": "",
      "QueryTimeout": 30
    },


Configure web server
--------------------

.. note::

    Mattermost is running on port 8065.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/mattermost.ini`` with the following content:

.. code-block:: ini

 [program:mattermost]
 command=%(ENV_HOME)s/mattermost/bin/mattermost
 autorestart=true
 directory=%(ENV_HOME)s/mattermost


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Setup a user
------------

You can now point your browser to your URL and setup a user.

Further customisation
---------------------

To further customise your configuration, you can open the ``system console`` in your browser and adapt any settings to your wishes. Setting the SMTP server is a good idea.

Updates
-------

Stop your service, backup your ``/home/isabell/mattermost/client/plugins``, ``/home/isabell/mattermost/config``, ``/home/isabell/mattermost/data``, ``/home/isabell/mattermost/logs`` and ``/home/isabell/mattermost/plugins`` directory and rename/delete your ``/home/isabell/mattermost`` directory.
Proceed with the installation steps and restore the ``client/plugins``, ``config``, ``data``, ``logs`` and ``plugins`` directories. Then you can start your service again.

.. _`Mattermost website`: https://mattermost.com/download/
.. _`Mattermost`: https://mattermost.com/


----

Tested with Mattermost 7.4.0 and Uberspace 7.13.0

.. author_list::
