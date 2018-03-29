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

You'll need your MySQL credentials_. Get them with ``my_print_defaults``:

::

 [gitea@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=gitea
 --password=MySuperSecretPassword
 [gitea@stardust ~]$ 

Your gitea URL needs to be setup:

::

 [gitea@stardust ~]$ uberspace web domain list
 ghost.uber.space
 [gitea@stardust ~]$ 

Installation
============

Like a lot of Go software, gitea is distributed as a single binary. Download it,
verify the checksum specified in the respective ``.sha256`` file and finally
make sure that the file can be executed.

::

  [gitea@stardust ~]$ mkdir ~/gitea
  [gitea@stardust ~]$ wget -O gitea/gitea https://dl.gitea.io/gitea/42.23.11/gitea-42.23.11-linux-amd64
  Resolving dl.gitea.io (dl.gitea.io)... 2400:cb00:2048:1::681b:8e9b, 2400:cb00:2048:1::681b:8f9b, 104.27.142.155, ...
  Connecting to dl.gitea.io (dl.gitea.io)|2400:cb00:2048:1::681b:8e9b|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 52960072 (51M) [application/octet-stream]
  Saving to: gitea/gitea’

  100%[=======================================================>] 52,960,072  9.99MB/s   in 5.8s   

  2018-03-25 18:36:36 (8.72 MB/s) - gitea/gitea’ saved [52960072/52960072]
  [gitea@stardust ~]$ sha256sum gitea/gitea
  6914f61121847bf7aad66ec63079fbf84c3be91ac9b0aade16e92f657155cd39  bin/gitea
  [gitea@stardust ~]$ chmod +x gitea/gitea
  [gitea@stardust ~]$

Configuration
=============

Configure port
--------------

Since Gitea uses its own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Change the configuration
------------------------

You need to create a new config file at ``~/gitea/custom/conf/app.ini`` to specify the
desired port, domain and disable public registration:

::

  [server]
  HTTP_PORT = 9000
  DOMAIN = gitea.uber.space
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

.. warning:: Replace ``<username>`` with your username!

.. code-block:: ini

  [program:gitea]
  command=/home/<username>/gitea/gitea web

In our example this would be:

.. code-block:: ini

  [program:gitea]
  command=/home/gitea/gitea/gitea web

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [gitea@stardust ~]$ supervisorctl reread
 gitea: available
 [ghost@stardust ~]$ supervisorctl update
 gitea: added process group
 [gitea@stardust ~]$ supervisorctl status
 gitea                            RUNNING   pid 26020, uptime 0:03:14
 [gitea@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your gitea URL and finish the installation.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Gitea's `releases <https://github.com/go-gitea/gitea/releases/latest>`_ for the latest version. If a newer
version is available, repeat the "Installation" step followed by ``supervisorctl restart gitea`` to restart gitea.

.. _Gitea: https://gitea.io/en-US/
.. _Gogs: https://gogs.io
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _Documentation: https://docs.gitea.io/en-us/config-cheat-sheet/
.. _feed: https://github.com/go-gitea/gitea/releases.atom
