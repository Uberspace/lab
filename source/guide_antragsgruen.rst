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

Unfortunately, the Antragsgrün web installer `doesn't work anymore`_ on uberspace since v4.9.1. However, you can install that version and use the built-in web updater (see below) to upgrade to the latest version.

Downloading
-----------

Download the `v4.9.1 Antragsgrün release`_ ``.tar.bz2`` archive, then ``cd`` to your :manual:`document root <web-documentroot>`, download the archive and extract it on the fly, omitting the top-level directory from the archive:

.. code-block:: console

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$ rm nocontent.html
 [isabell@stardust html]$ curl -L https://github.com/CatoTH/antragsgruen/releases/download/v4.9.1/antragsgruen-4.9.1.tar.bz2 | tar -xjf - --strip-components=1
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

Use the built-in `web updater`_. When you're applying several updates at once (e.g. because of updating from v4.9.1 to v4.12.0, via v4.10.0,  v4.10.1
 etc.), don't forget to execute the database migration after every single update step, not only once after all the file updates are completed. Otherwise you might run into database errors.


.. _Antragsgrün: https://antragsgruen.de/
.. _`system requirements`: https://github.com/CatoTH/antragsgruen#requirements
.. _`v4.9.1 Antragsgrün release`: https://github.com/CatoTH/antragsgruen/releases/tag/v4.9.1
.. _`web updater`: https://github.com/CatoTH/antragsgruen#using-the-web-based-updater
.. _`doesn't work anymore`: https://github.com/CatoTH/antragsgruen/issues/827

----


Tested with Antragsgrün 4.10.1, Uberspace 7.13.0, and PHP 8.1

.. author_list::
