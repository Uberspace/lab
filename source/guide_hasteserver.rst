.. author:: tobimori <tobias@moeritz.cc>

.. tag:: lang-nodejs
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/haste.png
      :align: center

#############
Haste
#############

.. tag_list::

Haste_  is an open-source pastebin software written in :manual:`Node.js <lang-nodejs>`, which is easily installable in any network. It can be backed by either redis or filesystem, and has a very easy adapter interface for other stores. A publicly available version can be found at hastebin.com_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

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
=============

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


Configure storage
===================

`Haste server`_ currently supports six storage solutions, of which four are supported by Uberspace.

File
------

To use file storage change the storage section in ``config.js`` to something like:

.. code-block:: json

  {
    "type": "file",
    "path": "./data"
  }

where ``path`` represents where you want the files stored.

Redis
--------

To use redis storage you must setup redis as specified :lab:`here <guide_redis>`, then install the ``redis`` package in npm with ``npm install redis``.

Once you've done that, your config section should look like:

.. code-block:: json

  {
    "type": "redis",
    "host": "localhost",
    "port": 6379,
    "db": 2
  }

If your Redis server is configured for password authentification, use the ``password`` field.

Postgres
-----------

To use postgres storage you must setup postgres as specified :lab:`here <guide_postgresql>`, then install the ``pg`` package in npm with ``npm install pg``.

Once you've done that, your config section should look like:

.. code-block:: json

  {
    "type": "postgres",
    "connectionUrl": "postgres://user:password@localhost:5432/database"
  }

You can also just set the environment variable for ``DATABASE_URL`` to your database connection url.

You will have to manually add a table to your postgres database:

.. code-block:: console

  [isabell@stardust ~]$ create table entries (id serial primary key, key varchar(255) not null, value text not null, expiration int, unique(key));

Memcached
-------------

To use memcache storage you must setup Memcached as specified :lab:`here <guide_memchached>`, then install the ``memcached`` package in npm with ``npm install memcached``.

Once you've done that, your config section should look like:

.. code-block:: json

  {
    "type": "memcached",
    "host": "127.0.0.1",
    "port": 11211
  }

.. note:: 

  When using a storage solution except for the file storage, you can also set an ``expire`` option to the number of seconds to expire keys in. This is off by default, but will constantly kick back expirations on each view or post.

Configure web server
==========================

.. note::

    haste-server is running on port 7777 in the default configuration.

.. include:: includes/web-backend.rst

Setup daemon
====================

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
.. _`Haste server`: https://github.com/seejohnrun/haste-server
.. _hastebin.com: https://hastebin.com
.. _GitHub: https://github.com/seejohnrun/haste-server

----

Tested with haste-server using file storage and Uberspace 7.5.1.

.. author_list::
