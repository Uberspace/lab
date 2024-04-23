.. highlight:: console

.. spelling::
    Offen
    offen

.. author:: Frederik Ring <hioffen@posteo.de>

.. tag:: web
.. tag:: analytics
.. tag:: privacy
.. tag:: golang

.. sidebar:: Logo

  .. image:: _static/images/offen.png
      :align: center

#####
Offen
#####

.. tag_list::

Offen_ is an open alternative to common web analytics tools.
Gain insights while your users have full access to their data.
Lightweight, self hosted and free.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`mail <mail-access>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

Offen is distributed under the Apache 2.0 license which can be found here:

  * https://github.com/offen/offen/blob/development/LICENSE

For information about third party software bundled by Offen, check
the `NOTICE` file included in the download.

Prerequisites
=============

Your Offen subdomain needs to be setup (note that this does not need to contain
the word "offen", it can also be "analytics" or whatever you feel like):

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 offen.yourdomain.org
 [isabell@stardust ~]$

.. note:: This subdomain setup is required so that Offen can set cookies from
    the same domain that your target site is running on. I.e. if your site is
    running on `www.yourdomain.org`, Offen is ideally running on
    `offen.yourdomain.org`. You could use the `isabell.uber.space` domain if you
    want to, but that will make Offen issue 3rd party cookies, which are subject
    to blocking in many scenarios. A domain can be added at a later point in
    time though.

.. include:: includes/my-print-defaults.rst

Installation
============

.. _Download:

Download the binary distribution
--------------------------------

Offen is distributed as a single binary file. To kick off your install, download
the latest release:

::

 [isabell@stardust ~]$ mkdir -p ~/tmp/offen-download
 [isabell@stardust ~]$ curl -sSL https://get.offen.dev | tar -xvz -C ~/tmp/offen-download
 LICENSE
 NOTICE
 README.md
 checksums.txt
 offen-darwin-10.6-amd64
 offen-darwin-10.6-amd64.asc
 offen-linux-amd64
 offen-linux-amd64.asc
 offen-windows-4.0-amd64.exe
 offen-windows-4.0-amd64.exe.asc
 [isabell@stardust ~]$

.. note:: The distribution tarball also contains non-Linux binaries which is why
    you also see those `darwin` and `windows` files. We will delete them later.

Next, we should check if the binary matches the signature - i.e. it has not been
altered by 3rd parties - using GPG (this step is optional, but `highly
recommended`):

::

 [isabell@stardust ~]$ curl -sSL https://keybase.io/hioffen/pgp_keys.asc | gpg --import
 gpg: key C90B8DA1: public key "Offen (Signing Binaries) <hioffen@posteo.de>" imported
 gpg: Total number processed: 1
 gpg:               imported: 1  (RSA: 1)
 gpg: no ultimately trusted keys found
 [isabell@stardust ~]$ gpg --verify ~/tmp/offen-download/offen-linux-amd64.asc ~/tmp/offen-download/offen-linux-amd64
 gpg: Signature made Mo 13 Jul 2020 18:05:28 CEST using RSA key ID C90B8DA1
 gpg: Good signature from "Offen (Signing Binaries) <hioffen@posteo.de>"
 gpg: WARNING: This key is not certified with a trusted signature!
 gpg:          There is no indication that the signature belongs to the owner.
 Primary key fingerprint: F20D 4074 068C 636D 58B5  3F46 FD60 FBED C90B 8DA1
 [isabell@stardust ~]$

.. note:: GPG will print warnings about the signing key not being certified
    as your Uberspace's keyring is likely empty and does therefore not know
    about anyone who has signed Offen's key. `This is expected behavior`. You
    can check the Offen Keybase_ profile for further proof that this key is
    the correct one.

Install the command
-------------------

Next, you can install the Linux binary on your Uberspace:

::

 [isabell@stardust ~]$ cp ~/tmp/offen-download/offen-linux-amd64 ~/bin/offen
 [isabell@stardust ~]$ which offen
 ~/bin/offen
 [isabell@stardust ~]$

Cleaning up
-----------

You can now safely delete the downloaded files (remember to check or keep
`LICENSE` and `NOTICE` files if you are interested in such things):

::

 [isabell@stardust ~]$ rm -rf ~/tmp/offen-download
 [isabell@stardust ~]$

Configuration
=============

Create a config file
--------------------

In its most basic setup, Offen sources configuration values from an
``offen.env`` file, that is expected in ``~/.config/offen.env``:

::

 [isabell@stardust ~]$ mkdir -p ~/.config
 [isabell@stardust ~]$ touch ~/.config/offen.env
 [isabell@stardust ~]$

Populate the config file
------------------------

For Offen to run on your Uberspace you will need to populate this ``.env``
file with the following:

A Secret
--------

Offen requires a unique secret for signing login cookies and certain URLs. You
can use the ``offen`` command you just installed to create one for you
(passing ``-quiet`` will make ``secret`` output the generated value
only):

::

 [isabell@stardust ~]$ echo "OFFEN_SECRET=$(offen secret -quiet)" >> ~/.config/offen.env
 [isabell@stardust ~]$

.. note:: Changing this secret at a later point is possible, but will invalidate
 all currently active login sessions, as well as all pending invites or password
 resets.

Database setup
--------------

Offen will store its data in the MariaDB provided by your Uberspace. First,
create a dedicated database for Offen to use:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_offen"
 [isabell@stardust ~]$

Next, edit the config file at ``~/.config/offen.env`` and append the dialect
and the connection string (do not overwrite the secret you just created):

.. code-block:: ini

 OFFEN_DATABASE_DIALECT=mysql
 OFFEN_DATABASE_CONNECTIONSTRING="isabell:MySuperSecretPassword@tcp(localhost:3306)/isabell_offen?parseTime=true"

SMTP credentials
----------------

Offen needs to be able to send out transactional email so that you can:

* reset your password in case you forgot it
* invite others to collaborate with you on this instance

.. note:: This section uses your Uberspace's default mail setup because it's
 easy and already present, but you are free to use whatever SMTP service you
 like if you have different requirements.

Edit ``~/.config/offen.env`` and append the SMTP credentials like this (do not
overwrite the existing values):

.. code-block:: ini

 OFFEN_SMTP_HOST="stardust.uberspace.de"
 OFFEN_SMTP_PASSWORD="YourSuperSecretPassword"
 OFFEN_SMTP_USER="isabell@uber.space"
 OFFEN_SMTP_SENDER="isabell@uber.space"

.. note:: For your ``@uber.space`` address the password is the same as for SSH
 access, which you can set in your dashboard.

Setup the daemon
----------------

Offen needs to run at all times so it can accept incoming events. Create a file
``~/etc/services.d/offen.ini`` and populate it with the following:

.. code-block:: ini

 [program:offen]
 command=%(ENV_HOME)s/bin/offen
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check the logs and your configuration.

Point the web backend to Offen
------------------------------

As a last step you need to point your web backend to your Offen service.

.. note:: Offen is running on port 3000.

.. include:: includes/web-backend.rst

.. note:: If you need to use a different port, set ``OFFEN_SERVER_PORT`` in your
 configuration file.

.. note:: Uberspace set ``X-Frame-Options: SAMEORIGIN`` by default. You need to suppress it, if you run into problems: ``uberspace web header suppress / X-Frame-Options``.


Finishing the installation
==========================

Point your browser to the `https://offen.yourdomain.org/setup/` page and create
your user and a first account.

Embedding Offen on your website
===============================

All you need to do to embed your Offen install on a website is to add the
script to your document:

.. code-block:: html

 <script async src="https://offen.yourdomain.org/script.js" data-account-id="<YOUR_ACCOUNT_ID>"></script>

.. note:: You will also find this snippet for copy / pasting when you log in to
    your account.

Updating the version in use
===========================

If you want to update Offen to a newer version than you have originally
installed, repeat the steps in the :ref:`Download<Download>` section.

After having done so, stop the daemon, update the binary, check its version
and restart the daemon:

.. code-block:: console
 :emphasize-lines: 4

 [isabell@stardust ~]$ supervisorctl stop offen
 [isabell@stardust ~]$ cp ~/tmp/offen-download/offen-linux-amd64 ~/bin/offen
 [isabell@stardust ~]$ offen version
 INFO[0000] Binary built using                            revision=v0.1.1
 [isabell@stardust ~]$ rm -rf ~/tmp/offen-download
 [isabell@stardust ~]$ supervisorctl start offen
 [isabell@stardust ~]$

.. note:: Before upgrading, always check the Releases_ page to confirm your
 update is compatible with the version you are running. Running
 ``offen version`` will tell you which version your Uberspace is currently
 using.

Refer to the `documentation <https://docs.offen.dev/running-offen/downloads-distributions/>`_
for info on how to download a specific version of Offen.

Official docs
=============

Offen has `a dedicated documentation site <https://docs.offen.dev>`_ that will
tell you more about how to use and configure Offen.

Project updates
===============

.. note:: Check Offen's Twitter_ or our Releases_ page regularly to stay
 informed about the newest versions and changes.


.. _Offen: https://www.offen.dev
.. _Releases: https://github.com/offen/offen/releases
.. _Twitter: https://twitter.com/hioffen
.. _Keybase: https://keybase.io/hioffen

----

Tested with Offen v0.1.1, Uberspace 7.7

.. author_list::
