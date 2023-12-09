.. highlight:: console

.. spelling::
    Nodemule

.. author:: Gerald Schneider <gerald@schneidr.de>

.. tag:: geolocation
.. tag:: mqtt
.. tag:: lang-nodejs
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/owntracks.png
      :align: center

#########
OwnTracks
#########

.. tag_list::

OwnTracks_ is an Open Source project which provides an iOS and an Android app with which your smartphone records its current location.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`
  * :lab:`Mosquitto <guide_mosquitto>`

License
=======

The OwnTracks components are distributed under different licenses, including `GNU Public License`_ and `MIT License`_.


Prerequisites
=============

* Either a CentOS 7 environment or a working Docker installation to compile the binaries
* Node version 18, the compilation process for the frontend is not compatible with Node 20 yet

Installation
============

Mosquitto
---------

Follow the :lab:`Mosquitto <guide_mosquitto>` guide to set up the MQTT broker Mosqitto.

Make a note of the port you opened in your firewall, you will need it later for the recorder and for the client setup. Then create users. You need at least two users, one for the recorder and one for every user you want to allow access to.

.. code-block:: console

 [isabell@stardust ~]$ mosquitto_passwd -c ~/etc/mosquitto/passwd recorder
 Password: [hidden]
 Reenter password: [hidden]
 [isabell@stardust ~]$ mosquitto_passwd ~/etc/mosquitto/passwd isabell
 Password: [hidden]
 Reenter password: [hidden]
 [isabell@stardust ~]$

.. note:: Make sure that you use the `-c` argument **only** on the first user. Otherwise a new password file will be created.

Compiling the binaries
----------------------

Sadly, there are no precompiled binaries or packages available that could be used on Uberspace, we need to compile it ourselves. Another hurdle are missing header files on the Uberspace hosts, so we can't compile it there.

If you have a CentOS 7 environment available you can compile it directly by following the `Building from source`_ instructions, if you have a Docker installation available you can use the environment in this `Docker image`_

Build the Docker image
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

 [isabell@localmachine ~]$ mkdir ~/tmp
 [isabell@localmachine ~]$ cd ~/tmp
 [isabell@localmachine tmp]$ git clone https://github.com/schneidr/owntracks-recorder-centos-build owntracks
 [isabell@localmachine tmp]$ cd owntracks
 [isabell@localmachine owntracks]$ docker build -t owntracks-recorder-centos .
 [isabell@localmachine owntracks]$ cp config.mk.in config.mk
 [isabell@localmachine owntracks]$

You need to change some values to change in ``config.mk``, some can be overriden later in the configuration, but not all of them:

.. code-block:: ini

  INSTALLDIR = /usr/local
  STORAGEDEFAULT = /home/isabell/lib/ot-recorder/
  DOCROOT = /home/isabell/lib/ot-recorder/htdocs
  CONFIGFILE = /home/isabell/etc/default/ot-recorder

.. note:: You might want to keep your ``config.mk`` file for later updates, but you can get the values from the compiled binaries using the ``--version`` argument.

Compiling ot-recorder
^^^^^^^^^^^^^^^^^^^^^

Check the `recorder release page`_ for the latest version and use it for the ``RECORDER_VERSION`` variable:

.. code-block:: console

 [isabell@localmachine owntracks]$ docker run -it --rm -v $PWD:/work -e RECORDER_VERSION=0.9.6 owntracks-recorder-centos:latest
 [isabell@localmachine owntracks]$

The container will download and compile the requested version. Afterwards you will find three new files in the directory:

* libconfig.so.9
* ocat
* ot-recorder

These files need to be copied to your Uberspace server. First, create the necessary directories an change your environment variables:

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p ~/bin/lib ~/etc/default/
 [isabell@stardust ~]$ echo 'export LD_LIBRARY_PATH="/home/isabell/bin/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
 [isabell@stardust ~]$ echo 'export PATH="/home/isabell/bin:$PATH"' >> ~/.bashrc
 [isabell@stardust ~]$ source ~/.bashrc
 [isabell@stardust ~]$

Now upload the file ``libconfig.so.9`` into the directory ``/home/isabell/bin/lib``, both ``ocat`` and ``ot-recorder`` need to be placed into ``/home/isabell/bin/``. Make sure they keep their executable permissions. Afterwards you should be able to call the binaries.

.. code-block:: console

 [isabell@stardust ~]$ ocat --version
 This is OwnTracks Recorder, version 0.9.6
 built with:
         WITH_MQTT = yes
         WITH_HTTP = yes
         WITH_TOURS = yes
         WITH_PING = yes
         CONFIGFILE = "/home/isabell/etc/default/ot-recorder"
         DOCROOT = "/home/isabell/lib/ot-recorder/htdocs"
         DEFAULT_HISTORY_HOURS = 6
         JSON_INDENT = "NULL"
         LIBMOSQUITTO_VERSION = 1.6.10
         MDB VERSION = LMDB 0.9.22: (March 21, 2018)
         GIT VERSION = tarball
 [isabell@stardust ~]$

Configuration
=============

Create configuration file
-------------------------

Create a config file in ``~/etc/default/ot-recorder``. Add the following content:

.. code-block:: ini
 :emphasize-lines: 4

 OTR_HOST="isabell.uber.space"
 OTR_USER="recorder"
 OTR_PASS="c9itHRjPfu9qUnEMbA9zJEPbHvA3kutv"
 OTR_PORT=40132
 OTR_STORAGEDIR="/home/isabell/lib/ot-recorder"
 OTR_VIEWSDIR="/home/isabell/etc/ot-recorder/views"
 OTR_CAFILE="/etc/ssl/certs/ca-bundle.crt"

For ``OTR_PORT`` you need to use the port you noted earlier during the Mosqitto installation.

Setup daemon
------------

Create a config file in ``~/etc/services.d/ot-recorder.ini`` with the following content:

.. code-block:: ini

 [program:ot-recorder]
 command=ot-recorder 'owntracks/#'
 autostart=yes
 autorestart=unexpected
 environment=LD_LIBRARY_PATH="/home/isabell/bin/lib:/lib64"
 startsecs=30

Adding the environment variable ``LD_LIBRARY_PATH`` makes sure the necessary libraries are found (supervisord does not source the ``.bashrc`` file).

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.


Setup frontend
--------------

To set up the web frontend you need to download the latest archive from the `frontend releases page`_, extract it, build it with ``yarn`` and copy it into your web directory.

.. code-block:: console

 [isabell@stardust ~]$ wget https://github.com/owntracks/frontend/archive/refs/tags/v2.12.0.tar.gz
 [isabell@stardust ~]$ tar xfz v2.12.0.tar.gz
 [isabell@stardust ~]$ cd frontend-2.12.0/
 [isabell@stardust frontend-2.12.0]$ yarn install
 [isabell@stardust frontend-2.12.0]$ yarn build
 [isabell@stardust frontend-2.12.0]$ mkdir /var/www/virtual/$USER/isabell.uber.space/
 [isabell@stardust frontend-2.12.0]$ cp dist/* /var/www/virtual/$USER/isabell.uber.space/
 [isabell@stardust frontend-2.12.0]$

.. warning:: Since recording your movements is a sensitive thing you should protect that web frontend with a ``.htaccess`` file with basic auth.

.. note::

    OwnTracks is by default running on port 8083.

While some resources of the frontend are loaded directly from the web server, some requests need to be directed directly to the recorder daemon. To make them accessible from the outside, configure :manual:`web-backends <web-backends>`:

.. code-block:: console

 [isabell@stardust ~]$ uberspace web backend set --http --port 8083 isabell.uber.space/api
 [isabell@stardust ~]$ uberspace web backend set --http --port 8083 isabell.uber.space/ws
 [isabell@stardust ~]$

Now the frontend is available via the uberspace URL ``https://isabell.uber.space``.

Set up views
^^^^^^^^^^^^

`OwnTracks views`_ are a nice feature to share your movements during a restricted timespan without actual timestamps, just the locations. This is useful for example, to share a road trip with family and friends.

To set up views you need to copy some more files and map a couple more paths to the backend.

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p ~/lib/ot-recorder/htdocs
 [isabell@stardust ~]$ cd recorder-0.9.6/
 [isabell@stardust recorder-0.9.6]$ cp docroot/static docroot/utils ~/lib/ot-recorder/htdocs
 [isabell@stardust recorder-0.9.6]$

For the backend configuration:

.. code-block:: console

 [isabell@stardust ~]$ uberspace web backend set --http --port 8083 isabell.uber.space/utils
 [isabell@stardust ~]$ uberspace web backend set --http --port 8083 isabell.uber.space/static
 [isabell@stardust ~]$ uberspace web backend set --http --port 8083 isabell.uber.space/view
 [isabell@stardust ~]$

Now you can place your view definitions in ``~/etc/...`` and the view is instantly reachable from the web.

Client Setup
============

Apps for Android and iOS are available from the `App Stores`_, other clients are available as well. The client setup is pretty easy.

.. table:: client connection settings
   :widths: auto

   ==========  =====
   Key         Value
   ==========  =====
   Modus       MQTT
   Hostname    `Uberspace URL without https://`
   Port        `noted in Mosquitto setup`
   Client ID   `free to choose`
   Username    `configured username`
   Password    `configured password`
   Device ID   `free to choose`
   Tracker ID  `free to choose`
   Seurity     TLS
   ==========  =====

.. note::

    In the frontend you are able to filter for `Username` and then further for all `Devices` of the specified users. The ``Device ID`` configured here will show up there.

    The Tracker ID is explained in the `Tracker ID booklet page`_

Update
======

.. note:: Check the update `recorder release page`_ and the `frontend releases page`_ regularly to stay informed about the newest version.

The update steps are basically the same as the installation steps, without one time configurations like supervisord and web backends.

Restart your supervisorctl afterwards. If it's not in state RUNNING, check the log files.


.. _OwnTracks: https://owntracks.org/
.. _GNU Public License: https://github.com/owntracks/recorder/blob/master/LICENSE
.. _MIT License: https://github.com/owntracks/frontend/blob/main/LICENSE
.. _Building from source: https://github.com/owntracks/recorder#building-from-source
.. _Docker image: https://github.com/schneidr/owntracks-recorder-centos-build
.. _recorder release page: https://github.com/owntracks/recorder/releases
.. _frontend releases page: https://github.com/owntracks/frontend/releases
.. _OwnTracks views: https://github.com/owntracks/recorder#views
.. _Tracker ID booklet page: https://owntracks.org/booklet/features/tid/
.. _App Stores: https://owntracks.org/booklet/guide/apps/

----

Tested with OwnTracks 0.9.6, Uberspace 7.15.6

.. author_list::
