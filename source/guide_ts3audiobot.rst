.. highlight:: console

.. author:: Felix Franz <https://www.felix-franz.com/>

.. tag:: web

.. _TS3AudioBot: https://github.com/Splamy/TS3AudioBot
.. _TeamSpeak3: https://teamspeak.com
.. _youtube-dl: https://github.com/ytdl-org/youtube-dl

###########
TS3AudioBot
###########

.. tag_list::

TS3AudioBot_ is a open-source TeamSpeak3 bot, playing music and much more.

.. warning:: For using the bot, you also need a TeamSpeak3_ server!

----

.. note:: For this guide you should be familiar with the basic concepts of

  * TeamSpeak3_
  * :manual:`.htaccess <web-documentroot>`
  * :manual:`supervisord <daemons-supervisord>`
..  * :manual:`domains <web-domains>`
  * :manual:`lang-dotnet`


License
=======

TS3AudioBot_ was written by `Splamy <https://splamy.de/>`_ and licensed under `OSL-3.0 <https://github.com/Splamy/TS3AudioBot#license>`_.


Installation
============

Download release file:

::

 [isabell@stardust ~]$ mkdir ts3audiobot
 [isabell@stardust ~]$ cd ts3audiobot
 [isabell@stardust ts3audiobot]$ wget https://github.com/Splamy/TS3AudioBot/releases/latest/download/TS3AudioBot_dotnet_core_3.1.zip

Extract zip archive:

::

 [isabell@stardust ts3audiobot]$ unzip TS3AudioBot_dotnet_core_3.1.zip
 [isabell@stardust ts3audiobot]$ rm TS3AudioBot_dotnet_core_3.1.zip

Now we will configure the bot.
To set your TeamSpeak user as bot admin, you unique id is required.
Go to your TeamSpeak client and open the `Identities` window in the `Tools` menu.
Copy your `unique id`.

To configure the bot, start it an interactively insert your configuration data (unique TeamSpeak user id, server name, server password, ...).
After the configuration is done the bot will automatically connect to the TeamSpeak3 server.

::

 [isabell@stardust ts3audiobot]$ dotnet TS3AudioBot.dll

.. warning::

 The bot also starts a webinterface by default on port 58913. If the port is already used you need to change this port.

 If you see such a error message stop the bot by ``Ctrl+C`` and configure another port.
 You might re-try this process until you reach a freee port.
 Change ``~/ts3audiobot/ts3audiobot.toml`` from

 .. code-block:: toml

  port = 58913

 to

 .. code-block:: toml

  port = <another port>

The bot should now be connected.
Check it by connecting youself to the server.

You can also test if the bot plays music by connecting to the bot's TeamSpeak channel and send it following private message:

::

 !play https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3

Because the TS3AudioBot programm will be stopped if you disconnect your terminal, you need to configure a service.
Stop the bot by inserting ``Ctrl+C``.
Create ``~/etc/services.d/ts3audiobot.ini`` with following content:

.. code-block:: ini

 [program:ts3audiobot]
 command=dotnet TS3AudioBot.dll
 directory=/home/isabell/ts3audiobot/

.. include:: includes/supervisord.rst

Playing youtube videos is currently not possible.
Therefore we need youtube-dl_.

First clone the repo:

::

 [isabell@stardust ts3audiobot]$ git clone https://github.com/ytdl-org/youtube-dl.git

Then configure the path in ``~/ts3audiobot/ts3audiobot.toml``, change

.. code-block:: toml

 youtube-dl = { path = "" }

to

.. code-block:: toml

 youtube-dl = { path = "./youtube-dl" }

Restart the bot to active the new config:

::

 supervisorctl restart ts3audiobot

Test if you are now able to play youtube videos by sending ``!play <youtube url>`` to your bot.

To be able to connect to the web interface add a reverse proxy to the bot.
If you have changed the default port above, you need to do the same here.

Configure ``~/html/.htaccess`` like this:

.. code-block:: htaccess

 RewriteEngine On
 RewriteRule ^(.*) http://isabell.local.uberspace.de:58913/$1 [P]

You should now be able to reach the bot on ``https://isabell.uber.space``.


Additional Configuration
========================

**Rename your bot**

Change ``name`` value in ``~/ts3audiobot/ts3audiobot.toml``.

**Connect to special channel**

Change ``channel`` value in ``~/ts3audiobot/ts3audiobot.toml``.


**Allow everyone to change music**

Uncomment groupid and userid in the Playing rights part of ``~/ts3audiobot/rights.toml``

**More Configurations**

Refer to the `official TS3AudioBot wiki <https://github.com/Splamy/TS3AudioBot/wiki/Configuration>`_ for more configuration options.


Control the bot via TeamSpeak
=============================

Connect to your TeamSpeak server and to the channel with the bot.
The run a command.

.. list-table:: common Commands
 :widths: 20 30
 :header-rows: 1

 * - Command
   - Description
 * -
    ``!play https://www.youtube.com/watch?v=example``

    ``!play https://example.com/music.mp3``
   - Plays a new song
 * - ``!pause``
   - Pauses playing
 * - ``!play``
   - Continues current paused song
 * - ``!stop``
   - Stops playing a song
 * - ``!add``
   - Adds song to the queue
 * - ``!next``
   - Plays next song in queue
 * - ``!previous``
   - Plays previous song in queue
 * - ``!help``
   - Shows a (hopefully) helping message

Refer to the `official TS3AudioBot wiki <https://github.com/Splamy/TS3AudioBot/wiki/CommandSystem>`_ for more commands.


Control the bot via the web interface
=====================================

Connect to the TeamSpeak Server an join the channel with the bot.
Go to Tools and click on Identities in your TeamSpeak and copy the unique id.
Generate an api token sending the message ``!api token`` to the bot.
Open the Webinterface on ``https://isabell.uber.space`` and insert unique id and token.
You should now be able to control the bot!


Updates
=======

Replace all files with the current release (backup your data in advance):

::

 [isabell@stardust ~]$ cd ts3audiobot
 [isabell@stardust ts3audiobot]$ wget https://github.com/Splamy/TS3AudioBot/releases/latest/download/TS3AudioBot_dotnet_core_3.1.zip
 [isabell@stardust ts3audiobot]$ unzip -o TS3AudioBot_dotnet_core_3.1.zip
 [isabell@stardust ts3audiobot]$ rm TS3AudioBot_dotnet_core_3.1.zip


Uninstallation
==============

Remove reverse proxy to the web interface:

::

 [isabell@stardust ~]$ rm ~/html/.htaccess

.. include:: includes/supervisord.rst


Remove Service file:

::

 [isabell@stardust ~]$ rm ~/etc/services.d/ts3audiobot.ini

.. include:: includes/supervisord.rst

Delete files:

::

 [isabell@stardust ~]$ rm -R ~/ts3audiobot


Debugging
=========

Refer to the `official TS3AudioBot wiki <https://github.com/Splamy/TS3AudioBot/wiki>`_!
