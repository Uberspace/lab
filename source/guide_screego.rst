.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-go
.. tag:: ports
.. tag:: screen-sharing
.. tag:: self-hosting
.. tag:: STUN
.. tag:: TURN
.. tag:: WebRTC

.. sidebar:: Logo

  .. image:: _static/images/screego.png
      :align: center

#######
Screego
#######

.. tag_list::

Screego_ is an open-source software that provides screen sharing via WebRTC. A demo can be found at https://app.screego.net.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`

License
=======

All relevant legal information can be found here:

  * https://github.com/screego/server/blob/master/LICENSE

Prerequisites
=============

.. include:: includes/open-port.rst

Installation
============

Create a new directory, enter the directory you just created, download the latest version, unpack the archive, delete the archive afterwards, make the binary executable and create the file ``screego.config`` as a copy of the file ``screego.config.example``:

.. note:: Replace ``1.11.1`` with the version of the `latest release`_.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/screego
 [isabell@stardust ~]$ cd ~/screego
 [isabell@stardust screego]$ wget "https://github.com/screego/server/releases/download/v1.11.1/screego_1.11.1_linux_amd64.tar.gz"
 [isabell@stardust screego]$ tar xvf screego_1.11.1_linux_amd64.tar.gz
 [isabell@stardust screego]$ rm screego_1.11.1_linux_amd64.tar.gz
 [isabell@stardust screego]$ chmod +x screego
 [isabell@stardust screego]$ cp screego.config.example screego.config
 [isabell@stardust screego]$

Configuration
=============

Configure Screego
-----------------

.. note:: You can use the following command to generate your own ``SCREEGO_SECRET``: ``tr -dc A-Za-z0-9 < /dev/urandom | head -c 40; echo``

.. warning:: Replace ``isabell`` with your username, ``<YOUR_SECRET>`` with your secret and ``40132`` with your port!

The following settings must be adjusted in the ``~/screego/screego.config``:

::

 SCREEGO_EXTERNAL_IP=dns:isabell.uber.space

 SCREEGO_SECRET=<YOUR_SECRET>
 
 SCREEGO_TURN_ADDRESS=0.0.0.0:40132

.. note::
  Please have a look at "`NAT Traversal`_" on the official project page. In most cases STUN should be sufficient, but if TURN is used it is necessary to open more ports and specify them under ``SCREEGO_TURN_PORT_RANGE`` in the ``screego.config`` file. For the number of ports to be opened, the following currently applies approximately: ``shared video streams * users in the room * 4``
  There is also a `bug in the TURN server`_ which results in not all connections being properly cleaned up. This means that even more ports may be required.

Setup daemon
------------

Create ``~/etc/services.d/screego.ini`` with the following content:

::

 [program:screego]
 directory=%(ENV_HOME)s/screego/
 command=%(ENV_HOME)s/screego/screego serve
 autostart=yes
 autorestart=yes
 startsecs=30
             
.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Setup web backend
-----------------

.. note:: The default port for Screego is ``5050``.

.. include:: includes/web-backend.rst

.. warning:: Replace ``isabell`` with your username!

If Screego is running, you can now find the website at ``https://isabell.uber.space``.

Best practices
==============

Security
--------

Keep the software up to date.

If you do not want third parties to be able to create new rooms on your server, then set ``SCREEGO_AUTH_MODE=all`` in the ``screego.config`` file so that a login with username and password is mandatory (the command ``./screego hash -h`` can help you to create a user file required for this). If you want to prevent someone from entering an existing room via the direct link that exists for each room, choose a more complex room ID.

Updates
=======

.. note:: Check the `GitHub release page <latest release_>`_ regularly to stay informed about the newest version.

To update the software, download the latest version and replace all files (``LICENSE``, ``README.md``, ``screego`` and ``screego.config.example``). Also check if there are any changes in the ``screego.config.example`` compared to your currently used ``screego.config``.

.. _Screego: https://screego.net
.. _firewall: https://manual.uberspace.de/basics-ports.html
.. _latest release: https://github.com/screego/server/releases
.. _NAT Traversal: https://screego.net/#/nat-traversal
.. _bug in the TURN server: https://github.com/pion/turn/issues/246

----

Tested with Screego 1.11.1, Uberspace 7.16.1

.. author_list::
