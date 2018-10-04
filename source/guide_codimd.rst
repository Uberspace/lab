.. highlight:: console
.. author:: stunkymonkey <stunkymonkey.de>

.. sidebar:: Logo

  .. image:: _static/images/codimd.png
      :align: center

######
CodiMD
######

CodiMD_ lets you create real-time collaborative markdown notes on all platforms.
Inspired by Hackpad, with more focus on speed and flexibility, and build from HackMD_ source code.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * supervisord_
  * domains_
  * Node.js_ and its package manager npm_


Prerequisites
=============

.. include:: includes/my-print-defaults.rst

We're using Node.js_ in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

You need a special database for CodiMD_:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE <username>_gitea CHARACTER SET utf8 COLLATE utf8_general_ci;"
  [isabell@stardust ~]$

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/hackmdio/codimd.git
  Cloning into 'codimd'...
  remote: Enumerating objects: 13, done.
  remote: Counting objects: 100% (13/13), done.
  remote: Compressing objects: 100% (11/11), done.
  remote: Total 12832 (delta 4), reused 8 (delta 2), pack-reused 12819
  Receiving objects: 100% (12832/12832), 19.75 MiB | 1.20 MiB/s, done.
  Resolving deltas: 100% (7868/7868), done.
  [isabell@stardust ~]$ cd codimd
  [isabell@stardust ~]$ bin/setup
  [isabell@stardust ~]$


Remove UglifyJS
---------------

The UglifyJS plugin freezes the compilation step, because it tries to compile everything in parallel and then reaches the maximum memory-limit/user of uberspace. And since it's apparently not necessary, we'll just remove it.

Open ``webpack.production.js`` and comment out this line:

.. code-block:: javascript

  var ParallelUglifyPlugin = require('webpack-parallel-uglify-plugin')

So that it looks like this:

.. code-block:: javascript

  //var ParallelUglifyPlugin = require('webpack-parallel-uglify-plugin')


And comment out this block:

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

  /*  new ParallelUglifyPlugin({
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

  [isabell@stardust ~]$ npm run build
  [isabell@stardust ~]$


Configuration
=============

I don’t know why, but when I tried it, CodiMD ignored the config files. So we’ll make this very short and replace the content of config.json with this:

.. code-block:: JSON

  {
    "production": {}
  }

That’s all. The actual configuration will be done through environment!

Configure port
--------------

Since CodiMD uses its own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst


Get Session Cookie
------------------

Generate random string to sign our session cookies with:

.. code-block:: console

  [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;
  extremerandom
  [isabell@stardust ~]$

And remember it.

Setup daemon
------------

Create a file ``~/etc/services.d/codemd.ini`` and put the following in it:

.. code-block:: ini

	[supervisord]
	loglevel=warn

	[program:codimd]
	environment=
		CMD_SESSION_SECRET="<random>",
		CMD_DOMAIN="<domain>",
		CMD_PORT=<port>,
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

	directory=/home/<username>/codimd
	command=node app.js

In our example this would be:

.. code-block:: ini

	[supervisord]
	loglevel=warn

	[program:codimd]
	environment=
		CMD_SESSION_SECRET="extremerandom",
		CMD_DOMAIN="isabell.uber.space",
		CMD_PORT=9000,
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

	directory=/home/isabell/codimd
	command=node app.js



Replace the values in ``CMD_SESSION_SECRET``, ``CMD_DOMAIN``, ``CMD_PORT`` and ``CMD_DB_URL`` and you're good to go!

See `here <https://github.com/hackmdio/codimd#environment-variables-will-overwrite-other-server-configs>`_ for a detailed look at what these options do.


Once you run the following step, this will create a CodiMD instance without reliance on third-party CDN servers, which is private to people who had an account created via CLI.



Finishing installation
======================

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl reread
  [isabell@stardust ~]$ supervisorctl update
  [isabell@stardust ~]$

Add a user
----------

Since we don’t want to run a public instance and have disabled registration, we use the CLI to add a user:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/codemd
  [isabell@stardust ~]$ CMD_DB_URL="mysql://<username>:<mysql_pw>@localhost:3306/<username>_codimd" bin/manage_users --add isabell@uberspace.de
  [isabell@stardust ~]$

It will prompt you for a password now.

.. warning::

  Don’t forget your password, neither the site nor the CLI currently seem to offer a way to reset it!


Configure web server
--------------------

In order for your CodeMD instance to be reachable from the web, you need to put a file called ``.htaccess`` into your ``~/html`` folder (or any other DocumentRoot, see the `document root`_ for details), with the following content:

.. code-block:: ini

  DirectoryIndex disabled

  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteCond %{ENV:HTTPS} !=on
  RewriteRule .* https://%{SERVER_NAME}%{REQUEST_URI} [R=301,L]
  RewriteRule (.*) http://localhost:<PORT>/$1 [P]

Again, don't forget to fill in your port number in the last line!

And you're done!

.. Updates
   =======
   If you want to update your CodiMD installation, follow `these instruction <https://github.com/hackmdio/codimd#upgrade>`_, and merge it with this manual. Good luck.
   .. note:: Check the `changelog <https://github.com/hackmdio/codimd/releases>`_ regularly to stay informed about new updates and releases.

.. _HackMD: https://hackmd.io/
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _domains: https://manual.uberspace.de/en/web-domains.html

----

Manual derived from `this blog <https://w.h8.lv/s/how_to_install_hackmd_on_uberspace>`_

Tested with CodiMD 1.2.0, Uberspace 7.1.13

.. authors::
