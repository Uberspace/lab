.. highlight:: console
.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/antragsgruen.png
      :align: center

###########
Antragsgrün
###########

.. tag_list::

Antragsgrün_ is an open source web tool used by organisations such as the European and German Green Parties for discussing motions, amendments, and candidacies. It is written in PHP and distributed under the GPLv3 license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Use the recommended :manual:`PHP <lang-php>` version as listed in the `system requirements`_:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

Your domain should be set up:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Installation
============

Downloading
-----------

Get the link to the `latest Antragsgrün release`_ ``.tar.bz2`` release archive, then ``cd`` to your :manual:`document root <web-documentroot>`, download the archive and extract it on the fly, omitting the top-level directory from the archive:

.. code-block:: console

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ rm nocontent.html
 [isabell@stardust html]$ curl -L https://github.com/CatoTH/antragsgruen/releases/download/v4.8.1/antragsgruen-4.8.1.tar.bz2 | tar -xjf - --strip-components=1
   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
 100   661  100   661    0     0   2980      0 --:--:-- --:--:-- --:--:--  2990
 100 22.2M  100 22.2M    0     0  5084k      0  0:00:04  0:00:04 --:--:-- 6629k
 [isabell@stardust html]$

Setup
-----

Create the database
^^^^^^^^^^^^^^^^^^^

First, create a MySQL database to hold your Antragsgrün installation

.. code-block:: console

  [isabell@stardust html]$ mysql --verbose --execute="CREATE DATABASE ${USER}_antragsgruen"
  --------------
  CREATE DATABASE isabell_antragsgruen
  --------------
  [isabell@stardust html]$


Web installer
^^^^^^^^^^^^^

You can now head over to your ``https://USER.uber.space`` web site and complete the web installer. Use ``localhost`` as your database server, the name of database you created in the previous step (``isabell_antragsgruen`` in our example) and your personal MySQL password.

Updates
=======

Use the built-in `web updater`_.


.. _Antragsgrün: https://antragsgruen.de/
.. _`system requirements`: https://github.com/CatoTH/antragsgruen#requirements
.. _`latest Antragsgrün release`: https://github.com/CatoTH/antragsgruen/releases/latest
.. _`web updater`: https://github.com/CatoTH/antragsgruen#using-the-web-based-updater

----


Tested with Antragsgrün 4.10.1, Uberspace 7.13.0, and PHP 8.1

.. author_list::
