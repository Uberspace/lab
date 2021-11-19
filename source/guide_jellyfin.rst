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

We will install Jellyfin as a self contained binary. To install the stable version of Jellyfin, we will download the `.tar.gz` files from release_, then use a TAR utility to extract the files and launch `jellyfin`.

We will pick up the combined archives, including both the server and WebUI, as we need both of them.

Make some space
---------------
.. code-block:: bash

  [isabell@stardust ~]$ mkdir ~/jellyfin
  [isabell@stardust ~]$

Download the source
-------------------
.. code-block:: bash

  [isabell@stardust ~]$ wget -O ~/jellyfin/jellyfin.tar.gz https://repo.jellyfin.org/releases/server/linux/stable/combined/jellyfin_10.7.7_amd64.tar.gz
  [isabell@stardust ~]$

Extract the binary
---------------
.. code-block:: bash

  [isabell@stardust ~]$ tar --strip-components=1 -xzf ~/jellyfin/jellyfin.tar.gz -C jellyfin
  [isabell@stardust ~]$ rm ~/jellyfin/jellyfin.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Configure the web server
------------------------

.. note::
    Syncthing is running on port 8096.

.. include:: includes/web-backend.rst

Set up the daemon
-----------------

To start Jellyfin automatically and run it in the background, create ``~/etc/services.d/jellyfin.ini`` with the following content:

.. code-block:: ini

  [program:jellyfin]
  command=%(ENV_HOME)s/jellyfin/jellyfin_10.7.7/jellyfin

.. include:: includes/supervisord.rst

.. note::

  If `jellyfin` is not ``RUNNING``, check your configuration and the logs using ``supervisorctl maintail``.

Finishing installation
======================

Point your browser to ``https://isabell.uber.space/`` and follow the initial setup wizard.

-  Libraries and users can always be added later from the dashboard.
- Remember the username and password so you can login after the setup.

Best practices
==============

Tuning
------

.. warning::
  Jellyfin transcodes media and that's *very* CPU heavy work, and as such may not be particularly suited for shared hosting.

Make sure to go into the Admin Dashboard and set the ``Transcoding thread count`` to 1.

.. code-block:: besteffort

  -> [Hamburger-Menu] -> [Admin - Dashboard]
  -> [Server - Playback] -> [Transcoding thread count] : Set to 1



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
