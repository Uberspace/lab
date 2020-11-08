.. author:: this.ven <lab@thisven.tuttle.uberspace.de>

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
Reach outside your own site with federation via ActivityPub. WriteFreely lets anyone on Mastodon, Pleroma, or any ActivityPub-enabled service follow your blog, bookmark your posts, and share them with their followers.
WriteFreely is written in Go (golang), so it runs anywhere and takes up very few resources.

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

Use ``wget`` to download the `latest release`_:

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/writeas/writefreely/releases/download/v0.12.0/writefreely_0.12.0_linux_amd64.tar.gz
  [isabell@stardust ~]$ tar xzf writefreely_0.12.0_linux_amd64.tar.gz
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

Change to _writefreely_ directory and start config mode to create a config file:

.. note:: You need to select ``Production, behind reverse proxy`` in Server setup.

.. code-block:: console

  [isabell@stardust ~]$ cd ~/writefreely
  [isabell@stardust writefreely]$ ./writefreely config start
  [isabell@stardust writefreely]$
  
Alter _bind_ key and add TLS certificates paths in ``config.ini``; look for the ``[server]`` block:

.. code-block:: ini

  ...

  bind                 = 0.0.0.0
  tls_cert_path        = /home/isabell/etc/certificates/isabell.uber.space.crt
  tls_key_path         = /home/isabell/etc/certificates/isabell.uber.space.key

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

You can overwrite the default design with own CSS in _Customize_ settings. There are some examples for basic selectors in Writefreely's documentation_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

.. code-block:: console

  [isabell@stardust ~]$ mv ~/writefreely ~/writefreely-backup
  [isabell@stardust ~]$ wget https://github.com/writeas/writefreely/releases/download/v0.13.0/writefreely_0.13.0_linux_amd64.tar.gz
  [isabell@stardust ~]$ tar xzf writefreely_0.13.0_linux_amd64.tar.gz
  [isabell@stardust ~]$ cp ~/writefreely-backup/config.ini ~/writefreely/config.ini
  [isabell@stardust ~]$ cp ~/writefreely-backup/keys/ ~/writefreely/keys/
  
Restart Writefreely by ``supervisorctl restart writefreely`` command. If it's not starting, repeat `config mode procedure`_.

----

Tested on Uberspace v7.7.0 with Go 1.15.1 and Writefreely v0.12.0.

.. author_list::

.. _Writefreely: https://writefreely.org/
.. _`AGPL v3.0`: https://www.gnu.org/licenses/agpl-3.0.html
.. _`latest release`: https://github.com/writeas/writefreely/releases/latest
.. _`admin guide`: https://writefreely.org/docs/latest/admin/config
.. _documentation: https://writefreely.org/docs/latest/writer/css
.. _feed: https://github.com/writeas/writefreely/releases/latest
.. _`config mode procedure`: #writefreely-config
