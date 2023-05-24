.. highlight:: console

.. author:: Jonathan Herper <jonathan@herper.me>

.. tag:: fediverse
.. tag:: npm
.. tag:: calendar

.. sidebar:: Logo


  .. image:: _static/images/gancio.png
      :align: center


#########
Gancio
#########

.. tag_list::

Gancio_ is a shared agenda for local communities connected to the Fediverse.
----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`Postgresql <guide_postgresql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://framagit.org/les/gancio/-/blob/master/LICENSE

Prerequisites
=============
If you want to run Gancio with postgresql instead of sqlite you need a running :lab:`Postgresql <guide_postgresql>` database server.

::

Gancio v1.6.13 is running with node 14=> and 16=<

.. code-block:: console
  :emphasize-lines:1, 7

  [isabell@stardust ~]$ uberspace tools version list node
  - 12
  - 14
  - 16
  - 18
  - 19
  [isabell@stardust ~]$ uberspace tools version use node 16
  Selected Node.js version 16
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$ 


Installation
============

We will install gancio using yarn, which makes it quite easy:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ yarn global add --network-timeout 1000000000 --silent https://gancio.org/latest.tgz


.. note:: you can ignore warnings for "unmet peer dependency" and outdated packages.


Configuration
=============



Configure Database Access
-------------------------


Postgres
^^^^^^^^

Setup a dedicated postgres user and database for gancio:

.. code-block:: console

  [isabell@stardust ~]$ createuser gancio -P
  Enter password for new role:
  Enter it again:
  [isabell@stardust ~]$ createdb \
    --encoding=UTF8 \
    --lc-collate=C \
    --lc-ctype=C \
    --owner="gancio" \
    --template=template0 \
    gancio
  [isabell@stardust ~]$

You can verify access with:

.. code-block:: console

  [isabell@stardust ~]$ psql gancio gancio



You will be asked for your database credentials at the setup process when you visit your Gancio instance for the first time. 


Setup daemon
------------

Create ``~/etc/services.d/gancio.ini`` with the following content:

.. code-block:: ini

 [program:gancio]
 command=/home/<username>/bin/gancio 
 directory=/home/<username>/
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Point the ``uberspace web backend`` on ``/`` to the listener on port 13120.

.. include:: includes/web-backend.rst

Updates
=======

.. code-block:: console
  :emphasize-lines:1, 6, 10, 11
  [isabell@stardust ~]$ yarn global remove gancio
  [1/2] Removing module gancio...
  [2/2] Regenerating lockfile and installing missing dependencies...
  success Uninstalled packages.
  Done in 12.09s.
  [isabell@stardust ~]$ yarn cache clean
  yarn cache v1.22.19
  success Cleared cache.
  Done in 12.99s.
  [isabell@stardust ~]$ yarn global add --network-timeout 1000000000 --silent https://gancio.org/latest.tgz
  [isabell@stardust ~]$ supervisorctl restart gancio
  gancio: stopped
  gancio: started

.. author_list::