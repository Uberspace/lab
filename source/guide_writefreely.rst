.. author:: this.ven <https://this.ven.uber.space>
.. author:: Jan Klomp <https://jan.klomp.de>


.. tag:: blog
.. tag:: lang-go
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/writefreely.svg
      :align: center

###########
Writefreely
###########

.. tag_list::

WriteFreely_ is built around writing. There's no news feed, notifications, or unnecessary likes or claps to take you away from your train of thought.
Reach outside your own site with federation via ActivityPub. WriteFreely lets anyone on Mastodon, Pleroma, or any ActivityPub-enabled service follow your blog, bookmark your posts, and share them with their followers. WriteFreely is written in Go (golang), so it runs anywhere and takes up very few resources.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Writefreely is released under the `AGPL v3.0`_.

Prerequisites
=============

Set up your URL:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Installation
============

.. note:: Version 15.1 and higher require ``GLIBC 2.28`` which is not available for CentOS 7. 

Use ``wget`` to download `version 15.0`_:

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/writefreely/writefreely/releases/download/v0.15.0/writefreely_0.15.0_linux_amd64.tar.gz
  [isabell@stardust ~]$ tar xzf writefreely_0.15.0_linux_amd64.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Database Setup
--------------

Create a new database:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_writefreely CHARACTER SET latin1 COLLATE latin1_swedish_ci;"
  [isabell@stardust ~]$

Writefreely Config
------------------

Change to `writefreely` directory and start config mode to create a config file:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/writefreely
  [isabell@stardust writefreely]$ ./writefreely config start
  [isabell@stardust writefreely]$

Setup Writefreely interactively. Use ``Production behind reverse proxy`` in `Server setup` and confirm default port:

.. code-block::

  Loaded configuration config.ini.

   ✍ WriteFreely Configuration ✍

   This quick configuration process will update the application's config
  file, config.ini.

   It validates your input along the way, so you can be sure any future
  errors aren't caused by a bad configuration. If you'd rather configure your
  server manually, instead run: writefreely --create-config and edit that
  file.

  Server setup
  Production, behind reverse proxy
  Local port: 8080

Choose ``MySQL`` in `Database Setup` and use credentials shown earlier. Use ``<username>_writefreely``, replacing ``<username>`` with your username. Confirm default MySQL host and port:

.. code-block::

  Database setup
  MySQL
  Username: isabell
  Password: *******************
  Database name: isabell_writefreely
  Host: localhost
  Port: 3306

Enter admin and blog details as needed, enter your domain with ``https://`` and without port. Choose other options to your liking:

.. code-block::

  App setup
  Single user blog
  Admin username: admin
  Admin password: <choose_a_password>
  Blog name: this.ven
  Public URL: https://isabell.uber.space

  ...

  2020/11/08 23:52:14 Done!

After interactive configuration alter `bind` key in ``config.ini``; look for the ``[server]`` block:

.. code-block:: ini

  ...

  bind                 = 0.0.0.0

  ...

Learn about other configuration options in the documentation's `admin guide`_.

Key generation
--------------

Generate the encryption keys for your instance:

.. code-block:: console

  [isabell@stardust writefreely]$ ./writefreely keys generate
  [isabell@stardust writefreely]$

Web Backend Config
------------------

.. note:: Writefreely is running on port 8080.

.. include:: includes/web-backend.rst

Supervisord Daemon Setup
------------------------

Create ``~/etc/services.d/writefreely.ini`` with the following content:

.. code-block:: ini

  [program:writefreely]
  directory=%(ENV_HOME)s/writefreely/
  command=%(ENV_HOME)s/writefreely/writefreely
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Your Writefreely installation should now be reachable on ``https://isabell.uber.space``. Log in with the username and password provided during configuration.

RSS feed is automatically served at: ``https://isabell.uber.space/feed/``

You can overwrite the default design with own CSS in `Customize` settings. There are some examples for basic selectors in Writefreely's documentation_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

First, backup your current installation by renaming the writefreely directory:

.. code-block:: console

  [isabell@stardust ~]$ mv ~/writefreely ~/writefreely-backup

Copy the link to the newest tarball, use ``wget`` and ``tar`` to download and extract it (same procedure as in the installation_ step):

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/writeas/writefreely/releases/download/v0.13.0/writefreely_0.13.0_linux_amd64.tar.gz
  [isabell@stardust ~]$ tar xzf writefreely_0.13.0_linux_amd64.tar.gz

Copy the config and key files and do a database migration:

.. code-block:: console

  [isabell@stardust ~]$ cp ~/writefreely-backup/config.ini ~/writefreely/config.ini
  [isabell@stardust ~]$ cp ~/writefreely-backup/keys/* ~/writefreely/keys/*
  [isabell@stardust ~]$ ~/writefreely/writefreely db migrate
  [...]
  2024/02/06 14:09:10 Closing database connection...
  [isabell@stardust ~]$

Restart Writefreely using the ``supervisorctl restart writefreely`` command. If it's not starting, repeat `config mode procedure`_.

----

Tested on Uberspace v7.15.9 with Go 1.21.6 and Writefreely v0.15.0.

.. author_list::

.. _Writefreely: https://writefreely.org/
.. _`AGPL v3.0`: https://www.gnu.org/licenses/agpl-3.0.html
.. _`version 15.0`: https://github.com/writefreely/writefreely/tree/v0.15.0
.. _`admin guide`: https://writefreely.org/docs/latest/admin/config
.. _documentation: https://writefreely.org/docs/latest/writer/css
.. _feed: https://github.com/writeas/writefreely/releases/latest
.. _installation: #installation
.. _`config mode procedure`: #writefreely-config
