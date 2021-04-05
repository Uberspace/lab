.. author:: Lukas Fritze <https://fritzedesign.de>

.. highlight:: console

.. tag:: project-management
.. tag:: collaboration
.. tag:: self-hosting
.. tag:: proprietary


.. sidebar:: About

  .. image:: _static/images/focalboard.svg
      :align: center

##########
Focalboard
##########

.. tag_list::

Focalboard_ is an open source, self-hosted alternative to Trello, Notion, and Asana. It helps define, organize, track and manage work across individuals and teams.

Check out the `source code`_, and contribute to the future of this project.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`


License
=======

All relevant legal information can be found here

  * `Focalboard License`_


Prerequisites
=============

To start you need a PostgreSQL database. Install and configure PostgreSQL server as described in the :lab:`PostgreSQL guide <guide_postgresql>`.

This is the hard part. After creating a user and a database you can continue installing Focalboard.

Installation
============

Step 1 - Download
-----------------

Download the archive package from GitHub. Make sure to use the latest release_ in the download path.

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/mattermost/focalboard/releases/download/v0.6.1/focalboard-server-linux-amd64.tar.gz
  [isabell@stardust ~]$

Extract (``-x``) the archive:

.. code-block:: console

  [isabell@stardust ~]$ tar -x --gzip --file focalboard-server-linux-amd64.tar.gz
  [isabell@stardust ~]$

The extraction step unpacked the content to the directory ``focalboard`` so you can remove the archive:

.. code-block:: console

  [isabell@stardust ~]$ rm focalboard-server-linux-amd64.tar.gz
  [isabell@stardust ~]$

Step 2 - Database configuration
-------------------------------

Edit the database config in the file ``~/focalboard/config.json``. These two values must be changed:

.. warning:: Replace ``<db_user>``, ``<db_password>`` and ``<db_name>`` with your values.

.. code-block:: json

  "dbtype": "postgres",
  "dbconfig": "postgres://<db_user>:<db_password>@localhost/<db_name>?sslmode=disable&connect_timeout=10",

For example:

.. code-block:: json

  "dbtype": "postgres",
  "dbconfig": "postgres://isabell_focalboard:sup3r-s3cr3t@localhost/focalboard?sslmode=disable&connect_timeout=10",


Step 3 - Adding a service
-------------------------

Setting it up as a service. Create  ``~/etc/services.d/focalboard.ini`` with the following content:

.. code-block:: ini

  [program:focalboard]
  directory=/home/isabell/focalboard
  command=/home/isabell/focalboard/bin/focalboard-server
  startsecs=60
  autostart=yes
  autorestart=yes

Adjust the paths if you choose to install it in an other location in step 1.

.. include:: includes/supervisord.rst


Step 4 - Make it accessible
---------------------------

.. include:: includes/web-backend.rst

The default port used for Focalboard is ``8000``. It can be changed in the file ``~/focalboard/config.json``.


Finishing installation
======================

After installing follow these guides:

* `Server Setup Guide`_
* `User Guide`_

---

Tested with Focalboard v0.6.1 64-bit, Uberspace 7.9.0.0

.. author_list::


.. _Focalboard: https://www.focalboard.com
.. _source code: https://github.com/mattermost/focalboard
.. _Server Setup Guide: https://www.focalboard.com/guide/server-setup/
.. _User Guide: https://www.focalboard.com/guide/user
.. _Focalboard License: https://github.com/mattermost/focalboard/blob/main/LICENSE.txt
.. _release: https://github.com/mattermost/focalboard/releases
