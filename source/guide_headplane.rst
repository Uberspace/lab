.. author:: Lukas Wolfsteiner <https://lukas.wolfsteiner.media>

.. tag:: vpn
.. tag:: wireguard
.. tag:: self-hosting
.. tag:: lang-nodejs
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/headplane.svg
      :align: center

#########
Headplane
#########

.. tag_list::

A feature-complete web UI for Headscale, allowing you to manage your nodes, networks, and ACLs with ease. It is open source and integrates directly with your Headscale instance.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here:

  * https://github.com/tale/headplane/blob/main/LICENSE

Prerequisites
=============

- Node.js 22 LTS or newer (see :manual:`Node.js <lang-nodejs>`)
- PNPM 10.x (see [pnpm installation](https://pnpm.io/installation))
- A running Headscale instance (see :lab:`Headscale <guide_headscale>`) on the same Uberspace account
- Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Clone the Headplane repository and install dependencies:

::

 [isabell@stardust ~]$ git clone https://github.com/tale/headplane.git
 [isabell@stardust ~]$ cd headplane
 [isabell@stardust headplane]$ git checkout v0.6.0  # Or latest release
 [isabell@stardust headplane]$ pnpm install
 [isabell@stardust headplane]$ pnpm build

Create a directory for persistent data:

::

 [isabell@stardust ~]$ mkdir -p ~/opt/headplane

Configuration
=============

Copy the example configuration and edit it:

::

 [isabell@stardust headplane]$ cp config.example.yaml ~/opt/headplane/config.yaml
 [isabell@stardust headplane]$ edit ~/opt/headplane/config.yaml

.. warning::
   - Set the correct Headscale API URL (e.g. ``http://localhost:8080`` if running on the same account).
   - If you want to access Headplane from a different domain or subdomain, configure CORS headers accordingly (see Headplane docs).
   - Set a strong admin password and secret.
   - Make sure the data directory is writable by your user.

Example config snippet:

.. code-block:: yaml

  headscale:
    url: "http://localhost:8080"
  server:
    host: "0.0.0.0"
    port: 3000
  cors:
    enabled: true
    origin: ["https://<your-domain>"]

Setup daemon
------------

Create ``~/etc/services.d/headplane.ini`` with the following content:

.. code-block:: ini

  [program:headplane]
  directory=%(ENV_HOME)s/headplane
  command=/usr/bin/node build/server/index.js
  startsecs=5
  stopsignal=INT

  # [optionally] Depend on Headscale being available
  priority=100
  depends_on=headscale

  # [optionally] start & restart automatically
  autostart=true
  autorestart=true

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration and the logs using ``supervisorctl maintail`` or ``tail -f ~/headplane/logs/*.log``.

Configure Uberspace web backend
-------------------------------

Now, connect the Uberspace web backend to your running Headplane instance:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set <your-headscale-domain>/admin --http --port 3000
  Set backend for /admin to port 3000; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. note::
   By default, Headplane serves its UI at ``<your-headscale-domain>/admin``. Adjust the path if you change the admin prefix in your config and web backend.

Integration with Headscale
==========================

- Ensure Headscale is running and accessible at the URL configured in Headplane's config.
- Both services should run as user daemons via supervisord.
- If you use different domains or subdomains, configure CORS headers in Headplane.
- For advanced integration (e.g. process management), see the [Headplane docs](https://github.com/tale/headplane/blob/main/docs/Configuration.md).

Finishing installation
======================

Point your browser to ``https://<your-headscale-domain>/admin`` and log in with your admin credentials.

Best practices
==============

- Use strong passwords and secrets.
- Regularly update both Headplane and Headscale.
- Backup your configuration and data directories.

References
==========

.. _Source: https://github.com/tale/headplane

.. _Bare-Metal Guide: https://github.com/tale/headplane/blob/main/docs/Bare-Metal.md
.. _Configuration Guide: https://github.com/tale/headplane/blob/main/docs/Configuration.md

Updates
=======

.. note:: Check the [Headplane releases](https://github.com/tale/headplane/releases) page regularly to stay informed about the newest version.

.. _feed: https://github.com/tale/headplane/releases.atom

To update Headplane, pull the latest code, rebuild, and restart the service:

::

 [isabell@stardust headplane]$ git pull
 [isabell@stardust headplane]$ pnpm install
 [isabell@stardust headplane]$ pnpm build
 [isabell@stardust headplane]$ supervisorctl restart headplane

.. _Headplane: https://github.com/tale/headplane

----

Tested with Headplane 0.6.0, Headscale 0.26.1, Uberspace 7.16.7

.. author_list::
