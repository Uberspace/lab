.. author:: luto <http://luto.at>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: version-control

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitea.png
      :align: center

#####
Gitea
#####

.. tag_list::

Gitea_ is a painless self-hosted Git service written in Go and distributed under the MIT License, designed to provide
similar core functionality as GitLab or GitHub, but at a much smaller resource footprint. The project started as a fork
of the then-popular Gogs_, but quickly became more active and bigger than the original.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

You need a database for gitea:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_gitea"
  [isabell@stardust ~]$

Your gitea URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Like a lot of Go software, gitea is distributed as a single binary. Download Gitea's latest `release <https://github.com/go-gitea/gitea/releases/latest>`_,
verify the checksum specified in the respective ``.sha256`` file and finally
make sure that the file can be executed.

::

  [isabell@stardust ~]$ mkdir ~/gitea
  [isabell@stardust ~]$ wget -O gitea/gitea https://github.com/go-gitea/gitea/releases/download/v1.7.2/gitea-1.7.2-linux-amd64
  Resolving dl.gitea.io (github.com)... 2400:cb00:2048:1::681b:8e9b, 2400:cb00:2048:1::681b:8f9b, 104.27.142.155, ...
  Connecting to dl.gitea.io (github.com)|2400:cb00:2048:1::681b:8e9b|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 52960072 (51M) [application/octet-stream]
  Saving to: gitea/gitea’

  100%[=======================================================>] 52,960,072  9.99MB/s   in 5.8s

  2018-09-16 18:36:36 (8.72 MB/s) - gitea/gitea’ saved [60473144/60473144]
  [isabell@stardust ~]$ sha256sum gitea/gitea
  b84098f0b0018071aa1ba5522078820494def29e6385c25c581c4362a4e463b3 gitea/gitea
  [isabell@stardust ~]$ chmod +x gitea/gitea
  [isabell@stardust ~]$

Configuration
=============

Change the configuration
------------------------

You need to create a custom directory

::

  [isabell@stardust ~]$ mkdir -p ~/gitea/custom/conf/
  [isabell@stardust ~]$


and a new config file at ``~/gitea/custom/conf/app.ini`` to specify the port and domain and to disable public registration:

.. code-block:: ini

  [server]
  HTTP_PORT = 9000
  DOMAIN = isabell.uber.space
  ROOT_URL = https://%(DOMAIN)s

  [service]
  DISABLE_REGISTRATION = true

Gitea provides many other configuration options. Take a look at the Documentation_
to learn more.

Configure web server
--------------------

.. note::

    Gitea is running on port 9000.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/gitea.ini`` with the following content:

.. code-block:: ini

  [program:gitea]
  command=%(ENV_HOME)s/gitea/gitea web

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to the ``/install`` path on your domain to finish the installation.

.. note:: Using the same public key for Gitea and your Uberspace will prevent you from logging in with this key via SSH. Login via password still works as expected, you can use the Dashboard_ to manage your keys.

SSH key management through gitea
================================

If you want that gitea manages SSH authorized_keys you can do:

::

 [isabell@stardust ~]$ ln -s ~/.ssh ~/gitea/

Add your key in gitea and then change the line in ``.ssh/authorized_keys`` to the following:

.. code-block:: sh

 command="if [ -t 0 ]; then bash; elif [[ $SSH_ORIGINAL_COMMAND =~ ^(scp|rsync|mysqldump).* ]]; then eval $SSH_ORIGINAL_COMMAND; else /home/<username>/gitea/gitea serv key-1 --config='/home/<username>/gitea/custom/conf/app.ini'; fi",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-...

.. warning:: Replace ``<username>`` with your username and put your public key after ``ssh-``!

Tuning
======

You can easily add AsciiDoc rendering to Gitea. Install asciidoctor via ruby gems:

::

 [isabell@stardust ~]$ gem install asciidoctor

Edit your config file at ``~/gitea/custom/conf/app.ini`` to enable asciidoctor in Gitea:

.. code-block:: ini

  [markup.asciidoc]
  ENABLED = true
  FILE_EXTENSIONS = .adoc,.asciidoc
  RENDER_COMMAND = "asciidoctor -e -a leveloffset=-1 --out-file=- -"
  IS_INPUT_FILE = false

In the end stop (``supervisorctl stop gitea``) and restart (``supervisorctl stop gitea``) Gitea. Try it with a .adoc or .asciidoc file.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Gitea's `releases <https://github.com/go-gitea/gitea/releases/latest>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop gitea`` and repeat the "Installation" step followed by ``supervisorctl start gitea`` to restart gitea.

.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _Documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gitea 1.11.4, Uberspace 7.6.0

.. author_list::
