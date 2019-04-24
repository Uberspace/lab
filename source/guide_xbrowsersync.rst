.. highlight:: console

.. author:: Phil <development@beph.de>

.. tag:: lang-nodejs

.. sidebar:: Logo

  .. image:: _static/images/xbrowsersync.svg
      :align: center

################
xBrowserSync API
################

xBrowserSync is a free and open-source browser bookmark syncing tool with support for Chrome, Firefox and Android (via app).

The xBrowserSync API provides an individual sync server where your bookmarks stored encrypted.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`supervisord <supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :lab:`MongoDB <guide_mongodb>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

MongoDB
-------

Install :lab:`MongoDB <guide_mongodb>`.


Subdomain & Web backends
------------------------

Setup a web backend on port ``8080``

::

   [isabell@stardust ~]$ uberspace web backend set / --http --port 8080


Installation
============

Download xBrowserSync API
-------------------------
Get the xBrowserSync API source code from GitHub_ and clone it to ``~/xbrowsersync/api``, be sure to replace the pseudo branch number ``v1.1.18`` here with the latest release branch from the GitHub_ repository.

::

 [isabell@stardust ~]$ git clone https://github.com/xbrowsersync/api.git --branch v1.1.8 xbrowsersync/api
 [...]
 Receiving objects: 100% (117/117), 566.29 KiB | 1.45 MiB/s, done.
 Resolving deltas: 100% (14/14), done.
 [...]
 [isabell@stardust ~]$

Creating MongoDB User & Tables
--------------------------------

Open a Mongo shell and enter the mongo command listed below.
This creates a new database user and the tables needed by xBrowserSync.
Replace ``<password>`` with a cleartext password of your choice, which is used as password for a new created database user.
Afterwards leave the shell with the ``exit`` command.

::

  [isabell@stardust ~]$ mongo
  [...]
  >use admin
   db.createUser({ user: "xbrowsersyncdb", pwd: "<password>", roles: [ { role: "readWrite", db: "xbrowsersync" }, { role: "readWrite", db: "xbrowsersynctest" } ] })
   use xbrowsersync
   db.newsynclogs.createIndex( { "expiresAt": 1 }, { expireAfterSeconds: 0 } )
   db.newsynclogs.createIndex({ "ipAddress": 1 })
   >exit
   [isabell@stardust ~]$


Installation
------------

Now you can install all the depenencies needed for xBrowserSync by using npm.
Additionally you can let npm run a so called `security audit`_, which detects and updates insecure dependencies.

::

  [isabell@stardust ~]$ cd ~/xbrowsersync/api
  [isabell@stardust api]$ npm install
  [isabell@stardust api]$ [...]
  [isabell@stardust api]$ npm audit fix
  [isabell@stardust api]$ [...]
  [isabell@stardust api]$

Configuration
-------------

.. warning::
  You are recommended to look also at the other configuration settings.
  For example: If you plan to use only a single account you should limit the number of accounts.

Copy the sample configuration file:

::

  [isabell@stardust api]$ cp config/settings.default.json config/settings.json

Use a your favourite text editor and edit the file settings.json.
At least the ``server.host`` and ``db.username`` and ``db.password`` have to be changed.
Furthermore you should change the log path:

::

  {
    "allowedOrigins": [],
    "dailyNewSyncsLimit": 3,
    "db": {
      "authSource": "admin",
      "connTimeout": 30000,
      "host": "127.0.0.1",
      "name": "xbrowsersync",
      "username": "xbrowsersyncdb",
      "password": "<password>",
      "port": 27017
    },
    "log": {
      "file": {
        "enabled": true,
        "level": "info",
        "path": "/home/<username/xbrowsersync/api/log/xbrowsersync.log",
        "rotatedFilesToKeep": 5,
        "rotationPeriod": "1d"
      },
      "stdout": {
        "enabled": true,
        "level": "info"
      }
    },
    "maxSyncs": 5242,
    "maxSyncSize": 512000,
    "server": {
      "behindProxy": false,
      "host": "0.0.0.0",
      "https": {
        "certPath": "",
        "enabled": false,
        "keyPath": ""
      },
      "port": 8080
    },
    "status": {
      "allowNewSyncs": true,
      "message": "",
      "online": true
    },
    "tests": {
      "db": "xbrowsersynctest",
      "port": 8081
    },
    "throttle": {
      "maxRequests": 1000,
      "timeWindow": 300000
    }
  }

Create a service & start xBrowserSync
-------------------------------------

Create a service file under ``~/etc/services.d/xbrowsersync.ini`` and replace ``<username>`` with your Uberspace username:

 ::

  [program:xbrowsersync]
  command=node /home/<username>/xbrowsersync/api/dist/api.js
  autostart=yes
  autorestart=yes


Then start your daemon:

::

  [isabell@stardust ~]$ supervisorctl reread
  [isabell@stardust ~]$ supervisorctl update
  [isabell@stardust ~]$

Using xBrowserSync
==================

If your installation was successful you now can reach xBrowserSync by pointing with your browser to your specified domain and see a default status page.

.. warning::
  Always take a backup of your browsers bookmarks.
  For example by using your browsers bookmark export function before start using xBrowserSync.

Now you can install the xBrowserSync AddOn to your Browser.
Open the settings panel and enter your personal xBrowserSync URL.
Then go back and follow the AddOn instructions.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version available, update your branch according to the version number (``v1.1.18``)

::

 [isabell@stardust ~]$ cd ~/xbrowsersync/api
 [isabell@stardust api]$ git pull origin v1.1.18
 [isabell@stardust api]$


.. _xBrowserSync: https://www.xbrowsersync.org/
.. _GitHub: https://github.com/xbrowsersync/
.. _feed: https://github.com/xbrowsersync/api/releases.atom
.. _security audit: https://docs.npmjs.com/cli/audit

----

Tested with xBrowserSync 1.1.18, Uberspace 7.2.8.2

.. author_list::
