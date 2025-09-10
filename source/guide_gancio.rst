.. highlight:: console

.. author:: Jonathan Herper <jonathan@herper.me>

.. tag:: fediverse
.. tag:: npm
.. tag:: calendar
.. tag:: lang-php
.. tag:: lang-nodejs

.. sidebar:: Logo


  .. image:: _static/images/gancio.png
      :align: center


######
Gancio
######

.. tag_list::

Gancio_ is a shared agenda for local communities connected to the Fediverse.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`Domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://framagit.org/les/gancio/-/blob/master/LICENSE

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Gancio v1.6.14 is running with node 14=> and 18=<.

.. code-block:: console
  :emphasize-lines: 1,7

  [isabell@stardust ~]$ uberspace tools version list node
  - 12
  - 14
  - 16
  - 18
  - 19
  [isabell@stardust ~]$ uberspace tools version use node 18
  Selected Node.js version 18
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$


Installation
============

We will install gancio using yarn:

.. code-block:: console

  [isabell@stardust ~]$ yarn global add --network-timeout 1000000000 --silent https://gancio.org/latest.tgz

.. note:: you can ignore warnings for "unmet peer dependency" and outdated packages.

Create a database for the application:

::

 [isabell@stardust html]$ mysql -e "CREATE DATABASE ${USER}_ganico"
 [isabell@stardust html]$

Configuration
=============


You will be asked for your database credentials at the setup process when you visit your Gancio instance for the first time.


Setup daemon
------------

Create ``~/etc/services.d/gancio.ini`` with the following content:

.. code-block:: ini

 [program:gancio]
 command=%(ENV_HOME)s/bin/gancio
 directory=%(ENV_HOME)s
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Point the ``uberspace web backend`` on ``/`` to the listener on port 13120.

.. include:: includes/web-backend.rst


Problems after updating to gancio 1.27.0
----------------------------------------

.. note:: After updating to gancio 1.27.0, in the web-admin-interface, you may encounter the error ``Cannot reach myself from the server! Please check that proxy, firewall and network are correctly configured.``

You can solve that by setting your IP address in your ``config.json``.

First, get your :manual_anchor:`Uberspace IP address <background-network.html#uberspace-ip-addresses>`:

.. code-block:: console

 [isabell@stardust ~]$ ip addr | grep $USER
 61: veth_isabell@if62: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
     inet 100.64.118.2/30 scope global veth_isabell
 [isabell@stardust ~]$

In this case, it's ``100.64.118.2``, but make sure to use your own. Use your favourite editor to edit ``~/config.json`` and set the IP address as ``server`` in the ``host`` block.

 .. code-block:: JSON
   :emphasize-lines: 5

   {
    "baseurl": "",  
    "hostname": "",  
    "server": {
      "host": "100.64.118.2",
      "port": 13120
   },

After that, restart gancio:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl restart gancio
 gancio: stopped
 gancio: started


Updates
=======

.. code-block:: console
  :emphasize-lines: 1,6,10,11

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

.. _Gancio: https://gancio.org

----

Tested with Gancio 1.27.0 and Uberspace 7.15.4.0

.. author_list::
