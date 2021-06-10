.. author:: this.ven <http://this.ven.uber.space>
.. highlight:: console

.. tag:: lang-go
.. tag:: chat
.. tag:: bridge
.. tag:: communication

.. sidebar:: Logo

  .. image:: _static/images/matterbridge-logo.svg
      :align: center

############
Matterbridge
############

.. tag_list::

Matterbridge_ is a simple chat bridge for integrating a lot of different chat platforms and communication services written in Go. It supports Discord, Gitter, IRC, Keybase, Matrix, Mattermost, Microsoft Teams, Mumble, Nextcloud Talk, Rocket.chat, Slack, Ssh-chat, Telegram, Twitch, VK, WhatsApp, XMPP, Zulip and more with REST API.

----

.. note:: Depending on your intention to use this bridge service you should at least have one of the following communcation services setup and running on your Uberspace:

  * :lab:`ejabberd <guide_ejabberd>`
  * :lab:`mattermost <guide_mattermost>`
  * :lab:`mumble <guide_mumble>`
  * :lab:`nextcloud <guide_nextcloud>`
  * :lab:`prosody <guide_prosody>`
  * :lab:`rocketchat <guide_rocketchat>`
  * :lab:`synapse <guide_synapse>`

License
=======

All relevant legal information can be found here

  * https://github.com/42wim/matterbridge/blob/master/LICENSE

Installation
============

Download the most recent matterbridge binary from _https://github.com/42wim/matterbridge/releases_, rename it to ``matterbridge`` and make it executable inside a new directory.

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p ~/matterbridge
 [isabell@stardust ~]$ cd ~/matterbridge
 [isabell@stardust matterbridge]$ wget https://github.com/42wim/matterbridge/releases/download/v1.22.2/matterbridge-1.22.2-linux-64bit
 [isabell@stardust matterbridge]$ mv matterbridge-1.22.2-linux-64bit matterbridge
 [isabell@stardust matterbridge]$ chmod +x matterbridge
 [isabell@stardust matterbridge]$

Configuration
=============

Service sections
----------------

Create the config file ``~/matterbridge/matterbridge.toml` and add sections_ for the services you want be bridged. In some cases you need a dedicated user for matterbridge to avoid message relay loops.

For example if you want to connect your Matrix homeserver with your registered IRC account you'd use the following configuration:

.. code-block:: toml

 [matrix.mymatrix]
 Server="https://isabell.uber.space"
 NoHomeServerSuffix=false
 Login="matterbridge"
 Password="<matrix-password>"
 RemoteNickFormat="[{PROTOCOL}] <{NICK}> "

 [irc.myirc]
 Nick="<irc-nickname>"
 NickServNick="<irc-nickname>"
 NickServPassword="<irc-password>"
 Server="<irc-server>:<irc-port>"
 UseTLS=true
 UseSASL=true

Use your ``<irc-nickname>``, `ìrc-password>`` along ``<irc-server>`` and ``<irc-port>`` for the section below and don't forgett to create a new ``matterbridge`` Matrix_user_ identified with ``<matrix-password>`` before starting matterbridge. If using password protected channels or other options to connect to IRC refer to the wiki_.

Other services
^^^^^^^^^^^^^^

You can add other services, e.g. a mumble bridge by appending:

.. code-block:: toml

 [mumble.mymumble]
 Server = "isabell.uber.space:<mumble-port>"
 Nick = "matterbridge"
 Password = "<mumble-password>"
 TLSClientCertificate="mumble.crt"
 TLSClientKey="mumble.key"
 SkipTLSVerify=false

Change ``<mumble-port>`` as well as ``<mumble-password>`` according to your configuration and create a client certificate before starting matterbridge:

.. code-block:: console

 [isabell@stardust matterbridge]$ openssl req -x509 -newkey rsa:4096 -nodes -days 10000 -keyout ~/matterbridge/mumble.key -out ~/matterbridge/mumble.crt 
 [isabell@stardust matterbridge]$

You can confirm the default values for the certificate.

Gateway sections
----------------

Next step is to define a gateway_ between the services configured before and specify channels according to the channel_rules_. IRC rooms need to start with # and have to be written in lowercase only.

.. code-block:: toml

 [[gateway]]
 name="gateway1"
 enable=true

 [[gateway.inout]]
 account="irc.myirc"
 channel="#<irc-room>"

 [[gateway.inout]]
 account="matrix.mymatrix"
 channel="#<irc-room>:isabell.uber.space"
  
Change <irc-room> to fit your needs.

Test run
--------

Run matterbridge with your configuration and watch for errors by executing:

.. code-block:: console

 [isabell@stardust matterbridge]$ ./matterbridge -conf matterbridge.toml
 [0000]  INFO main:         Running version 1.22.2 641ed187
 [0000]  INFO router:       Parsing gateway gateway1
 [0000]  INFO router:       Starting bridge: irc.myirc 
 [0000]  INFO irc:          Connecting irc.example.org:6697
 [0007]  INFO irc:          Connection succeeded
 [0007]  INFO irc:          irc.myirc: joining #irc-room (ID: #irc-room.myirc)
 [0007]  INFO router:       Starting bridge: matrix.mymatrix 
 [0007]  INFO matrix:       Connecting https://isabell.uber.space
 [0007]  INFO matrix:       Connection succeeded
 [0007]  INFO matrix:       matrix.mymatrix: joining #irc-room:isabell.uber.space (ID: #irc-room:isabell.uber.spacematrix.mymatrix)
 [0007]  INFO main:         Gateway(s) started succesfully. Now relaying messages
 ...

If there are no errors, hit STRG + C and proceed (considering advanced_settings_). Otherwise check your configuration and run matterbridge again. 

Setup daemon
------------

Create ``~/etc/services.d/matterbridge.ini`` with the following content:

.. code-block:: ini

 [program:matterbridge]
 command=%(ENV_HOME)s/matterbridge/matterbridge -conf %(ENV_HOME)s/matterbridge/matterbridge.toml
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Updates
=======

.. note:: Check the release_ page or update feed_ regularly to stay informed about the newest version.

Repeat the Installation step to upgrade and restart the matterbridge service.

Tested on uberspace 7.11.1 and matterbridge 1.22.

.. _Matterbridge: https://github.com/42wim/matterbridge
.. _sections: https://github.com/42wim/matterbridge/wiki/How-to-create-your-config#step-2
.. _wiki: https://github.com/42wim/matterbridge/wiki/Section-IRC-%28basic%29
.. _Matrix_user: https://lab.uberspace.de/guide_synapse.html#adding-users
.. _gateway: https://github.com/42wim/matterbridge/wiki/Gateway-config-%28basic%29
.. _channel_rules: https://github.com/42wim/matterbridge/wiki/Gateway-config-%28channel-rules%29
.. _advanced_settings: https://github.com/42wim/matterbridge/wiki/Settings
.. _release: https://github.com/42wim/matterbridge/releases
.. _feed: https://github.com/42wim/matterbridge/releases.atom

----

.. author_list::
