.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: documentation

.. sidebar:: Logo

  .. image:: _static/images/docusaurus.svg
      :align: center

##########
Docusaurus
##########

.. tag_list::

.. abstract::
  Docusaurus_ makes it easy to maintain Open Source documentation websites.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Node and npm
------------

We're using :manual:`Node.js <lang-nodejs>` in the latest version:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '12'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We create the application directory and install the latest version. The website is created with ``docusaurus-init``.

.. code-block:: console

 [isabell@stardust ~]$ mkdir docusaurus
 [isabell@stardust ~]$ cd docusaurus
 [isabell@stardust docusaurus]$ npm install --global docusaurus-init
 (...)
 [isabell@stardust docusaurus]$ docusaurus-init
 (...)
 [isabell@stardust docusaurus]$

Setup daemon
------------

Create ``~/etc/services.d/docusaurus.ini`` with the following content:

.. code-block:: ini

 [program:docusaurus]
 directory=%(ENV_HOME)s/docusaurus/website
 command=npm start
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Configure web server
--------------------

.. note::

    Docusaurus is running on port 3000.

.. include:: includes/web-backend.rst

Updates
-------

.. note:: Check the update feed_ regularly to stay informed about the newest version.

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl stop docusaurus
 [isabell@stardust ~]$ cd docusaurus
 [isabell@stardust docusaurus]$ npm update docusaurus
 [isabell@stardust docusaurus]$ supervisorctl start docusaurus
 [isabell@stardust docusaurus]$

.. _Docusaurus: https://docusaurus.io/
.. _feed: https://github.com/facebook/docusaurus/releases

----

Tested with Docusaurus 1.14.4 and Uberspace 7.6.12

.. author_list::
