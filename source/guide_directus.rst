.. highlight:: console

.. author:: j3n57h0m45 <https://github.com/j3n57h0m45>


.. tag:: self-hosting
.. tag:: database

.. sidebar:: About

  .. image:: _static/images/directus.png
        :align: center

########
Directus
########

.. tag_list::

Directus_ is a real-time API and App dashboard for managing SQL database content.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`the shell <basics-shell>`
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here in the GitHub_ repository of the project:

  * https://github.com/directus/directus/blob/main/license

Prerequisites
=============

Node and npm
------------

We're using :manual:`Node.js <lang-nodejs>`, its package manager :manual_anchor:`npm <lang-nodejs.html#npm> as well as ``npx``:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '16'
 [isabell@stardust ~]$ npm --version
 7.20.0
 [isabell@stardust ~]$ npx --version
 10.2.2
 [isabell@stardust ~]$

Installation
============

Create directory ``directus`` and sub directory ``logs``.

::

 [isabell@stardust ~]$ mkdir -p ~/directus/logs
 [isabell@stardust directus]$

.. note::

  As CentOS 7 (uberspace) only provides ``glibc 2.17``, the ``argon2`` module on needs to be manually recompiled. This will avoid the ``Error: /lib64/libc.so.6: version GLIBC_2.25``.
    
  .. code-block:: bash
    
    [isabell@stardust ~]$ cd ~/directus
    [isabell@stardust directus]$ npm install @mapbox/node-pre-gyp argon2 directus
    [isabell@stardust directus]$ npx node-pre-gyp rebuild -C ./node_modules/argon2
    [isabell@stardust directus]$


Initialize a new instance of Directus_

::

 [isabell@stardust ~]$ cd ~/directus
 [isabell@stardust directus]$ npx directus init
 ? Choose your database client
   PostgreSQL / Redshift
   MySQL / MariaDB / Aurora
 ❯ SQLite
   Microsoft SQL Server
   Oracle Database (Alpha)
 ⠹ Installing Database Driver...
 ? Choose your database client SQLite
 ? Database File Path: (/home/isabell/directus/data.db)
 Create your first admin user:
 ? Email admin@example.com
 ? Password **********
 Your project has been created at /home/isabell/directus.
 The configuration can be found in /home/isabell/directus/.env
 [isabell@stardust directus]$

Configuration
=============

Setup daemon
------------

Create ``~/etc/services.d/directus.ini`` with the following content:

.. code-block:: ini

  [program:directus]
  process_name=%(program_name)s
  directory=%(ENV_HOME)s/directus
  command=%(ENV_HOME)s/bin/npx directus start
  autostart=true
  autorestart=true
  environment=NODE_ENV=production
  startsecs=60
  stderr_logfile=%(ENV_HOME)s/logs/%(program_name)s.err.log
  stdout_logfile=%(ENV_HOME)s/logs/%(program_name)s.out.log

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to URL and log into your admin user account.

Tuning
======

See official documentation_ of the project.

Updates
=======

.. note:: 

  Check GitHub_ repository of the project regularly to stay informed about the newest version. To update an existing installation use the following commands:
    
  .. code-block:: bash

    [isabell@stardust ~]$ cd ~/directus
    [isabell@stardust directus]$ supervisorctl stop directus
    [isabell@stardust directus]$ npx ncu -u
    [isabell@stardust directus]$ npm install
    [isabell@stardust directus]$ npx node-pre-gyp rebuild -C ./node_modules/argon2
    [isabell@stardust directus]$ npx directus database migrate:latest
    [isabell@stardust directus]$ supervisorctl start directus
    [isabell@stardust directus]$


.. _Github: https://github.com/directus/directus
.. _Directus: https://github.com/directus/directus
.. _documentation: https://docs.directus.io/


----

Tested with directus v9.0.0-rc.88, Uberspace 7.11.3

.. author_list::