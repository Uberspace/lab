.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/passbolt.png
      :align: center

#########
Passbolt
#########

.. tag_list::

Passbolt_

The password manager your team was waiting for. Free, open source, self-hosted, extensible, OpenPGP based.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

Passbolt is released under the `AGPL-3.0 license`_.

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2. Since new Uberspaces are currently setup with PHP 7.1 by default you need to set this version manually:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Create the database:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_passbolt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
 [isabell@stardust ~]$

Installation
============

To install Passbolt we clone the current version using Git. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will under your ``html``.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ git clone https://github.com/passbolt/passbolt_api.git .
 Cloning into '.'...
 (...)
 [isabell@stardust ~]$

Configuration
=============

Generate an OpenPGP key:

.. warning:: Do not set a passphrase or an expiration date.

Save your fingerprint and replace ``SERVER_KEY@EMAIL.TEST`` with your email.

.. code-block:: console
 :emphasize-lines: 2,3,4

 [isabell@stardust ~]$ gpg --gen-key
 [isabell@stardust ~]$ gpg --list-keys --fingerprint
 [isabell@stardust ~]$ gpg --armor --export-secret-keys SERVER_KEY@EMAIL.TEST > /var/www/virtual/$USER/html/config/gpg/serverkey_private.asc
 [isabell@stardust ~]$ gpg --armor --export SERVER_KEY@EMAIL.TEST > /var/www/virtual/$USER/html/config/gpg/serverkey.asc
 [isabell@stardust ~]$

Install the dependencies:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ composer install --no-dev
 [isabell@stardust html]$ cp config/passbolt.default.php config/passbolt.php
 [isabell@stardust html]$

Edit following settings in ``config/passbolt.php``:
 * ``fullBaseUrl`` in ``App``: ``https://isabell.uber.space``
 * ``username``, ``password`` and ``database`` in ``Datasources``: :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * ``username`` and ``password in ``EmailTransport``
 * ``fingerprint`` in ``passbolt - gpg - serverKey``: Insert your gpg fingerprint without spaces (!)
 * Uncomment public and private path under fingerprint

Finish the installation and fill in your email and name when asked for:

::

 [isabell@stardust html]$ ./bin/cake passbolt healthcheck
 (...)
 No error found. Nice one sparky!
 [isabell@stardust html]$ ./bin/cake passbolt install
 [isabell@stardust html]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Passbolt's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation. The update process varies between patch, minor or major update. You can easily follow the instructions in the Passbolt`s `update documentation`_.


.. _Passbolt: https://www.passbolt.com/
.. _feed: https://github.com/passbolt/passbolt_api/releases.atom
.. _AGPL-3.0 license: https://opensource.org/licenses/agpl-3.0
.. _stable releases: https://github.com/passbolt/passbolt_api/releases
.. _update documentation: https://help.passbolt.com/hosting/update

----

Tested with Passbolt 2.12.0 and Uberspace 7.4

.. author_list::
