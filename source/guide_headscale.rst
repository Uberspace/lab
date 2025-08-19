.. author:: Lukas Wolfsteiner <https://lukas.wolfsteiner.media>

.. tag:: vpn
.. tag:: wireguard
.. tag:: self-hosting
.. tag:: lang-go
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/headscale.svg
      :align: center

#########
Headscale
#########

.. tag_list::

Headscale_ is an open source, self-hosted implementation of the Tailscale control server. It allows you to create your own private mesh VPN using the WireGuard protocol, providing secure connectivity between your devices without relying on a third-party service.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`

License
=======

Headscale is released under the _[BSD-3-Clause License](https://github.com/juanfont/headscale/blob/main/LICENSE)_.

All relevant legal information can be found here:

  * https://github.com/juanfont/headscale/blob/main/LICENSE

Prerequisites
=============

We're using the latest headscale release for Linux x86_64. Check the official releases_ for the latest version.

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the latest headscale binary from the official GitHub releases page. Replace ``<VERSION>`` with the latest version (e.g., ``0.26.1``):

::

 [isabell@stardust ~]$ wget -O ~/bin/headscale \
   https://github.com/juanfont/headscale/releases/download/v<VERSION>/headscale_<VERSION>_linux_amd64
 [isabell@stardust ~]$ chmod +x ~/bin/headscale

.. note:: Ensure ``~/bin`` is in your ``$PATH``. You can check with ``echo $PATH``.

Create a directory for headscale data, configuration and logs:

::

 [isabell@stardust ~]$ mkdir -p ~/opt/headscale
 [isabell@stardust ~]$ mkdir -p ~/etc/headscale
 [isabell@stardust ~]$ mkdir -p ~/logs/headscale

Download the example configuration file:

::

 [isabell@stardust ~]$ wget -O ~/etc/headscale/config.yaml \
   https://github.com/juanfont/headscale/raw/v<VERSION>/config-example.yaml
 [isabell@stardust ~]$

Edit ``~/etc/headscale/config.yaml`` with your favourite editor and make the following adjustments:

.. warning::
  Review and adjust the configuration to suit your environment. At minimum, set the ``server_url``, ``private_key_path``, and ``database.sqlite``/``database.postgres``. For a simple SQLite setup, use:

  .. code-block:: yaml

    server_url: "https://<your-domain>:443"
    private_key_path: "~/etc/headscale/private.key"

    database:
      type: "sqlite"

      sqlite:
        path: "~/opt/headscale/db.sqlite"

    unix_socket: "~/opt/headscale/headscale.sock"

  Generate a private key if needed:

  ::

    [isabell@stardust ~]$ headscale generate private-key --config ~/etc/headscale/config.yaml > ~/etc/headscale/private.key

Configuration
=============

Configure headscale for Uberspace web backend
--------------------------------------------

To run headscale behind Uberspace's native web backend (reverse proxy), you need to:

- Set headscale to listen on all interfaces (0.0.0.0:8080).
- Disable TLS in headscale (let Uberspace handle HTTPS).
- Set the correct server_url (your public domain, with https).
- Ensure WebSocket support (Uberspace's web backend supports this by default).

Edit your ``~/etc/headscale/config.yaml`` as follows:

.. code-block:: yaml
   :emphasize-lines: 1,2,3,4,5

   server_url: "https://<your-domain>"
   listen_addr: "0.0.0.0:8080"
   tls_cert_path: ""
   tls_key_path: ""
   unix_socket: "~/opt/headscale/headscale.sock"
   private_key_path: "~/etc/headscale/private.key"
   database:
     type: "sqlite"
     sqlite:
       path: "~/opt/headscale/db.sqlite"

To validate your configuration, run:

    [isabell@stardust ~]$ headscale configtest --config ~/etc/headscale/config.yaml

.. note::
   TLS is handled by Uberspace's web backend. Do not set ``tls_cert_path`` or ``tls_key_path`` in your headscale config.

Test daemon
-----------

Test the daemon by running ``headscale serve --config ~/etc/headscale/config.yaml`` in a terminal.

If it's not in state running without errors, check the shell output for errors.


Setup daemon
------------

Create ``~/etc/services.d/headscale.ini`` with the following content:

.. code-block:: ini

  [program:headscale]
  command=%(ENV_HOME)s/bin/headscale serve --config %(ENV_HOME)s/etc/headscale/config.yaml
  directory=%(ENV_HOME)s/headscale
  stderr_logfile=%(ENV_HOME)s/logs/headscale/err.log
  stdout_logfile=%(ENV_HOME)s/logs/headscale/out.log
  autostart=true
  autorestart=true
  stopsignal=INT
  startsecs=5

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration and the logs using ``supervisorctl maintail`` or ``tail -f ~/logs/headscale/out.log``.

Configure Uberspace web backend
-------------------------------

Now, connect the Uberspace web backend to your running headscale instance:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set <your-domain> --http --port 8080
  Set backend for <your-domain> to port 8080; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. note::
   Uberspace's web backend will handle HTTPS and proxy all requests (including WebSockets) to your headscale service.

Initial usage
=============

Once headscale is running, you can begin managing users and nodes.

Create a user:

::

 [isabell@stardust ~]$ headscale users create <USER>

Generate a preauth key for device registration:

::

 [isabell@stardust ~]$ headscale preauthkeys create --user <USER>

Use the preauth key with the Tailscale client on your device:

::

 $ tailscale up --login-server https://<your-domain> --authkey <PREAUTHKEY>

For more commands, see ``headscale help`` or the official documentation_.

Updates
=======

.. note:: Check the releases_ page regularly to stay informed about the newest version.

To update headscale, download the new binary and replace the old one. Then restart the service:

::

 [isabell@stardust ~]$ supervisorctl restart headscale

.. _Headscale: https://github.com/juanfont/headscale
.. _releases: https://github.com/juanfont/headscale/releases
.. _documentation: https://headscale.net/stable/

----

Tested with Headscale 0.26.1, Uberspace 7.16.7

.. author_list::
