.. highlight:: console

.. author:: Dustin Skoracki <https://github.com/d-sko>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: chat

.. sidebar:: About

  .. image:: _static/images/rocketchat.svg
      :align: center

###########
Rocket.Chat
###########

.. tag_list::

Rocket.Chat_ is an self hosted, open source chat software written in JavaScript.

----

.. error::

  This guide seems to be **broken** for the current versions of RocketChat, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1272

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`
  * :lab:`MongoDB <guide_mongodb>`

License
=======

All relevant legal information can be found here

  * https://github.com/RocketChat/Rocket.Chat/blob/master/LICENSE

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 12:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '12'
 [isabell@stardust ~]$

We'll also need :lab:`MongoDB <guide_mongodb>`, so follow the MongoDB guide and come back when it's running.

Check your chat URL setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download the latest Rocket.Chat release:

::

 [isabell@stardust ~]$ curl -L https://releases.rocket.chat/latest/download -o ~/rocket.chat.tgz
 curl -L https://releases.rocket.chat/latest/download -o rocket.chat.tgz
   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
 100   223  100   223    0     0    333      0 --:--:-- --:--:-- --:--:--   333
 100  146M  100  146M    0     0  13.0M      0  0:00:11  0:00:11 --:--:-- 14.0M
 [isabell@stardust ~]$

And then extract the archive, use ``--strip-components=1`` to remove the ``bundle`` prefix from the path:

::

 [isabell@stardust ~]$ mkdir ~/rocket.chat
 [isabell@stardust ~]$ tar -xzf ~/rocket.chat.tgz -C ~/rocket.chat --strip-components=1
 [isabell@stardust ~]$ chmod -R ug=rwX,o= rocket.chat
 [isabell@stardust ~]$

You can delete the archive now:

::

 [isabell@stardust ~]$ rm ~/rocket.chat.tgz
 [isabell@stardust ~]$

Now we install the required dependencies:

::

 [isabell@stardust ~]$ cd ~/rocket.chat/programs/server
 [isabell@stardust server]$ npm install
 [...]
 very long npm chatter
 [...]
 [isabell@stardust server]$ cd ~
 [isabell@stardust ~]$

Configuration
=============

Configure MongoDB
-----------------

First stop MongoDB

::

 [isabell@stardust ~]$ supervisorctl stop mongodb
 mongodb: stopped
 [isabell@stardust ~]$

Generate a keyfile

::

 [isabell@stardust ~]$ openssl rand -base64 756 > ~/mongodb/security.key
 [isabell@stardust ~]$ chmod 400 ~/mongodb/security.key
 [isabell@stardust ~]$


Update the daemon configuration file ``~/etc/services.d/mongodb.ini``, add the options ``  --keyFile %(ENV_HOME)s/mongodb/security.key`` and ``--replSet rs01``:

.. code-block:: ini

 [program:mongodb]
 command=mongod
   --dbpath %(ENV_HOME)s/mongodb
   --bind_ip 127.0.0.1
   --auth
   --keyFile %(ENV_HOME)s/mongodb/security.key
   --unixSocketPrefix %(ENV_HOME)s/mongodb
   --replSet rs01
 autostart=yes
 autorestart=yes

This is required because Rocket.Chat uses Meteor Oplog Tailing for performance improvements (see `the docs <https://rocket.chat/docs/installation/manual-installation/mongo-replicas/>`_ for further information).

Then tell supervisord to update and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 mongodb: changed
 [isabell@stardust ~]$ supervisorctl update
 mongodb: stopped
 mongodb: updated process group
 [isabell@stardust ~]$

Now initiate the replica set:

::

 [isabell@stardust ~]$ mongo --username ${USER}_mongoroot --eval "printjson(rs.initiate())"
 MongoDB shell version v4.2.3
 Enter password:
 connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("d0f22c61-382c-4178-9a6d-09b42674c14d") }
 MongoDB server version: 4.2.3
 {
 	"info2" : "no configuration specified. Using a default configuration for the set",
 	"me" : "127.0.0.1:27017",
 	"ok" : 1
 }
 [isabell@stardust ~]$

As last part of the MongoDB configuration we need a user for Rocket.Chat.
Generate a random password:

::

 [isabell@stardust ~]$ pwgen 32 1
 randompassword
 [isabell@stardust ~]$

Create ``~/rocket.chat-user-setup.js`` with the following content:

.. code-block:: none
 :emphasize-lines: 3,4

 db.createUser(
    {
      user: "<username>_rocketchat",
      pwd: "<password>",
      roles: [
        {role:"dbOwner", db:"rocketchat"},
        {role:"readWrite", db:"local"},
        {role:"clusterMonitor", db:"admin"}
      ]
    }
 )

Replace ``<username>`` with your username and ``<password>`` with the generated password.

Use mongo to add the user:

::

 [isabell@stardust ~]$ mongo admin --username ${USER}_mongoroot ~/rocket.chat-user-setup.js
 MongoDB shell version v4.2.3
 Enter password:
 connecting to: mongodb://127.0.0.1:27017/admin?compressors=disabled&gssapiServiceName=mongodb
 Implicit session: session { "id" : UUID("de28d438-1b38-4c59-964b-8a2f7f88d2d9") }
 MongoDB server version: 4.2.3
 Successfully added user: {
	 "user" : "isabell_rocketchat",
	 "roles" : [
 		{
 			"role" : "dbOwner",
 			"db" : "rocketchat"
 		},
 		{
 			"role" : "readWrite",
 			"db" : "local"
 		},
 		{
 			"role" : "clusterMonitor",
 			"db" : "admin"
 		}
 	]
 }
 [isabell@stardust ~]$

Remove the ``~/rocket.chat-user-setup.js`` file:

::

 [isabell@stardust ~]$ rm ~/rocket.chat-user-setup.js
 [isabell@stardust ~]$

Configure Webserver
-------------------

.. note:: Rocket.Chat is running on port 3000 by default. You'll set this in the `daemon setup <#setup-daemon>`_.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/rocket.chat.ini`` with the following content:

.. code-block:: ini

 [program:rocket.chat]
 command=node %(ENV_HOME)s/rocket.chat/main.js
 environment=
        MONGO_URL="mongodb://%(ENV_USER)s_rocketchat:<password>@localhost:27017/rocketchat?replicaSet=rs01&authSource=admin",
        MONGO_OPLOG_URL="mongodb://%(ENV_USER)s_rocketchat:<password>@localhost:27017/local?replicaSet=rs01&authSource=admin",
        ROOT_URL="https://%(ENV_USER)s.uber.space/",
        PORT=3000,
        TMPDIR="%(ENV_HOME)s/tmp"
 startsecs=90
 autostart=yes
 autorestart=yes

.. note:: Don't forget to replace all occurrences of ``<password>`` and to set your ``ROOT_URL`` if you don't use your default uberspace domain!

Now let's start the service:

.. include:: includes/supervisord.rst

Finishing installation
======================

Point your browser to the domain you've configured in the daemon ini file (``ROOT_URL``) and follow the setup assistant.

See the `Administrator Guides`_ for further configuration options.

.. note:: it may take a minute or so until Rocket.Chat is fully loaded, so don't worry if you see a *502 bad gateway* for a while after starting Rocket.Chat

Updates
=======

Stop Rocket.Chat:

::

 [isabell@stardust ~]$ supervisorctl stop rocket.chat
 rocket.chat: stopped
 [isabell@stardust ~]$

Remove the old installation:

::

 [isabell@stardust ~]$ rm -rf ~/rocket.chat
 [isabell@stardust ~]$

Follow the `Installation <#installation>`_ procedure to install the new release.

Start Rocket.Chat again after the installation is finished:

::

 [isabell@stardust ~]$ supervisorctl start rocket.chat
 rocket.chat: started
 [isabell@stardust ~]$

.. note:: it may take a minute or so until Rocket.Chat is fully loaded, so don't worry if you see a *502 bad gateway* for a while after starting Rocket.Chat

.. note:: Check the `Rocket.Chat releases`_ page regularly to stay informed about the newest version.


.. _Rocket.Chat: https://rocket.chat
.. _Administrator Guides: https://rocket.chat/docs/administrator-guides/
.. _Rocket.Chat releases: https://github.com/RocketChat/Rocket.Chat/releases

----

Tested with Rocket.Chat 3.7.0, Uberspace 7.7.7.0

.. author_list::
