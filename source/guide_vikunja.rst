.. author:: Sascha Mann <https://saschamann.eu/>
.. author:: Tobias Quathamer <t.quathamer@mailbox.org>

.. tag:: lang-go
.. tag:: lang-javascript
.. tag:: project-management
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/vikunja.png
      :align: center


#######
Vikunja
#######

.. tag_list::

Vikunja_ is a self-hosted to-do and project management app using the AGPL licence_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`Mail <mail-access>`


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

Find the latest version of Vikunja on the releases_ page and download it:

.. code-block:: console

  [isabell@stardust ~]$ VERSION=0.24.6
  [isabell@stardust ~]$ mkdir ~/vikunja
  [isabell@stardust ~]$ wget -O ~/vikunja/vikunja.zip "https://dl.vikunja.io/vikunja/$VERSION/vikunja-v$VERSION-linux-amd64-full.zip"
  [...]
  Saving to: ‘/home/isabell/vikunja/vikunja.zip’

  100%[==========================================================>] 30,607,427  70.3MB/s   in 0.4s

  2024-10-14 20:24:47 (70.3 MB/s) - '/home/isabell/vikunja/vikunja.zip' saved [30607427/30607427]


Verifying (optional)
--------------------

Optionally you can verify the downloaded file using :command:`gpg`. To do so, download the pgp signature file and trust key
and verify the binary:

.. code-block:: console
  :emphasize-lines: 7

  [isabell@stardust ~]$ wget --output-document ~/vikunja/vikunja.zip.asc "https://dl.vikunja.io/vikunja/$VERSION/vikunja-v$VERSION-linux-amd64-full.zip.asc"
  [...]
  [isabell@stardust ~]$ gpg --keyserver keyserver.ubuntu.com --recv FF054DACD908493A
  [...]
  [isabell@stardust ~]$ gpg --verify ~/vikunja/vikunja.zip.asc ~/vikunja/vikunja.zip
  gpg: Signature made Sun Sep 29 16:24:53 2024 CEST using RSA key ID D908493A
  gpg: Good signature from "Frederic (Vikunja) (The key to sign vikunja releases.) <  frederic@vikunja.io>"
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 7D06 1A4A A614 36B4 0713  D42E FF05 4DAC D908 493A

If the verification is fine, we get a ``Good signature from "Frederic (Vikunja) (The key to sign vikunja releases.) <frederic@vikunja.io>"`` line. You can ignore the ``WARNING`` here.


Extract Archive
---------------

Extract the archive containing the Vikunja binary and config file, and rename the binary:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/vikunja
  [isabell@stardust vikunja]$ unzip vikunja.zip
  Archive:  vikunja.zip
    inflating: vikunja-v0.24.4-linux-amd64
    inflating: vikunja-v0.24.4-linux-amd64.sha256
    inflating: LICENSE
    inflating: config.yml.sample
  [isabell@stardust vikunja]$ mv vikunja-v$VERSION-linux-amd64 vikunja
  [isabell@stardust vikunja]$

Clean up the no longer needed archive, signature, and binary hash:

.. code-block:: console

  [isabell@stardust ~]$ rm ~/vikunja/vikunja.zip ~/vikunja/vikunja.zip.asc ~/vikunja/vikunja-v$VERSION-linux-amd64.sha256
  [isabell@stardust ~]$


Set permissions
---------------

The downloaded binary should already be executable. If this is not the case,
set the corresponding permission manually:

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
    password: "SuperSecretDBPassword"
    # Database host
    host: "localhost"
    # Database to use
    database: "isabell_vikunja"
  [...]

There are a couple of settings in the :code:`service` section which need to be set. If you are using Vikunja just for yourself and some friends, you might want to disable registration. Note that you can still create new users by using the :command:`vikunja` binary.

.. code-block:: yaml
  :emphasize-lines: 4,6,8

  [...]
  service:
    # The public facing URL where your users can reach Vikunja. Used in emails and for the communication between api and frontend.
    publicurl: "https://isabell.uber.space/"
    # Whether to let new users registering themselves or not
    enableregistration: false
    # The time zone all timestamps are in. Please note that time zones have to use [the official tz database names](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). UTC or GMT offsets won't work.
    timezone: "UTC"
  [...]

If you want Vikunja to send reminder mails for due tasks (or password reset links), you need to enable the mailer.
Create a new mailbox for vikunja, naming it e. g. :code:`vikunja`:

::

  [isabell@stardust ~]$ uberspace mail user add vikunja
  Enter a password for the mailbox:
  Please confirm your password:
  New mailbox created for user: 'vikunja', it will be live in a few minutes...

Now fill in the details in the configuration file.

.. code-block:: yaml
  :emphasize-lines: 4,6,13,15,19

  [...]
  mailer:
    # Whether to enable the mailer or not. If it is disabled, all users are enabled right away and password reset is not possible.
    enabled: true
    # SMTP Host
    host: "stardust.uberspace.de"
    # SMTP Host port.
    # **NOTE:** If you're unable to send mail and the only error you see in the logs is an `EOF`, try setting the port to `25`.
    port: 587
    # SMTP Auth Type. Can be either `plain`, `login` or `cram-md5`.
    authtype: "plain"
    # SMTP username
    username: "vikunja@isabell.uber.space"
    # SMTP password
    password: "SuperSecretMailPassword"
    # Whether to skip verification of the tls certificate on the server
    skiptlsverify: false
    # The default from address when sending emails
    fromemail: "vikunja@isabell.uber.space"
  [...]

Lastly, you should think about some sensible default values for your newly created
users. If you are e. g. in Germany, you should set the appropriate timezone and start of
the week.

.. code-block:: yaml
  :emphasize-lines: 4,6

  [...]
  defaultsettings:
    # Start of the week for the user. `0` is sunday, `1` is monday and so on.
    week_start: 1
    # The time zone of each individual user. This will affect when users get reminders and overdue task emails.
    timezone: "Europe/Berlin"
  [...]

.. note::

  See the Vikunja documentation_ and the configuration sample for all configuration options.


Finishing installation
======================

In order to set up the database, run all migrations for Vikunja.

::

  [isabell@stardust ~]$ ~/vikunja/vikunja migrate
  2024-10-15T18:41:36+02:00: INFO ▶ 001 Using config file: /home/isabell/vikunja/config.yml
  2024-10-15T18:41:36+02:00: INFO ▶ 002 Running migrations…
  2024-10-15T18:41:41+02:00: INFO ▶ 0df Ran all migrations successfully.
  [isabell@stardust ~]$

Now create the first user.

::

  [isabell@stardust ~]$ ~/vikunja/vikunja user create --username isabell --password SuperSecret --email isabell@uber.space
  2024-10-15T20:47:39+02:00: INFO ▶ 001 Using config file: /home/isabell/vikunja/config.yml
  2024-10-15T20:47:39+02:00: INFO ▶ 002 Running migrations…
  2024-10-15T20:47:39+02:00: INFO ▶ 06a Ran all migrations successfully.

  User was created successfully.
  [isabell@stardust ~]$


Service for Vikunja
-------------------

To keep Vikunja up and running in the background, you need to create a service that takes care of it. Create a config file :file:`~/etc/services.d/vikunja.ini` for the service:

.. code-block:: ini

  [program:vikunja]
  directory=%(ENV_HOME)s/vikunja
  command=%(ENV_HOME)s/vikunja/vikunja
  startsecs=30
  autorestart=yes

.. include:: includes/supervisord.rst

.. note::
  The status of vikunja must be :code:`RUNNING`. If it's not,
  check the log output at :file:`~/logs/supervisord.log` and the
  configuration file :file:`~/vikunja/config.yml`.

Uberspace web backend
---------------------

In order to access Vikunja, you need to configure a web backend. Vikunja
serves both the API part and the frontend part via port 3456.

.. note:: Vikunja is running on port 3456.

.. include:: includes/web-backend.rst

Installed files and folders are:

* ``~/vikunja``
* ``~/etc/services.d/vikunja.ini``

Now we are done and can access Vikunja through ``isabell.uber.space``.


Optional steps
==============

Enabling migrations from other services
---------------------------------------

If you've used other organizers previously, Vikunja comes with a few migration
services. You can import your data from another Vikunja instance, TickTick,
Trello, Microsoft To Do, and Todoist. You need to enable the specific
migration service in the configuration file and restart Vikinja.

::

  [isabell@stardust ~]$ supervisorctl restart vikunja
  vikunja: stopped
  vikunja: started
  [isabell@stardust ~]$


Change log levels
-----------------

By default the log configuration is very verbose. You can change it to only log warnings, errors, or critical events by editing the config file and restarting Vikunja:

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


Updates
=======

.. note:: Check the changelog_ or releases_ page regularly to stay informed about the newest version.


Manual updating
-----------------

* Stop the application :command:`supervisorctl stop vikunja`
* Do the *download* (and optionally *verifying*) part from above.
* Check if you have to modify the config file. (See documentation_.)
* Start the application :command:`supervisorctl start vikunja`
* Check if the application is running :command:`supervisorctl status vikunja`


.. _Vikunja: https://vikunja.io/
.. _documentation: https://vikunja.io/docs/
.. _licence: https://kolaente.dev/vikunja/vikunja/src/branch/main/LICENSE
.. _releases: https://dl.vikunja.io/vikunja
.. _changelog: https://kolaente.dev/vikunja/vikunja/src/branch/main/CHANGELOG.md

----

Tested with Vikunja 0.24.4, Uberspace 7.16.1

.. author_list::
