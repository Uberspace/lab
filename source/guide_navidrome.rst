.. highlight:: console
.. author:: marci <marci@uber.space>
.. tag:: React
.. tag:: web
.. tag:: mediaplayer
.. tag:: streaming
.. tag:: Subsonic
.. tag:: golang
.. tag:: JavaScript

.. sidebar:: Logo

  .. image:: _static/images/navidrome.png
      :align: center

#########
Navidrome
#########

.. tag_list::


Navidrome_ allows you to enjoy your music collection from anywhere, by making it available through a modern Web UI and through a wide range of third-party compatible mobile apps.

If you want to try out Navidrome without installing it first, visit the demo-page_.



----

Prerequisites
=============

Our Navidrome URL needs to be setup:

.. include:: includes/web-domain-list.rst

You need a directory to store the Navidrome executable, a directory as Navidrome working directory, and a directory for the music-files:

.. code-block:: console

  [isabell@stardust ~]$ mkdir --parents ~/opt/navidrome
  [isabell@stardust ~]$ mkdir --parents ~/var/lib/navidrome
  [isabell@stardust ~]$ mkdir --parents ~/music
  [isabell@stardust ~]$

Installation
============

Now  download the latest release and it's checksum from the github-page_:

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/navidrome/navidrome/releases/download/v0.47.5/navidrome_0.47.5_Linux_x86_64.tar.gz
  [isabell@stardust ~]$ wget https://github.com/navidrome/navidrome/releases/download/v0.47.5/navidrome_checksums.txt
  [isabell@stardust ~]$

After downloading, check the integrity of the tar-archive. If hashsums are matching, extract the archive to our directory for the executable of Navidrome:

.. code-block:: console

  [isabell@stardust ~]$ sha256sum --check navidrome_checksums.txt 2>&1 | grep Linux_x86_64
  [isabell@stardust ~]$ navidrome_0.47.5_Linux_x86_64.tar.gz: OK
  [isabell@stardust ~]$ tar -xvzf navidrome_0.47.5_Linux_x86_64.tar.gz -C ~/opt/navidrome
  LICENSE
  README.md
  navidrome
  [isabell@stardust ~]$

The downloaded files can then be deleted:

.. code-block:: console

  [isabell@stardust ~]$ rm navidrome_0.47.5_Linux_x86_64.tar.gz
  [isabell@stardust ~]$ rm navidrome_checksums.txt
  [isabell@stardust ~]$


Configuration
=============

Create config file
------------------
Create the configuration-file ``~/var/lib/navidrome/navidrome.toml`` and add the following line:

.. code-block:: ini

 MusicFolder = '/home/<username>/music/'

For a more detailed configuration check the configuration-options-page_.

Setup daemon
------------
Setup the service for Navidrome and therefore create ``~/etc/services.d/navidrome.ini`` with the following content:

.. code-block:: ini

 [program:navidrome]
 directory=%(ENV_HOME)s/var/lib/navidrome
 command=%(ENV_HOME)s/opt/navidrome/navidrome --configfile %(ENV_HOME)s/var/lib/navidrome/navidrome.toml
 startsecs=60
 autorestart=yes


.. include:: includes/supervisord.rst

By default Navidrome is running on port 4533.

.. include:: includes/web-backend.rst


Finishing installation
======================

Now, create an admin account by visiting https://isabell.uber.space with your favorite browser. And of course, use a good password for the administrator-account!

Best practices
==============

To get music into Navidrome, tag the music-files on your personal computer and afterwards upload them via rsync over ssh:

.. code-block:: console

  [isabell@stardust ~]$ rsync --recursive --times --progress --protect-args /home/isabell/music/ isabell.uber.space:/home/isabell/music
  [isabell@stardust ~]$

Updates
=======

.. note:: Check the `release-page`_ regularly to stay informed about updates.

To upgrade, unzip the new code-archive into ``~/opt/navidrome/`` and restart our navidrome-service:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart navidrome
  [isabell@stardust ~]$


Debugging
=========
You can check the service’s log file using:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl tail navidrome stderr
  [isabell@stardust ~]$



.. _demo-page: https://www.navidrome.org/demo/
.. _Navidrome: https://www.navidrome.org/
.. _github-page: https://github.com/navidrome/navidrome
.. _release-page: https://github.com/navidrome/navidrome/releases
.. _configuration-options-page: https://www.navidrome.org/docs/usage/configuration-options/

----

Tested with Navidrome v0.47.5 and Uberspace v7.13.0

.. author_list::
