.. author:: Stunkymonkey <stunkymonkey.de>
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

Mumble_ is a voice over IP (VoIP) application primarily designed for use by gamers and is similar to programs such as TeamSpeak_.

Mumble uses a client–server architecture which allows users to talk to each other via the same server (murmur). It has a very simple administrative interface and features high sound quality and low latency. All communication is encrypted to ensure user privacy.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * supervisord_

License
=======

All relevant legal information can be found here

  * https://github.com/mumble-voip/mumble/blob/master/LICENSE

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

You need a database for mumble:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_mumble"
  [isabell@stardust ~]$

Installation
============

Check the Mumble_ website or GitHub_ for the feed_ and copy the download link to the ``murmur-static``-file. Replace the URL with the one you just copied.

.. note:: the server for mumble is called murmur

.. code-block:: console

  [isabell@stardust ~]$ wget https://github.com/mumble-voip/mumble/releases/download/66.6.6/murmur-static_x86-66.6.6.tar.bz2
  --2018-10-06 21:14:34--  https://github.com/mumble-voip/mumble/releases/download/66.6.6/murmur-static_x86-66.6.6.tar.bz2
  Resolving github.com (github.com)... 192.30.253.113, 192.30.253.112
  Connecting to github.com (github.com)|192.30.253.113|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Location: https://github-production-release-asset-2e65be.s3.amazonaws.com/1413319/a7d2b00a-e4a8-11e6-80bb-d224f64df619?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20181006%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181006T191435Z&X-Amz-Expires=300&X-Amz-Signature=b2af6f60968f675bb8427af7341716d75a1ee162f822abdd878877514b9205be&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3Dmurmur-static_x86-66.6.6.tar.bz2&response-content-type=application%2Foctet-stream [following]
  --2018-10-06 21:14:35--  https://github-production-release-asset-2e65be.s3.amazonaws.com/1413319/a7d2b00a-e4a8-11e6-80bb-d224f64df619?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20181006%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181006T191435Z&X-Amz-Expires=300&X-Amz-Signature=b2af6f60968f675bb8427af7341716d75a1ee162f822abdd878877514b9205be&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3Dmurmur-static_x86-66.6.6.tar.bz2&response-content-type=application%2Foctet-stream
  Resolving github-production-release-asset-2e65be.s3.amazonaws.com (github-production-release-asset-2e65be.s3.amazonaws.com)... 52.216.2.32
  Connecting to github-production-release-asset-2e65be.s3.amazonaws.com (github-production-release-asset-2e65be.s3.amazonaws.com)|52.216.2.32|:443... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 11939824 (11M) [application/octet-stream]
  Saving to: ‘murmur-static_x86-66.6.6.tar.bz2’

  100%[======================================================================================================================================>] 11,939,824  7.45MB/s   in 1.5s   

  2018-10-06 21:14:37 (7.45 MB/s) - ‘murmur-static_x86-66.6.6.tar.bz2’ saved [11939824/11939824]

  [isabell@stardust ~]$


extract it and rename it to mumble:


.. code-block:: console

  [isabell@stardust ~]$ tar xvjf murmur-static_x86-66.6.6.tar.bz2
  murmur-static_x86-66.6.6/
  murmur-static_x86-66.6.6/murmur.x86
  murmur-static_x86-66.6.6/LICENSE
  murmur-static_x86-66.6.6/dbus/
  murmur-static_x86-66.6.6/dbus/weblist.pl
  murmur-static_x86-66.6.6/dbus/murmur.pl
  murmur-static_x86-66.6.6/ice/
  murmur-static_x86-66.6.6/ice/icedemo.php
  murmur-static_x86-66.6.6/ice/Murmur.ice
  murmur-static_x86-66.6.6/ice/weblist.php
  murmur-static_x86-66.6.6/murmur.ini
  murmur-static_x86-66.6.6/README
  [isabell@stardust ~]$ mv murmur-static_x86-66.6.6/ mumble/
  [isabell@stardust ~]$


Configuration
=============

Configure port
--------------

.. include:: includes/open-port.rst

edit config file ``~/mumble/murmur.ini`` to specify the desired port, domain and mysql-database. Minimal config would look like this:

.. code-block:: ini
  :emphasize-lines: 1,3,4,7

  database=<username>_mumble
  dbDriver=QMYSQL
  dbUsername=<username>
  dbPassword=<mysql_password>
  dbOpts="UNIX_SOCKET=/var/lib/mysql/mysql.sock"
  welcometext="<br />Welcome to this server running <b>Murmur</b>.<br />Enjoy your stay!<br />"
  port=<your_port>
  serverpassword=
  allowping=true
  bonjour=false

For more configuration options look at the documentation_ site.

Setup daemon
------------

Create ``~/etc/services.d/mumble.ini`` with the following content:

.. code-block:: ini

  [program:mumble]
  command=%(ENV_HOME)s/mumble/murmur.x86 -fg -ini %(ENV_HOME)s/mumble/murmur.ini

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 mumble: available
 [isabell@stardust ~]$ supervisorctl update
 mumble: added process group
 [isabell@stardust ~]$ supervisorctl status
 mumble                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state ``RUNNING``, check your configuration.


Finishing installation
======================

To connect to your server, open mumble on your computer or phone and add a new server:

* Address: ``<username>.uber.space``
* Port: your port
* Username: any username you'd like

Best practices
==============

uberspace already provides letsencrypt certificates. To add them append these lines to your ``murmur.ini`` and adjust your username and the domain.

.. code-block:: ini

  sslCert=/home/isabell/etc/certificates/isabell.uber.space.crt
  sslKey=/home/isabell/etc/certificates/isabell.uber.space.key

Last we have to restart the server before expiry. Edit your cron tab using the ``crontab -e``.

::

  @monthly supervisorctl restart mumble > /dev/null

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version repeat the Installation_ and execute:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart mumble
  mumble: stopped
  mumble: started
  [isabell@stardust ~]$

.. _Teamspeak: https://www.teamspeak.com/
.. _Mumble: https://mumble.info/
.. _Github: https://github.com/mumble-voip/mumble
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _feed: https://github.com/mumble-voip/mumble/releases
.. _documentation: https://wiki.mumble.info/wiki/Murmur.ini


----

Tested with Murmur 1.2.19, Uberspace 7.3.0.0

.. authors::
