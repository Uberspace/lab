.. author:: benks <uberspace@benks.io>

.. tag:: web
.. tag:: streaming
.. tag:: radio
.. tag:: webradio


.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/icecast2.png
      :align: center

########
Icecast2
########

.. tag_list::


'Icecast'_ is a streaming media server which currently supports Ogg Vorbis and MP3 audio streams. It can be used to create an Internet radio station or a privately running jukebox and many things in between. It is very versatile in that new formats can be added relatively easily and supports open standards for communication and interaction.

Icecast is distributed under the GNU GPL, version 2. A copy of this license is included with this software in the COPYING file.

Find the Icecast2 docu here_

----

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Aquire one of your 20 listening ports from uberspace with

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ uberspace port add
  Port 40132 will be open for TCP and UDP traffic in a few minutes.
  [isabell@stardust ~]$

Here it is ''40132''. Note it down for later. Below it will be referenced with ``$yourlisteningport``.
It may take a few minutes for the port to be accessible from the Internet.

You can check on your Linux machine if the port is open with

.. code-block:: console

  [you@yourmachine ~]$ nmap isabell.uber.space -p 40132 | grep 40132
  40132/tcp open  unknown
  [you@yourmachine ~]$ 

Installation
============

.. code-block:: console

  [isabell@stardust ~]$ cd ~/tmp
  [isabell@stardust ~/tmp]$ wget http://downloads.xiph.org/releases/icecast/icecast-2.4.4.tar.gz
  [isabell@stardust ~/tmp]$ tar -xzf icecast-2.4.4.tar.gz
  [isabell@stardust ~/tmp]$ icecast-2.4.4
  [isabell@stardust ~/tmp]$ ./configure --prefix=$HOME
  [isabell@stardust ~/tmp]$ make
  [isabell@stardust ~/tmp]$ make install
  [isabell@stardust ~/tmp]$ rm -r icecast-2.4.4
  [isabell@stardust ~/tmp]$ rm icecast-2.4.4.tar.gz
  [isabell@stardust ~/tmp]$

As ``--prefix=$HOME`` was used, components of icecast are in the home directory now:

  * ~/bin/icecast (icecast binary)
  * ~/etc/icecast.xml (config)
  * ~/share/icecast/ (files of the web interface)
  * ~/share/doc/icecast/ (documentation)


Configuration
=============

Before editing a config, it's best practice to copy the untouched config file to a *.dist file.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ cp ~/etc/icecast.xml ~/etc/icecast.xml.dist
  [isabell@stardust ~]$ 

You can then later compare your config with the default one with ``diff``.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ diff ~/etc/icecast.xml ~/etc/icecast.xml.dist
  [isabell@stardust ~]$ 

Time to choose a couple of passwords for different users. On your own Linux machine you may want to generate them. Maybe you have to install ``pwgen``. Generate at least three and note it down for the next step.

.. code-block:: console

 [you@yourmachine ~]$ pwgen -syc 12 1
 y0uRS3cR3t_1!
 [you@yourmachine ~]$ pwgen -syc 12 1
 y0uRS3cR3t_2!
 [you@yourmachine ~]$ pwgen -syc 12 1
 y0uRS3cR3t_3!
 [you@yourmachine ~]$ 

Edit ``~/etc/icecast.xml`` and change the following entries:

::

  <hostname>isabell.uber.space</hostname>

::

  <source-password>y0uRS3cR3t_1!</source-password>

::

  <admin-password>y0uRS3cR3t_2!</admin-password>

::

  <relay-password>y0uRS3cR3t_3!</relay-password>

::

  <admin>yourmailadress</admin>

::

  <location>YourLocation</location>

::

  <listen-socket>
     <port>$yourlisteningport</port>
     <!-- <bind-address>127.0.0.1</bind-address> -->
     <shoutcast-mount>/stream</shoutcast-mount>
  </listen-socket>

Save and exit.

Create the directory for the log files.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ mkdir -p /home/isabell/var/log/icecast/
  [isabell@stardust ~]$ 


Try to manually run icecast with your config to print out possible errors.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ /home/isabell/bin/icecast -c /home/isabell/etc/icecast.xml
  [isabell@stardust ~]$ 

If it is running without errors, close it with ``ctrl``+``c``. Otherwise most likely you need to fix them in your config.

Now you can set up the service by creating a file ``~/etc/services.d/icecast.ini`` with the following content. Be sure to place your username.

::
  [program:icecast]
  command=/home/isabell/bin/icecast -c /home/isabell/etc/icecast.xml
  autostart=yes
  autorestart=yes

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl reread
  [isabell@stardust ~]$ supervisorctl update

Check the status of your icecast2 service.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl status
  [isabell@stardust ~]$ 

If your service is not running, check your config.

Finally configure the backend with your listening port from above.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ uberspace web backend set / --http --port $yourlisteningport
  [isabell@stardust ~]$ 

Check if that went well

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ uberspace web backend list
  [isabell@stardust ~]$ 

Find more configuration possibilities in the configdocu_.

With this basic setup you can already stream audio from a source client like mixxx_ to your icecast server by providing 

  * the listening port,
  * ``source`` as username and the source-password,
  * your hostname or ip address.

On the icecast website you can find a list of other possible clients_.

Administration
==============

To view streams, kick clients or view statistics open your web-domain in a browser and login with your chosen admin credentials.

If you need to stop, start or restart your icecast service use:

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl restart icecast
  [isabell@stardust ~]$ 

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl start icecast
  [isabell@stardust ~]$ 

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl stop icecast
  [isabell@stardust ~]$ 

You can find your logs here:

``/home/isabell/var/log/icecast/error.log``
``/home/isabell/var/log/icecast/access.log``

You may want to change the log level from Info ``3`` to Debug ``4`` for debugging.

::

  <loglevel>4</loglevel> <!-- 4 Debug, 3 Info, 2 Warn, 1 Error -->

After having changed the ``icecast.xml`` you need to restart the service.


Updates
=======

.. note:: Check the latest news_ regularly to stay informed about the newest changes.


.. _here: https://icecast.org/docs/icecast-2.4.1/
.. _`Icecast2`: https://icecast.org
.. _news: https://icecast.org
.. _configdocu: https://icecast.org/docs/icecast-2.4.1/config-file.html
.. _clients: https://icecast.org/apps/
.. _mixxx: https://mixxx.org/
----

Tested with icecast-2.4.1 and Uberspace 7

.. author_list::
