.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-go
.. tag:: time-tracking

.. sidebar:: Logo

  .. image:: _static/images/traggo.png
      :align: center

######
Traggo
######

.. tag_list::

Traggo_ is an open-source, tag-based time tracking tool. It offers customizable dashboards with diagrams, a list and calendar view of the tracked time, and a sleek web interface with multiple themes and simple user management.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`

License
=======

All relevant legal information can be found here:

  * https://github.com/traggo/server/blob/master/LICENSE

Installation
============

Create a new directory ``~/traggo`` and enter the directory you just created:

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/traggo
 [isabell@stardust ~]$ cd ~/traggo

Now download the latest version, unpack the archive, delete the archive afterwards:

.. note:: Replace ``0.7.1`` with the version of the `latest release`_.

.. code-block:: console

 [isabell@stardust traggo]$ traggo]$ wget https://github.com/traggo/server/releases/download/v0.7.1/traggo_0.7.1_linux_amd64.tar.gz --2025-08-13 11:46:25--  https://github.com/traggo/server/releases/download/v0.7.1/traggo_0.7.1_linux_amd64.tar.gz
 Resolving github.com (github.com)... 140.82.121.3
 […]
 Length: 6646788 (6.3M) [application/octet-stream]
 Saving to: ‘traggo_0.7.1_linux_amd64.tar.gz’
 
 100%[===============================================>] 6,646,788   --.-K/s   in 0.1s
 
 2025-08-13 11:46:26 (45.6 MB/s) - ‘traggo_0.7.1_linux_amd64.tar.gz’ saved [6646788/6646788]
 [isabell@fairydust traggo]$ tar xvf traggo_0.7.1_linux_amd64.tar.gz
 .env.sample
 LICENSE
 README.md
 traggo
 [isabell@fairydust traggo]$ rm traggo_0.7.1_linux_amd64.tar.gz

Make the binary executable and create the file ``.env.local`` as a copy of the file ``.env.sample``:

.. code-block:: console

 [isabell@stardust traggo]$ chmod +x traggo
 [isabell@stardust traggo]$ cp .env.sample .env.local
 [isabell@stardust traggo]$

Configuration
=============

Configure Traggo
----------------

Adjust your ``.env.local`` as follows:

::

 # the port the http server should use
 TRAGGO_PORT=3030

 # default username and password
 TRAGGO_DEFAULT_USER_NAME=admin
 TRAGGO_DEFAULT_USER_PASS=change_me_soon

 # bcrypt password strength (higher = more secure but also slower)
 TRAGGO_PASS_STRENGTH=10

 # how verbose traggo/server should log (must be one of: debug, info, warn, error, fatal, panic)
 TRAGGO_LOG_LEVEL=warn

 # the database dialect (must be one of: sqlite3)
 TRAGGO_DATABASE_DIALECT=sqlite3

 # the database connection string, differs depending on the dialect
 # sqlite3:  path/to/database.db
 TRAGGO_DATABASE_CONNECTION=data/traggo.db

Setup daemon
------------

Create ``~/etc/services.d/traggo.ini`` with the following content:

::

 [program:traggo]
 directory=%(ENV_HOME)s/traggo/
 command=%(ENV_HOME)s/traggo/traggo
 autostart=yes
 autorestart=yes
 startsecs=30
             
.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Setup web backend
-----------------

.. note:: The default port for Traggo is ``3030``.

.. include:: includes/web-backend.rst

.. warning:: Replace ``isabell`` with your username!

If Traggo is running, you can now find it at ``https://isabell.uber.space``.

Best practices
==============

Security
--------

Keep the software up to date.

After logging in for the first time, immediately change the default password (``change_me_soon``) via the web interface.

Updates
=======

.. note:: Check the `GitHub release page <latest release_>`_ regularly to stay informed about the newest version.

To update the software, download the latest version and replace all files (``LICENSE``, ``README.md``, ``traggo``, and ``.env.sample``). Also check if there are any changes in the ``.env.sample`` file compared to your currently used ``.env.local`` file.

.. _Traggo: https://traggo.net
.. _latest release: https://github.com/traggo/server/releases

----

Tested with Traggo 0.7.1, Uberspace 7.16.7

.. author_list::
