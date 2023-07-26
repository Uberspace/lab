.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>
.. author:: knhash <https://knhash.in>

.. tag:: password-manager
.. tag:: rust
.. tag:: web


.. sidebar:: Logo

  .. image:: _static/images/vaultwarden.png
      :align: center

############
vaultwarden
############

.. tag_list::

Bitwarden_ is an open source password manager. Your vault is encrypted with your master key, so even if your server is compromised the hacker will only get some unreadable gibberish. Hosting your own Bitwarden server can be useful if you are paranoid about the server security and want to be in full control, or want the premium features for free because you have a webspace anyway.

.. note :: The installation of the official `bitwarden server repository`_ via docker is heavy, difficult and relies on docker, which isn't supported at Uberspace due to the fact of shared hosting. In this guide we'll use the Rust implementation `vaultwarden`_ (formerly Bitwarden_rs) of the Bitwarden API, so you can still use the official clients.

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

If you want to use vaultwarden with your own domain you need to set up your domain first:

.. include:: includes/web-domain-list.rst


Installation
============

Install vaultwarden
--------------------

We will be installing vaultwarden by extracting a standalone, statically-linked binary from the official Docker image.

Create a directory in ``/home/isabell`` for vaultwarden. In the vaultwarden directory, also create a directory to store the actual data.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/vaultwarden
 [isabell@stardust ~]$ mkdir ~/vaultwarden/data
 [isabell@stardust ~]$

Download the Docker Image Extractor.

.. code-block:: console

 [isabell@stardust ~]$ wget -O ~/vaultwarden/docker-image-extract https://raw.githubusercontent.com/jjlin/docker-image-extract/main/docker-image-extract
 [isabell@stardust ~]$

Change into the ``~/vaultwarden`` directory. Fetch and extract the binary from the appropriate image.

.. code-block:: console

  [isabell@stardust ~]$ cd ~/vaultwarden
  [isabell@stardust vaultwarden]$ chmod +x docker-image-extract
  [isabell@stardust vaultwarden]$ ./docker-image-extract vaultwarden/server:alpine
  Getting API token...
  Getting image manifest for vaultwarden/server:alpine...
  Downloading layer 8516f4cd818630cd60fa18254b072f8d9c3748bdb56f6e2527dc1c204e8e017c...
  Extracting layer...
  ...
  Image contents extracted into ./output.
  [isabell@stardust vaultwarden]$

Update default configuration
----------------------------

Use your favourite editor to create ``~/vaultwarden/.env`` with the following content:

.. code-block:: ini
 :emphasize-lines: 1,2,5,6,7

 SMTP_HOST=stardust.uberspace.de
 SMTP_FROM=isabell@uber.space
 SMTP_PORT=587
 SMTP_SECURITY=starttls
 SMTP_USERNAME=isabell@uber.space
 SMTP_PASSWORD=MySuperSecretPassword
 DOMAIN=https://isabell.uber.space
 ROCKET_ADDRESS=0.0.0.0
 ROCKET_PORT=8000

Replace the mail placeholder variables with your valid SMTP credentials, otherwise the vaultwarden server will not be able to send you mail notifications or tokens to verify newly created user accounts.
``SMTP_USERNAME`` and ``SMTP_PASSWORD`` must be the login data from a valid mail account. Replace the server domain with your final URL.

.. note :: You can configure any type of service here, you're not limited to an uberspace SMTP user. If you prefer e.g. gmail refer to their documentations for ``SMTP_PORT`` etc. accordingly.

You can edit other options, look into `.env.template <https://github.com/dani-garcia/vaultwarden/blob/main/.env.template>`_ to see a list of available options.


Configuration
=============

Setup web backend
-----------------

.. note::
    vaultwarden will run on port 8000 (you can change this in the ``.env`` config file).

.. include:: includes/web-backend.rst

If you want to use a subdomain refer to the :manual:`web-backend manual <web-backends>`.

Setup web vault
---------------

Now it's time to test if everything works.

.. note :: Setting both ``ENV_FILE`` and ``DATA_FOLDER`` as temporary environment variables is necessary for vaultwarden to find the correct config and data directory.

.. code-block:: console

 [isabell@stardust ~]$ export ENV_FILE=$HOME/vaultwarden/.env
 [isabell@stardust ~]$ export DATA_FOLDER=$HOME/vaultwarden/data
 [isabell@stardust ~]$ cd ~/vaultwarden/output
 [isabell@stardust output]$ ./vaultwarden
 /--------------------------------------------------------------------\
 |                       Starting Vaultwarden                         |
 |                          Version 1.23.1                            |
 |--------------------------------------------------------------------|
 | This is an *unofficial* Bitwarden implementation, DO NOT use the   |
 | official channels to report bugs/features, regardless of client.   |
 | Send usage/configuration questions or feature requests to:         |
 |   https://vaultwarden.discourse.group/                             |
 | Report suspected bugs/issues in the software itself at:            |
 |   https://github.com/dani-garcia/vaultwarden/issues/new            |
 \--------------------------------------------------------------------/
 Running migration 20180711181453
 Running migration 20180827172114
 ...
 [2021-12-29 10:40:35.407][start][INFO] Rocket has launched from http://0.0.0.0:8000

If there is no error, you are good to go. You should be able to access your vault on ``https://isabell.uber.space``

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/vaultwarden.ini`` with the following content:

.. code-block:: ini

  [program:vaultwarden]
  directory=%(ENV_HOME)s/vaultwarden/output/
  command=%(ENV_HOME)s/vaultwarden/output/vaultwarden
  autostart=yes
  autorestart=yes
  startsecs=60
  environment=ENV_FILE="%(ENV_HOME)s/vaultwarden/.env",DATA_FOLDER="%(ENV_HOME)s/vaultwarden/data"

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration. You can check the service's log file using ``supervisorctl tail -f vaultwarden``.



Finishing installation
======================

You are done. Point your Browser to your installation URL ``https://isabell.uber.space`` and create your user.

Best practices
==============

Backing up your vault manually
------------------------------

You can create a backup of the database manually. ``cd`` to your project folder, create a folder to store the backup in and use the given sqlite3 backup command. This will ensure the database does not become corrupted if the backup happens during a database write.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/vaultwarden/data/db-backup
 [isabell@stardust ~]$ sqlite3 ~/vaultwarden/data/db.sqlite3 ".backup '$HOME/vaultwarden/data/db-backup/backup.sqlite3'"

.. note ::  You could run this command through a CRON job everyday - note that it will overwrite the same backup.sqlite3 file each time. If you want to save every version of the backup, please read further.

Alternatively, you can do the backup with a timestamp and it can be useful if you don't want that the CRON job overwrites the backup file. ``$(date +%Y-%m-%d)`` in the file name in the following command will generate a name with current year, month and day.

.. code-block:: console

 [isabell@stardust ~]$ sqlite3 ~/vaultwarden/data/db.sqlite3 ".backup '$HOME/vaultwarden/data/db-backup/$(date +%Y-%m-%d).sqlite3'"

To do this, create a bash script with the last command and save it as ``~/backup-vaultwarden.sh`` and make it executable.

.. code-block:: console

 [isabell@stardust ~]$ chmod +x backup-vaultwarden.sh

Now you can add this script into your crontab.

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

By default, vaultwarden allows any anonymous user to register new accounts on the server without first being invited. **This is necessary to create your first user on the server**, but it's recommended to disable it in the admin panel (if the admin panel is enabled) or with the environment variable to prevent attackers from creating accounts on your vaultwarden server.

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

vaultwarden displays password hints on the login page to accommodate small/local deployments that do not have SMTP configured, which could be abused by an attacker to facilitate password-guessing attacks against users on the server. This can be disabled in the admin panel by unchecking the ``Show password hints option`` or with the environment variable:

Use your favourite editor to edit ``~/vaultwarden/.env`` and add the the following content:

.. code-block:: ini

 SHOW_PASSWORD_HINT=false
 
Secure the ``ADMIN_TOKEN`` 
^^^^^^^^^^^^^^^^^^^^^^^^^^

Since version ``1.28.0``, vaultwarden recommends_ hashing the ``ADMIN_TOKEN`` using Argon2 by generating a `PHC string`_ instead of using plain text. If you are using the admin panel, consider securing your token as follows:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden/output
 [isabell@stardust ~]$ ./vaultwarden hash
 Generate an Argon2id PHC string using the 'bitwarden' preset:

 Password:
 Confirm Password:

 ADMIN_TOKEN='$argon2id$v=19$m=65540,t=3,p=4$Ghv9VB ... SDSMvJbhDVlU'

 Generation of the Argon2id PHC string took: 401.754824ms
 [isabell@stardust ~]$
 
Finally, update the token in the admin panel.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.
.. warning ::  Be careful while upgrading. Have a `backup of the data`_ before attempting upgrade.


Updating vaultwarden is really easy.
  - Stop the server
  - Backup ``data`` and ``.env``
  - Pull latest image and extract binary
  - Start the server again

.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden
 [isabell@stardust vaultwarden]$ supervisorctl stop vaultwarden
 vaultwarden: stopped
 [isabell@stardust vaultwarden]$ ./docker-image-extract vaultwarden/server:alpine
 Getting API token...
 Getting image manifest for vaultwarden/server:alpine...
 Fetching and extracting layer 97518928ae5f3d52d4164b314a7e73654eb686ecd8aafa0b79acd980773a740d...
 ...
 Image contents extracted into ./output.
 [isabell@stardust vaultwarden]$ supervisorctl start vaultwarden
 vaultwarden: started
 [isabell@stardust vaultwarden]$
 
Hint: If the update fails
-------------------------

When you get the error message ``No layers returned. Verify that the image and tag are valid.`` you'll have to update the Docker Image Extractor first as described below:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/vaultwarden
 [isabell@stardust ~]$ rm docker-image-extract
 [isabell@stardust ~]$ wget -O ~/vaultwarden/docker-image-extract https://raw.githubusercontent.com/jjlin/docker-image-extract/main/docker-image-extract
 [isabell@stardust ~]$ chmod +x docker-image-extract
 [isabell@stardust ~]$

Acknowledgements
================
This guide is based on the official `vaultwarden documentation`_. Previously, it was based on the `bitwarden_rs guide from Tom Schneider <https://vigonotion.com/blog/install-bitwarden-rs-on-uberspace/>`_.

.. _async: https://github.com/dani-garcia/vaultwarden/tree/async
.. _At the moment: https://github.com/dani-garcia/bitwarden_rs/pull/728
.. _bitwarden server repository: https://github.com/bitwarden/server
.. _Bitwarden: https://bitwarden.com/
.. _feed: https://github.com/dani-garcia/vaultwarden/releases
.. _Github: https://github.com/dani-garcia/vaultwarden
.. _GNU General Public License: https://github.com/dani-garcia/vaultwarden/blob/master/LICENSE.txt
.. _PHC string: https://github.com/P-H-C/phc-string-format/blob/master/phc-sf-spec.md
.. _recommends: https://github.com/dani-garcia/vaultwarden/wiki/Enabling-admin-page#secure-the-admin_token
.. _rust toolchain: https://rustup.rs/
.. _this page: https://github.com/dani-garcia/bw_web_builds/releases
.. _vaultwarden documentation: https://github.com/dani-garcia/vaultwarden/wiki/Pre-built-binaries#extracting-binaries-without-docker-installed
.. _vaultwarden: https://github.com/dani-garcia/vaultwarden
.. _web-vault-feed: https://github.com/dani-garcia/bw_web_builds/releases
.. _backup of the data: https://github.com/dani-garcia/vaultwarden/wiki/General-%28not-docker%29#backup

----

Tested with vaultwarden 1.23.1 and Web-Vault v2.25.0, Uberspace 7.12

.. author_list::
