.. highlight:: console

.. author:: Achim | pxlfrk <hallo@pxlfrk.de>

.. tag:: passwordmanager
.. tag:: rust
.. tag:: web


.. sidebar:: Logo

  .. image:: _static/images/bitwarden.svg
      :align: center

############
Bitwarden_rs
############

.. tag_list::

Bitwarden_ is an open source password manager. Your vault is encrypted with your master key, so even if your server is compromised the hacker will only get some unreadable gibberish. Hosting your own Bitwarden server can be usefull if you are paranoid about the server security and want to be in full control, or want the premium features for free because you have a webspace anyway.

.. note :: The installation of the official `bitwarden server repository`_ via docker is heavy, difficult and relies on docker, which `isn't supported`_ at uberspace due to the fact of shared hosting. In this guide we'll use the Rust implementation `Bitwarden_rs`_ of the Bitwarden API, so you can still use the official clients.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`mail <mail-access>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`
  

License
=======

Roundcube is released under the GNU General Public License_ version 3 or any later version.

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 13:

::

 [isabell@stardust ~]$ uberspace tools version use node 13
 Selected Node.js version 13
 The new configuration is adapted immediately. Minor updates will be applied automatically.
 [isabell@stardust ~]$

If you want to use Bitwarden_rs with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst


Installation
============

Install Rust
-------------------

To compile the project, we need to install the `rust toolchain`_. Install it via rustup and use the following configuration when asked:

 * Enter ``2`` to customize the installation.
 * Press ``Enter`` to use the host triple as default.
 * Type ``nightly`` as default toolchain as it is required for bitwarden_rs.
 * Type ``default`` to use the default install profile. 
 * Enter ``y`` to add rust  to the PATH.
 * Enter ``1`` to proceed with the installation

.. code-block:: console
 :emphasize-lines: 16,21,24,27,30,42

 [isabell@stardust ~]$ curl https://sh.rustup.rs -sSf | sh
 info: downloading installer

 Welcome to Rust!
 [...]
 Current installation options:
 
   default host triple: x86_64-unknown-linux-gnu
     default toolchain: nightly
               profile: default
  modify PATH variable: yes

 1) Proceed with installation (default)
 2) Customize installation
 3) Cancel installation
 >	2

 I'm going to ask you the value of each of these installation options.
 You may simply press the Enter key to leave unchanged.

 Default host triple?

 Default toolchain? (stable/beta/nightly/none)
	nightly

 Profile (which tools and data to install)? (minimal/default/complete)
	default

 Modify PATH variable? (y/n)
	y

 Current installation options:

   default host triple: x86_64-unknown-linux-gnu
     default toolchain: nightly
               profile: default
  modify PATH variable: yes

 1) Proceed with installation (default)
 2) Customize installation
 3) Cancel installation
 >	1
 [...]
 Rust is installed now. Great!


To finish the setup, logout and login again or run

.. code-block:: console

 [isabell@stardust ~]$ source $HOME/.cargo/env.

Install Bitwarden_rs
--------------------

Clone the repository into your document root. It will create the directory ``~/bitwarden_rs`` automatically.

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/dani-garcia/bitwarden_rs.git
 
In order to build bitwarden_rs  sucessfully you'll need to set an environment variable pointing to the sqlite3 header files:

.. code-block:: console

 [isabell@stardust ~]$ export SQLITE3_LIB_DIR=/var/lib64

``cd`` into the automatically created folder:

.. code-block:: console

 [isabell@stardust ~]$ cd bitwarden_rs
 [isabell@stardust bitwarden_rs]$ 

Build the server executable:
.. note :: If that doesn't work the first time, just try again.

.. code-block:: console

 [isabell@stardust bitwarden_rs]$ cargo build --release --features sqlite

In the next step we will download the latest build for the web vault. Check `this page`_ for the newest build number and **replace it** in the following snippet:

.. note :: If you don't want to use the web-vault feature (web-app access to your vaults) for any security reasons you can skip this step. Add the following line to your ``env`` file later if you do so:
  ``WEB_VAULT_ENABLED=false``

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust bitwarden_rs]$ [isabell@stardust bitwarden_rs]$ wget https://github.com/dani-garcia/bw_web_builds/releases/download/v2.11.0/bw_web_v2.13.2.tar.gz
 [isabell@stardust bitwarden_rs]$ tar -xvzf bw_web_v2.13.2.tar.gz
 [isabell@stardust bitwarden_rs]$ rm -r bw_web_v*.tar.gz

 
Generate an ``openssl -base64`` key now and save it temporarily, you'll need it in the next step.

.. code-block:: console

 [isabell@stardust bitwarden_rs]$  openssl rand -base64 48
 [isabell@stardust bitwarden_rs]$  Ig/8bZXhqVFK11F2tQZTfODO/6QpCHE3DGyCH/2Eh40xUWMFC13J6nJVPLlyU3nO

Use your favourite editor to create ``~/bitwarden_rs/.env`` with the following content:

.. code-block:: ini

 ADMIN_TOKEN=PASTE YOUR TOKEN GENERATED ABOVE HERE # generate one with ~$ openssl rand -base64 48
 ROCKET_PORT=62714 # your port here

 SMTP_HOST=stardust.uberspace.de
 SMTP_FROM=isabell@uber.space
 SMTP_PORT=587
 SMTP_SSL=true
 SMTP_USERNAME=isabell@uber.space
 SMTP_PASSWORD=MySuperSecretPassword
 
 DOMAIN=https://isabell.uber.space:8443

Replace the mail placeholder variables with your valid IMAP credentials, otherwise the bitwarden_rs server will not be able to send you mail notifications or tokens to verify newly created user accounts.
``SMTP_USERNAME`` and ``SMTP_PASSWORD`` must be the login data from a valid mail account. Replace the server domain with your final URL.

.. note :: You can configure any type of service here, you're not limited to an uberspace IMAP user. If you prefer e.g. gmail refer to their documentations for ``SMTP_Port`` etc. accordingly.
You can edit other options, look into .env.template to see a list of available options.


Configuration
=============

Setup web backend
-----------------

.. note::

    Enter the port you configured in the ``env`` file before.
If you want to use a subdomain refer to the :manual:`web-backend manual <web-backends>`.

.. include:: includes/web-backend.rst

Setup web vault
---------------

Now it's time to test if everything works. If there is no error, you are good to go. You should be able to access your vault on ``https://isabell.uber.space``

.. code-block:: console

 [isabell@stardust ~]$ cd ~/bitwarden_rs
 [isabell@stardust bitwarden_rs]$ target/release/bitwarden_rs
 /--------------------------------------------------------------------\
 |                       Starting Bitwarden_RS                        |
 |                      Version 1.14.1-843604c9                       |
 |--------------------------------------------------------------------|
 | This is an *unofficial* Bitwarden implementation, DO NOT use the   |
 | official channels to report bugs/features, regardless of client.   |
 | Report URL: https://github.com/dani-garcia/bitwarden_rs/issues/new |
 \--------------------------------------------------------------------/

 [2020-04-03 17:27:40][start][INFO] Rocket has launched from http://0.0.0.0:62714

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/bitwarden_rs.ini`` with the following content:

.. code-block:: ini

 [program:bitwarden_rs]
	directory=%(ENV_HOME)s/bitwarden_rs
	command=node %(ENV_HOME)s/bitwarden_rs/target/release/bitwarden_rs
	autostart=yes
	autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

 
Finishing installation
======================

Your done. Point your Browser to your installation URL ``https://isabell.uber.space`` and create your user.


Update
======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Updating bitwarden_rs is really easy. Just stop the server, pull everything and download the new web vault, build the executable and start the server again:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/bitwarden_rs
 [isabell@stardust bitwarden_rs]$ supervisorctl stop bitwarden_rs
 [isabell@stardust bitwarden_rs]$ git pull
 [isabell@stardust bitwarden_rs]$ mv web-vault web-vault.old && mkdir web-vault && cd web-vault
 [isabell@stardust web-vault]$ wget new-release.tar.gz
 [isabell@stardust web-vault]$ tar -xvzf new-release.tar.gz
 [isabell@stardust web-vault]$ cd ..
 [isabell@stardust bitwarden_rs]$ cargo build --release
 [isabell@stardust bitwarden_rs]$ 
 
.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration. You can check the service's log file using ``supervisorctl tail -f bitwarden_rs``.

Acknowledgements
================
This guide is based on the official `bitwarden_rs documentation`_ as well as the `bitwarden_rs guide from Tom Schneider <https://vigonotion.com/blog/install-bitwarden-rs-on-uberspace/>`_.


.. _this page: https://github.com/dani-garcia/bw_web_builds/releases):
.. _rust toolchain: https://rustup.rs/
.. _isn't supported: https://wiki.uberspace.de/faq#docker)
.. _bitwarden server repository: https://github.com/bitwarden/server
.. _bitwarden_rs documentation: https://github.com/dani-garcia/bitwarden_rs/wiki/Building-binary
.. _Bitwarden_rs: https://github.com/dani-garcia/bitwarden_rs
.. _Bitwarden: https://bitwarden.com/
.. _Github: https://github.com/dani-garcia/bitwarden_rs
.. _feed: https://github.com/dani-garcia/bitwarden_rs/releases
.. _GNU General Public License: https://roundcube.net/license/


----

Tested with Bitwarden_rs 2.13.2, Uberspace 7.5.1.0

.. author_list::

