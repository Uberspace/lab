.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-rust
.. tag:: ports
.. tag:: remote-desktop
.. tag:: self-hosting

.. sidebar:: Logo

  .. image:: _static/images/rustdesk.svg
      :align: center

########
RustDesk
########

.. tag_list::

RustDesk_ is an open-source remote desktop software that allows remote access to and control of other computers. In addition to a client, which is available for various operating systems, a server compound is also required for `hole punching`_ (see: `How does RustDesk work?`_). Although there are public servers, it is possible to host a RustDesk server yourself, as there is a free version (`RustDesk Server`_) in addition to a paid version (RustDesk Server Pro).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here:

  * https://github.com/rustdesk/rustdesk-server/blob/master/LICENSE

Prerequisites
=============

To make the application accessible from the outside, open three `ports in the firewall <firewall_>`_:

.. code-block:: console
 :emphasize-lines: 1,3,5

  [isabell@stardust ~]$ uberspace port add
  Port 40130 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$ uberspace port add
  Port 40131 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$ uberspace port add
  Port 40132 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$


At least two of these should be consecutive, as one of them cannot be specified explicitly, but results from the other selected port. In our case, we will specify ``40131`` and ``40132`` explicitly later (see :ref:`setup-daemon`), ``40130`` will then be used automatically.

Installation
============

Create a new directory, enter the directory you just created, download the latest version, unpack the archive and delete it afterwards:

.. note:: Replace ``1.1.10-3`` with the version of the `latest release`_.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/rustdesk
 [isabell@stardust ~]$ cd ~/rustdesk
 [isabell@stardust rustdesk]$ wget "https://github.com/rustdesk/rustdesk-server/releases/download/1.1.10-3/rustdesk-server-linux-amd64.zip"
 [isabell@stardust rustdesk]$ unzip -j rustdesk-server-linux-amd64.zip
 [isabell@stardust rustdesk]$ rm rustdesk-server-linux-amd64.zip
 [isabell@stardust rustdesk]$

Configuration
=============

.. _setup-daemon:
             
Setup daemons
-------------

.. warning:: Replace ``isabell`` with your username and ``40131``/``40132`` with your ports!

Create ``~/etc/services.d/rustdesk_hbbs.ini`` with the following content:

::

 [program:rustdesk_hbbs]
 directory=%(ENV_HOME)s/rustdesk/
 command=%(ENV_HOME)s/rustdesk/hbbs -r isabell.uber.space:40132 -p 40131 -k _
 autostart=yes
 autorestart=yes
 startsecs=30

Create ``~/etc/services.d/rustdesk_hbbr.ini`` with the following content:

::

 [program:rustdesk_hbbr]
 directory=%(ENV_HOME)s/rustdesk/
 command=%(ENV_HOME)s/rustdesk/hbbr -p 40132 -k _
 autostart=yes
 autorestart=yes
 startsecs=30

Explanation of used parameters:

::

  -r: Specifies a relay server so that the client doesn't have to.
  -p: Specifies a custom port.
  -k: "-k _" prevents users from establishing unencrypted connections by requiring a key.
             
After creating the configuration, tell supervisord to refresh its configuration and start the services:

.. code-block:: console
 :emphasize-lines: 1,4,7

 [isabell@stardust ~]$ supervisorctl reread
 rustdesk_hbbr: available
 rustdesk_hbbs: available
 [isabell@stardust ~]$ supervisorctl update
 rustdesk_hbbr: added process group
 rustdesk_hbbs: added process group
 [isabell@stardust ~]$ supervisorctl status
 rustdesk_hbbr                            RUNNING   pid 26020, uptime 0:03:14
 rustdesk_hbbs                            RUNNING   pid 26021, uptime 0:03:14
 [isabell@stardust ~]$      

If they are not in the RUNNING state, check your configuration.

Setup client
------------

.. note:: These settings may be located elsewhere on mobile devices and/or have a slightly different name.

When you start the client for the first time, the line "**Ready, For faster connection, please set up your own server**" will be displayed at the bottom. This means that you are currently connected to a public server. To use your own server, go to ``Settings -> Network`` and enter the following:

.. warning:: Replace ``isabell`` with your username and ``40131`` with your port!

::

 ID server: isabell.uber.space:40131
 Relay server:
 API server:
 Key: <paste the content of ~/rustdesk/id_ed25519.pub here>

.. note:: The file ``id_ed25519.pub`` was created automatically (as were several others) when ``hbbs`` or ``hbbr`` was started successfully for the first time.

You should now only see "**Ready**" at the bottom of the client window.

Best practices
==============

Security
--------

Keep the software up to date. If you do not want third parties to be able to connect to your server, keep the public key (= the content of the file ``id_ed25519.pub``) secret or only pass it on to authorized persons.

Updates
=======

.. note:: Check the `GitHub release page <latest release_>`_ regularly to stay informed about the newest version.

To update the software, download the latest version and replace the files ``hbbs``, ``hbbr`` and ``rustdesk-utils``.

.. _RustDesk: https://rustdesk.com
.. _hole punching: https://en.wikipedia.org/wiki/Hole_punching_(networking)
.. _How does RustDesk work?: https://github.com/rustdesk/rustdesk/wiki/How-does-RustDesk-work%3F
.. _RustDesk Server: https://github.com/rustdesk/rustdesk-server
.. _firewall: https://manual.uberspace.de/basics-ports.html
.. _latest release: https://github.com/rustdesk/rustdesk-server/releases

----

Tested with RustDesk Server 1.1.10-3, Uberspace 7.15.11

.. author_list::
