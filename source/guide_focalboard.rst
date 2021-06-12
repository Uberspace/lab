.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: web
.. tag:: project-management

.. sidebar:: Logo

  .. image:: _static/images/focalboard.svg
      :align: center

##########
Focalboard
##########

.. tag_list::

.. abstract::
  Focalboard_ is an open source, self-hosted alternative to Trello, Notion, and Asana.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

It's recommended to use a PostgreSQL database. Install and configure PostgreSQL server as described in the :lab:`PostgreSQL guide <guide_postgresql>`.

Installation
============

Download the latest release_ to your home directory and extract the application.

.. code-block:: console

 [isabell@stardust ~]$ wget https://github.com/mattermost/focalboard/releases/download/v0.6.1/focalboard-linux.tar.gz
 [isabell@stardust ~]$ tar --extract --gzip --file focalboard-linux.tar.gz
 [isabell@stardust ~]$ rm focalboard-linux.tar.gz
 [isabell@stardust ~]$


Configuration
=============

You need to modify ``~/focalboard-app/config.json``:

 * Change ``"localOnly": true,`` to ``"localOnly": false,``
 * Add ``"session_expire_time": 2592000,``
 * Add ``"session_refresh_time": 18000,``

If PostgreSQL is used, the database configuration also needs to be adjusted. Edit the database config in the file ``~/focalboard-app/config.json``. These two values must be changed:
.. warning:: Replace ``<db_user>``, ``<db_password>`` and ``<db_name>`` with your values.

.. code-block:: json

 "dbtype": "postgres",
 "dbconfig": "postgres://<db_user>:<db_password>@localhost/<db_name>?sslmode=disable&connect_timeout=10",

For example:
.. code-block:: json

 "dbtype": "postgres",
 "dbconfig": "postgres://isabell_focalboard:sup3r-s3cr3t@localhost/focalboard?sslmode=disable&connect_timeout=10",

Setup daemon
------------

Create ``~/etc/services.d/focalboard.ini`` with the following content:

.. code-block:: ini

 [program:focalboard]
 directory=%(ENV_HOME)s/focalboard-app
 command=%(ENV_HOME)s/focalboard-app/focalboard-server
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Configure web server
--------------------

.. note::

    Focalboard is running on port 8088.

.. include:: includes/web-backend.rst

Configure application
---------------------

Open a browser and point it to the domain and you should be redirected to the login screen. Click the link to register a new user instead, and complete the registration.

The first user registration will always be permitted, but subsequent registrations will require an invite link which includes a code. You can invite additional users by clicking on your username in the top left, then selecting "Invite users".

More information can be found in the official documentation_

Updates
-------

.. note:: Check the git repository_ regularly to stay informed about changes.

To update the application, stop the daemon and repeat the installation step.

.. _Focalboard: https://focalboard.com/
.. _release: https://github.com/mattermost/focalboard/releases/
.. _documentation: https://www.focalboard.com/guide/server-setup/
.. _repository: https://github.com/mattermost/focalboard/

----

Tested with Focalboard 0.6.1 and Uberspace 7.10.0

.. author_list::
