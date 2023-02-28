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
It consists of a server for sending and receiving messages in real-time per WebSocket which is distributed as a single binary. It can be accessed via the built-in web-UI, the `cli <https://github.com/gotify/cli>`_ or `the Android app <https://github.com/gotify/android>`_ (available via `F-Droid <https://f-droid.org/de/packages/com.github.gotify/>`_ and `GooglePlay <https://play.google.com/store/apps/details?id=com.github.gotify>`_ ).

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

  [isabell@stardust ~]$ uberspace web backend set /gotify/ --http --port 52111 --remove-prefix
  Set backend for / to port 52111; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html

Note the `--remove-prefix` option here. Without it, gotify will not work behind a sub path (e.g. `isabell.uber.space/gotify/`).


Installation
============

Like a lot of Go software, gotify is distributed as a single binary. Since version 2.1.7 gotify requires GLIBC 2.28, which is not available in U7. Thus we need to build gotify from source. The building is done as is described in `gotify's documentation <https://gotify.net/docs/dev-setup>`_ but building without docker and only for one architecture:

.. warning::

  The ``yarn build`` command may fail at first with an ``code: 'EPIPE', syscall: 'write'`` error message.
  Just run it again until you get ``Done in 60.48s.``. 

::

  [isabell@stardust ~]$ git clone https://github.com/gotify/server.git
  [isabell@stardust ~]$ cd server
  [isabell@stardust ~/server]$ git checkout v2.2.2
  Note: switching to 'v2.2.2'.
  [isabell@stardust server]$ make download-tools
  go install github.com/go-swagger/go-swagger/cmd/swagger@v0.26.1
  [isabell@stardust server]$ go get -d
  [isabell@stardust server]$ cd ui
  [isabell@stardust ui]$ yarn
  yarn install v1.22.19
  [1/4] Resolving packages...
  success Already up-to-date.
  Done in 2.53s.
  [isabell@stardust ~/server/ui]$ NODE_OPTIONS=--openssl-legacy-provider yarn build
  yarn run v1.22.19
  $ react-scripts build
  Creating an optimized production build...
  Browserslist: caniuse-lite is outdated. Please run:
    npx browserslist@latest --update-db
    Why you should do it regularly: https://github.com/browserslist/browserslist#browsers-data-updating
  Compiled successfully.
  
  File sizes after gzip:
  
    252.57 KB  build/static/js/2.62492a59.chunk.js
    15.19 KB   build/static/js/main.d0066ad9.chunk.js
    2.4 KB     build/static/css/2.0f3898ba.chunk.css
    778 B      build/static/js/runtime-main.2e858444.js
  
  The project was built assuming it is hosted at ./.
  You can control this with the homepage field in your package.json.
  
  The build folder is ready to be deployed.
  
  Find out more about deployment here:
  
    https://cra.link/deployment
  
  Done in 59.93s.
  [isabell@stardust ui]$ cd ..
  [isabell@stardust server]$ go run hack/packr/packr.go
  [isabell@stardust server]$ export LD_FLAGS="-w -s -X main.Version=$(git describe --tags | cut -c 2-) -X main.BuildDate=$(date "+%F-%T") -X main.Commit=$(git rev-parse --verify HEAD) -X main.Mode=prod";
  [isabell@stardust server]$ go build -ldflags="$LD_FLAGS" -o gotify-server
  [isabell@stardust server]$ mv gotify-server ../gotify-linux-amd64


Configuration
=============

Config file
-----------

Without configuration, gotify will listen on port 80. To change that to our previously chosen ``52111``,
we will use an environment variable. It is also possible to use a config file, but we will ignore that for now.
If you still want to change values in the config, download the example config and adjust it to your needs:

::

  [isabell@stardust gotify]$ wget -O config.yml https://raw.githubusercontent.com/gotify/server/master/config.example.yml
  [isabell@stardust gotify]$

Documentation for the config file can be found on the `gotify website <https://gotify.net/docs/config>`_.


Setup daemon
------------

Create ``~/etc/services.d/gotify.ini`` with the following content.

.. code-block:: ini

  [program:gotify]
  command=%(ENV_HOME)s/gotify/gotify-linux-amd64
  directory=%(ENV_HOME)s/gotify/
  environment=GOTIFY_SERVER_PORT=52111

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
