.. author:: Rychart Redwerkz <https://zkrew.red>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: version-control

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/forgejo.svg
      :align: center

.. spelling:wordlist:
  forgejo
  Forgejo

#######
Forgejo
#######

.. tag_list::

Forgejo_ is a self-hosted Git service with a functionality similar to GitHub, GitLab and BitBucket.
It's a soft-fork of Gitea_ and uses the same MIT licence_. As most applications written in Go it's easy to install.

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

  [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_forgejo"
  [isabell@stardust ~]$

We can use the uberspace or [your own domain](https://manual.uberspace.de/web-domains/#setup):

.. include:: includes/web-domain-list.rst


Installation
============


Download
--------

Check current version of Forgejo at releases_ page:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/forgejo
  [isabell@stardust ~]$ wget -O ~/forgejo/forgejo https://codeberg.org/attachments/be5952ea-6cfb-4be5-a593-3564c4bd8cc9
  [...]
  Saving to: ‘/home/redwerkz/forgejo/forgejo’

  100%[=======================================================>] 117,987,088 79.8MB/s   in 1.4s

  2023-02-17 19:38:27 (79.8 MB/s) - ‘/home/redwerkz/forgejo/forgejo’ saved [117987088/117987088]
  [isabell@stardust ~]$


Set permissions
---------------

Make the downloaded binary executable:

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/forgejo/forgejo
  [isabell@stardust ~]$


Configuration
=============

We will need to create some random characters as a security key for the configuration:

.. code-block:: console

  [isabell@stardust ~]$ ~/forgejo/forgejo generate secret SECRET_KEY
  <RANDOM_64_CHARACTERS_FROM_GENERATOR>
  [isabell@stardust ~]$

Copy or save the output for later.

Forgejo configuration file
--------------------------

Create a custom directory for your configurations:

.. code-block:: console

  [isabell@stardust ~]$ mkdir --parents ~/forgejo/custom/conf/
  [isabell@stardust ~]$

Create a config file ``~/forgejo/custom/conf/app.ini`` with the content of the following code block:

.. note:: Replace ``isabell`` with your username, fill the database password ``PASSWD =`` with yours and enter the generated random into ``SECRET_KEY =``.

.. code-block:: ini
  :emphasize-lines: 2,9-11,17,25,30

  [server]
  DOMAIN               = isabell.uber.space
  ROOT_URL             = https://%(DOMAIN)s
  OFFLINE_MODE         = true ; privacy option.
  LFS_START_SERVER     = true ; Enables Git LFS support

  [database]
  DB_TYPE  = mysql
  NAME     = isabell_forgejo
  USER     = isabell
  PASSWD   = <MySQL_PASSWORD>

  [security]
  INSTALL_LOCK        = true
  MIN_PASSWORD_LENGTH = 8
  PASSWORD_COMPLEXITY = lower ; This allows well to remember but still secure passwords
  SECRET_KEY          = <RANDOM_64_CHARACTERS_FROM_GENERATOR> ; the before generated security key

  [service]
  DISABLE_REGISTRATION       = true ; security option, only admins can create new users.
  SHOW_REGISTRATION_BUTTON   = false
  REGISTER_EMAIL_CONFIRM     = true
  DEFAULT_ORG_VISIBILITY     = private ; [public, limited, private]
  DEFAULT_KEEP_EMAIL_PRIVATE = true
  NO_REPLY_ADDRESS           = noreply.isabell.uber.space

  [mailer]
  ENABLED     = true
  MAILER_TYPE = sendmail
  FROM        = isabell@uber.space

.. note::

  This config block contains a secure and convenient basic configuration. You may change it depending on your needs and knowledge.
  See the Forgejo documentation_ and the Forgejo `configuration sample <https://codeberg.org/forgejo/forgejo/raw/branch/main/custom/conf/app.example.ini>`_
  for more configuration possibilities.

Database initialization
-----------------------

Migrate the database configurations:

.. code-block:: console

  [isabell@stardust ~]$ ~/forgejo/forgejo migrate
  [...]
  2023/02/17 19:43:28 models/db/engine.go:126:SyncAllTables() [I] [SQL] CREATE INDEX `IDX_package_version_created_unix` ON `package_version` (`created_unix`) [] - 25.0114ms
  2023/02/17 19:43:28 models/db/engine.go:126:SyncAllTables() [I] [SQL] CREATE INDEX `IDX_package_version_is_internal` ON `package_version` (`is_internal`) [] - 29.933338ms
  [isabell@stardust ~]$

Forgejo admin user
------------------

Set your admin login credentials:

.. code-block:: console

  [isabell@stardust ~]$ ADMIN_USERNAME=AdminUsername
  [isabell@stardust ~]$ ADMIN_PASSWORD='SuperSecretAdminPassword'
  [isabell@stardust ~]$ ~/forgejo/forgejo admin user create --username ${ADMIN_USERNAME} --password ${ADMIN_PASSWORD} --email ${USER}@uber.space --admin
  [...]
  2023/02/17 19:50:04 ...@v1.22.10/command.go:173:Run() [I] [SQL] COMMIT [] - 46.568973ms
  New user 'AdminUsername' has been successfully created!
  [isabell@stardust ~]$

.. note::

  Forgejo does not allow ``admin`` as name, of course you should choose and replace the password.

Finishing installation
======================

Service for Forgejo
-------------------

To keep Forgejo up and running in the background, you need to create a service that takes care for it. Create a config file ``~/etc/services.d/forgejo.ini`` for the service:

.. code-block:: ini

  [program:forgejo]
  directory=%(ENV_HOME)s/forgejo
  command=%(ENV_HOME)s/forgejo/forgejo web
  startsecs=30
  autorestart=yes

.. include:: includes/supervisord.rst

.. note:: The status of forgejo must be ``RUNNING``. If its not check the log output at ``~/logs/supervisord.log`` and the configuration file ``~/forgejo/custom/conf/app.ini``.

Uberspace web backend
---------------------

.. note:: forgejo is running on port 3000.

.. include:: includes/web-backend.rst

Done. We can point our browser to https://isabell.uber.space/.

Installed files and folders are:

* ``~/forgejo/``
* ``~/etc/services.d/forgejo.ini``

Backup
======

The Forgejo CLI (command line interface) has a build-in backup command to create a full backup in a zip file with the database, repos, config, log, data

.. note:: To restore a backup follow the `backup and restore documentation <https://docs.gitea.io/en-us/backup-and-restore/#restore-command-restore>`_

Execute the following command:

::

  [isabell@stardust ~]$ ~/forgejo/forgejo dump
  2023/02/17 20:33:59 ...dules/setting/log.go:288:newLogService() [I] Gitea v1.18.3-1 built with GNU Make 4.1, go1.19.5 : bindata, sqlite, sqlite_unlock_notify
  2023/02/17 20:33:59 ...dules/setting/log.go:335:newLogService() [I] Gitea Log Mode: Console(Console:info)
  [...]
  2023/02/17 20:33:59 cmd/dump.go:245:runDump() [I] Dumping local repositories... /home/isabell/forgejo/data/forgejo-repositories
  2023/02/17 20:34:04 cmd/dump.go:283:runDump() [I] Dumping database...
  [...]
  2023/02/17 20:34:04 cmd/dump.go:295:runDump() [I] Adding custom configuration file from /home/isabell/forgejo/custom/conf/app.ini
  2023/02/17 20:34:04 cmd/dump.go:323:runDump() [I] Packing data directory.../home/isabell/forgejo/data
  [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ or releases_ page regularly to stay informed about the newest version.


Manual updating
---------------

* Stop the application ``supervisorctl stop forgejo``
* Do the *Download* (and optionally *Verifying*) part from above.
* Check if you have to modify the config file. (See documentation_ and the `file sample <https://codeberg.org/forgejo/forgejo/raw/branch/main/custom/conf/app.example.ini>`_.)
* Do the database migration: ``~/forgejo/forgejo migrate``
* Start the application ``supervisorctl start forgejo``
* Check if the application is running ``supervisorctl status forgejo``


Additional configuration
========================

Forgejo ssh setup (optional)
----------------------------

Forgejo can manage the ssh keys. To use this feature we have to link the ssh folder into the forgejo folder.

.. code-block:: console

  [isabell@stardust ~]$ ln -s ~/.ssh ~/forgejo/.ssh
  [isabell@stardust ~]$

Now our Forgejo users can add their ssh keys via the menu in the up right corner: ``->`` settings ``->`` tab: SSH/GPG Keys ``->`` Add Key. Forgejo is automatically writing a ssh key command into the ``/home/isabell/.ssh/authorized_keys`` file. The key line is something similar like:

.. code-block:: bash

  command="/home/isabell/forgejo/forgejo --config='/home/isabell/forgejo/custom/conf/app.ini' serv key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAAC... youruser@yourhost

If we're using the same ssh key for auth to Uberspace and Forgejo, we need to modify the server ``/home/isabell/.ssh/authorized_keys`` file.

.. code-block:: bash

  command="if [ -t 0 ]; then bash; elif [[ ${SSH_ORIGINAL_COMMAND} =~ ^(scp|rsync|mysqldump).* ]]; then eval ${SSH_ORIGINAL_COMMAND}; else /home/isabell/forgejo/forgejo serv key-1 --config='/home/isabell/forgejo/custom/conf/app.ini'; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-...

.. warning::
  * Be careful to keep the key number ``key-X``, keep your key ``ssh-...`` and change the username ``isabell`` to yours.
  * Take care that there is no second line propagating the same ssh key.

.. note:: You can still use the Uberspace dashboard_ to add other ssh keys for running default ssh sessions.

To interact with Forgejo at our local machine like ``git clone isabell@isabell.uber.space:forgejouser/somerepo.git`` we configure the ``/home/localuser/.ssh/config`` file for our local machine with the git ssh key.

.. code-block::

  Host isabell.uber.space
      HostName isabell.uber.space
      User isabell
      IdentityFile ~/.ssh/id_your_git_key
      IdentitiesOnly yes

Forgejo using external renderer (optional)
------------------------------------------

| Forgejo supports custom file renderings (i.e. Jupyter notebooks, asciidoc, etc.) through external binaries to provide a preview.
| In this case we install an `external rendering <https://docs.gitea.io/en-us/external-renderers/>`_ extension for AsciiDoc.
| AsciiDoctors location will be here: ``~/.gem/ruby/2.7.0/*/asciidoctor*``

.. code-block:: console

  [isabell@stardust ~]$ gem install asciidoctor
  Fetching asciidoctor-2.0.10.gem
  WARNING:  You don't have /home/isabell/.gem/ruby/2.7.0/bin in your PATH,
  	  gem executables will not run.
  Successfully installed asciidoctor-2.0.10
  1 gem installed
  [isabell@stardust ~]$

.. note:: Don't be irritated by the warning that the bin folder isn't in the path. Uberspace is taking care of it. You can check with ``[isabell@stardust ~]$ which asciidoctor``.

Now we have to append the config file ``~/forgejo/custom/conf/app.ini`` with:

.. code-block:: ini

  [markup.asciidoc]
  ENABLED = true
  FILE_EXTENSIONS = .adoc,.asciidoc
  RENDER_COMMAND = "asciidoctor -e -a leveloffset=-1 --out-file=- -"
  IS_INPUT_FILE = false

..
  ##### Link section #####

.. _Forgejo: https://forgejo.org/
.. _Gitea: https://gitea.io/
.. _documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: view-source:https://forgejo.org/releases/rss.xml
.. _releases: https://codeberg.org/forgejo/forgejo/releases
.. _licence: https://codeberg.org/forgejo/forgejo/raw/branch/forgejo/LICENSE
.. _dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Forgejo 1.18.3-1, Uberspace 7.15.0

.. author_list::
