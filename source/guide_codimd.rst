.. highlight:: console
.. author:: stunkymonkey <http://stunkymonkey.de>

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

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`Node <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`


Prerequisites
=============

.. include:: includes/my-print-defaults.rst

We're using :manual:`Node <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Install the package manager ``yarn`` using the node.js package manager (``npm``):

::

 [isabell@stardust ~]$ npm install --global yarn
 /home/isabell/bin/yarn -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
 /home/isabell/bin/yarnpkg -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
 + yarn@1.16.0
 added 1 package in 1.08s
 [isabell@stardust ~]$

Installation
============

You'll need a database for CodiMD_.

Create Database
---------------

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_codimd CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
  [isabell@stardust ~]$

Download Sources
----------------

Go to the release_-site and download the latest version

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/codimd/server/archive/1.2.1.zip
  --2018-10-17 18:50:29--  https://github.com/codimd/server/archive/1.2.1.zip
  Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
  Connecting to github.com (github.com)|192.30.253.112|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: https://codeload.github.com/codimd/server/zip/1.2.1 [following]
  --2018-10-17 18:50:29--  https://codeload.github.com/codimd/server/zip/1.2.1
  Resolving codeload.github.com (codeload.github.com)... 192.30.253.121, 192.30.253.120
  Connecting to codeload.github.com (codeload.github.com)|192.30.253.121|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: unspecified [application/zip]
  Saving to: ‘1.2.1.zip’

      [     <=>                                           ] 7,090,453   6.28MB/s   in 1.1s

  2018-10-17 18:50:31 (6.28 MB/s) - ‘1.2.1.zip’ saved [7090453]
  [isabell@stardust ~]$ unzip 1.2.1.zip
  [...]
  [isabell@stardust ~]$ mv codimd-1.2.1/ codimd
  [isabell@stardust ~]$ rm 1.2.1.zip
  [isabell@stardust ~]$ cd codimd
  [isabell@stardust codimd]$

Install npm dependencies and create configs
-------------------------------------------

.. code-block:: console

  [isabell@stardust codimd]$ bin/setup
  copy config files
  install npm packages
  [...]
  [isabell@stardust codimd]$


Remove UglifyJS
---------------

The UglifyJS plugin gets the compilation step terminated, because it tries to compile everything in parallel and then reaches the maximum memory-limit/user of Uberspace. Since it's optional, we'll remove it.

Open ``webpack.production.js`` and comment out this line (currently line 6):

.. code-block:: javascript

  var ParallelUglifyPlugin = require('webpack-parallel-uglify-plugin')

So that it looks like this:

.. code-block:: javascript
  :emphasize-lines: 1

  //var ParallelUglifyPlugin = require('webpack-parallel-uglify-plugin')


And comment out this block (currently line 15 - 26):

.. code-block:: javascript

    new ParallelUglifyPlugin({
      uglifyJS: {
        compress: {
          warnings: false
        },
        output: {
          max_line_len: 1000000
        },
        mangle: false,
        sourceMap: false
      }
    }),

So that it looks like this:

.. code-block:: javascript
  :emphasize-lines: 1, 12

  /*new ParallelUglifyPlugin({
      uglifyJS: {
        compress: {
          warnings: false
        },
        output: {
          max_line_len: 1000000
        },
        mangle: false,
        sourceMap: false
      }
    }),*/

.. note:: The details were such at the time of writing, they might be different for the version you downloaded. If they are different, just comment out any blocks mentioning ``UglifyPlugin``.

Compilation
-----------

.. code-block:: console

  [isabell@stardust codimd]$ npm run build
  [...]
  [isabell@stardust codimd]$


Configuration
=============

Create config file
------------------

I don’t know why, but when I tried it, CodiMD ignored the config files. So we’ll make this very short and replace the content of ``config.json`` with this:

.. code-block:: JSON

  {
    "production": {}
  }

That’s all. The actual configuration will be done via environment variables in ``codimd.ini`` below.

Get Session Cookie
------------------

Generate random string to sign our session cookies with:

.. code-block:: console

  [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;
  extremerandom
  [isabell@stardust ~]$

Keep it at hand.

Configure Database
------------------

Enter your sql credetials in ``.sequelizerc``:

.. code-block:: ini
  :emphasize-lines: 7

  var path = require('path');

  module.exports = {
      'config':          path.resolve('config.json'),
      'migrations-path': path.resolve('lib', 'migrations'),
      'models-path':     path.resolve('lib', 'models'),
      'url':             'mysql://<username>:<mysql_pw>@127.0.0.1:3306/<username>_codimd'
  }

In our example this would be:

.. code-block:: ini
  :emphasize-lines: 7

  var path = require('path');

  module.exports = {
      'config':          path.resolve('config.json'),
      'migrations-path': path.resolve('lib', 'migrations'),
      'models-path':     path.resolve('lib', 'models'),
      'url':             'mysql://isabell:MySuperSecretPassword@127.0.0.1:3306/isabell_codimd'
  }

Setup daemon
------------

Create ``~/etc/services.d/codimd.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 6, 7, 20

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

In our example this would be:

.. code-block:: ini
  :emphasize-lines: 6, 7, 20

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

Replace the placeholders in ``CMD_SESSION_SECRET``, ``CMD_DOMAIN``, and ``CMD_DB_URL``.

See the `official documentation <https://github.com/codimd/server/blob/master/docs/configuration-config-file.md>`_ for a description of what the environment variables are used for.


Finishing installation
======================

Register our new service and start it
-------------------------------------

Once you finish this step, a CodiMD instance will be created that does not rely on third-party CDN servers and can only be used by people that have an account that was created via CLI.

.. include:: includes/supervisord.rst


Add a user
----------

Since we don’t want to run a public instance and have disabled registration, we use the CLI to add a user:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/codimd
  [isabell@stardust codimd]$ CMD_DB_URL="mysql://<username>:<mysql_pw>@127.0.0.1:3306/<username>_codimd" bin/manage_users --add isabell@uber.space
  [isabell@stardust codimd]$

It will prompt you for a password now.

.. warning::

  Don’t forget your password, neither the site nor the CLI currently seem to offer a way to reset it!


Configure web server
--------------------

.. include:: includes/web-backend.rst

.. note::

    CodiMD is running on port 60101.

Congratulations! You're done.


Updates
=======
.. note:: Check the release_ site regularly to stay informed about new releases.

.. code-block:: console

  [isabell@stardust codimd]$ cd ~
  [isabell@stardust ~]$ supervisorctl stop codimd
  codimd: stopped
  [isabell@stardust ~]$ mv codimd codimd-old
  [isabell@stardust ~]$

Redo these steps:

- `Download Sources`_
- `Remove UglifyJS`_
- `Compilation`_
- `Create config file`_
- `Configure Database`_

If everything is fine:

.. code-block:: console

  [isabell@stardust ~]$ node_modules/.bin/sequelize db:migrate
  [...]
  [isabell@stardust ~]$ supervisorctl start codimd
  codimd: started
  [isabell@stardust ~]$ rm codimd-old -rf
  [isabell@stardust ~]$

If you are having problems remove the ``~/codimd/`` and move ``~/codimd-old/`` back to its place.


.. _HackMD: https://hackmd.io/
.. _CodiMD: https://github.com/codimd/server
.. _release: https://github.com/codimd/server/releases

----

Tested with CodiMD 1.2.1, Uberspace 7.1.13

.. author_list::
