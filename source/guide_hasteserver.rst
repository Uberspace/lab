.. author:: tobimori <tobias@moeritz.cc>

.. tag:: lang-nodejs
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/haste.png
      :align: center

#####
Haste
#####

.. tag_list::

Haste_  is an open-source pastebin software written in :manual:`Node.js <lang-nodejs>`, which is easily installable in any network. It can be backed by either redis or filesystem, and has a very easy adapter interface for other stores. A publicly available version can be found at hastebin.com_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

haste-server_ is released under the `MIT License`_.

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` version 12, but others should work too:

::

  [isabell@stardust ~]$ uberspace tools version use node 12
  Selected Node.js version 12
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$

Setup your URL:

.. include:: includes/web-domain-list.rst

Installation
============

First clone the GitHub_ repository:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/seejohnrun/haste-server ~/haste
  Cloning into '/home/isabell/haste'...
  remote: Enumerating objects: 9, done.
  remote: Counting objects: 100% (9/9), done.
  remote: Compressing objects: 100% (9/9), done.
  remote: Total 2069 (delta 3), reused 0 (delta 0), pack-reused 2060
  Receiving objects: 100% (2069/2069), 1.38 MiB | 2.98 MiB/s, done.
  Resolving deltas: 100% (760/760), done.
  [isabell@stardust ~]$


Then install the dependencies with ``npm install``:

.. code-block:: console

  [isabell@stardust ~]$ cd haste/
  [isabell@stardust haste]$ npm install
  added 77 packages from 355 contributors and audited 94 packages in 4.674s
  [isabell@stardust ~]$


Configuration
=============

Storage
-------

haste-server_ currently supports six storage solutions, of which File, Redis and Postgres are supported by Uberspace. The File backend is the most basic option and does not require additional software, Redis and Postgres do require additional steps. With Redis and Postgres you can set the ``expire`` option. This is off by default, but will constantly kick back expirations on each view or post.

.. note::

  Pick only one.

File
^^^^

To use file storage change the storage section in ``config.js`` to something like:

.. code-block:: json

  {
    "type": "file",
    "path": "./data"
  }

where ``path`` represents where you want the files stored.

Redis
^^^^^

To use redis storage you must setup redis as specified :lab:`here <guide_redis>`, then install the ``redis`` package in npm with ``npm install redis``:

.. code-block:: console

  [isabell@stardust ~]$ npm install redis
  [...]
  + redis@3.0.2
  added 5 packages from 7 contributors and audited 6 packages in 1.312s
  [isabell@stardust ~]$

Make sure to also change the port in ``~/.redis/conf`` to something accessible, like ``6379`` and restart redis.

Once you've done that, your config section should look like:

.. code-block:: json

  {
    "type": "redis",
    "host": "localhost",
    "port": 6379,
    "db": 0
  }

If your Redis server is configured for password authentication, use the ``password`` field.

Postgres
^^^^^^^^

To use postgres storage you must setup postgres as specified :lab:`here <guide_postgresql>`, then install the ``pg`` package in npm with ``npm install pg``:

.. code-block:: console

  [isabell@stardust ~]$ npm install pg
  [...]
  + pg@8.0.3
  added 17 packages from 9 contributors and audited 28 packages in 1.56s
  [isabell@stardust ~]$

Once you've done that, create a new user for haste-server_ and set a password.

.. code-block:: console

  [isabell@stardust ~]$ createuser haste -P
  Enter password for new role:
  Enter it again:
  [isabell@stardust ~]$

After that, create a database owned by the created user.

.. code-block:: console

  [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=haste --template=template0 haste
  [isabell@stardust ~]$

You will have to manually add a table to your postgres database:

.. code-block:: console

  [isabell@stardust ~]$ pqsl haste haste
  Password for user haste:
  psql (9.6.17)
  Type "help" for help.

  haste=> create table entries (id serial primary key, key varchar(255) not null, value text not null, expiration int, unique(key));
  CREATE table
  haste=> \q
  [isabell@stardust ~]$

Once you've done that, your config section should look like:

.. code-block:: json

  {
    "type": "postgres",
    "connectionUrl": "postgres://haste:password@localhost:5432/haste"
  }

Replace ``password`` with the password of user haste.

For other configuration options, check the README_ file of haste-server_.

Configure web server
--------------------

.. note::

    haste-server_ is running on port 7777 in the default configuration.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/haste-server.ini`` with the following content:

.. code-block:: ini

  [program:haste-server]
  directory=%(ENV_HOME)s/haste/
  command=npm start
  autorestart=true

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.

Updates
=======

If there is a new version available, you can get the code using git:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/haste
  [isabell@stardust haste]$ git pull origin
  From https://github.com/seejohnrun/haste-server
  Updating b8b2e4bc..96ac381a
  […]
  [isabell@stardust ~]$

Then you need to restart the service daemon, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart haste-server
  haste-server: stopped
  haste-server: started
  [isabell@stardust ~]$

It might take a few minutes before Haste server comes back online because ``npm`` re-checks and installs dependencies. You can check the service's log file using ``supervisorctl tail -f haste-server``.

.. _Haste: https://github.com/seejohnrun/haste-server
.. _haste-server: https://github.com/seejohnrun/haste-server
.. _hastebin.com: https://hastebin.com
.. _GitHub: https://github.com/seejohnrun/haste-server
.. _README: https://github.com/seejohnrun/haste-server/blob/master/README.md
.. _MIT License: https://github.com/seejohnrun/haste-server/blob/master/README.md#license

----

Tested on Uberspace 7.5.1. with haste-server and

* File storage
* :lab:`Redis 5.0.8 <guide_redis>`
* :lab:`PostgreSQL 9.6.17 <guide_postgres>`

.. author_list::
