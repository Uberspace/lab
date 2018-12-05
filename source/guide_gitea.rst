.. author:: luto <luto.at>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitea.png
      :align: center

#####
Gitea
#####

Gitea_ is a painless self-hosted Git service written in Go and distributed under the MIT License, designed to provide
similar core functionality as GitLab or GitHub, but at a much smaller resource footprint. The project started as a fork
of the then-popular Gogs_, but quickly became more active and bigger than the original.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * supervisord_
  * domains_

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

You need a database for gitea:

.. warning:: Replace ``<username>`` with your username!

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_gitea"
  [isabell@stardust ~]$

Your gitea URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Like a lot of Go software, gitea is distributed as a single binary. Download Gitea's latests `release <https://github.com/go-gitea/gitea/releases/latest>`_,
verify the checksum specified in the respective ``.sha256`` file and finally
make sure that the file can be executed.

::

  [isabell@stardust ~]$ mkdir ~/gitea
  [isabell@stardust ~]$ wget -O gitea/gitea https://github.com/go-gitea/gitea/releases/download/v1.5.3/gitea-1.5.3-linux-amd64
  Resolving dl.gitea.io (github.com)... 2400:cb00:2048:1::681b:8e9b, 2400:cb00:2048:1::681b:8f9b, 104.27.142.155, ...
  Connecting to dl.gitea.io (github.com)|2400:cb00:2048:1::681b:8e9b|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 52960072 (51M) [application/octet-stream]
  Saving to: gitea/gitea’

  100%[=======================================================>] 52,960,072  9.99MB/s   in 5.8s

  2018-09-16 18:36:36 (8.72 MB/s) - gitea/gitea’ saved [60473144/60473144]
  [isabell@stardust ~]$ sha256sum gitea/gitea
  ae4f43f73acbd0b61fbca78385a017d7aaed6f7d50f2bff5c3f057acfb46c71a gitea/gitea
  [isabell@stardust ~]$ chmod +x gitea/gitea
  [isabell@stardust ~]$

Configuration
=============

Configure port
--------------

Since Gitea uses its own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Change the configuration
------------------------

You need to create a custom directory

::

  [isabell@stardust ~]$ mkdir -p ~/gitea/custom/conf/
  [isabell@stardust ~]$


and a new config file at ``~/gitea/custom/conf/app.ini`` to specify the
desired port, domain and disable public registration:

.. code-block:: ini

  [server]
  HTTP_PORT = 9000
  DOMAIN = isabell.uber.space
  ROOT_URL = https://%(DOMAIN)s

  [service]
  DISABLE_REGISTRATION = true

Gitea provides many other configuration options. Take a look at the Documentation_
to learn more.

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

Create ``~/etc/services.d/gitea.ini`` with the following content:

.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: ini

  [program:gitea]
  command=%(ENV_HOME)s/gitea/gitea web -port <yourport>

In our example this would be:

.. code-block:: ini

  [program:gitea]
  command=%(ENV_HOME)s/gitea/gitea web -port 9000

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 gitea: available
 [isabell@stardust ~]$ supervisorctl update
 gitea: added process group
 [isabell@stardust ~]$ supervisorctl status
 gitea                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your gitea URL and finish the installation.

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

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Gitea's `releases <https://github.com/go-gitea/gitea/releases/latest>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop gitea`` and repeat the "Installation" step followed by ``supervisorctl start gitea`` to restart gitea.

.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _Documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Gitea 1.5.3, Uberspace 7.1.16

.. authors::
