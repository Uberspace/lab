.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>

.. tag:: spreadsheet
.. tag:: lang-node-js
.. tag:: web
.. tag:: collaborative-editing


.. sidebar:: Logo

  .. image:: _static/images/ethercalc.png
      :align: center

#########
Ethercalc
#########

.. tag_list::

EtherCalc_ is a web spreadsheet based on node-js and redis. People can edit the same document at the same time. Everybody's changes are instantly reflected on all screens. Work together on inventories, survey forms, list management, brainstorming sessions and more!

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`
  * :lab:`redis <guide_redis>`
  

License
=======

Redis is distributed under different licenses, including `Common Public Attribution License (Socialtext Inc.)`_, `Apache License 2.0 (SheetJS)`_ and `MIT License`_.

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 12:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '12'
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

We’ll also need :lab:`Redis <guide_redis>`, so follow the Redis guide and come back when it’s running.


Installation
============

Install node module
-------------------

Install the node module using the provided node packet manager `npm`: 

.. code-block:: console

 [isabell@stardust ~]$ npm install ethercalc
 [isabell@stardust ~]$

.. warning:: Make sure that you installed and configured :lab:`Redis <guide_redis>` as described in the guide before, otherwise Ethercalc will crash immediately.

Fixing Path Issue
^^^^^^^^^^^^^^^^^
.. note:: At the time of creating this guide there is an issue_ of Ethercalc trying to access the Nodemule `Socialcalc` in an outdatet directory. You **can** skip this step, but if you ran into issues i recommend to set the following symlink to fix it:

::

 [isabell@stardust ~]$ ln -s /home/isabell/node_modules /home/isabell/node_modules/ethercalc/node_modules
 [isabell@stardust ~]$
 
Make sure to replace ``isabell`` with your own username!



Configuration
=============

Setup web backend
-----------------

.. note::

    Ethercalc is running on port 8000.

.. include:: includes/web-backend.rst


Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/ethercalc.ini`` with the following content:

.. code-block:: ini

 [program:ethercalc]
 command=%(ENV_HOME)s/node_modules/ethercalc/bin/ethercalc
 environment=NODE_ENV="production"
 autorestart=true

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

 
Finishing installation
======================

Your done. Point your Browser to your installation URL ``https://isabell.uber.space`` and
start collaborating in your shiny new Ethercalc!

Generating a new Spreadsheet by pointing to the URL ``https://isabell.uber.space/_new``.


Update
======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To get the latest version of Ethercalc you can use the ``npm`` package manager:

::

 [isabell@stardusts ~]$ npm update ethercalc
 [isabell@stardusts ~]$

.. include:: includes/supervisord.rst

Restart your supervisorctl afterwards. If it's not in state RUNNING, check your configuration.

It might take a few minutes before your Ethercalc comes back online because ``npm`` re-checks and installs dependencies. You can check the service's log file using ``supervisorctl tail -f ethercalc``.


.. _issue: https://github.com/audreyt/ethercalc/issues/542
.. _Ethercalc: https://ethercalc.net/
.. _Github: https://github.com/audreyt/ethercalc
.. _feed: https://github.com/audreyt/ethercalc/releases
.. _Common Public Attribution License (Socialtext Inc.): https://github.com/audreyt/ethercalc#common-public-attribution-license-socialtext-inc
.. _Apache License 2.0 (SheetJS): https://github.com/audreyt/ethercalc#apache-license-20-sheetjs
.. _MIT License: https://github.com/audreyt/ethercalc#mit-license-john-resig-the-dojo-foundation




----

Tested with Ethercalc 0.20200306.0, Uberspace 7.5.0.0

.. author_list::

