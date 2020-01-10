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

Configure port
--------------

.. include:: includes/open-port.rst

Write down your port.

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

Use this snippet to generate random passwords:

.. code-block:: console

 [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo
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
  </listen-socket>

Use the port you were assigned by ``uberspace port add`` above.

Save and exit.

Create the directory for the log files.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ mkdir -p ~/var/log/icecast/
  [isabell@stardust ~]$ 


Try to manually run icecast with your config to print out possible errors.

.. code-block:: console
 :emphasize-lines: 1

  [isabell@stardust ~]$ ~/bin/icecast -c ~/etc/icecast.xml
  [isabell@stardust ~]$ 

If it is running without errors, close it with ``ctrl``+``c``. Otherwise most likely you need to fix them in your config.

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
 :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl status
  [isabell@stardust ~]$ 

If your service is not running, check your config.

Configure web server
--------------------

.. note::

    Use the port you were assigned by ``uberspace port add`` above.

.. include:: includes/web-backend.rst

Find more configuration possibilities in the configdocu_.

With this basic setup you can already stream audio from a source client like mixxx_ to your icecast server by providing 

  * the listening port,
  * ``source`` as username and the source-password,
  * your hostname or ip address.

On the icecast website you can find a list of other possible clients_.

Administration
==============

You can find your logs here:

``~/var/log/icecast/error.log``
``~/var/log/icecast/access.log``

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

Tested with icecast-2.4.1 and Uberspace 7.3.10

.. author_list::
