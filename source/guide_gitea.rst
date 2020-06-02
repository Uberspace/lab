.. author:: Frank ℤisko <https://frank.zisko.io>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: version-control

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitea.png 
      :align: center


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

We need a database:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_gitea"
  [isabell@stardust ~]$

We can use the uberspace or your own domain:

.. include:: includes/web-domain-list.rst


Installation
============

Download and verify
-------------------

Check current version of Gitea at releases_ page.

.. code-block:: console

  [isabell@stardust ~]$ VERSION=1.11.5
  [isabell@stardust ~]$ mkdir -p ~/gitea
  [isabell@stardust ~]$ wget -O ~/gitea/gitea https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64
  --2020-06-01 21:00:31--  https://github.com/go-gitea/gitea/releases/download/v1.11.5/gitea-1.11.5-linux-amd64
  Resolving github.com (github.com)... 140.82.118.3
  Connecting to github.com (github.com)|140.82.118.3|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: [...]
  HTTP request sent, awaiting response... 200 OK
  Length: 83243800 (79M) [application/octet-stream]
  Saving to: ‘/home/test0r/gitea/gitea’
  
  100%[====================================================================================================================>] 83,243,800  14.9MB/s   in 9.8s   
  
  2020-06-01 21:00:42 (8.11 MB/s) - ‘/home/test0r/gitea/gitea’ saved [83243800/83243800]
  [isabell@stardust ~]$ wget -O ~/gitea/gitea.asc https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64.asc
  Resolving github.com (github.com)... 140.82.118.4
  Connecting to github.com (github.com)|140.82.118.4|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: [...]
  HTTP request sent, awaiting response... 200 OK
  Length: 833 [application/octet-stream]
  Saving to: ‘/home/test0r/gitea/gitea.asc’
  
  100%[====================================================================================================================>] 833         --.-K/s   in 0s      
  
  2020-06-01 21:03:17 (9.01 MB/s) - ‘/home/test0r/gitea/gitea.asc’ saved [833/833]
  [isabell@stardust ~]$ 
 
We use ``gpg`` to download the pgp key and verify our download.

.. code-block:: console

  [isabell@stardust ~]$ gpg --keyserver keys.gnupg.net --recv-keys 7C9E68152594688862D62AF62D9AE806EC1592E2
  gpg: directory `/home/isabell/.gnupg' created
  gpg: new configuration file `/home/isabell/.gnupg/gpg.conf' created
  gpg: WARNING: options in `/home/isabell/.gnupg/gpg.conf' are not yet active during this run
  gpg: keyring `/home/isabell/.gnupg/secring.gpg' created
  gpg: keyring `/home/isabell/.gnupg/pubring.gpg' created
  gpg: requesting key EC1592E2 from hkp server keys.gnupg.net
  gpg: /home/isabell/.gnupg/trustdb.gpg: trustdb created
  gpg: key EC1592E2: public key "Teabot <teabot@gitea.io>" imported
  gpg: no ultimately trusted keys found
  gpg: Total number processed: 1
  gpg:               imported: 1  (RSA: 1)
  [isabell@stardust ~]$ gpg --verify ~/gitea/gitea.asc ~/gitea/gitea
  gpg: Signature made Sat 09 May 2020 10:19:06 PM CEST using RSA key ID 9753F4B0
  gpg: Good signature from "Teabot <teabot@gitea.io>"
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 7C9E 6815 2594 6888 62D6  2AF6 2D9A E806 EC15 92E2
       Subkey fingerprint: CC64 B1DB 67AB BEEC AB24  B645 5FC3 4632 9753 F4B0
  [isabell@stardust ~]$ 

If the verification is fine, we get a ``gpg: Good signature from "Teabot <teabot@gitea.io>"`` line and we make the bin executeable.
  
.. code-block:: console

  [isabell@stardust ~]$ chmod u+x ~/gitea/gitea
  [isabell@stardust ~]$


Configuration
=============

Gitea configuration file
-------------------------

Before we write the configuration we need the MySQL database password and some random characters as security key. We catch the MySQL/MariaDB password ...

.. code-block:: console

  [isabell@stardust ~]$ my_print_defaults --defaults-file=~/.my.cnf client | grep -- --password | awk --field-separator = '{ print $2 }'
  xG9MD-15A4aMGsln,MTr
  [isabell@stardust ~]$ 

... and some random alpha-num chars for the security key. For this we pipe some random characters from the ``/dev/urandom`` device into the translate tool ``tr`` to delete the complementary of alpha-numeric characters until we have 32 characters.

.. code-block:: console

  [isabell@stardust ~]$ cat /dev/urandom | tr --delete --complement 'a-zA-Z0-9' | fold --width=32 | head --lines=1
  SomeRandomCharactersyHxLQeGr976f
  [isabell@stardust ~]$ 

Create a custom directory.

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p ~/gitea/custom/conf/
  [isabell@stardust ~]$ 

The minimum set of ``~/gitea/custom/conf/app.ini`` is:

.. code-block:: ini

  [server]
  HTTP_PORT = 9000
  DOMAIN = isabell.uber.space
  ROOT_URL = https://%(DOMAIN)s

  [service]
  DISABLE_REGISTRATION = true

When using this, we have to finish the installation via gitea web service https://isabell.uber.space/install. This is exposed without any password request. We improve the configiguration with some modifications, e.g.:

* Filling the database access data that we would otherwise enter in the web installation step. (``[database]`` section)
* As security feature we lock the web installation and change the default password complexity to allow well to remember and secure passwords. (See `XKCD No. 936 <https://xkcd.com/936/>`_  and `Explained XKCD No. 936 <https://explainxkcd.com/wiki/index.php/936:_Password_Strength>`_ for the math behind it. 😉 ``[security]`` section)
* We disallow public registration and set some privacy settings. (``[service]`` section)
* Naming the repositories path.
* Set the eye-friendly dark theme as default theme, set mailing, set time and set logging options.

For more informations about the possibilities and configuration options see the Gitea documentation_ and the Gitea `configuration sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample>`_.

.. note:: The minimum improvements are written in the sections of ``[database]``, ``[security]`` and ``[service]``.

.. warning:: Replace ``isabell`` with your username, fill the database password ``PASSWD =`` with yours and enter the generated random into ``SECRET_KEY =``.

.. code-block:: ini

  APP_NAME = Gitea
  RUN_USER = isabell
  RUN_MODE = prod ; Either "dev", "prod" or "test", default is "dev".
  
  [server]
  HTTP_PORT            = 9000
  DOMAIN               = isabell.uber.space
  ROOT_URL             = https://%(DOMAIN)s
  STATIC_URL_PREFIX    = 
  OFFLINE_MODE         = true
  DISABLE_SSH          = false
  SSH_DOMAIN           = isabell.uber.space
  SSH_PORT             = 22
  LANDING_PAGE         = explore ; [home, explore, organizations, login]
  LFS_START_SERVER     = true
  LFS_CONTENT_PATH     = /home/isabell/gitea/data/lfs
  LFS_JWT_SECRET       = 
  LFS_HTTP_AUTH_EXPIRY = 24m
  
  [database]
  DB_TYPE           = mysql
  HOST              = 127.0.0.1:3306
  NAME              = isabell_gitea
  USER              = isabell
  PASSWD            = <MySQL_PASSWORD>
  SSL_MODE          = disable
  
  [security]
  INSTALL_LOCK          = true
  MIN_PASSWORD_LENGTH   = 8
  PASSWORD_COMPLEXITY   = lower,digit
  PASSWORD_HASH_ALGO    = pbkdf2 ; [pbkdf2, argon2, scrypt, bcrypt]
  LOGIN_REMEMBER_DAYS   = 5
  CSRF_COOKIE_HTTP_ONLY = true
  INTERNAL_TOKEN        = 
  SECRET_KEY            = <RANDOM_32_CHARS>
  
  [service]
  DISABLE_REGISTRATION                   = true
  SHOW_REGISTRATION_BUTTON               = false
  REQUIRE_EXTERNAL_REGISTRATION_PASSWORD = false
  ALLOW_ONLY_EXTERNAL_REGISTRATION       = false
  REQUIRE_SIGNIN_VIEW                    = true
  ENABLE_CAPTCHA                         = false
  REGISTER_EMAIL_CONFIRM                 = true
  ACTIVE_CODE_LIVE_MINUTES               = 60
  RESET_PASSWD_CODE_LIVE_MINUTES         = 60
  ENABLE_NOTIFY_MAIL                     = false
  SHOW_MILESTONES_DASHBOARD_PAGE         = true
  DEFAULT_ALLOW_CREATE_ORGANIZATION      = true
  DEFAULT_ORG_VISIBILITY                 = private ; [public, limited, private]
  DEFAULT_ORG_MEMBER_VISIBLE             = false
  DEFAULT_ENABLE_TIMETRACKING            = true
  DEFAULT_KEEP_EMAIL_PRIVATE             = true
  NO_REPLY_ADDRESS                       = noreply.isabell.uber.space
  
  [repository]
  ROOT = /home/isabell/gitea/repositories
  DEFAULT_PRIVATE = private ; [last, private, public]

  [ui]
  THEMES        = gitea,arc-green
  DEFAULT_THEME = arc-green

  [mailer]
  ENABLED     = true
  MAILER_TYPE = sendmail
  FROM        = isabell@uber.space
  
  [time]
  FORMAT              = 2006-01-02 15:04:05
  DEFAULT_UI_LOCATION = Europe/Amsterdam
  
  [log]
  MODE      = file
  LEVEL     = info ; [Trace, Debug, Info, Warn, Error, Critical, Fatal, None]
  ROOT_PATH = /home/isabell/gitea/log
  
  [log.file]
  LOG_ROTATE   = true
  DAILY_ROTATE = true
  MAX_DAYS     = 14
  COMPRESS     = false

Gitea using external renderer (optional)
----------------------------------------

We can install an extra `external rendering <https://docs.gitea.io/en-us/external-renderers/>`_ extension AsciiDoc.

.. code-block:: console
  
  [isabell@stardust ~]$ gem install asciidoctor
  Fetching asciidoctor-2.0.10.gem
  WARNING:  You don't have /home/test0r/.gem/ruby/2.7.0/bin in your PATH,
  	  gem executables will not run.
  Successfully installed asciidoctor-2.0.10
  1 gem installed
  [isabell@stardust ~]$

.. note:: Don't be irritated by the warning that the bin folder isn't in the path. Uberspace is taking care of it and provide it via ``/opt/uberspace/etc/isabell/binpaths/ruby/asciidoctor``. You can check with ``[isabell@stardust ~]$ which asciidoctor``.

Now we have to append the config file ``~/gitea/custom/conf/app.ini`` with:

.. code-block:: ini

  [markup.asciidoc]
  ENABLED = true
  FILE_EXTENSIONS = .adoc,.asciidoc
  RENDER_COMMAND = "asciidoctor -e -a leveloffset=-1 --out-file=- -"
  IS_INPUT_FILE = false

Gitea initalization
-------------------

Above we locked the registration and the web installation feature, so this service will never be exposed in an unsecure way to the internet. So we have to do the provided steps to create the database layout and generate security keys manually.

.. code-block:: console
  
  [isabell@stardust ~]$ ~/gitea/gitea migrate
  ... a lot of console output about the database commands.
  [isabell@stardust ~]$ ~/gitea/gitea generate secret INTERNAL_TOKEN 
  Some-Random-Characters-eyJhbUNIn6CJ9.eyJuYmYiOjE1OTEwNDAyNTB9.xYynv0JXwO-aqE5XEkGZE8mEeiQEOl-rU0JXpdPbLck
  [isabell@stardust ~]$ ~/gitea/gitea generate secret SECRET_KEY 
  Some-Random-Characters-omddgYYpZTiMbrtBtgHU1f8ASXvS9Tlx6ETYiCwbJ
  [isabell@stardust ~]$ ~/gitea/gitea generate secret JWT_SECRET 
  Some-Random-Characters-qRsvc0BtKZRmNvbo22a8
  [isabell@stardust ~]$ ~/gitea/gitea generate secret LFS_JWT_SECRET 
  Some-Random-Characters-Lj7hGewx62tFGHZwRsVc
  [isabell@stardust ~]$ 

Gitea admin user
----------------

We generate a safe password for the admin user. For this we use ``head`` to pipe some random characters from the ``/dev/urandom`` device into the translate tool ``tr`` to delete the complementary of alpha-numeric characters until we have 16 characters and then write into a variable to use it in the next two steps.

.. code-block:: console

  [isabell@stardust ~]$ ADMPWD=$(head /dev/urandom | tr --complement --delete A-Za-z0-9 | head --bytes=16 ; echo '')

Now we create an admin user via Gitea `command line <https://docs.gitea.io/en-us/command-line/#admin>`_. Gitea isn't allowing ``admin`` as name. We choose ``adminuser`` and the generated password from above. To ensure we remember the password beyond this installation session we store the password in a text file.

.. code-block:: console
  
  [isabell@stardust ~]$ ~/gitea/gitea admin create-user --username adminuser --password ${ADMPWD} --email ${USER}@uber.space --admin
  ...
  New user 'adminuser' has been successfully created!
  [isabell@stardust ~]$ echo "usr: adminuser" > ~/gitea/gitea-admin.txt
  [isabell@stardust ~]$ echo "pwd: ${ADMPWD}" >> ~/gitea/gitea-admin.txt
  [isabell@stardust ~]$ 

Gitea ssh setup (optional)
--------------------------

Gitea can manage the ssh keys. To use this feature we have to link the ssh folder into the gitea folder.

.. code-block:: console
  
  [isabell@stardust ~]$ ln -s ~/.ssh ~/gitea/.ssh
  [isabell@stardust ~]$ 

Now our Gitea users can add their ssh keys via the menu in the up right corner: ``->`` settings ``->`` tab: SSH/GPG Keys ``->`` Add Key. Gitea is automatically writing a ssh key command into the ``/home/isabell/.ssh/authorized_keys`` file. The key line is something similar like:

.. code-block:: config

  command="/home/isabell/gitea/gitea --config='/home/isabell/gitea/custom/conf/app.ini' serv key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAAC... youruser@yourhost

If we're using the same ssh key for auth to uberspace and Gitea, we need to modify the server ``/home/isabell/.ssh/authorized_keys`` file.

.. code-block:: config

  command="if [ -t 0 ]; then bash; elif [[ ${SSH_ORIGINAL_COMMAND} =~ ^(scp|rsync|mysqldump).* ]]; then eval ${SSH_ORIGINAL_COMMAND}; else /home/isabell/gitea/gitea serv key-1 --config='/home/isabell/gitea/custom/conf/app.ini'; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-...

.. note:: Be careful to keep the key number ``key-X``, keep your key ``ssh-...`` and change the username isabell to yours.

.. note:: You can still use the Uberspace dashboard_ to add ssh keys.

To interact with Gitea at our local machine like ``git clone isabell@isabell.uber.space:giteauser/somerepo.git`` we configure the ``/home/localuser/.ssh/config`` file for our local machine with the git ssh key.

.. code-block:: config

  Host isabelle.uber.space
      HostName isabelle.uber.space
      User isabelle
      IdentityFile ~/.ssh/id_your_git_key
      IdentitiesOnly yes


Finishing installation
======================

Uberspace daemon for Gitea
---------------------------

Create a file ``~/etc/services.d/gitea.ini`` for the service ...

.. code-block:: ini

  [program:gitea]
  command=%(ENV_HOME)s/gitea/gitea web

.. include:: includes/supervisord.rst

.. note:: The status of gitea must be ``RUNNING``. If not, check the configuration file ``~/gitea/custom/conf/app.ini``.

Uberspace web backend
---------------------

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set / --http --port 9000
  Set backend for / to port 9000; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$ uberspace web backend list
  [isabell@stardust ~]$ 

.. note:: If we run the service under a domain subfolder aka prefix, you need to append the above command like ``uberspace web backend set exampe.net/subfolder --http --port 9000 --remove-prefix``.


Done. We can point our browser to https://isabell.uber.space/.

Installed files and folders are:

* ``~/gitea``
* ``~/etc/services.d/gitea.ini``
* ``~/.gem/ruby/2.7.0/*/asciidoctor*``, if AsciiDoctor is installed.


Updates
=======

.. note:: Check the update feed_ or releases_ page regularly to stay informed about the newest version.

To update do:

* Stop the application ``supervisorctl stop gitea``
* Do the *download and verify* part from above.
* Check if you have to modify the config file. (See documentation_ and the `file sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample>`_.)
* Do the application migration: ``~/gitea/gitea migrate``
* Start the application ``supervisorctl start gitea``
* Check if the application is running ``supervisorctl status gitea``


.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
.. _releases: https://github.com/go-gitea/gitea/releases/latest
.. _licence: https://github.com/go-gitea/gitea/blob/master/LICENSE
.. _dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gitea 1.11.5, Uberspace 7.6.2.0

.. author_list::
