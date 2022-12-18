.. author:: tobimori <tobias@moeritz.cc>
.. author:: Felix Förtsch <https://felixfoertsch.de>

.. tag:: web
.. tag:: analytics
.. tag:: lang-nodejs

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ackee.png
      :align: center

#####
Ackee
#####

.. tag_list::

Ackee_ is a self-hosted open-source web analytics tool built with :manual:`Node.js <lang-nodejs>`.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :manual:`Domains <web-domains>`

License
=======

Ackee_ is released under the `MIT License`_.

Prerequisites
=============

Ackee_ requires a MongoDB_ database. Set it up using the :lab:`MongoDB Uberlab guide <guide_mongodb>`. You will need your MongoDB_ admin name and password later.

Starting with `Version 2.0.0`_, Ackee also requires the use of :manual:`Node.js <lang-nodejs>` 14.

::

 [isabell@stardust ~]$ uberspace tools version use node 14
 Using 'Node.js' version: '14'
 Selected node version 14
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Set up your domain:

.. include:: includes/web-domain-list.rst

Installation
============

Install ``yarn`` globally:

.. code-block:: console

  [isabell@stardust ~]$ npm install yarn -g
  [isabell@stardust ~]$

Clone the `GitHub repository <https://github.com/electerious/Ackee>`_ and install the dependencies:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/electerious/Ackee
  [isabell@stardust ~]$ cd Ackee
  [isabell@stardust Ackee]$ yarn

Configuration
=============

Ackee Config
------------

Create a new, empty ``.env`` file in the root of the Ackee_ directory. Add the following content, replacing the placeholders. The environment variables ``ACKEE_USERNAME`` and ``ACKEE_PASSWORD`` define the credentials to log into the web interface. If you want to use Ackee_ to analyze a domain other than ``isabell.uber.space``, you have to add it under ``ACKEE_ALLOW_ORIGIN`` (read more about the CORS headers `in the Ackee documentation <https://github.com/electerious/Ackee/blob/master/docs/CORS%20headers.md>`_).

.. code-block:: console

  ACKEE_MONGODB=mongodb://<admin>_mongoroot:<password>@localhost:27017/admin
  ACKEE_USERNAME=<ackee_username>
  ACKEE_PASSWORD=<ackee_password>
  ACKEE_ALLOW_ORIGIN="https://isabell.uber.space"

.. note :: If you want to allow multiple sites, you can add them to   ``ACKEE_ALLOW_ORIGIN`` separated by a comma (e.g. ``ACKEE_ALLOW_ORIGIN="https://isabell.uber.space,https://my-other-domain.de"``).


Web Backend Config
------------------

.. note:: Ackee_ is running on port 3000.

.. include:: includes/web-backend.rst

Supervisord Daemon Setup
------------------------

Create ``~/etc/services.d/ackee.ini`` with the following content:

.. code-block:: ini

  [program:ackee]
  directory=%(ENV_HOME)s/Ackee
  command=yarn start
  autostart=yes
  autorestart=yes
  startsecs=30

.. include:: includes/supervisord.rst

Set a link to the log file destination so you can more easily access the logs:

.. code-block:: console

  [isabell@stardust html]$ ln --symbolic ~/.npm/_logs/ ~/logs/npm/
  [isabell@stardust html]$

Finishing installation
======================

Go to ``https://isabell.uber.space``. Login using the credentials defined in section `Ackee Config`. Add the domains you want to analyze in the web interface: After adding, it shows a tracking snippet you can add to these pages. If data does not show up after implementing the tracking script, remember that cross site tracking always takes extra consideration of `CORS <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_.

Updates
=======

Update by running ``git pull`` in Ackee's directory, updating its dependencies with ``yarn`` and restarting the service with ``supervisorctl restart ackee``.

.. _Ackee: https://ackee.electerious.com/
.. _MongoDB: https://mongodb.com
.. _Version 2.0.0: https://github.com/electerious/Ackee/releases/tag/v2.0.0
.. _MIT License: https://github.com/electerious/Ackee/blob/master/LICENSE

----

Tested on Uberspace v7.11.1.1 with NodeJS v14, Ackee v3.0.6 and MongoDB v4.4.

.. author_list::
