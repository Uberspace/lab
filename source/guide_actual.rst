.. author:: knhash <https://knhash.in>

.. tag:: accounting
.. tag:: personal-finance
.. tag:: web

.. sidebar:: Logo

    .. image:: _static/images/actual.png
      :align: center

.. highlight:: console

######
Actual
######

.. error::

  This guide seems to be **broken** for the current versions of Actual, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1891

.. tag_list::

`Actual Budget`_ is a super fast and privacy-focused app for managing your finances. At its heart is the well proven and much loved Envelope Budgeting methodology. It features multi-device sync, and optional end-to-end encryption.

You can find the source code on `Git Hub`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`the shell <basics-shell>`
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============
Your website domain or subdomain needs to be setup up:

.. include:: includes/web-domain-list.rst


Installation
============

This installation broadly follows the `Quick Start Guide`_.

First you need to clone the Actual Server project to your Uberspace account, you can do this using Git.

::

  [isabell@stardust ~]$ git clone https://github.com/actualbudget/actual-server.git
  Cloning into 'actual-server'...
  [isabell@stardust ~]$

Now navigate to the directory where you cloned the project.

::

  [isabell@stardust ~]$ cd actual-server
  [isabell@stardust actual]$

By default, current versions of Actual depend on a cryptography library called bcrypt in version 5.1.1 or later.
This versions is not compatible with Uberspace v7 and needs to be downgraded to 5.1.0.
To do so, open `package.json` in your favorite editor and replace

.. code-block:: json

  "bcrypt": "^5.1.1",

by

.. code-block:: json

  "bcrypt": "5.1.0",

in the `dependencies` section.

Install all the dependencies using `yarn`.
Be sure to pass the option `--refresh-lockfile`,
so that the changes to `packages.json` are taken into account.

::

  [isabell@stardust actual]$ yarn install --refresh-lockfile
  […]
  ➤ YN0000: └ Completed in 1m 50s
  ➤ YN0000: · Done with warnings in 2m 2s
  [isabell@stardust actual]$

Configuration
=============

Setup daemon
------------
Create ``~/etc/services.d/actual.ini`` with the following content:

.. code-block:: ini

  [program:actual]
  directory=%(ENV_HOME)s/actual-server
  command=yarn start
  autostart=true
  autorestart=true
  stopsignal=INT
  startsecs=30

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::

    Actual is running on port ``5006``.

.. include:: includes/web-backend.rst


Updates
=======

When a new Actual release is published, follow these steps to update:

1. Stop the server if it's running using ``supervisorctl stop actual``.
2. Discard the changes to `packages.json` and `yarn.lock` using ``git checkout packages.json yarn.lock``
3. Run ``git pull`` from the directory you cloned the project into. This will download the latest server code.
4. Replace the version of the bcrypt dependency as described above.
5. Run ``yarn install --refresh-lockfile`` from that same directory.
   This will download the latest web client code, along with any updated dependencies for the server.
6. Restart the server by running ``supervisorctl start actual``.

.. code-block:: bash

  [isabell@stardust ~]$ supervisorctl stop actual
  actual: stopped
  [isabell@stardust ~]$ cd ~/actual-server
  [isabell@stardust actual-server]$ git checkout packages.json yarn.lock
  […]
  [isabell@stardust actual-server]$ git pull
  remote: Enumerating objects: 4, done.
  remote: Counting objects: 100% (4/4), done.
  […]
  [apply changes to `packages.json`]
  […]
  [isabell@stardust actual-server]$ yarn install --refresh-lockfile
  […]
  [isabell@stardust actual-server]$ supervisorctl start actual
  actual: started
  [isabell@stardust actual-server]$

.. _Actual Budget: https://actualbudget.org/
.. _Git Hub:  https://github.com/actualbudget/actual-server
.. _Quick Start Guide: https://actualbudget.org/docs/install/local

----

Tested with Actual 24.10.1, Uberspace 7.16.2

.. author_list::
