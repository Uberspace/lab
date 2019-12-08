.. author:: Jonas <https://github.com/jfowl>

.. tag:: lang-go

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gotify.png
      :align: center

######
Gotify
######

.. tag_list::

Gotify_ is a self-hosted push notification service written in Go and distributed under the MIT License.
It consists of a server for sending and receiving messages in real-time per WebSocket which is distributed as a single binary. It can be accessed via the built-in web-ui, the `cli <https://github.com/gotify/cli>`_ or `the Android app <https://github.com/gotify/android>`_ (available via `F-Droid <https://f-droid.org/de/packages/com.github.gotify/>`_ and `GooglePlay <https://play.google.com/store/apps/details?id=com.github.gotify>`_ ).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`MySQL <database-mysql>` (optional)

Prerequisites
=============


Gotify comes with a built-in sqlite database, but if you prefer to use MySQL, you
can do so.

Gotify can run under a subdomain (e.g. https://gotify.isabella.uber.space) or via a subpath (e.g.
https://isabella.uber.space/gotify/).

For both options you need to configure a `web backend <webbackend_>`_.
The subpath option looks like this:

::

  [isabell@stardust ~]$ uberspace web backend set /gotify/ --http --port <port>
  Set backend for / to port <port>; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html

Replace ``<port>`` with a port number above 1000 of your choice and remember it.


Installation
============

Like a lot of Go software, gotify is distributed as a single binary. Download gotify's latests `release <https://github.com/gotify/server/releases/latest>`_, unzip it and make sure that the file can be executed.

::

  [isabell@stardust ~]$ mkdir ~/gotify && cd ~/gotify
  [isabell@stardust gotify]$ wget https://github.com/gotify/server/releases/download/v2.0.10/gotify-linux-amd64.zip
  Resolving github.com (github.com)... 140.82.118.4
  Connecting to github.com (github.com)|140.82.118.4|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Length: 52960072 (51M) [application/octet-stream]
  Saving to: gotify-linux-amd64.zip

 100%[==========================================>] 10,200,261  12.0MB/s

  2019-10-26 01:15:11 (12.0 MB/s) - 'gotify-linux-amd64.zip' saved [10200261/10200261]
  [isabell@stardust gotify]$ unzip gotify-linux-amd64.zip
  Archive:  gotify-linux-amd64.zip
    inflating: gotify-linux-amd64
    inflating: LICENSE
     creating: licenses/
    inflating: licenses/github.com_gotify_plugin-api
  [...]
    inflating: licenses/golang.org_x_crypto


Configuration
=============

Config file
-----------

Without configuration, gotify will listen on port 80. To change that to our previously choosen ``<port>``,
we will use an environment variable. It is also possible to use a config file. To download the
example config, run:

::

  [isabell@stardust gotify]$ wget -O config.yml https://raw.githubusercontent.com/gotify/server/master/config.example.yml

Documentation for the config file can be found on the `gotify website <https://gotify.net/docs/config>`_.


Setup daemon
------------

Create ``~/etc/services.d/gotify.ini`` with the following content and replace
``<port>`` with the actual port:

.. code-block:: ini

  [program:gotify]
  command=%(ENV_HOME)/gotify/gotify-linux-amd64
  directory=%(ENV_HOME)/gotify/
  environment=GOTIFY_SERVER_PORT=<port>
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

The default user and password is ``admin`` and ``admin``, but you are advised
to change in as soon as you log in. You can replace the admin user with an
other user with admin privileges later on.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check gotify's `releases <https://github.com/gotify/server/releases/latest>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop gotify`` and repeat the "Installation" step followed by ``supervisorctl start gotify`` to restart gotify.

.. _Gotify: https://gotify.net/
.. _Documentation: https://gotify.net/docs/
.. _feed: https://github.com/gotify/server/releases.atom
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gotify 2.0.10, Uberspace 7.3.6.1

.. author_list::
