.. author:: stunkymonkey <http://stunkymonkey.de>, updated by franok <https://franok.de>
.. highlight:: console

.. tag:: lang-cpp
.. tag:: voip
.. tag:: ports

.. sidebar:: Logo

  .. image:: _static/images/mumble.svg
      :align: center

######
Mumble
######

.. tag_list::

Mumble_ is a voice over IP (VoIP) application primarily designed for use by gamers and is similar to programs such as TeamSpeak_. In contrast to Teamspeak, Mumble is an open-source project.

Mumble uses a client–server architecture which allows users to talk to each other via the same server (murmur). It has a very simple administrative interface and features high sound quality and low latency. All communication is encrypted to ensure user privacy.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * supervisord_

License
=======

All relevant legal information can be found here

  * https://github.com/mumble-voip/mumble/blob/master/LICENSE

Pre-Note
=============

.. note::
  The official Mumble project decided to no longer provide static murmur server binaries starting with version 1.4.x.

  `Some fellow Ubernauts have undertaken efforts <https://github.com/Uberspace/lab/issues/1191>`_ to compile a static murmur binary on their own. You can have a look at it on GitHub_.

  This guide uses the self-compiled server binary, which currently comes with some limitations, i.e. MySQL is currently not supported as a database. For Ubernauts who have been hosting a Mumble server based on this guide before Mumble v1.4, this might be a breaking change. The default database for a Mumble server is SQLite and requires no further configuration.

  Please read the `release notes <https://github.com/franok/mumble-build-container/releases>`_ of every new release. Releases of the self-compiled server binary may occur more often than the offical Mumble releases. However, no warranty is made regarding up-to-dateness and functional correctness. Consider subscribing to new releases, e.g. by using :lab:`uu-notify <guide_uu-notify>`.


Installation
============

Check the `GitHub release section`_ and copy the release tag version of the latest release. Set the variable ``MURMUR_VERSION`` to the version you just copied.

.. note:: The server for mumble is called murmur

.. code-block:: console

  [isabell@stardust ~]$ mkdir mumble
  [isabell@stardust ~]$ cd mumble/
  [isabell@stardust mumble]$ MURMUR_VERSION=v0.0.0_build-YYYY-000
  [isabell@stardust mumble]$ wget https://github.com/franok/mumble-build-container/releases/download/$MURMUR_VERSION/murmur-static.zip
  --2022-12-14 20:01:29--  https://github.com/franok/mumble-build-container/releases/download/v1.4.287/murmur-static.zip
  Resolving github.com (github.com)... 192.30.253.113, 192.30.253.112
  Connecting to github.com (github.com)|192.30.253.113|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: ...
  Saving to: ‘murmur-static.zip’

  murmur-static.zip     100%[=============================>]   7,39M  4,47MB/s    in 1,7s

  2022-12-14 20:01:33 (4,47 MB/s) - ‘murmur-static.zip’ saved [7753035/7753035]

  [isabell@stardust mumble]$


Extract the zip file:


.. code-block:: console

  [isabell@stardust mumble]$ unzip -l murmur-static.zip
  Archive:  murmur-static.zip
    Length      Date    Time    Name
  ---------  ---------- -----   ----
      18545  2022-12-06 21:27   murmur.ini
   18621464  2022-12-06 21:28   murmur.x86_64
  ---------                     -------
  18640009                     2 files

  [isabell@stardust mumble]$


Configuration
=============

Configure port
--------------

.. include:: includes/open-port.rst

Edit the config file ``~/mumble/murmur.ini`` to specify the desired port. Minimal config would look like this:

.. code-block:: ini
  :emphasize-lines: 2,3

  welcometext="<br />Welcome to this server running <b>Murmur</b>.<br />Enjoy your stay!<br />"
  port=<your_port>
  serverpassword=changeThisPassword!
  allowping=true
  bonjour=false


For more configuration options look at the documentation_ site.

Setup daemon
------------

Create ``~/etc/services.d/mumble.ini`` with the following content:

.. code-block:: ini

  [program:mumble]
  command=%(ENV_HOME)s/mumble/murmur.x86_64 -fg -ini %(ENV_HOME)s/mumble/murmur.ini

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.


Finishing installation
======================

To connect to your server, open a Mumble client on your computer or phone and add a new server:

* Address: ``<username>.uber.space``
* Port: your port
* Username: any username you'd like

Best practices
==============

Uberspace already provides letsencrypt certificates. To add them, append these lines to your ``murmur.ini`` and adjust your username and the domain.

.. code-block:: ini

  sslCert=/home/isabell/etc/certificates/isabell.uber.space.crt
  sslKey=/home/isabell/etc/certificates/isabell.uber.space.key

The server needs to be restarted, before the certificates expire.
Therefore, add the following line to your contrab using ``crontab -e``:

::

  @monthly supervisorctl restart mumble > /dev/null

Updates
=======

.. note:: `Subscribe to the releases <https://github.com/franok/mumble-build-container/releases>`_ to stay informed about the latest versions (e.g. by using :lab:`uu-notify <guide_uu-notify>`).

If there is a new version repeat the Installation_ and execute:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart mumble
  mumble: stopped
  mumble: started
  [isabell@stardust ~]$

.. _Teamspeak: https://www.teamspeak.com/
.. _Mumble: https://mumble.info/
.. _GitHub: https://github.com/franok/mumble-build-container
.. _`GitHub release section`: https://github.com/franok/mumble-build-container/releases
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _documentation: https://wiki.mumble.info/wiki/Murmur.ini


----

Tested with self-compiled static Murmur v1.4.287, Uberspace v7.14.0

.. author_list::
