.. author:: Frank ℤisko, https://frank.zisko.io

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

.. include:: includes/my-print-defaults.rst

We need a database:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_gitea"
  [isabell@stardust ~]$

We can use the uberspace or your own domain:

.. include:: includes/web-domain-list.rst


Installation
============


We set some variables
---------------------

Check current version of Gitea at releases_ page.

Set the variables for ``VERSION``, ``APPDOMAIN`` (if using your own) and ``APPDOMAINSUBF`` (if you're using a subfolder. Root is fine, too).

.. code-block:: sh
  
  [isabell@stardust ~]$ 

  VERSION=1.11.5
  
  DOWNLINK=https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64
  DOWNFILE=gitea-${VERSION}-linux-amd64
  
  CHECKLINK=https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64.asc
  CHECKFILE=gitea-${VERSION}-linux-amd64.asc
  CHECKKEY=7C9E68152594688862D62AF62D9AE806EC1592E2
  
  DOWNFOLDER=/home/${USER}/downloads
  
  APPPATH=/home/${USER}/opt/gitea
  APPPORT=9000
  APPDOMAIN=${USER}.uber.space # Or your own domain. See above in the prerequisites.
  # Empty if not using:
  APPDOMAINSUBF=/gitea 
  APPWEBPAGE=${APPDOMAIN}${APPDOMAINSUBF}
  APPROOTURL=https://${APPDOMAIN}${APPDOMAINSUBF}/


Download, verify and place the files
------------------------------------

.. code-block:: sh
  
  [isabell@stardust ~]$ 
  ### Download ### 
  DOWNFILEPATH=${DOWNFOLDER}/${DOWNFILE}
  CHECKFILEPATH=${DOWNFOLDER}/${CHECKFILE}
  mkdir -p ${DOWNFOLDER}
  wget -O ${DOWNFILEPATH} ${DOWNLINK} -nc # If it's already downloaded, we save traffic.
  wget -O ${CHECKFILEPATH} ${CHECKLINK} # This small file we always download.
  
  ### Verify ### 
  gpg --keyserver keys.gnupg.net --recv-keys ${CHECKKEY}
  gpg --verify ${CHECKFILEPATH} ${DOWNFILEPATH}
  if [ $? -eq 0 ]; then
      echo "Successfully verified gpg signature."
  else
      echo -e "\033[1;31mCRITICAL\033[0m: gpg verification failed."
      echo -e "\033[0;31mAborting.\033[0m"
      exit 1
  fi
  
  ### Place and rights ### 
  mkdir -p ${APPPATH}
  cp ${DOWNFILEPATH} ${APPPATH}/gitea
  chmod u+x ${APPPATH}/gitea


Gitea configuration file
-------------------------

We set the config file with some improvements. 

* We import the username and password of the database automatically. 
* As security feature we disallow registration and lock the web installation. 
* We change the default password complexity. See https://xkcd.com/936/ for well to remember and secure passwords. ;-)

For more informations about the configuration file see:

* Documentation_
* `Configuration sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample>`_

.. code-block:: sh
  
  [isabell@stardust ~]$ 
  mkdir -p ${APPPATH}/custom/conf/
  cat > ${APPPATH}/custom/conf/app.ini <<__EOF__
  ; For more config stuff check: 
  ; https://docs.gitea.io/en-us/config-cheat-sheet/
  ; https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample
  APP_NAME = Gitea
  RUN_USER = ${USER}
  RUN_MODE = prod ; Either "dev", "prod" or "test", default is "dev"
  
  [server]
  ; http needet for internal handling ;-)
  ;PROTOCOL             = http
  HTTP_PORT            = ${APPPORT}
  ; If PROTOCOL is set to unix or fcgi+unix, this should be the name of the Unix socket file to use:
  ;HTTP_ADDR            = 0.0.0.0
  DOMAIN               = ${APPDOMAIN}
  ROOT_URL             = ${APPROOTURL}
  STATIC_URL_PREFIX    = 
  OFFLINE_MODE         = true
  DISABLE_SSH          = false
  SSH_DOMAIN           = ${USER}.uber.space
  SSH_PORT             = 22
  LANDING_PAGE         = explore ; [home, explore, organizations, login]
  LFS_START_SERVER     = true
  LFS_CONTENT_PATH     = ${APPPATH}/data/lfs
  LFS_JWT_SECRET       = 
  LFS_HTTP_AUTH_EXPIRY = 24m
  
  [database]
  ; [mysql, postgres, mssql, sqlite3]
  DB_TYPE           = mysql
  ; HOST = /var/run/mysqld/mysqld.sock
  HOST              = 127.0.0.1:3306
  NAME              = ${USER}_gitea
  USER              = ${USER}
  PASSWD            = `my_print_defaults --defaults-file=/home/${USER}/.my.cnf client | grep -- --password | awk -F = '{ print $2 }'`
  SSL_MODE          = disable
  CHARSET           = utf8
  ; For SQLite3 only, the database file path:
  PATH              = ${APPPATH}/data/gitea.db
  ;LOG_SQL           = true
  ;DB_RETRIES        = 12
  ;DB_RETRY_BACKOFF  = 3s
  ;MAX_OPEN_CONNS    = 0
  ;MAX_IDLE_CONNS    = 2
  ;CONN_MAX_LIFETIME = 3s
  
  [security]
  ; Set false to finish installation via web ${APPROOTURL}install.
  INSTALL_LOCK          = true
  MIN_PASSWORD_LENGTH   = 8
  ; Comma separated list of classes. (lower,upper,digit,spec | off)
  ; spec include chars as !";$%&'()*+,-./\:;|<=>?@{}[]~^'``
  PASSWORD_COMPLEXITY   = lower,digit
  PASSWORD_HASH_ALGO    = pbkdf2 ; [pbkdf2, argon2, scrypt, bcrypt]
  LOGIN_REMEMBER_DAYS   = 5
  ; Set to true to prevent all users (including admin) from creating custom git hooks
  DISABLE_GIT_HOOKS     = false
  ONLY_ALLOW_PUSH_IF_GITEA_ENVIRONMENT_SET = true
  ; Set false to allow JavaScript to read CSRF cookie.
  CSRF_COOKIE_HTTP_ONLY = true
  INTERNAL_TOKEN        = 
  SECRET_KEY            = `head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32 ; echo ''`
  
  [ssh.minimum_key_sizes]
  ED25519 = 256
  ECDSA = 256
  RSA = 2048
  DSA = 1024 ; -1 disables.
  
  [openid]
  ENABLE_OPENID_SIGNIN = true
  ENABLE_OPENID_SIGNUP = false
  
  [oauth2]
  JWT_SECRET = 
  
  [U2F]
  ; NOTE: THE DEFAULT VALUES HERE WILL NEED TO BE CHANGED
  ; Two Factor authentication with security keys
  ; https://developers.yubico.com/U2F/App_ID.html
  ;APP_ID = http://localhost:3000/
  ; Comma seperated list of trusted facets
  ;TRUSTED_FACETS = http://localhost:3000/
  
  [admin]
  DISABLE_REGULAR_ORG_CREATION = false
  DEFAULT_EMAIL_NOTIFICATIONS = onmention ; [enabled, onmention, disabled]
  
  [service]
  ; Registration.
  DISABLE_REGISTRATION                   = true
  SHOW_REGISTRATION_BUTTON               = false
  REQUIRE_EXTERNAL_REGISTRATION_PASSWORD = false
  ALLOW_ONLY_EXTERNAL_REGISTRATION       = false
  REQUIRE_SIGNIN_VIEW                    = true
  ENABLE_CAPTCHA                         = false
  REGISTER_EMAIL_CONFIRM                 = true
  ACTIVE_CODE_LIVE_MINUTES               = 60
  RESET_PASSWD_CODE_LIVE_MINUTES         = 60
  ; User defaults.
  ENABLE_NOTIFY_MAIL                     = false
  ENABLE_USER_HEATMAP                    = true
  SHOW_MILESTONES_DASHBOARD_PAGE         = true
  DEFAULT_ALLOW_CREATE_ORGANIZATION      = true
  DEFAULT_ORG_VISIBILITY                 = private ; [public,limited,private]
  DEFAULT_ORG_MEMBER_VISIBLE             = false
  DEFAULT_ENABLE_TIMETRACKING            = true
  DEFAULT_KEEP_EMAIL_PRIVATE             = true
  NO_REPLY_ADDRESS                       = noreply.${USER}.uber.space
  AUTO_WATCH_NEW_REPOS                   = true
  AUTO_WATCH_ON_CHANGES                  = false
  
  [picture]
  DISABLE_GRAVATAR        = true
  ENABLE_FEDERATED_AVATAR = false
  
  [repository]
  ROOT = ${APPPATH}/repositories
  DEFAULT_PRIVATE = private ; [last, private, public]
  DISABLE_HTTP_GIT = false ; Disable the ability to interact with repositories using the HTTP protocol.
  ; Allow users to push local repositories to Gitea and have them automatically created for a user or an org
  ENABLE_PUSH_CREATE_USER = false
  ENABLE_PUSH_CREATE_ORG = false
  
  [repository.issue]
  LOCK_REASONS = Too heated,Off-topic,Resolved,Spam,Irrelevant
  
  [repository.pull-request]
  WORK_IN_PROGRESS_PREFIXES                     = WIP:,[WIP]
  CLOSE_KEYWORDS                                = close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved, done, fertig, erledigt, geschlossen, abgeschlossen
  REOPEN_KEYWORDS                               = reopen, reopens, reopened, geöffnet, geoeffnet, wiedergeöffnet, wiedergeoeffnet, korrigieren
  DEFAULT_MERGE_MESSAGE_COMMITS_LIMIT           = 64
  DEFAULT_MERGE_MESSAGE_SIZE                    = 5120
  DEFAULT_MERGE_MESSAGE_ALL_AUTHORS             = false
  DEFAULT_MERGE_MESSAGE_MAX_APPROVERS           = 16
  DEFAULT_MERGE_MESSAGE_OFFICIAL_APPROVERS_ONLY = true
  
  [repository.signing]
  SIGNING_KEY = default
  WIKI = never
  
  [ui]
  EXPLORE_PAGING_NUM      = 64
  ISSUE_PAGING_NUM        = 32
  MEMBERS_PAGING_NUM      = 64
  FEED_MAX_COMMIT_NUM     = 16
  GRAPH_MAX_COMMIT_NUM    = 256
  CODE_COMMENT_LINES      = 4
  THEMES                  = gitea,arc-green
  DEFAULT_THEME           = arc-green
  ; All available reactions users can choose on issues/prs and comments.
  ; Values can be emoji alias (:smile:) or a unicode emoji.
  ; For custom reactions, add a tightly cropped square image to public/emoji/img/reaction_name.png
  ;     https://gitea.com/gitea/gitea.com/issues/8
  ;     https://docs.gitea.io/en-us/customizing-gitea/
  REACTIONS               = +1, -1, laugh, confused, heart, hooray, eyes
  SHOW_USER_EMAIL         = true
  DEFAULT_SHOW_FULL_NAME  = false
  SEARCH_REPO_DESCRIPTION = true
  USE_SERVICE_WORKER      = true
  
  [ui.admin]
  USER_PAGING_NUM   = 128
  REPO_PAGING_NUM   = 128
  ORG_PAGING_NUM    = 128
  NOTICE_PAGING_NUM = 64
  
  [ui.user]
  REPO_PAGING_NUM = 64
  
  [ui.meta]
  AUTHOR = Gitea
  DESCRIPTION = Gitea (Git with a cup of tea) is a painless self-hosted Git service written in Go
  KEYWORDS = go,git,self-hosted,gitea
  
  [ui.notification]
  MIN_TIMEOUT  = 5s
  MAX_TIMEOUT  = 60s
  TIMEOUT_STEP = 5s
  
  [markdown]
  ENABLE_HARD_LINE_BREAK = true
  CUSTOM_URL_SCHEMES     = git,svn,ftp,ftps,sftp
  FILE_EXTENSIONS        = .md,.markdown,.mdown,.mkd
  
  [mailer]
  ENABLED        = true
  MAILER_TYPE    = sendmail
  FROM           = ${USER}-gitea@${APPDOMAIN}
  SUBJECT_PREFIX = "Gitea: "
  ;SENDMAIL_PATH  = 
  
  [time]
  ; They want it this way:
  FORMAT              = 2006-01-02 15:04:05
  DEFAULT_UI_LOCATION = Europe/Amsterdam
  
  [other]
  SHOW_FOOTER_BRANDING           = false
  SHOW_FOOTER_VERSION            = false
  SHOW_FOOTER_TEMPLATE_LOAD_TIME = true
  
  [log]
  MODE      = file
  LEVEL     = info ; [Trace, Debug, Info, Warn, Error, Critical, Fatal, None]
  ROOT_PATH = ${APPPATH}/log
  
  [log.file]
  LOG_ROTATE   = true
  DAILY_ROTATE = true
  MAX_DAYS     = 14
  COMPRESS     = false
  __EOF__


Gitea using external renderer (optional)
----------------------------------------

We can install an extra `external rendering <https://docs.gitea.io/en-us/external-renderers/>`_ extension AsciiDoc.

.. code-block:: sh
  
  [isabell@stardust ~]$ 
  # Check for pre installed asciidoctor.
  if [[ -z $(asciidoctor --version) ]]
  then 
    gem install asciidoctor 2>&1 >> /home/${USER}/.${APPNAME}-install-gems.log
    # Uberspace is making a lot of comfort. The installed gem will be linked automatically via /opt/uberspace/etc/${USER}/binpaths/ruby/
  else 
    echo "asciidoctor already installed."
  fi
  cat >> ${APPPATH}/custom/conf/app.ini <<__EOF__
  [markup.asciidoc]
  ENABLED = true
  FILE_EXTENSIONS = .adoc,.asciidoc
  RENDER_COMMAND = "asciidoctor -e -a leveloffset=-1 --out-file=- -"
  IS_INPUT_FILE = false
  __EOF__


Gitea initalization
-------------------

Above we locked the registration and the web installation feature. Now we create the database layout and security keys.

.. code-block:: sh
  
  [isabell@stardust ~]$ 

  ${APPPATH}/gitea migrate 2>&1 > /home/${USER}/.${APPNAME}-migrate.log

  ${APPPATH}/gitea generate secret INTERNAL_TOKEN 2>&1 > /home/${USER}/.${APPNAME}-secret-INTERNAL_TOKEN.log
  ${APPPATH}/gitea generate secret SECRET_KEY 2>&1 > /home/${USER}/.${APPNAME}-secret-SECRET_KEY.log
  ${APPPATH}/gitea generate secret JWT_SECRET 2>&1 > /home/${USER}/.${APPNAME}-secret-JWT_SECRET.log
  ${APPPATH}/gitea generate secret LFS_JWT_SECRET 2>&1 > /home/${USER}/.${APPNAME}-secret-LFS_JWT_SECRET.log


Gitea admin user
----------------

We create an admin user via Gitea `command line <https://docs.gitea.io/en-us/command-line/#admin>`_ . They aren't allowing ``admin`` as name. By default we print the users name and random password to the bash output and write it into ``/home/${USER}/.gitea-admin.txt`` file.

.. code-block:: sh
  
  [isabell@stardust ~]$ 
  USERSNAME="admingitea"
  USERSPWD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16 ; echo '')
  echo "$(date "+%Y-%m-%dT%H:%M:%S") ${APPPATH}/gitea admin create-user --username ${USERSNAME} --password ${USERSPWD} --email ${USER}@uber.space --admin" >> /home/${USER}/.gitea-create-admin.log
  ${APPPATH}/gitea admin create-user --username ${USERSNAME} --password ${USERSPWD} --email ${USER}@uber.space --admin 2>&1 >> /home/${USER}/.gitea-create-admin.log
  cat > /home/${USER}/.gitea-admin.txt <<__EOF__
  Gitea Administrator
  Username: ${USERSNAME}
  Password: ${USERSPWD}
  E-Mail  : ${USER}@uber.space
  __EOF__
  echo " "
  echo -e "\033[0;33mCreated administrator.\033[0m"
  echo -e "    Username: \033[0;36m${USERSNAME}\033[0m"
  echo -e "    Password: \033[0;36m${USERSPWD}\033[0m"
  echo -e "    Saved in: \033[0;36m/home/${USER}/.gitea-admin.txt\033[0m"
  USERSNAME=""
  USERSPWD=""


Gitea ssh setup (optional)
--------------------------

Gitea can manage the ssh keys. 

.. code-block:: sh
  
  [isabell@stardust ~]$ ln -s ~/.ssh ${APPPATH}/.ssh

We add the git ssh key in the Gitea web application and extend the ``~/.ssh/authorized_keys`` file after the three dots.

.. code-block:: sh

  cat >> /home/${USER}/.ssh/authorized_keys <<__EOF__
  command="if [ -t 0 ]; then bash; elif [[ \$SSH_ORIGINAL_COMMAND =~ ^(scp|rsync|mysqldump).* ]]; then eval \$SSH_ORIGINAL_COMMAND; else ${APPPATH}/gitea serv key-1 --config='${APPPATH}/custom/conf/app.ini'; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-...
  __EOF__

.. warning:: Append the ssh authorized_keys file with your public key after ``ssh-``!

.. note:: You can still use the Uberspace Dashboard_ to add ssh keys.


Uberspace service for Gitea
---------------------------

.. code-block:: sh

  [isabell@stardust ~]$
  cat > /home/${USER}/etc/services.d/gitea.ini <<__EOF__
  [program:gitea]
  command=%(ENV_HOME)s/opt/gitea/gitea web
  __EOF__
  echo " "
  echo -e "\033[0;33mCreated Gitea service.\033[0m"
  supervisorctl reread
  supervisorctl update
  supervisorctl status

The status of gitea must be RUNNING. If not, check configuration.


Uberspace web backend
---------------------

If you're using your own domain and didn't put into uberspace:

.. code-block:: sh

  if [ "${APPDOMAIN}" == "${USER}.uber.space" ]; then
      echo "Using default domain: ${USER}.uber.space"
  else
      uberspace web domain add ${APPDOMAIN}
  fi

We're connecting the uberspace :manual:`web backends <web-backends>` with the application:

.. code-block:: sh

  uberspace web backend set ${APPWEBPAGE} --http --port ${APPPORT} --remove-prefix
  uberspace web backend list
  echo -e "\033[0;33mNow you can visit your application page:\033[0m  \n     \033[1;36m${APPROOTURL}\033[0m"


Uninstallation Script
=====================

.. code-block:: sh

  cat > /home/${USER}/.gitea-uninstall.sh <<__EOF__
  echo -e "\033[0;33mGitea uninstallation.\033[0m"
  supervisorctl stop gitea
  supervisorctl remove gitea
  rm /home/${USER}/etc/services.d/gitea.ini
  supervisorctl reread
  supervisorctl update
  supervisorctl status
  uberspace web backend del ${APPWEBPAGE}
  echo -e "\033[1;33mAttention\033[0m: Delete gitea line in \033[0;36m/home/${USER}/.ssh/authorized_keys\033[0m by yourself."
  mysql -e "DROP DATABASE ${USER}_gitea"
  gem uninstall asciidoctor -x
  rm -rf ${APPPATH}
  echo "If wanted, remove manually ${DOWNFILEPATH}."
  echo "If wanted, remove manually ${CHECKFILEPATH}."
  #rm /home/${USER}/.${APPNAME}-admin.txt
  #rm /home/${USER}/.${APPNAME}-migrate.log
  #rm /home/${USER}/.${APPNAME}-secret-INTERNAL_TOKEN.log
  #rm /home/${USER}/.${APPNAME}-secret-SECRET_KEY.log
  #rm /home/${USER}/.${APPNAME}-secret-JWT_SECRET.log
  #rm /home/${USER}/.${APPNAME}-secret-LFS_JWT_SECRET.log
  #rm /home/${USER}/.${APPNAME}-install-gems.log
  #rm /home/${USER}/.${APPNAME}-uninstall.sh
  if [ "${APPDOMAIN}" != "${USER}.uber.space" ]; then
      echo "Maybe you want to delete used doamin ${APPDOMAIN}."
      echo "    uberspace web domain del ${APPDOMAIN}"
      echo "Maybe you're using this for other services."
  fi
  echo -e "\033[0;33mGitea uninstallation finished.\033[0m"
  __EOF__
  chmod u+x /home/${USER}/.gitea-uninstall.sh
  echo " "
  echo -e "\033[0;33mTo uninstall Gitea run:\033[0m"
  echo -e "     \033[0;36m/home/${USER}/.gitea-uninstall.sh\033[0m"


Finished
========

Done. Installed files and folders are:
* ``~/opt/gitea``
* ``~/.gitea-*``
* ``~/etc/services.d/gitea.ini``
* ``~/.gem/ruby/2.7.0/*/asciidoctor*``


Updates
=======

.. note:: Check the update feed_ or releases_ page regularly to stay informed about the newest version.

To update do:

* Stop the application ``supervisorctl stop gitea``
* Set the variables again.
* Do the download, verify and place part from above.
* To migrate the application redo the initalization from above.
* Start the application ``supervisorctl start gitea``
* Check if the application is running ``supervisorctl status gitea``

.. note:: If the service is not ``RUNNUNG`` check and compare your config file with the Gitea Documentation_ and the `file sample <https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample>`_.

.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _Documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
.. _releases: https://github.com/go-gitea/gitea/releases/latest
.. _licence: https://github.com/go-gitea/gitea/blob/master/LICENSE
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gitea 1.11.5, Uberspace 7.6.0

.. author_list::
