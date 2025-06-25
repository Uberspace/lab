.. highlight:: console
.. author:: Doug Webb <https://dougwebb.site>

.. tag:: lang-php
.. tag:: web
.. tag:: wiki
.. tag:: collaborative-editing
.. tag:: groupware
.. tag:: photo-management
.. tag:: file-storage

.. sidebar:: Logo

  .. image:: _static/images/mediawiki.png
      :align: center

#########
MediaWiki
#########

.. tag_list::

MediaWiki_ is the wiki platform behind Wikipedia. It helps you collect and organise knowledge and make it available to people. It's powerful, multilingual, free and open, extensible, customisable, reliable, and free of charge.

Last update: 2024-05-05

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

.. warning:: The setup described in this guide has an unresolved issue with the DiscussionTools extension. The issue is tracked on `Uberspace Github <https://github.com/Uberspace/lab/issues/1845>`_ and previously on `MediaWiki Phabricator <https://phabricator.wikimedia.org/T380885>`_.

License
=======

MediaWiki_ is free software; you can redistribute it and/or modify it under the terms of the `GNU General Public License <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_ as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Copyright 2001 - 2024. A list of authors can be found `here <https://gerrit.wikimedia.org/g/mediawiki/core/%2B/HEAD/CREDITS>`_.

Extensions and skins may be released under different licenses than MediaWiki itself. Most of them are usually distributed with a copy of their respective licenses and copyright notices.

Prerequisites
=============

Uberspace satisfies or exceeds all MediaWiki `requirements <https://www.mediawiki.org/wiki/Manual:Installation_requirements>`_ out of the box.

.. note:: Uberspace only supports PHP 8.x, however the main MediaWiki documentation `notes <https://www.mediawiki.org/wiki/Manual:Installation_requirements#PHP>`_: *"PHP 8 is not in use by Wikimedia wikis, and thus gets less testing, but other groups do use MediaWiki with PHP 8 without issue. If you encounter any bugs when using MediaWiki with PHP 8, please report them."*

Set up a new database for MediaWiki:

.. code-block:: console

  [isabell@stardust ~]$ mariadb -e "CREATE DATABASE ${USER}_mediawiki"
  [isabell@stardust ~]$

Your MediaWiki domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Official, generalist installation manual for Mediawiki: `https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki <https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki>`_

Change into your :manual:`document root <web-documentroot>`, download the latest MediaWiki release found at `https://www.mediawiki.org/wiki/Download <https://www.mediawiki.org/wiki/Download>`_ (here 1.41.1) and extract.

.. code-block:: console

  [isabell@stardust ~]$ cd html
  [isabell@stardust html]$ wget https://releases.wikimedia.org/mediawiki/1.41/mediawiki-1.41.1.tar.gz
  [isabell@stardust html]$ tar -xzvf mediawiki-*.tar.gz --strip-components=1
  [isabell@stardust html]$ rm mediawiki-*.tar.gz

At this point, the wiki installer should be available at ``https://<UberspaceUsername>.uber.space/``, click *"complete the installation"* to start the graphical `configuration <https://www.mediawiki.org/wiki/Manual:Config_script>`_. Leave default values or change as desired. On the "Connect to database" page:

* Database name: ``<UberspaceUsername>_mediawiki``
* Database username: ``<UberspaceUsername>``
* Database password: find out using ``my_print_defaults client``

When the graphical installation completes, locally download the ``LocalSettings.php`` that should have been automatically generated and transfer it to ``~/html`` on your Uberspace. This can be achieved using one of the tools suggested on :manual:`SFTP <basics-SFTP>` with host ``sftp://<UberspaceUsername>.uber.space`` and your Uberspace credentials.

After this, the installed wiki should be available under ``https://<UberspaceUsername>.uber.space``

----

Tested with MediaWiki 1.41.1, PHP 8.3.6 and Uberspace 7.15.14.1

.. author_list::
