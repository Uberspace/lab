.. author:: Marc Redwerkz <https://wzrd.pw>

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
It's a hard-fork of Gitea_, created in 2022. Forgejo changed_ it's license in August 2024 from MIT (inherited from Gitea) to the GNU GPL v2 licence_. Like most applications written in Go it's easy to install.

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

  [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_forgejo CHARACTER SET utf8mb4 COLLATE utf8mb4_bin"
  [isabell@stardust ~]$

We can use the uberspace or `your own domain <https://manual.uberspace.de/web-domains/#setup>`_:

.. include:: includes/web-domain-list.rst


Installation
============


Download
--------

Check current version of Forgejo at releases_ page or scrape it from feed_ with this one liner:

.. code-block:: console

  [isabell@stardust ~]$ FORGEJO_HOME="$HOME/forgejo"
  [isabell@stardust ~]$ mkdir $FORGEJO_HOME
  [isabell@stardust ~]$ feed_url='https://forgejo.org/releases/rss.xml'
  [isabell@stardust ~]$ latest=$(curl -s "$feed_url" | grep -oP '<title>\Kv[0-9]+\.[0-9]+\.[0-9]+(?=</title>)' | head -n 1 | sed 's/^v//')
  [isabell@stardust ~]$ wget -c -P /tmp https://codeberg.org/forgejo/forgejo/releases/download/v${latest}/forgejo-${latest}-linux-amd64.xz
  [...]
  Saving to: ‘/tmp/forgejo-9.0.3-linux-amd64.xz’

  100%[=======================================================>] 33,034,888  62.1MB/s   in 0.5s

  2024-12-27 17:08:07 (62.1 MB/s) - ‘/tmp/forgejo-9.0.3-linux-amd64.xz’ saved [33034888/33034888]

  [isabell@stardust ~]$

Extract binary
--------------

Extract the downloaded binary:

.. code-block:: console

  [isabell@stardust ~]$ unxz /tmp/forgejo-${latest}-linux-amd64.xz
  [isabell@stardust ~]$ mv /tmp/forgejo-${latest}-linux-amd64 $FORGEJO_HOME/forgejo-${latest}
  [isabell@stardust ~]$

Set permissions
---------------

Make the binary executable:

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x $FORGEJO_HOME/forgejo-${latest}
  [isabell@stardust ~]$ ln --force --symbolic $FORGEJO_HOME/forgejo-${latest} $FORGEJO_HOME/forgejo
  [isabell@stardust ~]$


Configuration
=============

We will need to create some random characters as a security key for the configuration:

.. code-block:: console

  [isabell@stardust ~]$ $FORGEJO_HOME/forgejo generate secret SECRET_KEY
  <RANDOM_64_CHARACTERS_FROM_GENERATOR>
  [isabell@stardust ~]$

Copy or save the output for later.

Forgejo configuration file
--------------------------

Create a custom directory for your configurations:

.. code-block:: console

  [isabell@stardust ~]$ mkdir --parents $FORGEJO_HOME/custom/conf/
  [isabell@stardust ~]$ touch $FORGEJO_HOME/custom/conf/app.ini
  [isabell@stardust ~]$

Create a config file ``$FORGEJO_HOME/custom/conf/app.ini`` with the content of the following code block:

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
  HOST     = 127.0.0.1:3306
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
  PROTOCOL    = sendmail ; [smtp, smtps, smtp+starttls, smtp+unix, sendmail, dummy]
  FROM        = isabell@uber.space

.. note::

  This config block contains a secure and convenient basic configuration. You may change it depending on your needs and knowledge.
  See the Forgejo documentation_ and the Forgejo `configuration sample <https://codeberg.org/forgejo/forgejo/raw/branch/main/custom/conf/app.example.ini>`_
  for more configuration possibilities.

Database initialization
-----------------------

Migrate the database configurations:

.. code-block:: console

  [isabell@stardust ~]$ $FORGEJO_HOME/forgejo migrate
  2024/12/27 17:17:48 cmd/migrate.go:33:runMigrate() [I] AppPath: /home/isabell/forgejo/forgejo
  2024/12/27 17:17:48 cmd/migrate.go:34:runMigrate() [I] AppWorkPath: /home/isabell/forgejo
  2024/12/27 17:17:48 cmd/migrate.go:35:runMigrate() [I] Custom path: /home/isabell/forgejo/custom
  2024/12/27 17:17:48 cmd/migrate.go:36:runMigrate() [I] Log path: /home/isabell/forgejo/log
  2024/12/27 17:17:48 cmd/migrate.go:37:runMigrate() [I] Configuration file: /home/isabell/forgejo/custom/conf/app.ini
  2024/12/27 17:17:48 ...2@v2.27.4/command.go:269:Run() [I] PING DATABASE mysql
  [isabell@stardust ~]$

Forgejo admin user
------------------

Set your admin login credentials:

.. code-block:: console

  [isabell@stardust ~]$ ADMIN_USERNAME='admin_user'
  [isabell@stardust ~]$ ADMIN_PASSWORD='change_me!'
  [isabell@stardust ~]$ $FORGEJO_HOME/forgejo admin user create --username ${ADMIN_USERNAME} --password ${ADMIN_PASSWORD} --email ${USER}@uber.space --admin
  New user 'AdminUsername' has been successfully created!
  [isabell@stardust ~]$

.. note::

  Forgejo does not allow ``admin`` as name, of course you should choose and replace the password!

Finishing installation
======================

Service for Forgejo
-------------------

.. code-block:: console

  [isabell@stardust ~]$ touch $HOME/etc/services.d/forgejo.ini
  [isabell@stardust ~]$

To keep Forgejo up and running in the background, you need to create a service that takes care for it. Create a config file ``$HOME/etc/services.d/forgejo.ini`` for the service:

.. code-block:: ini

  [program:forgejo]
  directory=%(ENV_HOME)s/forgejo
  command=%(ENV_HOME)s/forgejo/forgejo web
  startsecs=30
  autorestart=yes

.. include:: includes/supervisord.rst

.. note:: The status of forgejo must be ``RUNNING``. If its not check the log output at ``$HOME/logs/supervisord.log`` and the configuration file ``$FORGEJO_HOME/custom/conf/app.ini``.

Uberspace web backend
---------------------

.. note:: forgejo is running on port 3000.

.. include:: includes/web-backend.rst

Done. We can point our browser to https://isabell.uber.space/.

Installed files and folders are:

* ``$FORGEJO_HOME``
* ``$HOME/etc/services.d/forgejo.ini``

Forgejo SSH setup
-----------------

In order for users to be able to push to your Forgejo instance, they need to add their SSH keys via the menu in the upper right corner: ``->`` Settings ``->`` SSH/GPG Keys ``->`` Add Key.
Forgejo automatically writes an SSH key command for each added SSH key into the ``$HOME/.ssh/authorized_keys`` file. The key line is something similar like:

.. code-block:: bash

  command="$FORGEJO_HOME/forgejo --config=$FORGEJO_HOME/custom/conf/app.ini serv key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty,no-user-rc,restrict ssh-ed25519 AAAAC... user@host

.. warning::
  If you're using the same SSH key for authentication to Uberspace and Forgejo, you need to modify the server ``$HOME/.ssh/authorized_keys`` file.
  Otherwise, you'll lock yourself out from accessing your Uberspace via SSH.
  An alternative approach would be to add another SSH key in the Uberspace dashboard and use that for logging into Uberspace.

  * Be careful to keep the key number ``key-X`` and keep your key ``ssh-...``.
  * Ensure that there is no second line propagating the same SSH key.

.. code-block:: bash

  command="if [ -t 0 ]; then bash; elif [[ ${SSH_ORIGINAL_COMMAND} =~ ^(scp|rsync|mysqldump).* ]]; then eval ${SSH_ORIGINAL_COMMAND}; else $FORGEJO_HOME/forgejo --config=$FORGEJO_HOME/custom/conf/app.ini serv key-1; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty,no-user-rc,restrict ssh-ed25519 AAAAC... youruser@yourhost

.. note:: You can still use the Uberspace dashboard_ to add other ssh keys for running default ssh sessions.

To interact with Forgejo at our local machine like ``git clone isabell@isabell.uber.space:forgejouser/somerepo.git`` we configure the ``/home/localuser/.ssh/config`` file for our local machine with the git ssh key.

.. code-block::

  Host isabell.uber.space
      User isabell
      IdentityFile ~/.ssh/id_ed25519
      IdentitiesOnly yes

Backup
======

The Forgejo CLI (command line interface) has a build-in backup command to create a full backup in a zip file with the database, repos, config, log, data

.. note:: To restore a backup follow the `backup and restore documentation <https://docs.gitea.io/en-us/backup-and-restore/#restore-command-restore>`_

Execute the following command:

::

  [isabell@stardust ~]$ $FORGEJO_HOME/forgejo dump
  2024/12/27 17:39:13 ...s/setting/session.go:77:loadSessionFrom() [I] Session Service Enabled
  [...]
  2024/12/27 17:39:13 cmd/dump.go:265:runDump() [I] Dumping local repositories... /home/isabell/forgejo/data/forgejo-repositories
  2024/12/27 17:39:13 cmd/dump.go:306:runDump() [I] Dumping database...
  [...]
  2024/12/72 17:39:13 cmd/dump.go:430:runDump() [I] Finish dumping in file forgejo-dump-1735313953.zip
  [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ or releases_ page regularly to stay informed about the newest version.


Manual updating
---------------

* Do the *Download* and *Set permissions* steps from above.
* Check if you have to modify the config file. (See documentation_ and the `file sample <https://codeberg.org/forgejo/forgejo/raw/branch/main/custom/conf/app.example.ini>`_.)
* Do the database migration: ``$FORGEJO_HOME/forgejo migrate``
* Start the application ``supervisorctl restart forgejo``
* Check if the application is running ``supervisorctl status forgejo``


Additional configuration
========================

Forgejo using external renderer (optional)
------------------------------------------

| Forgejo supports custom file renderings (i.e. Jupyter notebooks, asciidoc, etc.) through external binaries to provide a preview.
| In this case we install an `external rendering <https://docs.gitea.io/en-us/external-renderers/>`_ extension for AsciiDoc.
| AsciiDoctors location will be here: ``$HOME/.gem/ruby/3.2.0/*/asciidoctor*``

.. code-block:: console

  [isabell@stardust ~]$ gem install asciidoctor
  Fetching asciidoctor-2.0.23.gem
  WARNING:  You don't have /home/isabell/.gem/ruby/3.2.0/bin in your PATH,
  	  gem executables will not run.
  Successfully installed asciidoctor-2.0.23
  1 gem installed
  [isabell@stardust ~]$

.. note:: Don't be confused by the warning that the bin folder isn't in the path. Uberspace is taking care of it. You can check with ``[isabell@stardust ~]$ which asciidoctor``.

Now we have to append the config file ``$FORGEJO_HOME/custom/conf/app.ini`` with:

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
.. _feed: https://forgejo.org/releases/rss.xml
.. _releases: https://codeberg.org/forgejo/forgejo/releases
.. _licence: https://codeberg.org/forgejo/forgejo/raw/branch/forgejo/LICENSE
.. _changed: https://forgejo.org/2024-08-gpl/
.. _dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Forgejo 9.0.3, Uberspace 7.16.03

.. author_list::
