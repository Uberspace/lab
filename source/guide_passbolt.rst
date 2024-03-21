.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>, Andreas Fuchs <https://anfuchs.de/>

.. tag:: lang-php
.. tag:: web
.. tag:: password-manager

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

We’re using :manual:`PHP <lang-php>` in the stable version 8.1. 

::

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Create the database:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_passbolt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
 [isabell@stardust ~]$


Create an email user:

::

 [isabell@stardust ~]$ uberspace mail user add passbolt
 Enter a password for the mailbox: (...)
 Please confirm your password: (...)
 New mailbox created for user: 'passbolt', it will be live in a few minutes...
 [isabell@stardust ~]$

Installation
============

To install Passbolt we clone the current version using Git. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will be under your ``html``.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ git clone https://github.com/passbolt/passbolt_api.git .
 Cloning into '.'...
 (...)
 [isabell@stardust ~]$

Configuration
=============

Generate your OpenPGP key using headless mode. Add a gpg_batch.conf.

::

 [isabell@stardust ~]$ nano gpg_batch.conf

Copy following content to ``gpg_batch.conf`` and replace ``YOUR_NAME``, ``YOUR_COMMENT`` and ``SERVER_KEY@EMAIL.TEST`` with your mail:

::

 %echo Generating a GPG key
 Key-Type: RSA
 Key-Length: 3072
 Key-Usage: sign
 Subkey-Type: RSA
 Subkey-Length: 3072
 Subkey-Usage: encrypt
 Name-Real: YOUR_NAME
 Name-Comment: YOUR_COMMENT
 Name-Email: SERVER_KEY@EMAIL.TEST
 Expire-Date: 0
 %commit
 %echo done

::

Save your fingerprint and replace ``SERVER_KEY@EMAIL.TEST`` with your email. ``gpg --batch --gen-key gpg_batch.conf`` will run for multiple minutes. Just wait until it's finished!

::

 [isabell@stardust ~]$ mkdir -p ~/passbolt/config
 [isabell@stardust ~]$ gpg --batch --gen-key gpg_batch.conf
 [isabell@stardust ~]$ gpg --list-keys --fingerprint
 [isabell@stardust ~]$ gpg --armor --export-secret-keys SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey_private.asc
 [isabell@stardust ~]$ gpg --armor --export SERVER_KEY@EMAIL.TEST > ~/passbolt/config/serverkey.asc
 [isabell@stardust ~]$

Install the dependencies:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ wget --output-document=composer.phar https://getcomposer.org/composer-1.phar
 [isabell@stardust html]$ php composer.phar install --no-dev
 [isabell@stardust html]$ rm composer.phar
 [isabell@stardust html]$ cp config/passbolt.default.php config/passbolt.php
 [isabell@stardust html]$

Edit following settings in ``config/passbolt.php``:
 * ``fullBaseUrl`` : ``https://isabell.uber.space`` in ``App``
 * ``username``, ``password`` and ``database`` in ``Datasources.default``: :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * ``host`` : ``stardust.uberspace.de``, ``port`` : ``587``, ``tls`` : ``true``, ``username`` : ``isabell`` and ``password`` in ``EmailTransport.default``
 * ``from`` : ``['passbolt@isabell.uber.space' => 'Passbolt']`` in ``Email.default``
 * ``fingerprint`` in ``passbolt.gpg.serverKey``: Insert your gpg fingerprint without spaces (!)
 * ``public`` : ``/home/isabell/passbolt/config/serverkey.asc`` in ``passbolt.gpg.serverKey``
 * ``private`` : ``/home/isabell/passbolt/config/serverkey_private.asc`` in ``passbolt.gpg.serverKey``
 * optional add ``ssl.force`` : ``true`` in ``passbolt``


Finish the installation and fill in your email and name when asked for:

::

 [isabell@stardust html]$ ./bin/cake passbolt install
 [isabell@stardust html]$ ./bin/cake passbolt healthcheck
 (...)
 No error found. Nice one sparky!
 [isabell@stardust html]$

Finally, configure a cronjob so mails get sent automatically: Add the following
line to your crontab using the ``crontab -e`` command:

::

 * * * * * /home/$USER/html/bin/cake EmailQueue.sender >> ~/logs/passbolt_mails.log

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

Tested with Passbolt 4.5.2 and Uberspace 7.15.10

.. author_list::
