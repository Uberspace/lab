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

Headscale_ is an open source, self-hosted implementation of the Tailscale_ control server.

It allows you to create your own private mesh VPN using the WireGuard_ protocol, providing secure connectivity between your devices without relying on a third-party service.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`

License
=======

Headscale is released under the `BSD-3-Clause License`_.

All relevant legal information can be found in the `LICENSE`_ file in the repository of the project.

Prerequisites
=============

If you want to use Headscale with your own domain you need to add it first:

.. include:: includes/web-domain-list.rst

Installation
============

Download the latest Headscale binary from the official GitHub releases_ page. Replace ``0.26.1`` with the latest version:

.. code-block:: console

  [isabell@stardust ~]$ wget -O ~/bin/headscale \
    https://github.com/juanfont/headscale/releases/download/v0.26.1/headscale_0.26.1_linux_amd64
  [isabell@stardust ~]$ chmod +x ~/bin/headscale

By default, Headscale loads the configuration from ``$HOME/.headscale/config.yaml``, so we continue with creating the directory:

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p ~/.headscale

Then download the example configuration file:

.. code-block:: console

  [isabell@stardust ~]$ wget -O ~/.headscale/config.yaml \
    https://github.com/juanfont/headscale/raw/v0.26.1/config-example.yaml


Configuration
=============

Configure Headscale for Uberspace web backend
---------------------------------------------

To run Headscale behind Uberspace's native web backend (reverse proxy), you need to:

- Set Headscale to listen on interface ``0.0.0.0:8080`` by setting ``listen_addr`` to ``0.0.0.0:8080``.
- Disable TLS in Headscale (let Uberspace handle HTTPS) by setting ``tls_cert_path`` and ``tls_key_path`` to empty strings.
- Set the correct ``server_url`` (your public domain, with https) by setting ``server_url`` to ``https://isabell.uber.space:443``.
- Set a encryption key for the Headscale connection by setting the ``private_key_path`` to ``private.key`` (will be generated after configuration).

Edit ``~.headscale/config.yaml`` with your favourite editor and make the following adjustments:

.. warning::
  Review and adjust the configuration to suit your environment. At minimum, set the ``server_url``, ``private_key_path``, and ``database.sqlite``.

.. note::
   TLS is handled by Uberspace's web backend, do not set ``tls_cert_path`` or ``tls_key_path`` in your Headscale config. See Headscale's TLS_ documentation for more information.

For a simple and minimal setup, set the following values:

.. code-block:: yaml
   :emphasize-lines: 1

   server_url: "https://isabell.uber.space:443"
   listen_addr: "0.0.0.0:8080"

   tls_cert_path: ""
   tls_key_path: ""

   unix_socket: "headscale.sock"

   noise:
     private_key_path: "noise_private.key"

   database:
     type: "sqlite"

     sqlite:
       path: "db.sqlite"


Generate a private key (required for WireGuard):

.. code-block:: console

 [isabell@stardust ~]$ headscale generate private-key > ~/.headscale/private.key


.. note:: For further configuration options, see Headscale's Configuration_ documentation.


To validate your configuration, run:

.. code-block:: console

 [isabell@stardust ~]$ headscale configtest

If you see no errors, you can continue with the next step.

Test daemon
-----------

Test the daemon by running ``headscale serve`` in a terminal.

If it's not in state running without errors, check the shell output for errors.

Setup daemon
------------

Create ``~/etc/services.d/headscale.ini`` with the following content:

.. code-block:: ini

  [program:headscale]
  command=%(ENV_HOME)s/bin/headscale serve
  directory=%(ENV_HOME)s/.headscale
  stderr_logfile=%(ENV_HOME)s/logs/headscale.err.log
  stdout_logfile=%(ENV_HOME)s/logs/headscale.out.log
  autostart=true
  autorestart=true
  stopsignal=INT
  startsecs=5

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration and the logs using ``supervisorctl maintail`` or ``tail -f ~/logs/headscale.out.log``.

Configure Uberspace web backend
-------------------------------

Now, connect the Uberspace web backend to your running Headscale instance (use the port configured in your configuration file, like ``8080``):

.. include:: includes/web-backend.rst

.. note::
   Uberspace's web backend will handle HTTPS and proxy all requests (including WebSockets) to your Headscale service.

Usage
=====

Once Headscale is running, you can begin managing users and nodes.

Create a user:

.. code-block:: console

 [isabell@stardust ~]$ headscale users create <USER>

Generate a preauth key for device registration:

.. code-block:: console

 [isabell@stardust ~]$ headscale preauthkeys create --user <USER>

Use the preauth key with the Tailscale client on your device:

.. code-block:: console

 [isabell@stardust ~]$ tailscale up --login-server https://isabell.uber.space --authkey <PREAUTHKEY>

For more commands, see ``headscale help`` or the official documentation_.

Updates
=======

.. note:: Check the releases_ page regularly to stay informed about the newest version.

To update Headscale, download the new binary and replace the old one. Then restart the service:

.. include:: includes/supervisord.rst

.. _Headscale: https://github.com/juanfont/headscale
.. _Configuration: https://headscale.net/stable/ref/configuration/
.. _WireGuard: https://www.wireguard.com/
.. _Tailscale: https://tailscale.com/
.. _releases: https://github.com/juanfont/headscale/releases
.. _documentation: https://headscale.net/stable/
.. _BSD-3-Clause License: https://github.com/juanfont/headscale/blob/main/LICENSE
.. _LICENSE: https://github.com/juanfont/headscale/blob/main/LICENSE
.. _TLS: https://headscale.net/stable/ref/integration/reverse-proxy/#tls

----

Tested with Headscale 0.26.1, Uberspace 7.16.7

.. author_list::
