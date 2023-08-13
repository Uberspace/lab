.. author:: Frank ℤisko <https://frank.zisko.io>
.. author:: EV21 <uberlab@ev21.de>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: version-control

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitea.png
      :align: center

.. spelling::
  repos

#####
Gitea
#####

.. tag_list::

Gitea_ is a self-hosted Git service with a functionality similar to GitHub, GitLab and BitBucket. It's a fork of Gogs_ and uses the same MIT licence_. As most applications written in Go it's easy to install.

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

  [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_gitea"
  [isabell@stardust ~]$

We can use the uberspace or your own domain:

.. include:: includes/web-domain-list.rst


Installation
============


Download
--------

Check current version of Gitea at releases_ page:

.. code-block:: console

  [isabell@stardust ~]$ VERSION=1.19.3
  [isabell@stardust ~]$ mkdir ~/gitea
  [isabell@stardust ~]$ wget -O ~/gitea/gitea https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64
  [...]
  Saving to: ‘/home/isabell/gitea/gitea’

  100%[========================================================>] 83,243,800  14.9MB/s   in 9.8s

  2020-06-01 21:00:42 (8.11 MB/s) - ‘/home/isabell/gitea/gitea’ saved [83243800/83243800]
  [isabell@stardust ~]$


Verifying (optional)
--------------------

Optionally you can verify the downloaded file using ``gpg``. To do so, download the pgp signature file and trust key
and verify the binary:

.. code-block:: console
  :emphasize-lines: 7

  [isabell@stardust ~]$ wget --output-document ~/gitea/gitea.asc https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64.asc
  […]
  [isabell@stardust ~]$ curl --silent https://keys.openpgp.org/vks/v1/by-fingerprint/7C9E68152594688862D62AF62D9AE806EC1592E2 | gpg --import
  […]
  [isabell@stardust ~]$ gpg --verify ~/gitea/gitea.asc ~/gitea/gitea
  gpg: Signature made Do 03 Mär 2022 15:48:38 CET using RSA key ID 9753F4B0
  gpg: Good signature from "Teabot <teabot@gitea.io>"
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 7C9E 6815 2594 6888 62D6  2AF6 2D9A E806 EC15 92E2
       Subkey fingerprint: CC64 B1DB 67AB BEEC AB24  B645 5FC3 4632 9753 F4B0

If the verification is fine, we get a ``gpg: Good signature from "Teabot <teabot@gitea.io>"`` line. You need to ignore the ``WARNING`` here.


Set permissions
---------------

Make the downloaded binary executable:

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/gitea/gitea
  [isabell@stardust ~]$


Configuration
=============

We will need to create some random characters as a security key for the configuration:

.. code-block:: console

  [isabell@stardust ~]$ ~/gitea/gitea generate secret SECRET_KEY
  <RANDOM_64_CHARACTERS_FROM_GENERATOR>
  [isabell@stardust ~]$

Copy or save the output for later.

Gitea configuration file
-------------------------

Create a custom directory for your configurations:

.. code-block:: console

  [isabell@stardust ~]$ mkdir --parents ~/gitea/custom/conf/
  [isabell@stardust ~]$

Create a config file ``~/gitea/custom/conf/app.ini`` with the content of the following code block:

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
  NAME     = isabell_gitea
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
  ENABLED  = true
  PROTOCOL = sendmail
  FROM     = isabell@uber.space

  [other]
  SHOW_FOOTER_VERSION = false ; hide version number from strangers - you can still see it in the admin panel at /admin

.. note::

  This config block contains a secure and convenient basic configuration. You may change it depending on your needs and knowledge.
  See the Gitea documentation_ and the Gitea `configuration sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.example.ini>`_
  for more configuration possibilities.

Database initialization
-----------------------

Migrate the database configurations:

.. code-block:: console

  [isabell@stardust ~]$ ~/gitea/gitea migrate
  [...]
  2022/03/15 11:59:06 models/db/engine.go:194:InitEngineWithMigration() [I] [SQL] CREATE TABLE IF NOT EXISTS `upload` (`id` BIGINT(20) PRIMARY KEY AUTO_INCREMENT NOT NULL , `uuid` VARCHAR(40) NULL , `name` VARCHAR(255) NULL ) ENGINE=InnoDB DEFAULT CHARSET utf8mb4 ROW_FORMAT=DYNAMIC [] - 44.298441ms
  2022/03/15 11:59:06 models/db/engine.go:194:InitEngineWithMigration() [I] [SQL] CREATE UNIQUE INDEX `UQE_upload_uuid` ON `upload` (`uuid`) [] - 30.158825ms
  [isabell@stardust ~]$

Gitea admin user
----------------

Set your admin login credentials:

.. code-block:: console

  [isabell@stardust ~]$ ADMIN_USERNAME=AdminUsername
  [isabell@stardust ~]$ ADMIN_PASSWORD='SuperSecretAdminPassword'
  [isabell@stardust ~]$ ~/gitea/gitea admin user create --username ${ADMIN_USERNAME} --password ${ADMIN_PASSWORD} --email ${USER}@uber.space --admin
  [isabell@stardust ~]$

.. note::

  Gitea does not allow ``admin`` as name, of course you should choose and replace the password.

Finishing installation
======================

Service for Gitea
-----------------

To keep Gitea up and running in the background, you need to create a service that takes care for it. Create a config file ``~/etc/services.d/gitea.ini`` for the service:

.. code-block:: ini

  [program:gitea]
  directory=%(ENV_HOME)s/gitea
  command=%(ENV_HOME)s/gitea/gitea web
  startsecs=30
  autorestart=yes

.. include:: includes/supervisord.rst

.. note:: The status of gitea must be ``RUNNING``. If its not check the log output at ``~/logs/supervisord.log`` and the configuration file ``~/gitea/custom/conf/app.ini``.

Uberspace web backend
---------------------

.. note:: gitea is running on port 3000.

.. include:: includes/web-backend.rst

Done. We can point our browser to https://isabell.uber.space/.

Installed files and folders are:

* ``~/gitea``
* ``~/etc/services.d/gitea.ini``

Backup
======

The Gitea CLI (command line interface) has a build-in backup command to create a full backup in a zip file with the database, repos, config, log, data

.. note:: To restore a backup follow the `backup and restore documentation <https://docs.gitea.io/en-us/backup-and-restore/#restore-command-restore>`_

Execute the following command:

::

  [isabell@stardust ~]$ ~/gitea/gitea dump
  2022/03/08 17:26:01 ...dules/setting/log.go:283:newLogService() [I] Gitea v1.16.3 built with GNU Make 4.1, go1.17.7 : bindata, sqlite, sqlite_unlock_notify
  [...]
  2022/03/08 17:26:01 ...s/storage/storage.go:171:initAttachments() [I] Initialising Attachment storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/gitea/data/attachments
  2022/03/08 17:26:01 ...s/storage/storage.go:165:initAvatars() [I] Initialising Avatar storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/gitea/data/avatars
  2022/03/08 17:26:01 ...s/storage/storage.go:183:initRepoAvatars() [I] Initialising Repository Avatar storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/gitea/data/repo-avatars
  2022/03/08 17:26:01 ...s/storage/storage.go:177:initLFS() [I] Initialising LFS storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/gitea/data/lfs
  2022/03/08 17:26:01 ...s/storage/storage.go:189:initRepoArchives() [I] Initialising Repository Archive storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/gitea/data/repo-archive
  2022/03/08 17:26:01 cmd/dump.go:270:runDump() [I] Dumping database...
  [...]
  2022/03/08 17:26:01 cmd/dump.go:282:runDump() [I] Adding custom configuration file from /home/isabell/gitea/custom/conf/app.ini
  2022/03/08 17:26:01 cmd/dump.go:310:runDump() [I] Packing data directory.../home/isabell/gitea/data
  2022/03/08 17:26:01 cmd/dump.go:379:runDump() [I] Finish dumping in file gitea-dump-1646756761.zip
  [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ or releases_ page regularly to stay informed about the newest version.


Manual updating
-----------------

* Stop the application ``supervisorctl stop gitea``
* Do the *Download* (and optionally *Verifying*) part from above.
* Check if you have to modify the config file. (See documentation_ and the `file sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample>`_.)
* Do the database migration: ``~/gitea/gitea migrate``
* Start the application ``supervisorctl start gitea``
* Check if the application is running ``supervisorctl status gitea``


Automated updating by custom script
-----------------------------------

You can also automate the update by using a custom script that automatically executes all the update steps. Create ``~/bin/gitea-update`` with the following content:

.. code-block:: bash

  #!/usr/bin/env bash

  APP_NAME=Gitea
  GITEA_BINARY=$HOME/gitea/gitea
  TMP_LOCATION=$HOME/tmp
  PGP_KEY_FINGERPRINT=7C9E68152594688862D62AF62D9AE806EC1592E2

  ORG=go-gitea # Organisation or GitHub user
  REPO=gitea
  GITHUB_API_URL=https://api.github.com/repos/$ORG/$REPO/releases/latest

  function do_update_procedure
  {
    curl --location --progress-bar --output "$TMP_LOCATION"/gitea "$DOWNLOAD_URL"
    verify_file
    $GITEA_BINARY manager flush-queues
    supervisorctl stop gitea
    mv --verbose "$TMP_LOCATION"/gitea "$GITEA_BINARY"
    chmod u+x --verbose "$GITEA_BINARY"
    echo "$APP_NAME service takes 30 seconds to start"
    supervisorctl start gitea
    supervisorctl status gitea
  }

  function set_local_version
  {
    LOCAL_VERSION=$($GITEA_BINARY --version |
      awk '{print $3}')
  }

  function set_latest_version
  {
    curl --silent $GITHUB_API_URL > "$TMP_LOCATION"/github_api_response.json
    TAG_NAME=$(jq --raw-output '.tag_name' "$TMP_LOCATION"/github_api_response.json)
    LATEST_VERSION=${TAG_NAME:1}
    DOWNLOAD_URL=$(jq --raw-output '.assets[].browser_download_url' "$TMP_LOCATION"/github_api_response.json |
      grep --max-count=1 "linux-amd64")
  }

  function download_signature_file
  {
    SIGNATURE_FILE_URL=$(jq --raw-output '.assets[].browser_download_url' "$TMP_LOCATION"/github_api_response.json |
      grep "linux-amd64.asc")
    rm "$TMP_LOCATION"/github_api_response.json
    wget --quiet --progress=bar:force --output-document "$TMP_LOCATION"/gitea.asc "$SIGNATURE_FILE_URL"
  }

  function verify_file
  {
    download_signature_file

    ## downloading public key if it does NOT already exist OR if it is expired
    if ! gpg --fingerprint $PGP_KEY_FINGERPRINT ||
      (gpg --fingerprint $PGP_KEY_FINGERPRINT | grep expired)
    then
      ## currently the key download via gpg does not work on Uberspace
      #gpg --keyserver keys.openpgp.org --recv $PGP_KEY_FINGERPRINT
      curl --silent https://keys.openpgp.org/vks/v1/by-fingerprint/$PGP_KEY_FINGERPRINT | gpg --import
    fi

    if ! gpg --export-ownertrust | grep --quiet $PGP_KEY_FINGERPRINT:6:
    then echo "$PGP_KEY_FINGERPRINT:6:" | gpg --import-ownertrust
    fi

    if gpg --verify "$TMP_LOCATION"/gitea.asc "$TMP_LOCATION"/gitea
    then rm "$TMP_LOCATION"/gitea.asc; return 0
    else echo "gpg verification results in a BAD signature"; exit 1
    fi
  }

  # version_lower_than A B
  # returns whether A < B
  function is_version_lower_than
  {
    test "$(echo "$@" |                 # get all version arguments
      tr " " "\n" |                     # replace `space` with `new line`
      sed '/alpha/d; /beta/d; /rc/d' |  # remove pre-release versions (version-sort interprets suffixes as patch versions)
      sort --version-sort --reverse |   # latest version will be sorted to line 1
      head --lines=1)" != "$1"          # filter line 1 and compare it to A
  }

  function fix_stop_signal
  {
    if (grep --quiet HUP "$HOME"/etc/services.d/gitea.ini)
    then
      sed --in-place '/HUP/d' "$HOME"/etc/services.d/gitea.ini
      supervisorctl reread
      supervisorctl update
    fi
  }

  function is_update_available
  {
    set_local_version
    set_latest_version
    if is_version_lower_than "$LOCAL_VERSION" "$LATEST_VERSION"
    then return 0
    else return 1
    fi
  }

  function main
  {
    fix_stop_signal

    if is_update_available
    then
      echo "There is a new version available."
      echo "Doing update from $LOCAL_VERSION to $LATEST_VERSION"
      do_update_procedure
    else
      echo "Your $APP_NAME is already up to date."
      echo "You are running $APP_NAME $LOCAL_VERSION"
    fi
  }

  main "$@"
  exit $?

Now make the script executable.

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/bin/gitea-update
  [isabell@stardust ~]$

Run the updater

.. code-block:: console

  [isabell@stardust ~]$ gitea-update
  There is a new version available.
  Doing update from 1.19.1 to 1.19.2
  ###################################################################################### 100.0%
  pub   4096R/EC1592E2 2018-06-24 [expires: 2024-06-21]
        Key fingerprint = 7C9E 6815 2594 6888 62D6  2AF6 2D9A E806 EC15 92E2
  uid                  Teabot <teabot@gitea.io>
  sub   4096R/CBADB9A0 2018-06-24 [expires: 2024-06-21]
  sub   4096R/9753F4B0 2018-06-24 [expires: 2024-06-21]

  gpg: Signature made Wed 07 Sep 2022 00:26:25 CEST using RSA key ID 9753F4B0
  gpg: Good signature from "Teabot <teabot@gitea.io>"
  Flushed
  gitea: stopped
  ‘/home/isabell/tmp/gitea’ -> ‘/home/isabell/gitea/gitea’
  mode of ‘/home/isabell/gitea/gitea’ changed from 0664 (rw-rw-r--) to 0764 (rwxrw-r--)
  Gitea service takes 30 seconds to start
  gitea: started
  gitea                            RUNNING   pid 26730, uptime 0:00:30
  [isabell@stardust ~]$

Additional configuration
========================

Gitea ssh setup (optional)
--------------------------

Gitea can manage the ssh keys. To use this feature we have to link the ssh folder into the gitea folder.

.. code-block:: console

  [isabell@stardust ~]$ ln -s ~/.ssh ~/gitea/.ssh
  [isabell@stardust ~]$

Now our Gitea users can add their ssh keys via the menu in the up right corner: ``->`` settings ``->`` tab: SSH/GPG Keys ``->`` Add Key. Gitea is automatically writing a ssh key command into the ``/home/isabell/.ssh/authorized_keys`` file. The key line is something similar like:

.. code-block:: bash

  command="/home/isabell/gitea/gitea --config='/home/isabell/gitea/custom/conf/app.ini' serv key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAAC... youruser@yourhost

If we're using the same ssh key for auth to uberspace and Gitea, we need to modify the server ``/home/isabell/.ssh/authorized_keys`` file.

.. code-block:: bash

  command="if [ -t 0 ]; then bash; elif [[ ${SSH_ORIGINAL_COMMAND} =~ ^(scp|rsync|mysqldump).* ]]; then eval ${SSH_ORIGINAL_COMMAND}; else /home/isabell/gitea/gitea serv key-1 --config='/home/isabell/gitea/custom/conf/app.ini'; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-...

.. warning::
  * Be careful to keep the key number ``key-X``, keep your key ``ssh-...`` and change the username ``isabell`` to yours.
  * Take care that there is no second line propagating the same ssh key.

.. note:: You can still use the Uberspace dashboard_ to add other ssh keys for running default ssh sessions.

To interact with Gitea at our local machine like ``git clone isabell@isabell.uber.space:giteauser/somerepo.git`` we configure the ``/home/localuser/.ssh/config`` file for our local machine with the git ssh key.

.. code-block::

  Host isabell.uber.space
      HostName isabell.uber.space
      User isabell
      IdentityFile ~/.ssh/id_your_git_key
      IdentitiesOnly yes

Gitea using external renderer (optional)
----------------------------------------

| Gitea supports custom file renderings (i.e. Jupyter notebooks, asciidoc, etc.) through external binaries to provide a preview.
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

Now we have to append the config file ``~/gitea/custom/conf/app.ini`` with:

.. code-block:: ini

  [markup.asciidoc]
  ENABLED = true
  FILE_EXTENSIONS = .adoc,.asciidoc
  RENDER_COMMAND = "asciidoctor -e -a leveloffset=-1 --out-file=- -"
  IS_INPUT_FILE = false

..
  ##### Link section #####

.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
.. _releases: https://github.com/go-gitea/gitea/releases/latest
.. _licence: https://github.com/go-gitea/gitea/blob/master/LICENSE
.. _dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gitea 1.20.2, Uberspace 7.15.1

.. author_list::
