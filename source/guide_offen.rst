.. highlight:: console

.. author:: Frederik Ring <hioffen@posteo.de>

.. tag:: web
.. tag:: analytics
.. tag:: privacy

.. sidebar:: Logo

  .. image:: _static/images/offen.png
      :align: center

##########
Offen
##########

.. tag_list::

Offen_ is a fair and open alternative to common web analytics tools. Gain
insights while your users have full access to their data. Lightweight, self
hosted and free.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Offen is distributed under the Apache 2.0 license. All relevant legal
information can be found here

  * https://github.com/offen/offen/blob/development/LICENSE

Prerequisites
=============

Your offen subdomain needs to be setup (note that this does not need to contain
the word "offen", it can also be "analytics" or whatever you like):

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

Download the binary distribution
------

Offen is distributed as a single binary file. To kick off your install, download
the latest release:

::

 [isabell@stardust ~]$ mkdir -p ~/tmp/offen-download && cd ~/tmp/offen-download
 [isabell@stardust offen-download]$ curl -sSL https://get.offen.dev | tar -xvz
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
 [isabell@stardust offen-download]$

Next, we should check if the binary matches the signature - i.e. it has not been
altered by 3rd parties - using GPG (this step is optional, but `highly
recommended`):

::

 [isabell@stardust offen-download]$ curl -sSL https://keybase.io/hioffen/pgp_keys.asc | gpg --import
 gpg: Schlüssel C90B8DA1: Öffentlicher Schlüssel "Offen (Signing Binaries) <hioffen@posteo.de>" importiert
 gpg: Anzahl insgesamt bearbeiteter Schlüssel: 1
 gpg:                              importiert: 1  (RSA: 1)
 gpg: keine uneingeschränkt vertrauenswürdigen Schlüssel gefunden
 [isabell@stardust offen-download]$ gpg --verify offen-linux-amd64.asc offen-linux-amd64
 gpg: Signatur vom Mo 22 Jun 2020 09:27:16 CEST mittels RSA-Schlüssel ID C90B8DA1
 gpg: Korrekte Signatur von "Offen (Signing Binaries) <hioffen@posteo.de>"
 gpg: WARNUNG: Dieser Schlüssel trägt keine vertrauenswürdige Signatur!
 gpg:          Es gibt keinen Hinweis, daß die Signatur wirklich dem vorgeblichen Besitzer gehört.
 Haupt-Fingerabdruck  = F20D 4074 068C 636D 58B5  3F46 FD60 FBED C90B 8DA1
 [isabell@stardust offen-download]$

.. note:: GPG will print warnings about the signing key not being certified
    as your Uberspace's keyring is probably empty and does therefore not know
    about anyone who has signed Offen's key. `This is expected behavior`. You
    can check the Offen Keybase_ profile for further proof that this key is
    the correct one.

Next, you can install the Linux binary on your Uberspace:

::

 [isabell@stardust offen-download]$ cp offen-linux-amd64 ~/bin/offen
 [isabell@stardust offen-download]$ cd
 [isabell@stardust ~]$ which offen
 ~/bin/offen
 [isabell@stardust ~]$

.. note:: Our distribution tarball also contains non-Linux binaries which is why
    you also see those `darwin` and `windows` files. If you feel like it, you
    can safely delete the `~/tmp/offen-download` directory after installing.

    ::

     [isabell@stardust ~]$ rm -rf ~/tmp/offen-download
     [isabell@stardust ~]$

Configuration
=============

Create a config file
------

In its most basic configuration, Offen sources configuration values from an
:code:`offen.env` file, that is expected in :code:`~/.config/offen.env`:

::

 [isabell@stardust ~]$ mkdir -p ~/.config
 [isabell@stardust ~]$ touch ~/.config/offen.env
 [isabell@stardust ~]$

Populate the config file
-------------------

For Offen to run on your Uberspace you will need to populate this `.env` file
with the following:

A Secret
------------

Offen requires a unique secret for signing login cookies and certain URLs. You
can use the :code:`offen` command you just installed to create one for you
(passing :code:`-quiet` will make :code:`secret` output the generated value
only):

::

 [isabell@stardust ~]$ echo "OFFEN_SECRET=$(offen secret -quiet)" >> ~/.config/offen.env
 [isabell@stardust ~]$

Database setup
------------

In this setup, Offen stores its data in the MariaDB provided by your Uberspace.
First create a dedicated database for Offen to use:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE isabell_offen"
 [isabell@stardust ~]$

Next, edit the config file at `~/.config/offen.env` and add the dialect and the
connection string (do not overwrite the existing secret):

.. code-block:: ini

 OFFEN_DATABASE_DIALECT=mysql
 OFFEN_DATABASE_CONNECTIONSTRING="isabell:MySuperSecretPassword@tcp(localhost:3306)/isabell_offen?parseTime=true"

SMTP credentials
----

.. note:: Your Uberspace comes with SMTP, so you can definitely use this here
    if you feel like it.

Offen needs to be able to send out transactional emails so you can reset your
password in case you forgot it, and so that you can invite others to collaborate
with you on this instance. To enable Offen to send emails, edit
`~/.config/offen.env` and add the SMTP credentials like this (do not overwrite
the existing values):

.. code-block:: ini

 OFFEN_SMTP_HOST="yoursmtphost.org"
 OFFEN_SMTP_PASSWORD="yoursmtppassword"
 OFFEN_SMTP_USER="isabell@yoursmtphost.org"
 OFFEN_SMTP_SENDER="isabell@yoursmtphost.org"

.. warning:: Offen will start and run without these values being set, but
    remember that you won't be able to reset your password or invite others
    without this. You can always set it at a later point in time though.

Setup daemon
------------

Offen needs to run at all times so it can accept incoming events.

Create a file :code:`~/etc/services.d/offen.ini` and populate it with the
following:

.. code-block:: ini

 [program:offen]
 command=%(ENV_HOME)s/bin/offen
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Point the web backend to Offen
------------

As a last step you need to point your web backend to your Offen instance that
is now running on the default port 3000:

::

 [isabell@stardust ~]$ uberspace web backend set / --http --port 3000
 [isabell@stardust ~]$

.. note:: If you need to run Offen on a port other than 3000, set
    `OFFEN_SERVER_PORT` in your configuration file.


Finishing installation
======================

Point your browser to the `https://offen.yourdomain.org/setup/` page and create
your user and a first account.

Embedding Offen on your website
======================

All you need to do to embed your Offen install on a website is to add the
script to your document:

.. code-block:: html

 <script async src="https://offen.yourdomain.org/script.js" data-account-id="<YOUR_ACCOUNT_ID>"></script>

.. note:: You will also find this snippet for copy / pasting when you log in to
    your account.

Official docs
=======

Offen has a dedicated documentation site that will tell you a lot more about
how to use and configure Offen: https://docs.offen.dev

Updates
=======

.. note:: Check our Twitter_ or our Releases_ page regularly to stay informed
    about the newest version.


.. _Offen: https://www.offen.dev
.. _Releases: https://github.com/offen/offen/releases
.. _Twitter: https://twitter.com/hioffen
.. _Keybase: https://keybase.io/hioffen

----

Tested with Offen v0.1.0, Uberspace 7.7

.. author_list::
