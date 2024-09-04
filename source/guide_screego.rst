.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-go
.. tag:: ports
.. tag:: screen-sharing
.. tag:: webRTC

.. sidebar:: Logo

  .. image:: _static/images/screego.png
      :align: center

#######
screego
#######

.. tag_list::

screego_ is an open-source software that provides screen sharing via WebRTC. A demo can be found at https://app.screego.net.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall ports <basics-ports>`
  * :manual:`HTTPS <web-https>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here:

  * https://github.com/screego/server/blob/master/LICENSE

Prerequisites
=============

To make the application accessible from the outside, open two `ports in the firewall <firewall_>`_:

.. code-block:: console

  [isabell@stardust ~]$ uberspace port add
  Port 40130 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$ uberspace port add
  Port 40131 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$

Installation
============

Create a new directory, enter the directory you just created, download the latest version, unpack the archive, delete the archive afterwards and make the binary executable:

.. note:: Replace ``1.10.5`` with the version of the `latest release`_.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/screego
 [isabell@stardust ~]$ cd ~/screego
 [isabell@stardust screego]$ wget "https://github.com/screego/server/releases/download/v1.10.5/screego_1.10.5_linux_amd64.tar.gz"
 [isabell@stardust screego]$ tar xvf screego_1.10.5_linux_amd64.tar.gz
 [isabell@stardust screego]$ rm screego_1.10.5_linux_amd64.tar.gz
 [isabell@stardust screego]$ chmod +x screego
 [isabell@stardust screego]$

Configuration
=============

Configure screego
-----------------

.. note:: You can use the following command to generate your own ``SCREEGO_SECRET``: ``tr -dc A-Za-z0-9 < /dev/urandom | head -c 40; echo``

.. warning:: Replace ``isabell`` with your username, ``X940rRflEAWtVQvtPmCKgsj1WoJ8IoNZ2tEaDSxZ`` with your secret and ``40130``/``40131`` with your ports!

The following settings must be adjusted in the ``~/screego/screego.config``:

::

 SCREEGO_EXTERNAL_IP=dns:isabell.uber.space

 SCREEGO_SECRET=X940rRflEAWtVQvtPmCKgsj1WoJ8IoNZ2tEaDSxZ

 SCREEGO_SERVER_TLS=true

 SCREEGO_TLS_CERT_FILE=/readonly/isabell/certificates/isabell.uber.space.crt

 SCREEGO_TLS_KEY_FILE=/readonly/isabell/certificates/isabell.uber.space.key
 
 SCREEGO_SERVER_ADDRESS=0.0.0.0:40130
 
 SCREEGO_TURN_ADDRESS=0.0.0.0:40131
             
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

Open website
------------
.. warning:: Replace ``isabell`` with your username and ``40130`` with your port!

If screego is running, you can find the website here:

  * https://isabell.uber.space:40130/

Best practices
==============

Security
--------

Keep the software up to date.

If you do not want third parties to be able to connect to your server, then set ``SCREEGO_AUTH_MODE=auto`` in the ``screego.config`` file so that a login with username and password is always mandatory (the command ``./screego hash -h`` can help you to create a user file required for this).

Updates
=======

.. note:: Check the `GitHub release page <latest release_>`_ regularly to stay informed about the newest version.

To update the software, download the latest version and replace all files (``LICENSE``, ``README.md``, ``screego`` and ``screego.config.example``). Also check if there are any changes in the ``screego.config.example`` compared to your currently used ``screego.config``.

.. _screego: https://screego.net
.. _firewall: https://manual.uberspace.de/basics-ports.html
.. _latest release: https://github.com/screego/server/releases

----

Tested with screego 1.10.5, Uberspace 7.16.0

.. author_list::
