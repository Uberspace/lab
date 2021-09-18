.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>

.. tag:: passwordmanager
.. tag:: rust
.. tag:: web


.. sidebar:: Logo

  .. image:: _static/images/vaultwarden.png
      :align: center

############
Vaultwarden
############

.. tag_list::

Bitwarden_ is an open source password manager. Your vault is encrypted with your master key, so even if your server is compromised the hacker will only get some unreadable gibberish. Hosting your own Bitwarden server can be useful if you are paranoid about the server security and want to be in full control, or want the premium features for free because you have a webspace anyway.

.. note :: The installation of the official `bitwarden server repository`_ via docker is heavy, difficult and relies on docker, which `isn't supported`_ at uberspace due to the fact of shared hosting. In this guide we'll use the Rust implementation `Vaultwarden`_ (formerly Bitwarden_rs) of the Bitwarden API, so you can still use the official clients.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`mail <mail-access>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`


License
=======

vaultwarden is released under the GNU General Public License_ version 3.

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 14:

::

 [isabell@stardust ~]$ uberspace tools version use node 14
 Selected Node.js version 14
 The new configuration is adapted immediately. Minor updates will be applied automatically.
 [isabell@stardust ~]$

If you want to use vaultwarden with your own domain you need to set up your domain first:

.. include:: includes/web-domain-list.rst


Installation
============

Install Vaultwarden
--------------------

Clone the repository into your home directory. It will create the directory ``~/vaultwarden`` automatically.


.. warning :: At the moment (current date: 12.05.2021) there is an unofficial patch of some dependencies that have not yet made it into all the official repositories. You can find the discussion about it `on GitHub <https://github.com/Uberspace/lab/issues/708>`_. Therefore you have to use the special branch `async`_ to install vaultwarden currently. Make sure to check back and update your installation, once all dependencies have been updated.


.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/dani-garcia/vaultwarden.git
 [isabell@stardust ~]$ cd vaultwarden
 [isabell@stardust vaultwarden]$ git checkout origin/async
 [isabell@stardust vaultwarden]$

In order to build vaultwarden successfully you'll need to set an environment variable pointing to the sqlite3 header files:

.. code-block:: console

 [isabell@stardust ~]$ export SQLITE3_LIB_DIR=/var/lib64

``cd`` into the automatically created folder and create the ``data`` directory:

.. code-block:: console

 [isabell@stardust ~]$ cd vaultwarden
 [isabell@stardust vaultwarden]$ mkdir data
 [isabell@stardust vaultwarden]$

Build the server executable:

.. note :: If that doesn't work the first time and the build failed, **just try again until it's done**. Further ignore compiler-warnings regarding unused imports as they sould be gone as soon as the dependencies are updated (see linked Issue above). The build process of vaultwarden can take from 10 to 25 minutes will consume almost the entire system memory. Preferably stop other running services on your uberspace temporarily to prevent running into system memory issues.

.. code-block:: console

 [isabell@stardust vaultwarden]$ cargo build -j 1 --release --features sqlite

In the next step we will download the latest build for the web vault. Check `this page`_ for the newest build number and **replace it** in the following snippet:

.. note :: If you don't want to use the web-vault feature (web-app access to your vaults) for any security reasons you can skip this step. Please note that without the web-vault, newly created users can't verify their email address. So it would be best to disable the web-vault after you've created your user accounts. Add the following line to your ``env`` file later if you do so:
  ``WEB_VAULT_ENABLED=false``

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust vaultwarden]$ wget https://github.com/dani-garcia/bw_web_builds/releases/download/v2.22.3/bw_web_v2.22.3.tar.gz
 [isabell@stardust vaultwarden]$ tar -xvzf bw_web_v2.22.3.tar.gz
 [isabell@stardust vaultwarden]$ rm -r bw_web_v*.tar.gz


Generate an ``openssl -base64`` key now and save it temporarily, you'll need it in the next step.

.. code-block:: console

 [isabell@stardust vaultwarden]$  openssl rand -base64 48
 Ig/8bZXhqVFK11F2tQZTfODO/6QpCHE3DGyCH/2Eh40xUWMFC13J6nJVPLlyU3nO

Use your favourite editor to create ``~/vaultwarden/.env`` with the following content:

.. code-block:: ini
 :emphasize-lines: 1,4,5,8,9,11

 ADMIN_TOKEN=PASTE YOUR TOKEN GENERATED ABOVE HERE
 ROCKET_PORT=62714

 SMTP_HOST=stardust.uberspace.de
 SMTP_FROM=isabell@uber.space
 SMTP_PORT=587
 SMTP_SSL=true
 SMTP_USERNAME=isabell@uber.space
 SMTP_PASSWORD=MySuperSecretPassword

 DOMAIN=https://isabell.uber.space

Replace the mail placeholder variables with your valid IMAP credentials, otherwise the Vaultwarden server will not be able to send you mail notifications or tokens to verify newly created user accounts.
``SMTP_USERNAME`` and ``SMTP_PASSWORD`` must be the login data from a valid mail account. Replace the server domain with your final URL.

.. note :: You can configure any type of service here, you're not limited to an uberspace IMAP user. If you prefer e.g. gmail refer to their documentations for ``SMTP_Port`` etc. accordingly.

You can edit other options, look into .env.template to see a list of available options.


Configuration
=============

Setup web backend
-----------------

.. note:: Enter the port ``62714`` as configured in the ``env`` file before.

If you want to use a subdomain refer to the :manual:`web-backend manual <web-backends>`.

.. include:: includes/web-backend.rst

Setup web vault
---------------

Now it's time to test if everything works. If there is no error, you are good to go. You should be able to access your vault on ``https://isabell.uber.space``

.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden
 [isabell@stardust vaultwarden]$ ./target/release/vaultwarden
 /--------------------------------------------------------------------\
 |                       Starting Vaultwarden                         |
 |                  Version 1.21.0-436d8860 (HEAD)                    |
 |--------------------------------------------------------------------|
 | This is an *unofficial* Bitwarden implementation, DO NOT use the   |
 | official channels to report bugs/features, regardless of client.   |
 | Send usage/configuration questions or feature requests to:         |
 |   https://vaultwarden.discourse.group/                             |
 | Report suspected bugs/issues in the software itself at:            |
 |   https://github.com/dani-garcia/vaultwarden/issues/new            |
 \--------------------------------------------------------------------/

 [2021-09-08 13:37:42][start][INFO] Rocket has launched from http://0.0.0.0:62714

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/vaultwarden.ini`` with the following content:

.. code-block:: ini

 [program:vaultwarden]
 directory=%(ENV_HOME)s/vaultwarden
 command=%(ENV_HOME)s/vaultwarden/target/release/vaultwarden
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.


Finishing installation
======================

Your done. Point your Browser to your installation URL ``https://isabell.uber.space`` and create your user. You can access the admin panel via ``https://isabell.uber.space/admin`` and log in using the openssl token you created during the installation process.

Best practices
==============

Backing up your vault manually
------------------------------

You can create a backup of the database manually. ``cd`` to your project folder, create a folder to store the backup in and use the given sqlite3 backup command. This will ensure the database does not become corrupted if the backup happens during a database write.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden/data
 [isabell@stardust data]$ mkdir db-backup
 [isabell@stardust data]$ sqlite3 ~/vaultwarden/data/db.sqlite3 ".backup '$HOME/vaultwarden/data/db-backup/backup.sqlite3'"

.. note ::  You could run this command through a CRON job everyday - note that it will overwrite the same backup.sqlite3 file each time. If you want to save every version of the backup, please read further.

Alternatively, you can do the backup with a timestamp and it can be useful if you don't want that the CRON job overwrites the backup file. ``$(date +%Y-%m-%d)`` in the file name in the following command will generate a name with current year, month and day.

.. code-block:: console

 [isabell@stardust data]$ sqlite3 ~/vaultwarden/data/db.sqlite3 ".backup '$HOME/vaultwarden/data/db-backup/$(date +%Y-%m-%d).sqlite3'"

Restore up your vault manually
------------------------------

Before you restore a database backup make sure to stop the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl stop vaultwarden

To restore your database simply overwrite ``db.sqlite3`` with ``backup.sqlite3`` or the one with a specific timestamp. After replacing the file successfully you can restart the service again.

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl restart vaultwarden

Hardening
---------

Disable registration and invitations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, bitwarden_rs allows any anonymous user to register new accounts on the server without first being invited. **This is necessary to create your first user on the server**, but it's recommended to disable it in the admin panel (if the admin panel is enabled) or with the environment variable to prevent attackers from creating accounts on your bitwarden_rs server.

Use your favourite editor to edit ``~/vaultwarden/.env`` and add the following content:

.. code-block:: ini

 SIGNUPS_ALLOWED=false

.. note :: While through this setting users can't register on their own, they can still be invited by already registered users to create accounts on the server and join their organizations. This does not pose an immediate risk (as long as you trust your users), but it can be disabled in the admin panel or with the following environment variable:

.. code-block:: ini

 INVITATIONS_ALLOWED=false

In addition to ``SIGNUPS_ALLOWED=false`` you can create an except for specific domains. Make sure to sue this setting only in addition to ``SIGNUPS_ALLOWED=false``!

.. code-block:: ini

 SIGNUPS_DOMAINS_WHITELIST=example.com # single domain
 SIGNUPS_DOMAINS_WHITELIST=example.com,example.net,example.org # multiple domains

.. warning ::  be careful using this feature. `At the moment`_ the emails are currently not checked, meaning that anyone could still register, by providing a fake email address that has the proper domain. So at the moment this is more security by obscurity. This seems to be fixed in an upcoming release, so make sure to check the feed_ regularly to stay informed about the newest version.

Disable password hint display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

bitwarden_rs displays password hints on the login page to accommodate small/local deployments that do not have SMTP configured, which could be abused by an attacker to facilitate password-guessing attacks against users on the server. This can be disabled in the admin panel by unchecking the ``Show password hints option`` or with the environment variable:

Use your favourite editor to edit ``~/vaultwarden/.env`` and add the the following content:

.. code-block:: ini

 SHOW_PASSWORD_HINT=false

Update
======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Updating bitwarden_rs is really easy. Just stop the server, pull everything and download the new web vault, build the executable and start the server again. To get the download link for the newest version of the web-vault look here web-vault-feed_.


.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden
 [isabell@stardust bitwarden_rs]$ supervisorctl stop vaultwarden
 [isabell@stardust bitwarden_rs]$ git pull
 [isabell@stardust bitwarden_rs]$ mv web-vault web-vault.old && mkdir web-vault
 [isabell@stardust bitwarden_rs]$ wget new-release.tar.gz
 [isabell@stardust bitwarden_rs]$ tar -xvzf new-release.tar.gz
 [isabell@stardust bitwarden_rs]$ rm new-release.tar.gz
 [isabell@stardust bitwarden_rs]$ cargo build -j 1 --release --features sqlite
 ....
 [isabell@stardust vaultwarden]$

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration. You can check the service's log file using ``supervisorctl tail -f vaultwarden``.

Acknowledgements
================
This guide is based on the official `vaultwarden documentation`_ as well as the `bitwarden_rs guide from Tom Schneider <https://vigonotion.com/blog/install-bitwarden-rs-on-uberspace/>`_.

.. _async: https://github.com/dani-garcia/vaultwarden/tree/async
.. _At the moment: https://github.com/dani-garcia/bitwarden_rs/pull/728
.. _bitwarden server repository: https://github.com/bitwarden/server
.. _Bitwarden: https://bitwarden.com/
.. _feed: https://github.com/dani-garcia/vaultwarden/releases
.. _Github: https://github.com/dani-garcia/vaultwarden
.. _GNU General Public License: https://github.com/dani-garcia/vaultwarden/blob/master/LICENSE.txt
.. _isn't supported: https://wiki.uberspace.de/faq#docker
.. _rust toolchain: https://rustup.rs/
.. _this page: https://github.com/dani-garcia/bw_web_builds/releases
.. _vaultwarden documentation: https://github.com/dani-garcia/vaultwarden/wiki/Building-binary
.. _Vaultwarden: https://github.com/dani-garcia/vaultwarden
.. _web-vault-feed: https://github.com/dani-garcia/vaultwarden/releases/latest

----

Tested with vaultwarden 1.22.2 and Web-Vault v2.22.3, Uberspace 7.11.4

.. author_list::
