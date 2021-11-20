.. highlight:: console

.. author:: knhash <https://knhash.in>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: streaming
.. tag:: mediaplayer
.. tag:: gallery


.. sidebar:: About

  .. image:: _static/images/jellyfin.svg
      :align: center

##########
Jellyfin
##########

.. tag_list::

Jellyfin is the volunteer-built media solution that puts you in control of your media. Stream to any device from your own server, with no strings attached. Your media, your server, your way.

You can use Jellyfin alongside :lab:`Syncthing <guide_syncthing>`, to load your media onto Uberspace for streaming.

----

.. note:: For this guide you should be familiar with the basic concepts of

  - :manual:`supervisord <daemons-supervisord>`
  - :manual:`domains <web-domains>`

License
=======

The software is licensed under `GNU General Public License v2.0`_. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

Your dashboard URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Create a directory in ``/home/isabell`` for jellyfin and its files.

.. code-block:: bash

  [isabell@stardust ~]$ mkdir ~/jellyfin
  [isabell@stardust ~]$

Download the combined archive from release_, including both the server and WebUI, as we will need both of them.

.. code-block:: bash

  [isabell@stardust ~]$ wget -O ~/jellyfin/jellyfin.tar.gz https://repo.jellyfin.org/releases/server/linux/stable/combined/jellyfin_10.7.7_amd64.tar.gz
  [isabell@stardust ~]$

Extract the archive. Delete the archive post extraction.

.. code-block:: bash

  [isabell@stardust ~]$ tar -xvzf ~/jellyfin/jellyfin.tar.gz  -C jellyfin
  [isabell@stardust ~]$ rm ~/jellyfin/jellyfin.tar.gz
  [isabell@stardust ~]$

Create a symbolic link to the Jellyfin 10.7.7 directory. This allows an upgrade by repeating the above steps and enabling it by simply re-creating the symbolic link to the new version.

.. code-block:: bash

  [isabell@stardust ~]$ ln -s ~/jellyfin/jellyfin_10.7.7 ~/jellyfin/jellyfin
  [isabell@stardust ~]$

Create four sub-directories for Jellyfin data, and one to store your media library.

.. code-block:: bash

  [isabell@stardust ~]$  mkdir data cache config log library
  [isabell@stardust ~]$

Create a small script to run Jellyfin, ``jellyfin.sh`` in ``~/jellyfin`` with the following content.

.. code-block:: sh
  :emphasize-lines: 2

  #!/bin/bash
  JELLYFINDIR="/home/isabell/jellyfin"

  $JELLYFINDIR/jellyfin/jellyfin \
  -d $JELLYFINDIR/data \
  -C $JELLYFINDIR/cache \
  -c $JELLYFINDIR/config \
  -l $JELLYFINDIR/log

Make the startup script above executable.

.. code-block:: bash

  [isabell@stardust ~]$  chmod u+x ~/jellyfin/jellyfin.sh
  [isabell@stardust ~]$

Configuration
=============

Configure the web server
------------------------

.. note::
    Jellyfin will run on port 8096.

.. include:: includes/web-backend.rst

Set up the daemon
-----------------

To start Jellyfin automatically and run it in the background, create ``~/etc/services.d/jellyfin.ini`` with the following content:

.. code-block:: ini

  [program:jellyfin]
  command=bash %(ENV_HOME)s/jellyfin/jellyfin.sh

.. include:: includes/supervisord.rst

.. note::

  If `jellyfin` is not ``RUNNING``, check your configuration and the logs using ``supervisorctl maintail``.

Finishing installation
======================

User Setup
------------------

Point your browser to ``https://isabell.uber.space/`` and follow the initial setup wizard.

.. note::

  - Under ``Setup your media libraries``, you can point it to your previously created Library: ``/home/isabell/jellyfin/library``.
  - Libraries and users can always be added later from the dashboard.
  - Remember the username and password so you can login after the setup.


Tuning
------

.. warning::
  Jellyfin transcodes media and that's *very* CPU heavy work, and as such may not be particularly suited for shared hosting.

Make sure to go into the Admin Dashboard and set the ``Transcoding thread count`` to 1.

.. code-block:: besteffort

  -> [Hamburger-Menu] -> [Admin - Dashboard]
  -> [Server - Playback] -> [Transcoding thread count] : Set to 1
  -> [Scroll all the way down] -> [Save]


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _release: https://repo.jellyfin.org/releases/server/linux/stable/
.. _GNU General Public License v2.0: https://github.com/jellyfin/jellyfin/blob/master/LICENSE
.. _GitHub: https://github.com/jellyfin/jellyfin
.. _feed: https://jellyfin.org/index.xml
----

Tested with Jellyfin 10.7.7, Uberspace 7.11.5

.. author_list::
