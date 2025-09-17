.. highlight:: console
.. author:: this.ven <https://this.ven.uber.space>

.. spelling:word-list::
    pleroma

.. tag:: golang
.. tag:: microblogging
.. tag:: fediverse
.. tag:: ActivityPub

.. sidebar:: Logo

  .. image:: _static/images/gotosocial.png
      :align: center

##########
GoToSocial
##########

.. tag_list::

GoToSocial_ is an ActivityPub social network server, written in Golang and currently in alpha. It provides a lightweight, customizable, and safety-focused entryway into the Fediverse_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`
  * :manual:`web backends <web-backends>`

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

Create a directory structure in your home path and ``cd`` into the root of it.

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p ~/gotosocial/storage
  [isabell@stardust ~]$ cd ~/gotosocial
  [isabell@stardust gotosocial]$

Download the latest pre-compiled binary_ from the releases_ page.

.. code-block:: console

  [isabell@stardust gotosocial]$ wget https://codeberg.org/superseriousbusiness/gotosocial/releases/download/v0.19.2/gotosocial_0.19.2_linux_amd64.tar.gz

Extract the archive in place to populate the directory with the binary and static and example files.

.. code-block:: console

  [isabell@stardust gotosocial]$ tar xzf gotosocial_0.19.2_linux_amd64.tar.gz
  [isabell@stardust gotosocial]$


Configuration
=============

Configure GoToSocial
--------------------

Copy the example configuration file via ``cp ./example/config.yaml .`` and edit it using your favorite text editor. Change the following values.

.. code-block:: yaml
 :emphasize-lines: 1-6

 host: "isabell.uber.space"
 protocol: "https"
 port: 8080
 db-type: "sqlite"
 db-address: "sqlite.db"
 storage-local-base-path: "/home/isabell/gotosocial/storage"

We'll be using SQlite_, but you can also use :lab:`PostgreSQL <guide_postgresql>` by following the configuration_ guide for database_.

.. warning:: If you consider using a subdomain, you need to configure this as described in advanced_ installation before running ``./gotosocial`` for the first time!


Point the ``uberspace web backend`` on ``/`` to the listener on port 8080.

.. include:: includes/web-backend.rst

Test your installation by running ``./gotosocial --config-path ./config.yaml server start`` and opening ``https://isabell.uber.space`` in your web browser to access the splash screen.

If the splash screen loads successfully, hit ``Ctrl+C`` to abort GoToSocial and procede with the rest of the configuration.

Setup daemon
------------

Create ``~/etc/services.d/gotosocial.ini`` with the following content:

.. code-block:: ini

 [program:gotosocial]
 directory=%(ENV_HOME)s/gotosocial
 command=%(ENV_HOME)s/gotosocial/gotosocial --config-path ./config.yaml server start
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Administration
==============

Create a user
-------------

Create your user account and make it the instance admin. Replace the values for ``--username``, ``email`` and ``--password`` with your desired information.

.. code-block:: console

 [isabell@stardust gotosocial]$ ./gotosocial --config-path ./config.yaml admin account create --username isabell --email isabell@uber.space --password '5up3r_s3cur3_p4ssw0rD'

To promote the new user as instance admin_ use the following command:

.. code-block:: console

 [isabell@stardust gotosocial]$ ./gotosocial --config-path ./config.yaml admin account promote --username isabell

Login
-----

Login into your account. GoToSocial recommends using Pinafore_ or Tusky_. Setup your profile and start participating in the fediverse. You can also customize your profile and adjust settings_ by navigating to ``https://isabell.uber.space/settings`` with a web browser.

Customization
-------------

To provide some information on your instance, you might want set basic instance settings, such as contact user and email. Browse to ``https://isabell.uber.space/settings/admin/settings`` and configure the details.

Additionally, there is some documentation on `custom CSS`_, if you'd like to adjust the appearance of your instance.

Best Practices
==============

On a single-user instance you might want to disable further account registration and redirect the landing page to your user profile. For this, edit the configuration in ``~/gotosocial/config.yaml`` and adjust the following settings:

.. code-block:: yaml

 landing-page-user: "isabell"
 accounts-registration-open: false

Updates
=======

.. note:: Check the update feed_ regularly or follow the project in the fediverse_ to stay informed about the newest version.

.. warning:: Check the release notes if there are any additional steps (like config changes) needed for the current update and apply them.

Stop the service using ``supervisorctl stop gotosocial`` and rename your current installation to keep a backup.

.. code-block:: console

  [isabell@stardust ~]$ mv ~/gotosocial ~/gotosocial-backup

Repeat the installation_ step and copy your ``config.yaml``, ``sqlite.db`` and ``storage`` directory back into the new installation.

.. code-block:: console

  [isabell@stardust ~]$ cp ~/gotosocial-backup/config.yaml ~/gotosocial/config.yaml
  [isabell@stardust ~]$ cp -r ~/gotosocial-backup/sqlite.db ~/gotosocial/sqlite.db
  [isabell@stardust ~]$ cp -r ~/gotosocial-backup/storage ~/gotosocial/storage

Sart GoToSocial using the ``supervisorctl start gotosocial`` command. If it's not starting, investigate errors in the supervisord logfile located in ``~/tmp``. Otherwise have fun using the latest version and consider removing your backup after some days.

----

Tested with GoToSocial 0.19.2, Uberspace 7

.. _GoToSocial: https://gotosocial.org
.. _ActivityPub: https://activitypub.rocks
.. _Fediverse: https://fediverse.info
.. _binary: https://docs.gotosocial.org/en/v0.19.2/getting_started/installation/metal/#download-release
.. _releases: https://codeberg.org/superseriousbusiness/gotosocial/releases
.. _SQlite: https://manual.uberspace.de/database-sqlite
.. _configuration: https://docs.gotosocial.org/en/v0.19.2/configuration
.. _database: https://docs.gotosocial.org/en/v0.19.2/configuration/database
.. _advanced: https://docs.gotosocial.org/en/v0.19.2/advanced/host-account-domain/
.. _admin: https://docs.gotosocial.org/en/v0.19.2/admin/settings
.. _Pinafore: https://pinafore.social
.. _Tusky: https://tusky.app
.. _settings: https://docs.gotosocial.org/en/v0.19.2/user_guide/settings
.. _`custom css`: https://docs.gotosocial.org/en/v0.19.2/user_guide/custom_css/
.. _feed: https://codeberg.org/superseriousbusiness/gotosocial.rss
.. _fediverse: https://gts.superseriousbusiness.org/@gotosocial
.. _installation: #Installation

.. author_list::
