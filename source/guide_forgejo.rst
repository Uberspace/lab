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

We can use the uberspace or your own domain:

.. include:: includes/web-domain-list.rst


Installation
============


Download
--------

Check current version of Forgejo at releases_ page:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/forgejo
  [isabell@stardust ~]$ wget -O ~/forgejo/forgejo https://codeberg.org/attachments/a26d3acd-5c2e-4132-a283-8110da2872d4
  [...]
  Saving to: ‘/home/isabell/forgejo/forgejo’

  100%[=======================================================>] 117,891,760 81.0MB/s   in 1.4s

  2023-01-15 20:04:54 (81.0 MB/s) - ‘/home/isabell/forgejo/forgejo’ saved [117891760/117891760]
  [isabell@stardust ~]$


Verifying (optional)
--------------------

Optionally you can verify the downloaded file using ``gpg``. To do so, download the pgp signature file and trust key
and verify the binary:

.. code-block:: console
  :emphasize-lines: 7

  [isabell@stardust ~]$ wget -O ~/forgejo/forgejo.asc https://codeberg.org/attachments/e42286dd-d158-48c7-b400-a0d1d301be58
  […]
  [isabell@stardust ~]$ curl --silent https://openpgpkey.forgejo.org/.well-known/openpgpkey/forgejo.org/hu/dj3498u4hyyarh35rkjfnghbjxug6b19 | gpg --import
  gpg: key C5923710: no valid user IDs
  gpg: this may be caused by a missing self-signature
  gpg: Total number processed: 1
  gpg:           w/o user IDs: 1
  [isabell@stardust ~]$ gpg --verify ~/forgejo/forgejo.asc ~/forgejo/forgejo
  gpg: Signature made Fri 30 Dec 2022 00:54:23 CET using ? key ID 50D53707
  gpg: Can't check signature: Invalid public key algorithm

If the verification is fine, we get a ``gpg: Good signature from "Teabot <teabot@gitea.io>"`` line. You need to ignore the ``WARNING`` here.


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
  2023/01/15 20:12:16 models/db/engine.go:126:SyncAllTables() [I] [SQL] CREATE INDEX `IDX_package_version_package_id` ON `package_version` (`package_id`) [] - 31.649452ms
  2023/01/15 20:12:16 models/db/engine.go:126:SyncAllTables() [I] [SQL] CREATE INDEX `IDX_package_version_lower_version` ON `package_version` (`lower_version`) [] - 30.93972ms
  [isabell@stardust ~]$

Forgejo admin user
------------------

Set your admin login credentials:

.. code-block:: console

  [isabell@stardust ~]$ ADMIN_USERNAME=AdminUsername
  [isabell@stardust ~]$ ADMIN_PASSWORD='SuperSecretAdminPassword'
  [isabell@stardust ~]$ ~/forgejo/forgejo admin user create --username ${ADMIN_USERNAME} --password ${ADMIN_PASSWORD} --email ${USER}@uber.space --admin
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

* ``~/forgejo``
* ``~/etc/services.d/forgejo.ini``

Backup
======

The Forgejo CLI (command line interface) has a build-in backup command to create a full backup in a zip file with the database, repos, config, log, data

.. note:: To restore a backup follow the `backup and restore documentation <https://docs.gitea.io/en-us/backup-and-restore/#restore-command-restore>`_

Execute the following command:

::

  [isabell@stardust ~]$ ~/forgejo/forgejo dump
  2023/01/15 22:52:27 ...dules/setting/log.go:288:newLogService() [I] Gitea v1.18.0-1 built with GNU Make 4.1, go1.19.4 : bindata, sqlite, sqlite_unlock_notify
  2023/01/15 22:52:27 ...dules/setting/log.go:335:newLogService() [I] Gitea Log Mode: Console(Console:info)
  2023/01/15 22:52:27 ...dules/setting/log.go:249:generateNamedLogger() [I] Router Log: Console(console:info)
  2023/01/15 22:52:27 ...les/setting/cache.go:76:newCacheService() [I] Cache Service Enabled
  2023/01/15 22:52:27 ...les/setting/cache.go:91:newCacheService() [I] Last Commit Cache Service Enabled
  2023/01/15 22:52:27 ...s/setting/session.go:73:newSessionService() [I] Session Service Enabled
  2023/01/15 22:52:27 ...s/setting/setting.go:613:deprecatedSetting() [E] Deprecated fallback `[mailer]` `MAILER_TYPE` present. Use `[mailer]` `PROTOCOL` instead. This fallback will be removed in v1.19.0
  2023/01/15 22:52:27 ...es/setting/mailer.go:263:tryResolveAddr() [W] could not look up mailer.SMTP_ADDR: lookup : no such host
  2023/01/15 22:52:27 ...es/setting/mailer.go:226:newMailService() [I] Mail Service Enabled
  2023/01/15 22:52:27 ...es/setting/mailer.go:237:newRegisterMailService() [I] Register Mail Service Enabled
  2023/01/15 22:52:27 ...s/storage/storage.go:176:initAttachments() [I] Initialising Attachment storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/attachments
  2023/01/15 22:52:27 ...s/storage/storage.go:170:initAvatars() [I] Initialising Avatar storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/avatars
  2023/01/15 22:52:27 ...s/storage/storage.go:188:initRepoAvatars() [I] Initialising Repository Avatar storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/repo-avatars
  2023/01/15 22:52:27 ...s/storage/storage.go:182:initLFS() [I] Initialising LFS storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/lfs
  2023/01/15 22:52:27 ...s/storage/storage.go:194:initRepoArchives() [I] Initialising Repository Archive storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/repo-archive
  2023/01/15 22:52:27 ...s/storage/storage.go:200:initPackages() [I] Initialising Packages storage with type:
  2023/01/15 22:52:27 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/packages
  Failed to include repositories: open /home/isabell/forgejo/data/forgejo-repositories: no such file or directory
  2023/01/15 22:52:27 cmd/dump.go:245:runDump() [I] Dumping local repositories... /home/isabell/forgejo/data/forgejo-repositories
  2023/01/15 22:52:27 cmd/dump.go:163:fatal() [F] Failed to include repositories: open /home/isabell/forgejo/data/forgejo-repositories: no such file or directory
  [...]
  2022/03/08 17:26:01 ...s/storage/storage.go:171:initAttachments() [I] Initialising Attachment storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/attachments
  2022/03/08 17:26:01 ...s/storage/storage.go:165:initAvatars() [I] Initialising Avatar storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/avatars
  2022/03/08 17:26:01 ...s/storage/storage.go:183:initRepoAvatars() [I] Initialising Repository Avatar storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/repo-avatars
  2022/03/08 17:26:01 ...s/storage/storage.go:177:initLFS() [I] Initialising LFS storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/lfs
  2022/03/08 17:26:01 ...s/storage/storage.go:189:initRepoArchives() [I] Initialising Repository Archive storage with type:
  2022/03/08 17:26:01 ...les/storage/local.go:46:NewLocalStorage() [I] Creating new Local Storage at /home/isabell/forgejo/data/repo-archive
  2022/03/08 17:26:01 cmd/dump.go:270:runDump() [I] Dumping database...
  [...]
  2022/03/08 17:26:01 cmd/dump.go:282:runDump() [I] Adding custom configuration file from /home/isabell/forgejo/custom/conf/app.ini
  2022/03/08 17:26:01 cmd/dump.go:310:runDump() [I] Packing data directory.../home/isabell/forgejo/data
  2022/03/08 17:26:01 cmd/dump.go:379:runDump() [I] Finish dumping in file forgejo-dump-1646756761.zip
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


Automated updating by custom script
-----------------------------------

You can also automate the update by using a custom script that automatically executes all the update steps. Create ``~/bin/forgejo-update`` with the following content:

.. code-block:: bash

  #!/usr/bin/env bash

  APP_NAME=Forgejo
  FORGEJO_LOCATION=$HOME/forgejo/forgejo
  TMP_LOCATION=$HOME/tmp
  GPG_KEY_FINGERPRINT=7C9E68152594688862D62AF62D9AE806EC1592E2

  ORG=forgejo # Organisation or GitHub user
  REPO=forgejo
  GITHUB_API_URL=https://codeberg.org/$ORG/$REPO/releases/latest

  function do_update_procedure
  {
    $FORGEJO_LOCATION manager flush-queues
    forgejo_pid=$(supervisorctl pid forgejo)
    echo "Process-ID is $forgejo_pid"
    supervisorctl stop forgejo
    if [[ $forgejo_pid -gt 0 ]] && (ps --pid "$forgejo_pid" > /dev/null)
    then echo "still running! - killing it..."; kill "$forgejo_pid"
    fi
    if (lsof -nP -iTCP:3000 -sTCP:LISTEN)
    then echo "port 3000 is still in use, abbort"; exit 1
    fi
    wget --quiet --progress=bar:force --output-document "$TMP_LOCATION"/forgejo "$DOWNLOAD_URL"
    verify_file
    mv --verbose "$TMP_LOCATION"/forgejo "$FORGEJO_LOCATION"
    chmod u+x --verbose "$FORGEJO_LOCATION"
    supervisorctl start forgejo
    supervisorctl status forgejo
  }

  function get_local_version
  {
    LOCAL_VERSION=$($FORGEJO_LOCATION --version |
      awk '{print $3}')
  }

  function get_latest_version
  {
    curl --silent $GITHUB_API_URL > "$TMP_LOCATION"/github_api_response.json
    TAG_NAME=$(jq --raw-output '.tag_name' "$TMP_LOCATION"/github_api_response.json)
    LATEST_VERSION=${TAG_NAME:1}
    DOWNLOAD_URL=$(jq --raw-output '.assets[].browser_download_url' "$TMP_LOCATION"/github_api_response.json |
      grep --max-count=1 "linux-amd64")
  }

  function get_signature_file
  {
    SIGNATURE_FILE_URL=$(jq --raw-output '.assets[].browser_download_url' "$TMP_LOCATION"/github_api_response.json |
      grep "linux-amd64.asc")
    rm "$TMP_LOCATION"/github_api_response.json
    wget --quiet --progress=bar:force --output-document "$TMP_LOCATION"/forgejo.asc "$SIGNATURE_FILE_URL"
  }

  function verify_file
  {
    get_signature_file

    ## downloading public key if it does not already exist
    if ! gpg --fingerprint $GPG_KEY_FINGERPRINT
    then
      ## currently the key download via gpg does not work on Uberspace
      #gpg --keyserver keys.openpgp.org --recv $GPG_KEY_FINGERPRINT
      curl --silent https://keys.openpgp.org/vks/v1/by-fingerprint/$GPG_KEY_FINGERPRINT | gpg --import
    fi

    if ! gpg --export-ownertrust | grep --quiet $GPG_KEY_FINGERPRINT:6:
    then echo "$GPG_KEY_FINGERPRINT:6:" | gpg --import-ownertrust
    fi

    if gpg --verify "$TMP_LOCATION"/forgejo.asc "$TMP_LOCATION"/forgejo
    then rm "$TMP_LOCATION"/forgejo.asc; return 0
    else echo "gpg verification results in a BAD signature"; exit 1
    fi
  }

  ## version_lower_than A B returns whether A < B
  function version_lower_than
  {
    test "$(echo "$@" |
      tr " " "n" |
      sort --version-sort --reverse |
      head --lines=1)" != "$1"
  }

  function fix_stop_signal
  {
    if (grep --quiet HUP "$HOME"/etc/services.d/forgejo.ini)
    then
      sed --in-place '/HUP/d' "$HOME"/etc/services.d/forgejo.ini
      supervisorctl reread
      supervisorctl update
    fi
  }

  function main
  {
    fix_stop_signal
    get_local_version
    get_latest_version

    if [ "$LOCAL_VERSION" = "$LATEST_VERSION" ]
    then
      echo "Your $APP_NAME is already up to date."
      echo "You are running $APP_NAME $LOCAL_VERSION"
    else
      if version_lower_than "$LOCAL_VERSION" "$LATEST_VERSION"
      then
        echo "There is a new version available."
        echo "Doing update from $LOCAL_VERSION to $LATEST_VERSION"
        do_update_procedure
      fi
    fi
  }

  main "$@"
  exit $?

Now make the script executable.

.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/bin/forgejo-update
  [isabell@stardust ~]$

Run the updater

.. code-block:: console

  [isabell@stardust ~]$ forgejo-update
  There is a new version available.
  Doing update from 1.16.8 to 1.17.2
  Flushed
  Process-ID is 25538
  forgejo: stopped
  pub   4096R/EC1592E2 2018-06-24 [expires: 2024-06-21]
        Key fingerprint = 7C9E 6815 2594 6888 62D6  2AF6 2D9A E806 EC15 92E2
  uid                  Teabot <teabot@gitea.io>
  sub   4096R/CBADB9A0 2018-06-24 [expires: 2024-06-21]
  sub   4096R/9753F4B0 2018-06-24 [expires: 2024-06-21]

  gpg: Signature made Wed 07 Sep 2022 00:26:25 CEST using RSA key ID 9753F4B0
  gpg: Good signature from "Teabot <teabot@gitea.io>"
  ‘/home/isabell/tmp/forgejo’ -> ‘/home/isabell/forgejo/forgejo’
  mode of ‘/home/isabell/forgejo/forgejo changed from 0664 (rw-rw-r--) to 0764 (rwxrw-r--)
  forgejo: started
  forgejo                            RUNNING   pid 26730, uptime 0:00:30
  [isabell@stardust ~]$

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

Tested with Forgejo 1.18.0-1, Uberspace 7.14.0

.. author_list::
