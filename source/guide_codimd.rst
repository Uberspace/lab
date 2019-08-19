.. highlight:: console

.. author:: stunkymonkey <http://stunkymonkey.de>
.. author:: Matthias Kolja Miehl <https://makomi.net>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: collaborative-editing

.. sidebar:: Logo

  .. image:: _static/images/codimd.png
      :align: center

######
CodiMD
######

.. tag_list::

CodiMD_ lets you create real-time collaborative markdown notes on all platforms.
Inspired by HackMD_ but with more focus on speed and flexibility.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

Node version
------------

We're using :manual:`Node <lang-nodejs>` in the stable version 8:

.. code-block:: console

  [isabell@stardust ~]$ uberspace tools version show node
  Using 'Node.js' version: '8'
  [isabell@stardust ~]$

MySQL credentials
-----------------

.. include:: includes/my-print-defaults.rst

URL setup
---------

Your URL needs to be set up:

.. include:: includes/web-domain-list.rst

See section "setup" in the :manual:`domains <web-domains>` manual, in case you want to set up a custom URL like ``isabell.example``.

Required packages
-----------------

Install the package manager ``yarn`` using the node.js package manager (``npm``) as well as two additional missing packages ``webpack`` and ``cacache``:

.. code-block:: console

  [isabell@stardust ~]$ npm install --global yarn
  /home/isabell/bin/yarn -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
  /home/isabell/bin/yarnpkg -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
  + yarn@1.17.3
  added 1 package in 1.08s
  [isabell@stardust ~]$ yarn cache clean
  yarn cache v1.17.3
  success Cleared cache.
  Done in 0.06s.
  [isabell@stardust ~]$ npm install --global webpack cacache
  /home/isabell/bin/webpack -> /home/isabell/lib/node_modules/webpack/bin/webpack.js
  + webpack@4.35.3
  + cacache@12.0.0
  added 378 packages from 197 contributors in 21.094s
  [isabell@stardust ~]$

See the `official yarn setup instructions <https://yarnpkg.com/en/docs/install>`_ for a variety of systems in case you have trouble.

Installation
============

Create a database
-----------------

You'll need a database for CodiMD_.

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_codimd CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
  [isabell@stardust ~]$

Download sources
----------------

Download the `latest release <https://github.com/codimd/server/releases/latest>`_:

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/codimd/server/archive/1.4.0.zip
  --2019-07-16 19:35:44--  https://github.com/codimd/server/archive/1.4.0.zip
  Resolving github.com (github.com)... 140.82.118.4
  Connecting to github.com (github.com)|140.82.118.4|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: https://codeload.github.com/codimd/server/zip/1.4.0 [following]
  --2019-07-16 19:35:45--  https://codeload.github.com/codimd/server/zip/1.4.0
  Resolving codeload.github.com (codeload.github.com)... 140.82.113.9
  Connecting to codeload.github.com (codeload.github.com)|140.82.113.9|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: unspecified [application/zip]
  Saving to: ‘1.4.0.zip’

      [     <=>                                           ] 7,329,912   6.28MB/s   in 1.1s

  2019-07-16 19:35:48 (2.32 MB/s) - ‘1.4.0.zip’ saved [7329912]
  [isabell@stardust ~]$ unzip 1.4.0.zip
  [...]
  [isabell@stardust ~]$ rm 1.4.0.zip
  [isabell@stardust ~]$ mv server-1.4.0/ codimd
  [isabell@stardust ~]$ cd codimd
  [isabell@stardust codimd]$

Install npm dependencies and create example configurations
----------------------------------------------------------

.. code-block:: console

  [isabell@stardust codimd]$ bin/setup
  copy config files
  install npm packages
  [...]
  [isabell@stardust codimd]$

Remove UglifyJS
---------------

The ``UglifyJS`` plugin causes the upcomming compilation step to terminate prematurely. It tries to compile everything in parallel and as a result exceeds the user's memory limit as allotted by Uberspace. Since ``UglifyJS`` is optional, we'll remove it.

.. warning::

  Removing ``UglifyJS`` will result in larger files for clients to download and will most likely make the application feel sluggish on (older) mobile devices. Perform the compilation on a separate computer to work around this issue.

Open ``.babelrc`` and deactivate ``UglifyJS``:

.. code-block:: JSON
  :emphasize-lines: 6

  {
    "presets": [
      ["env", {
        "targets": {
          "node": "8",
          "uglify": true
        }
      }]
    ],
    "plugins": [
      "transform-runtime"
    ]
  }

Result:

.. code-block:: JSON
  :emphasize-lines: 6

  {
    "presets": [
      ["env", {
        "targets": {
          "node": "8",
          "uglify": false
        }
      }]
    ],
    "plugins": [
      "transform-runtime"
    ]
  }

Also, comment out each line of ``public/vendor/ot/compress.sh`` with a ``#``:

.. code-block:: console

  #uglifyjs --compress --mangle --output ot.min.js \
  #./text-operation.js \
  #./selection.js \
  #./wrapped-operation.js \
  #./undo-manager.js \
  #./client.js \
  #./codemirror-adapter.js \
  #./socketio-adapter.js \
  #./ajax-adapter.js \
  #./editor-client.js

.. note:: This is how it worked at the time of writing and it might be different for the version you downloaded. If it is different, try commenting out everything related to ``UglifyJS``. If the compilation fails the first time due to RAM limitations, just start it again. It tends to work the second time.

Compile the source
------------------

Now, let's build the front-end bundle. This will take some time.

.. code-block:: console

  [isabell@stardust codimd]$ npm run build
  [...]
  [isabell@stardust codimd]$

Configuration
=============

Create config file
------------------
Replace the content of ``config.json`` with the following, using your MySQL username and password from the previous step:

.. code-block:: JSON
  :emphasize-lines: 3,12,13,14

  {
    "production": {
          "domain": "<domain>",
          "loglevel": "info",
          "hsts": {
              "enable": true,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": true,
              "preload": true
          },
          "db": {
              "username": "<username>",
              "password": "<mysql_pw>",
              "database": "<username>_codimd",
              "host": "localhost",
              "port": "3306",
              "dialect": "mysql"
          }
      }
  }

Example:

.. code-block:: JSON
  :emphasize-lines: 3,12,13,14

  {
    "production": {
          "domain": "isabell.uber.space",
          "loglevel": "info",
          "hsts": {
              "enable": true,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": true,
              "preload": true
          },
          "db": {
              "username": "isabell",
              "password": "MySuperSecretPassword",
              "database": "isabell_codimd",
              "host": "localhost",
              "port": "3306",
              "dialect": "mysql"
          }
      }
  }

A backup of the original content can be found in ``config.json.example``.

.. note:: In case you are performing an update, use ``rm config.json && cp ../codimd-old/config.json .``.

.. note::

  ``config.json`` is read whenever the server is started via ``node app.js``. In order to make it use the the ``production`` section of ``config.json``, one has to set ``NODE_ENV`` accordingly: ``NODE_ENV=production node app.js``.

  The final server configuration will be done separately in ``~/etc/services.d/codimd.ini`` as described in the next main section.

Configure database
------------------

Open ``.sequelizerc`` and set the variable ``url`` as described below, again using your MySQL username and password:

.. code-block:: ini
  :emphasize-lines: 7

  var path = require('path');

  module.exports = {
      'config':          path.resolve('config.json'),
      'migrations-path': path.resolve('lib', 'migrations'),
      'models-path':     path.resolve('lib', 'models'),
      'url':             'mysql://<username>:<mysql_pw>@127.0.0.1:3306/<username>_codimd'
  }

Example:

.. code-block:: ini
  :emphasize-lines: 7

  var path = require('path');

  module.exports = {
      'config':          path.resolve('config.json'),
      'migrations-path': path.resolve('lib', 'migrations'),
      'models-path':     path.resolve('lib', 'models'),
      'url':             'mysql://isabell:MySuperSecretPassword@127.0.0.1:3306/isabell_codimd'
  }

Finishing installation
======================

Add a user
----------

Since we don’t want to run a public instance and have disabled user registration via the web interface, we will use the command line to add a user.

First, start the server once via ``node app.js`` to let it initialize/ migrate the database. Afterwards, terminate it using ``CTRL-C``.

.. code-block:: console

  [isabell@stardust ~]$ cd ~/codimd
  [isabell@stardust codimd]$ NODE_ENV=production node app.js
  [...]
  [isabell@stardust codimd]$

Then, add the first user. The username has to be formated like an email address.

.. code-block:: console

  [isabell@stardust ~]$ cd ~/codimd
  [isabell@stardust codimd]$ NODE_ENV=production bin/manage_users --add isabell@uber.space
  Password for isabell@uber.space:*************************
  Created user with email isabell@uber.space
  [isabell@stardust codimd]$

.. note::

  You can reset your password via the command line using ``NODE_ENV=production bin/manage_users --reset isabell@uber.space``.

Add CodiMD as a service
-----------------------

We will run CodiMD as a service, so it runs in the background and is restarted automatically.

Generate session cookie
~~~~~~~~~~~~~~~~~~~~~~~

Generate a random string to sign your session cookies with:

.. code-block:: console

  [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;
  extremerandom
  [isabell@stardust ~]$

Create service configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``~/etc/services.d/codimd.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 6,7,20

  [supervisord]
  loglevel=warn

  [program:codimd]
  environment=
  	CMD_SESSION_SECRET="<random>",
  	CMD_DOMAIN="<domain>",
  	CMD_PORT=60101,
  	NODE_ENV="production",
  	CMD_USECDN=false,
  	CMD_ALLOW_ANONYMOUS=false,
  	CMD_ALLOW_ANONYMOUS_EDITS=true,
  	CMD_ALLOW_FREEURL=true,
  	CMD_DEFAULT_PERMISSION=private,
  	CMD_SESSION_LIFE=1209600000,
  	CMD_EMAIL=true,
  	CMD_ALLOW_EMAIL_REGISTER=false,
  	CMD_IMAGE_UPLOAD_TYPE=filesystem,
  	CMD_PROTOCOL_USESSL=true,
  	CMD_DB_URL="mysql://<username>:<mysql_pw>@localhost:3306/<username>_codimd",

  directory=%(ENV_HOME)s/codimd
  command=node app.js

Example:

.. code-block:: ini
  :emphasize-lines: 6,7,20

  [supervisord]
  loglevel=warn

  [program:codimd]
  environment=
  	CMD_SESSION_SECRET="extremerandom",
  	CMD_DOMAIN="isabell.uber.space",
  	CMD_PORT=60101,
  	NODE_ENV="production",
  	CMD_USECDN=false,
  	CMD_ALLOW_ANONYMOUS=false,
  	CMD_ALLOW_ANONYMOUS_EDITS=true,
  	CMD_ALLOW_FREEURL=true,
  	CMD_DEFAULT_PERMISSION=private,
  	CMD_SESSION_LIFE=1209600000,
  	CMD_EMAIL=true,
  	CMD_ALLOW_EMAIL_REGISTER=false,
  	CMD_IMAGE_UPLOAD_TYPE=filesystem,
  	CMD_PROTOCOL_USESSL=true,
  	CMD_DB_URL="mysql://isabell:MySuperSecretPassword@localhost:3306/isabell_codimd",

  directory=%(ENV_HOME)s/codimd
  command=node app.js

See the `official documentation <https://github.com/codimd/server/blob/master/docs/configuration-config-file.md>`_ for a description of what each environment variable is used for.

Register our new service and start it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you finish this step, a CodiMD instance will be created that does not rely on third-party CDN servers and can only be used by people that have an account that was created via command line. It will continue to run after you quit your current SSH session.

.. include:: includes/supervisord.rst

Configure web backend
---------------------

.. include:: includes/web-backend.rst

.. note::

    CodiMD is running on port 60101.

See section "specific domain" in the :manual:`web-backends <web-backends>` manual, in case you want to set up the web backend for a custom URL like ``isabell.example``.

Congratulations! You're done.

Updates
=======

.. note:: Check the `release site <https://github.com/codimd/server/releases>`_ regularly to stay informed about the newest version. Subscribe to releases via the ``Watch`` button at the top, in case you have a GitHub account.

Perform the following steps, to update your `CodiMD`_ installation.

Make a backup of your data
--------------------------

Backup your notes by opening the main page at ``isabell.example`` and selecting "Export user data" from the top right user menu. In order to also backup notes from other users, have a look at section "Working with dumps" in the :manual:`MySQL <database-mysql>` manual.

Stop the service and backup the old installation directory
----------------------------------------------------------

.. code-block:: console

  [isabell@stardust codimd]$ cd ..
  [isabell@stardust ~]$ supervisorctl stop codimd
  codimd: stopped
  [isabell@stardust ~]$ mv codimd codimd-old
  [isabell@stardust ~]$

Install the latest version
--------------------------

Redo these steps:

- `Download sources`_
- `Remove UglifyJS`_
- `Compile the source`_
- `Create config file`_
- `Configure database`_

Make the switch
---------------

If you are having problems, remove ``~/codimd/`` and rename ``~/codimd-old/`` to ``codimd``:

.. code-block:: console

  [isabell@stardust codimd]$ cd ..
  [isabell@stardust ~]$ rm codimd -rf
  [isabell@stardust ~]$ mv codimd-old codimd
  [isabell@stardust ~]$ supervisorctl start codimd
  codimd: started
  [isabell@stardust ~]$

If everything is fine, migrate the database and delete your backup:

.. code-block:: console

  [isabell@stardust codimd]$ node_modules/.bin/sequelize db:migrate
  
  Sequelize CLI [Node: 8.13.0, CLI: 5.5.0, ORM: 5.8.12]
  
  Parsed url mysql://isabell:*****@localhost:3306/isabell_codimd
  No migrations were executed, database schema was already up to date.
  [isabell@stardust codimd]$ supervisorctl start codimd
  codimd: started
  [isabell@stardust codimd]$ cd ..
  [isabell@stardust ~]$ rm codimd-old -rf
  [isabell@stardust ~]$


.. _HackMD: https://hackmd.io/
.. _CodiMD: https://github.com/codimd/server

----

Tested with CodiMD 1.5.0 and Uberspace 7.3.4.2

.. author_list::
