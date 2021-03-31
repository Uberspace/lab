.. author:: benks <uberspace@benks.io>

.. tag:: lang-c
.. tag:: web
.. tag:: streaming
.. tag:: radio
.. tag:: webradio


.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/icecast.svg
      :align: center

########
Icecast2
########

.. tag_list::


`Icecast`_ is a streaming media server which currently supports Ogg Vorbis and MP3 audio streams. It can be used to create an Internet radio station or a privately running jukebox and many things in between. It is very versatile in that new formats can be added relatively easily and supports open standards for communication and interaction.

Icecast is distributed under the GNU GPL, version 2. A copy of this license is included with this software in the COPYING file.

Find the Icecast2 docu here_

----

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Configure port
--------------

.. include:: includes/open-port.rst

Write down your port.

Installation
============

.. code-block:: console

  [isabell@stardust ~]$ cd ~/tmp
  [isabell@stardust tmp]$ wget http://downloads.xiph.org/releases/icecast/icecast-2.4.4.tar.gz
  [isabell@stardust tmp]$ tar -xzf icecast-2.4.4.tar.gz
  [isabell@stardust tmp]$ cd icecast-2.4.4
  [isabell@stardust icecast-2.4.4]$ ./configure --prefix=$HOME
  [isabell@stardust icecast-2.4.4]$ make
  [isabell@stardust icecast-2.4.4]$ make install

If there were no errors, you can safely remove the installation directory and archive:

.. code-block:: console

  [isabell@stardust icecast-2.4.4]$ cd ..
  [isabell@stardust tmp]$ rm -r icecast-*
  [isabell@stardust tmp]$

As ``--prefix=$HOME`` was used, components of icecast are in the home directory now:

  * ~/bin/icecast (icecast binary)
  * ~/etc/icecast.xml (config)
  * ~/share/icecast/ (files of the web interface)
  * ~/share/doc/icecast/ (documentation)


Configuration
=============

Before editing a config, it's best practice to copy the untouched config file to a ``*.dist`` file.

.. code-block:: console

  [isabell@stardust ~]$ cp ~/etc/icecast.xml ~/etc/icecast.xml.dist
  [isabell@stardust ~]$

You can then later compare your config with the default one with ``diff``.

.. code-block:: console

  [isabell@stardust ~]$ diff ~/etc/icecast.xml ~/etc/icecast.xml.dist
  [isabell@stardust ~]$

Use this snippet to generate random passwords:

.. code-block:: console

 [isabell@stardust ~]$ pwgen 32 1
 topsecretrandompassword


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
     <ssl>1</ssl>
  </listen-socket>

::

  <paths>

::

     <ssl-certificate>/home/isabell/share/icecast/isabell.uber.space.pem</ssl-certificate>
  </paths>

Use the port you were assigned by ``uberspace port add`` above.

Create ``~/share/icecast/update-cert.sh`` to consolidate certificate keys into one file.

::

  #!/bin/sh
  CRTFILE=/home/isabell/etc/certificates/isabell.uber.space.crt
  KEYFILE=/home/isabell/etc/certificates/isabell.uber.space.key
  PEMFILE=/home/isabell/share/icecast/isabell.uber.space.pem

  cat $CRTFILE $KEYFILE > $PEMFILE
  chmod 640 $PEMFILE
  supervisorctl restart icecast

Change permissions and execute this script initially.

.. code-block:: console

  [isabell@stardust ~]$ chmod +x ~/var/log/icecast/
  [isabell@stardust ~]$ ~/share/icecast/update-cert.sh
  [isabell@stardust ~]$

Edit crontab with ``crontab -e`` and add following line for monthly execution.

::

  @monthly /home/isabell/share/icecast/update-cert.sh > /dev/null

Create the directory for the log files.

.. code-block:: console

  [isabell@stardust ~]$ mkdir -p ~/var/log/icecast/
  [isabell@stardust ~]$


Try to manually run icecast with your config to print out possible errors.

.. code-block:: console

  [isabell@stardust ~]$ ~/bin/icecast -c ~/etc/icecast.xml
  [isabell@stardust ~]$

If it is running without errors, close it with ``Ctrl+C``. Otherwise most likely you need to fix them in your config.

Now you can set up the service by creating a file ``~/etc/services.d/icecast.ini`` with the following content. Be sure to place your username.

.. code-block:: ini

  [program:icecast]
  command=%(ENV_HOME)s/bin/icecast -c %(ENV_HOME)s/etc/icecast.xml
  autostart=yes
  autorestart=yes

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl reread
  [isabell@stardust ~]$ supervisorctl update

Check the status of your icecast2 service.

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl status
  [isabell@stardust ~]$

If your service is not running, check your config.

Configure web server
--------------------

.. note::

    Use the port you were assigned by ``uberspace port add`` above.

.. include:: includes/web-backend.rst

Additional configuration
------------------------

Find more configuration possibilities in the configdocu_.

With this basic setup you can already stream audio from a source client like mixxx_ to your icecast server by providing

  * the listening port,
  * ``source`` as username and the source-password,
  * your hostname or ip address.

On the icecast website you can find a list of other possible clients_.

Administration
==============

You can find your logs in ``~/var/log/icecast/``.

You may want to change the log level from Info ``3`` to Debug ``4`` for debugging.

::

  <loglevel>4</loglevel> <!-- 4 Debug, 3 Info, 2 Warn, 1 Error -->

After having changed the ``icecast.xml`` you need to restart the service.

Best practices
==============

Source streaming can be done locally by oggfwd_ in combination with ffmpeg_ to encode to `Ogg Vorbis`_ format.

.. code-block:: console

  [isabell@localhost ~]$ ffmpeg -i $yourinputfile -vn -acodec libvorbis -b:a 128k -f ogg -y /dev/stdout |
  oggfwd isabell.uber.space $yourlisteningport y0uRS3cR3t_1! /stream.ogg

A more detailed setup for live streaming concerts with JACK audio server can be found at: https://wikis.ven.pm/streaming_setup

Updates
=======

.. note:: Check the latest news_ regularly to stay informed about the newest changes.


.. _here: https://icecast.org/docs/icecast-2.4.1/
.. _`Icecast`: https://icecast.org
.. _news: https://icecast.org
.. _configdocu: https://icecast.org/docs/icecast-2.4.1/config-file.html
.. _clients: https://icecast.org/apps/
.. _mixxx: https://mixxx.org/
.. _oggfwd: https://r-w-x.org/r/oggfwd
.. _ffmpeg: https://ffmpeg.org
.. _`Ogg Vorbis`: https://en.wikipedia.org/wiki/Vorbis

----

Tested with icecast-2.4.1 and Uberspace 7.3.10

.. author_list::
