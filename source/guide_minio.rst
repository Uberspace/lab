.. author:: Marius Bertram <marius@brtrm.de>

.. tag:: file-storage
.. tag:: lang-go

.. highlight:: console

.. sidebar:: MinIO

  .. image:: _static/images/minio_logo.png
      :align: center

#####
MinIO
#####

.. tag_list::

MinIO_ is an open source object storage server,
compatible with Amazon S3 writen in go.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Web Backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

MinIO is licensed under Apache-2.0

     https://github.com/minio/minio#license


Prerequisites
=============
Download the latest MinIO binary into your bin folder and make it executable:

.. code-block:: console

    [isabell@stardust ~]$ wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /home/isabell/bin/minio
    [isabell@stardust ~]$ chmod +x /home/isabell/bin/minio
    [isabell@stardust ~]$

Create a folder for your data:

.. code-block:: console

    [isabell@stardust ~]$ mkdir /home/isabell/minio
    [isabell@stardust ~]$

.. include:: includes/web-backend.rst

.. note:: MinIO default port is 9000

Setup config
============

Run Minio once to get the master AccessKey and SecretKey:

.. code-block:: console

    [isabell@stardust ~]$ /home/isabell/bin/minio server /home/isabell/minio
    [...]
    AccessKey: 2MN0QSZJS104ROKHYKNC
    SecretKey: rozZqplprT+PZrYb4Mr5GNxeeh+CegYiMBvrvwfD
    [...]
    [isabell@stardust ~]$

.. note:: The AccessKey and the SecretKey are generated randomly. You can also find the keys in the MinIO config. The config file is located in the folder ``~/minio/.minio.sys/config/config.json``

You can set your own AccessKey and SecretKey via ENVIROMENT VARIABLES:

.. code-block:: console

    [isabell@stardust ~]$ export MINIO_ACCESS_KEY=minio
    [isabell@stardust ~]$ export MINIO_SECRET_KEY=miniostorage
    [isabell@stardust ~]$

Setup Supervisord
=================
Create the configuration ``~/etc/services.d/minio.ini``:

.. code-block:: ini

    [program:minio]
    command=~/bin/minio server ~/minio
    autostart=yes
    autorestart=yes

.. include:: includes/supervisord.rst

MinIO Flags
===========

.. code-block:: console

    [isabell@stardust ~]$ minio server
    [...]
    FLAGS:
    --address value               bind to a specific ADDRESS:PORT, ADDRESS can be an IP or hostname (default: ":9000")
    --config-dir value, -C value  [DEPRECATED] path to legacy configuration directory (default: "/home/isabell/.minio")
    --certs-dir value, -S value   path to certs directory (default: "/home/isabell/.minio/certs")
    --quiet                       disable startup information
    --anonymous                   hide sensitive information from logging
    --json                        output server logs and startup information in json format
    --compat                      trade off performance for S3 compatibility
    --help, -h                    show help
    [...]
    [isabell@stardust ~]$

Test MinIO
==========
Open the url you set for MinIO.
On the webpage you can login with the AccessKey and SecretKey.
You can disable the webpage with the ENVIROMENT VARIABLES ``MINIO_BROWSER=OFF``.

Clients
=======
The devs of MinIO provide a minio client_.
But you can use every S3 compatible client or library.



Updates
=======

Just stop MinIO and replace the old binary with the newer one:

.. code-block:: console

    [isabell@stardust ~]$ supervisorctl stop minio
    [isabell@stardust ~]$ wget https://dl.min.io/server/minio/release/linux-amd64/minio -O ~/bin/minio
    [isabell@stardust ~]$ chmod +x ~/bin/minio
    [isabell@stardust ~]$ supervisorctl start minio
    [isabell@stardust ~]$

MinIO docs
==========
Offical MinIO Docs: https://docs.min.io

.. _Minio: https://min.io
.. _client: https://docs.min.io/docs/minio-client-quickstart-guide.html

----



.. author_list::
