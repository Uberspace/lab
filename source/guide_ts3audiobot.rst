.. highlight:: console

.. author:: Felix Franz <https://www.felix-franz.com>

.. tag:: web

.. _TS3AudioBot: https://github.com/Splamy/TS3AudioBot
.. _TeamSpeak3: https://teamspeak.com
.. _youtube-dl: https://github.com/ytdl-org/youtube-dl

###########
TS3AudioBot
###########

.. tag_list::

TS3AudioBot_ is a open-source TeamSpeak3 bot, playing music and much more.

.. warning:: To use the bot, you also need a TeamSpeak3_ server!

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
 (...)
 HTTP request sent, awaiting response... 200 OK
 Length: 12161538 (12M) [application/octet-stream]
 Saving to: ‘TS3AudioBot_dotnet_core_3.1.zip’

 100%[=====================================>] 12,161,538  49.3MB/s   in 0.2s

 2021-03-14 16:09:26 (49.3 MB/s) - ‘TS3AudioBot_dotnet_core_3.1.zip’ saved [12161538/12161538]

Extract zip archive:

::

 [isabell@stardust ts3audiobot]$ unzip TS3AudioBot_dotnet_core_3.1.zip
 [isabell@stardust ts3audiobot]$ rm TS3AudioBot_dotnet_core_3.1.zip

Now we will configure the bot.
To set your TeamSpeak user as bot admin, you unique id is required.
Go to your TeamSpeak client and open the `Identities` window in the `Tools` menu.
Copy your `unique id`.

To configure the bot, start it interactively and input your configuration data (unique TeamSpeak user id, server name, server password, ...).
After the configuration is done, the bot will automatically connect to the TeamSpeak3 server.

.. code-block:: console
 :emphasize-lines: 1,10,12,17,19

 [isabell@stardust ts3audiobot]$ dotnet TS3AudioBot.dll
 16:10:54.4473| INFO|| [============ TS3AudioBot started =============]
 16:10:54.5198| INFO|| [ Date/Time: Sunday, 14 March 2021 16:10:54
 16:10:54.5302| INFO|| [ Version: 0.11.0/master/c7e44e4d
 16:10:54.5310| INFO|| [ Platform: CentOS Linux 7 (Core) (64bit)
 16:10:54.5315| INFO|| [ Runtime: .NET Core (3.1.13) ServerGC:True GC:SustainedLowLatency
 16:10:54.5343| INFO|| [ Opus: libopus 1.0.2 (x64)
 16:10:54.5346| INFO|| [==============================================]
 16:10:55.2626| WARN|| No permission file found.
 Do you want to set up an admin in the default permission file template? [Y/n] Y
 Please enter an admin uid
 YourAdminUID
 16:11:36.1467| INFO|| Creating new permission file ({"AdminUids":["YourAdminUID"], "OverwriteIfExists":false})
 It seems like there are no bots configured.
 Fill out this quick setup to get started.
 Please enter the ip, domain or nickname (with port; default: 9987) where to connect to:
 1.3.3.7:9987
 Please enter the server password (or leave empty for none):
 SecretTSserverPWifAny
 16:12:41.2601| INFO|| Bot "default" connecting to "1.3.3.7:9987"
 16:12:41.8483| INFO|| Started Webserver on port 58913


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

Youtube Videos
==============

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

Restart the bot to activate the new config:

::

 supervisorctl restart ts3audiobot

Test if you are now able to play youtube videos by sending ``!play <youtube url>`` to your bot.

Configure the web server
========================

.. note::

    TS3AudioBot is running on port 58913.

.. include:: includes/web-backend.rst


Additional Configuration
========================

**Rename your bot**

Change ``name`` value in ``~/ts3audiobot/ts3audiobot.toml``.

**Connect to special channel**

Change ``channel`` value in ``~/ts3audiobot/ts3audiobot.toml``.


**Allow everyone to change music**

Uncomment groupid and userid in the Playing rights part of ``~/ts3audiobot/rights.toml``

**More Configurations**

Refer to the `official TS3AudioBot wiki configuration <https://github.com/Splamy/TS3AudioBot/wiki/Configuration>`_ for more configuration options.


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

Refer to the `official TS3AudioBot wiki command system <https://github.com/Splamy/TS3AudioBot/wiki/CommandSystem>`_ for more commands.


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

Remove web backend:

::

 [isabell@stardust ~]$ uberspace web backend del /
 The web backend has been deleted.


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

----

Tested with TS3AudioBot 0.11.0, Uberspace 7.9.0.0

.. author_list::
