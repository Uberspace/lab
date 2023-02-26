.. author:: Sascha Mann <https://saschamann.eu/>

.. tag:: lang-go
.. tag:: lang-javascript
.. tag:: project-management
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/vikunja.png
      :align: center

.. spelling::
  repos

#####
Vikunja
#####

.. tag_list::

Vikunja_ is a self-hosted to-do and project management app using the AGPL licence_. It split into two parts: the API and the frontends.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`


Prerequisites
=============

.. include:: includes/my-print-defaults.rst

We need a database:

.. code-block:: console

  [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_vikunja"
  [isabell@stardust ~]$

We can use the uberspace or your own domain:

.. include:: includes/web-domain-list.rst


Installation
============


Download
--------

Find the latest version of Vikunja's API-server on the releases_ page and extract it:

.. code-block:: console

  [isabell@stardust ~]$ VERSION=0.20.1
  [isabell@stardust ~]$ mkdir ~/vikunja
  [isabell@stardust ~]$ wget -O ~/vikunja/vikunja.zip "https://dl.vikunja.io/api/$VERSION/vikunja-v$VERSION-linux-amd64-full.zip"
  [...]
  Saving to: ‘/home/isabell/vikunja/vikunja.zip’

  100%[==============================================================================>] 18,397,951  28.5MB/s   in 0.6s

  2023-01-22 18:11:38 (28.5 MB/s) - ‘/home/isabell/vikunja/vikunja.zip’ saved [18397951/18397951]


Verifying (optional)
--------------------

Optionally you can verify the downloaded file using ``gpg``. To do so, download the pgp signature file and trust key
and verify the binary:

.. code-block:: console
  :emphasize-lines: 7

  [isabell@stardust ~]$ wget --output-document ~/vikunja/vikunja.zip.asc "https://dl.vikunja.io/api/$VERSION/vikunja-v$VERSION-linux-amd64-full.zip.asc"
  [...]
  [isabell@stardust ~]$ gpg --keyserver keyserver.ubuntu.com --recv FF054DACD908493A
  [...]
  [isabell@stardust ~]$ gpg --verify ~/vikunja/vikunja.zip.asc ~/vikunja/vikunja.zip
  gpg: Signature made Fri 11 Nov 2022 12:41:28 CET using RSA key ID D908493A
  gpg: Good signature from "Frederic (Vikunja) (The key to sign vikunja releases.) <frederic@vikunja.io>"
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 7D06 1A4A A614 36B4 0713  D42E FF05 4DAC D908 493A

If the verification is fine, we get a ``Good signature from "Frederic (Vikunja) (The key to sign vikunja releases.) <frederic@vikunja.io>"`` line. You need to ignore the ``WARNING`` here.


Extract Archive
---------------

Extract the archive containing the Vikunja binary and config file, and rename the binary:

.. code-block:: console

  [isabell@stardust ~]$ VERSION=0.20.1
  [isabell@stardust ~]$ cd ~/vikunja
  [isabell@stardust ~]$ unzip vikunja.zip
  Archive:  vikunja.zip
    inflating: LICENSE
    inflating: config.yml.sample
    inflating: vikunja-v0.20.1-linux-amd64.sha256
    inflating: vikunja-v0.20.1-linux-amd64
  [isabell@stardust ~]$ mv ~/vikunja/vikunja-v$VERSION-linux-amd64 ~/vikunja/vikunja
  [isabell@stardust ~]$


Clean up the no longer needed archive, signature, and binary hash:

.. code-block:: console

  [isabell@stardust ~]$ rm ~/vikunja/vikunja.zip ~/vikunja/vikunja.zip.asc ~/vikunja/vikunja-v$VERSION-linux-amd64.sha256
  [isabell@stardust ~]$


Set permissions
---------------

Make the downloaded binary executable:

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/vikunja/vikunja
  [isabell@stardust ~]$


Configuration
=============

Configuration file
------------------

Create a copy of the sample configuration file:

.. code-block:: console

  [isabell@stardust ~]$ cp ~/vikunja/config.yml.sample ~/vikunja/config.yml
  [isabell@stardust ~]$


Open the config file and fill in your database details:

.. code-block:: yaml
  :emphasize-lines: 4,6,8,12

  [...]
  database:
    # Database type to use. Supported types are mysql, postgres and sqlite.
    type: "mysql"
    # Database user which is used to connect to the database.
    user: "isabell"
    # Database password
    password: ""
    # Database host
    host: "localhost"
    # Database to use
    database: "isabell_vikunja"
    # When using sqlite, this is the path where to store the data
    path: "./vikunja.db"
    # Sets the max open connections to the database. Only used when using mysql and postgres.
    maxopenconnections: 100
    # Sets the maximum number of idle connections to the db.
    maxidleconnections: 50
    # The maximum lifetime of a single db connection in miliseconds.
    maxconnectionlifetime: 10000
    # Secure connection mode. Only used with postgres.
    # (see https://pkg.go.dev/github.com/lib/pq?tab=doc#hdr-Connection_String_Parameters)
    sslmode: disable
    # The path to the client cert. Only used with postgres.
    sslcert: ""
    # The path to the client key. Only used with postgres.
    sslkey: ""
    # The path to the ca cert. Only used with postgres.
    sslrootcert: ""
    # Enable SSL/TLS for mysql connections. Options: false, true, skip-verify, preferred
    tls: false
  [...]


.. note::

  See the Vikunja documentation_ and the configuration sample for all configuration options.


Finishing installation
======================

Service for Vikunja
-------------------

To keep Vikunja up and running in the background, you need to create a service that takes care for it. Create a config file ``~/etc/services.d/vikunja.ini`` for the service:

.. code-block:: ini

  [program:vikunja]
  directory=%(ENV_HOME)s/vikunja
  command=%(ENV_HOME)s/vikunja/vikunja
  startsecs=30
  autorestart=yes

.. include:: includes/supervisord.rst

.. note:: The status of vikunja must be ``RUNNING``. If its not check the log output at ``~/logs/supervisord.log`` and the configuration file ``~/vikunja/config.yml``.

Uberspace web backend
---------------------

.. note:: Vikunja is running on port 3456.

.. include:: includes/web-backend.rst

If we only want to install Vikunja's API-server, we are done now.

Installed files and folders are:

* ``~/vikunja``
* ``~/etc/services.d/vikunja.ini``

Updates
=======

.. note:: Check the changelog_ or releases_ page regularly to stay informed about the newest version.


Manual updating
-----------------

* Stop the application ``supervisorctl stop vikunja``
* Do the *Download* (and optionally *Verifying*) part from above.
* Check if you have to modify the config file. (See documentation_.)
* Start the application ``supervisorctl start vikunja``
* Check if the application is running ``supervisorctl status vikunja``


Installing the web frontend (optional)
======================================

Vikunja can be accessed through several ways: desktop or mobile apps, as well as a web frontend written in Javascript.

The web frontend is a static website. To install it, find the latest frontend version on the downloads_ page, download the files and unzip them into ``~/html``:

.. warning:: The frontend files on the download page are not ordered chronologically. Make sure you select the desired version!

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ FRONTEND_VERSION=0.20.3
  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ wget "https://dl.vikunja.io/frontend/vikunja-frontend-$FRONTEND_VERSION.zip"
  ...
  [isabell@stardust html]$ unzip "vikunja-frontend-$FRONTEND_VERSION.zip"
  ...
  [isabell@stardust html]$ rm "vikunja-frontend-$FRONTEND_VERSION.zip"
  [isabell@stardust html]$

Once you have installed the frontend, we need to reconfigure the `web backends <webbackend_>`_:

::

  [isabell@stardust ~]$ uberspace web backend set /api --http --port 3456
  Set backend for / to port <port>; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$ uberspace web backend set / --apache
  Set backend for / to apache.
  [isabell@stardust ~]$


Then create an ``.htaccess`` file with the following content:

::

  RewriteEngine on
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule ^(.*)$ /index.html [NC,L,QSA]


This forwards all requests to the frontend to ``index.html`` and will prevent you from getting stuck on a 404 page by accident.

Now we are done and can access Vikunja through ``isabell.uber.space``.


Optional steps
==============

Disabling registration
----------------------

By default, registration via the API is open to anyone. If you have registered an account for yourself and want to disable registration, change the config file and restart the API-server:

.. code-block:: yaml
  :emphasize-lines: 3

  [...]
  # Whether to let new users registering themselves or not
  enableregistration: false
  [...]


::

  [isabell@stardust ~]$ supervisorctl restart vikunja
  vikunja: stopped
  vikunja: started
  [isabell@stardust ~]$


Create an account through the CLI
---------------------------------

You can create an account through the CLI even when registration via the API is disabled (see above):

.. code-block:: bash
  :emphasize-lines: 1

  [isabell@stardust ~]$ ~/vikunja/vikunja user create --username isabell --password 'SuperSecretPassword' --email isabell@uber.space
  ...
  User was created successfully.
  [isabell@stardust ~]$


Change log levels
-----------------

By default the log configuration is very verbose. You can change it to only log warnings, errors, or critical events by editing the config file and restarting the API-server:

.. code-block:: yaml
  :emphasize-lines: 4,6,8

  [...]
  log:
    # Change the log level. Possible values (case-insensitive) are CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG.
    level: "WARNING"
    # The log level for database log messages. Possible values (case-insensitive) are CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG.
    databaselevel: "WARNING"
    # The log level for event log messages. Possible values (case-insensitive) are ERROR, INFO, DEBUG.
    eventslevel: "ERROR"
  [...]

::

  [isabell@stardust ~]$ supervisorctl restart vikunja
  vikunja: stopped
  vikunja: started
  [isabell@stardust ~]$


Activate mailer
---------------

In order to receive emails from Vikunja, e.g. notifications or password reset emails, you have to enable the mailer by adding your email config to Vikunja's config file and restarting the API-server:

.. code-block:: yaml
  :emphasize-lines: 4,8,10,12,14,16,18

  [...]
  service:
    # The URL of the frontend, used to send password reset emails.
    frontendurl: "https://isabell.uber.space"

  mailer:
    # Whether to enable the mailer or not. If it is disabled, all users are enabled right away and password reset is not possible.
    enabled: true
    # SMTP Host
    host: "stardust.uberspace.de"
    # SMTP Host port.
    port: 587
    # SMTP username
    username: "isabell@uber.space"
    # SMTP password
    password: "SuperSecretMailPassword"
    # The default from address when sending emails
    fromemail: "isabell@uber.space"
    [...]

::

  [isabell@stardust ~]$ supervisorctl restart vikunja
  vikunja: stopped
  vikunja: started
  [isabell@stardust ~]$


..
  ##### Link section #####

.. _Vikunja: https://vikunja.io/
.. _documentation: https://vikunja.io/docs/
.. _licence: https://kolaente.dev/vikunja/api/src/branch/main/LICENSE
.. _releases: https://dl.vikunja.io/api/
.. _changelog: https://kolaente.dev/vikunja/api/src/branch/main/CHANGELOG.md
.. _downloads: https://dl.vikunja.io/frontend/
.. _guide: https://lab.uberspace.de/howto_website/
.. _webbackend: https://manual.uberspace.de/web-backends.html

----

Tested with Vikunja backend 0.20.2, frontend 0.20.3, Uberspace 7.14.1

.. author_list::
