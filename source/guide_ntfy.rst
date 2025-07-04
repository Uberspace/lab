.. author:: jpmens <https://jpmens.net>

.. tag:: lang-go
.. tag:: notification

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ntfy.png
      :align: center

####
ntfy
####

.. tag_list::

ntfy_ (pronounce: notify) is a simple HTTP-based pub-sub notification service. It allows you to send notifications to your phone or desktop via scripts from any computer, entirely without signup, cost or setup.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Your ntfy URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Like a lot of Go software, ntfy is distributed as a single binary, which in this case is the server and the client component. Download ntfy's latest release_,
verify the checksum specified in the respective ``.sha256`` file and finally extract the files.

::

  [isabell@stardust ~]$ mkdir ~/ntfy
  [isabell@stardust ~]$ wget -O ntfy.tar.gz https://github.com/binwiederhier/ntfy/releases/download/v2.12.0/ntfy_2.12.0_linux_amd64.tar.gz
  [...]
  [isabell@stardust ~]$ tar --strip-components=1 -xzf ntfy.tar.gz -C ~/ntfy/
  [isabell@stardust ~]$ rm ntfy.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Create a configuration file
---------------------------

Use your favourite editor to edit ``~/ntfy/server/server.yml`` with the following settings. Make sure to replace the ``base-url`` and <username> with your own.

.. code-block::
 :emphasize-lines: 1,3,5,8

  base-url: https://isabell.uber.space
  listen-http: ":8008"
  cache-file: /home/<username>/ntfy/cache.db
  cache-duration: "12h"
  auth-file: "/home/<username>/ntfy/auth.db"
  auth-default-access: "deny-all"
  behind-proxy: true
  attachment-cache-dir: "/home/<username>/ntfy/attachments"
  attachment-total-size-limit: "1G"
  attachment-file-size-limit: "1M"
  attachment-expiry-duration: "3h"
  keepalive-interval: "45s"
  manager-interval: "2m"
  web-root: /
  upstream-base-url: "https://ntfy.sh"
  visitor-subscription-limit: 30
  log-level: INFO

Configure web server
--------------------

.. note::

    ntfy will be running on port 8008.

.. include:: includes/web-backend.rst

Setup daemon
------------

To start ntfy automatically and run it in the background, create ``~/etc/services.d/ntfy.ini`` with the following content:

.. code-block:: ini

  [program:ntfy]
  command=%(ENV_HOME)s/ntfy/ntfy serve --config %(ENV_HOME)s/ntfy/server/server.yml
  startsecs=5

.. include:: includes/supervisord.rst

Finishing installation
======================

Point your browser to the URL you set up, e. g. ``https://isabell.uber.space``.

Add admin user
--------------

To protect access to your ntfy instance, the default configuration above permits no access.

To add a new admin user:

.. code-block:: bash

  [isabell@stardust ~]$ ./ntfy/ntfy user --config ~/ntfy/server/server.yml add --role=admin isabell
  password:
  confirm:
  [isabell@stardust ~]$ ./ntfy/ntfy user --config ~/ntfy/server/server.yml list
  user isabell (role: admin, tier: none)
  - read-write access to all topics (admin role)
  user * (role: anonymous, tier: none)
  - no topic-specific permissions
  - no access to any (other) topics (server config)
  [isabell@stardust ~]$

To add a non-admin user, use ``--role=user``:


.. code-block:: bash

  [isabell@stardust ~]$ ./ntfy/ntfy user --config ~/ntfy/server/server.yml add --role=user isabell
  password:
  confirm:
  [isabell@stardust ~]$

Add access token
----------------

To avoid having to use your credentials on multiple clients, generate an access
token for your user:

.. code-block:: bash

  [isabell@stardust ~]$ ./ntfy/ntfy token --config ~/ntfy/server/server.yml add --expires=2d isabell
  token tk_<token-id> created for user isabell, expires <time when token expires>
  [isabell@stardust ~]$


Set up UnifiedPush
------------------

UnifiedPush application servers (e.g. synapse, mastodon) need to have anonymous
write access to the push message topic. Enable anonymous write-access to
UnifiedPush topics (prefixed with ``up*``):

.. code-block:: bash

  [isabell@stardust ~]$ ./ntfy/ntfy access --config ~/ntfy/server/server.yml '*' 'up*' write-only
  granted write-only access to topic up*

  user * (role: anonymous, tier: none)
  - write-only access to topic up*
  - no access to any (other) topics (server config)
  [isabell@stardust ~]$


Updates
=======

.. note:: Ntfy must be updated manually.

.. _ntfy: https://ntfy.sh/
.. _Documentation: https://ntfy.sh/
.. _release: https://github.com/binwiederhier/ntfy/releases/latest

----

Tested with ntfy 1.28.0 Uberspace 7.2.14.0

.. author_list::
