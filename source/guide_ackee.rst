.. author:: tobimori <tobias@moeritz.cc>
.. author:: Felix Förtsch <https://felixfoertsch.de>

.. tag:: web
.. tag:: analytics
.. tag:: lang-nodejs

.. highlight:: console

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
  ACKEE_ALLOW_ORIGIN="https://my-domain-other-than-isabell-on-stardust.de"


Web Backend Config
------------------

.. note::

    Ackee_ is running on port 3000.

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

.. include:: includes/supervisord.rst

Finishing installation
======================

Go to ``https://isabell.uber.space``. Login using the credentials defined in section `Ackee Config`. Add the domains you want to analyze in the web interface: After adding, it shows a tracking snippet you can add to these pages. If data does not show up after implementing the tracking script, remember that cross site tracking always takes extra consideration of `CORS <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_.

.. _Ackee: https://ackee.electerious.com/
.. _MongoDB: https://mongodb.com
.. _MIT License: https://github.com/electerious/Ackee/blob/master/LICENSE

----

Tested on Uberspace v7.7.1.2 with NodeJS v12, Ackee v1.7.1 and MongoDB v4.2.8.

.. author_list::
