.. highlight:: console

.. author:: Frederik Ring <hioffen@posteo.de>

.. tag:: analytics
.. tag:: web
.. tag:: lang-go

.. sidebar:: Logo

  .. image:: _static/images/offen.png
      :align: center

##########
Offen
##########

.. tag_list::

Offen_ is a fair alternative to common web analytics tools.
Gain insights while your users have full access to their data.

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
    `offen.yourdomain.org`. You can use the `username.uber.space` domain if you
    want to, but that will make Offen issue 3rd party cookies, which are subject
    to blocking in many scenarios. A domain can be added at a later point in
    time though.

Installation
============

Download the binary distribution
------

Offen is distributed as a single binary file. To kick off your install, download
the latest release:

::

 [isabell@stardust ~]$ mkdir tmp/offen-download && cd tmp/offen-download
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

Check if the download contains the expected contents:

::

 [isabell@stardust offen-download]$ md5sum -c checksums.txt
 offen-darwin-10.6-amd64: OK
 offen-darwin-10.6-amd64.asc: OK
 offen-linux-amd64: OK
 offen-linux-amd64.asc: OK
 offen-windows-4.0-amd64.exe: OK
 offen-windows-4.0-amd64.exe.asc: OK

Next, you can install the Linux binary on your Uberspace:

::

 [isabell@stardust offen-download]$ cp offen-linux-amd64 /home/isabell/bin/offen
 [isabell@stardust offen-download]$ cd
 [isabell@stardust ~]$ which offen
 ~/bin/offen

.. note:: Our distribution tarball also contains non-Linux binaries which is why
    you also see those `darwin` and `windows` files. If you feel like it, you
    can safely delete the tmp/offen-download directory after installing.

Configuration
=============

Create a config file
------

In its most basic configuration, Offen sources configuration values from an
:code:`offen.env` file, that is expected in :code:`~/.config/offen.env`:

::

 [isabell@stardust ~]$ mkdir -p .config
 [isabell@stardust ~]$ touch offen.env

Populate the config file
-------------------

For Offen to run on your Uberspace you will need to populate this `.env` file
with the following:

A Secret
------------

Offen requires a unique secret for signing login cookies and certain URLs. You
can use the :code:`offen` command you just installed to create one for you:

::

 [isabell@stardust ~]$ echo "OFFEN_SECRET=$(offen secret -quiet)" >> .config/offen.env

Database setup
------------

On your Uberspace, Offen stores its data in a local SQLite file that you can
store anywhere you want to. In this example we put it in an :code:`~/offen`
directory:

::

 [isabell@stardust ~]$ mkdir -p offen
 [isabell@stardust ~]$ touch offen/data.sqlite

Next, add the location of the SQLite file to your config file:

::

 [isabell@stardust ~]$ echo "OFFEN_DATABASE_CONNECTIONSTRING=/home/isabell/offen/data.sqlite" >> .config/offen.env

SMTP credentials
----

.. note:: Your Uberspace comes with email and SMTP, so you can definitely
    use this here if you feel like it.

Offen needs to be able to send out transactional emails so you can reset your
password in case you forgot it, and so that you can invite others to collaborate
with you on this instance. To enable Offen to send emails, set the following
SMTP credentials in your config file:

::

 [isabell@stardust ~]$ cat >> .config/offen.env << EOF
 > OFFEN_SMTP_HOST="yoursmtphost.org"
 > OFFEN_SMTP_PASSWORD="yoursmtppassword"
 > OFFEN_SMTP_USER="isabell@yoursmtphost.org"
 > OFFEN_SMTP_SENDER="isabell@yoursmtphost.org"
 > EOF

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
 command=/home/isabell/bin/offen
 autostart=yes
 autorestart=yes

Afterwards, ask supervisord to look for new .ini files:

::

 [isabell@stardust ~]$ supervisorctl reread
 offen: available

You are ready to start the daemon now:

::

 [isabell@stardust ~]$ supervisorctl update
 offen: added process group

Point the web backend to Offen
------------

As a last step you need to point your web backend to your Offen instance that
is now running on the default port 3000:

::

 [isabell@stardust ~]$ uberspace web backend set / --http --port 3000

.. note:: If you need to run Offen on a port other than 3000, set
    `OFFEN_SERVER_PORT` in your configuration file.


Finishing installation
======================

Point your browser to the `/setup` page on your domain and create your user
and a first account.

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

----

Tested with Offen v0.1.0-alpha.8, Uberspace 7.7

.. author_list::
