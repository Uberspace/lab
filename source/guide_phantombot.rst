.. author:: tobimori <tobias@moeritz.cc>

.. tag:: lang-java
.. tag:: streaming
.. tag:: self-hosting
.. tag:: chat

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/phantombot.png
      :align: center

##########
PhantomBot
##########

.. tag_list::

PhantomBot_ is an actively developed open source interactive Twitch bot written in Java 
that provides entertainment and moderation for your channel.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`

License
=======

PhantomBot_ is licensed under the `GNU General Public License v3 (GPL-3)`_.

Prerequisites
=============

Setup your URL for the bot panel:

.. include:: includes/web-domain-list.rst

Installation
============

Download the latest release from GitHub_. Make sure to replace ``X.X.X`` with the latest version!

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ wget https://github.com/PhantomBot/PhantomBot/releases/download/vX.X.X/PhantomBot-X.X.X.zip
  [isabell@stardust ~]$


Then unzip the release folder, rename it and switch into it:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ unzip PhantomBot-X.X.X.zip && mv PhantomBot-X.X.X phantombot && cd phantombot
  [...]
  [isabell@stardust phantombot]$

The last thing we need to do is to assign the right privileges to make the launch.sh, launch-service.sh & java runtime files executable.

.. code-block:: console

  [isabell@stardust phantombot]$ chmod u+x launch-service.sh launch.sh ./java-runtime-linux/bin/java
  [isabell@stardust phantombot]$

Configuration
=============

PhantomBot Setup
----------------

To setup PhantomBot for the first time, run launch.sh.

.. code-block:: console

  [isabell@stardust phantombot]$ ./launch.sh
  [...]

PhantomBot will guide you through its configuration. After the configuration is done, 
close PhantomBot by pressing ``CTRL-C`` and continue with the next step.

Configure web server
--------------------

PhantomBot_ binds to localhost in the default configuration. This prevents the Panel from being used with a :manual:`web backend <web-backends>`. 
To bind the bot to ``0.0.0.0``, add ``bindIP=0.0.0.0`` to botlogin.txt in the config folder.

.. code-block:: console

  [isabell@stardust phantombot]$ echo "bindIP=0.0.0.0" >> ~/phantombot/config/botlogin.txt
  [isabell@stardust phantombot]$

.. note::

    PhantomBot_ is running on port 25000 in the default configuration.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/phantombot.ini`` with the following content:

.. code-block:: ini

  [program:phantombot]
  command=%(ENV_HOME)s/phantombot/launch-service.sh
  autorestart=true
  autostart=true
  startsecs=30

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.

Updates
=======

Stop your PhantomBot_:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl stop phantombot
  [isabell@stardust ~]$

Then rename the old folder:

.. code-block:: console

  [isabell@stardust ~]$ mv phantombot phantombot-old
  [isabell@stardust ~]$

If you receive an error that the phantombot-old directory already contains a file, then either remove the phantombot-old directory or rename it:

.. code-block:: console

  [isabell@stardust ~]$ rm -rf phantombot-old
  [isabell@stardust ~]$ 

.. code-block:: console

  [isabell@stardust ~]$ mv phantombot-old new_directory_name_of_your_choosing
  [isabell@stardust ~]$ 

Get the latest PhantomBot_ release from GitHub_:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ wget https://github.com/PhantomBot/PhantomBot/releases/download/vX.X.X/PhantomBot-X.X.X.zip
  [isabell@stardust ~]$

Then unzip the release folder and rename it to make future updates a bit easier - but do not switch into it yet:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ unzip PhantomBot-X.X.X.zip && mv PhantomBot-X.X.X phantombot
  [...]
  [isabell@stardust ~]$

Copy your ``config`` folder to your new folder:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ cp -R ./phantombot-old/config/ ./phantombot/
  [...]
  [isabell@stardust ~]$ cp -R ./phantombot-old/scripts/lang/custom/ ./phantombot/scripts/lang/

The last thing we need to do is to assign the right privileges to make the launch.sh, launch-service.sh & java runtime files executable.

.. code-block:: console
  [isabell@stardust ~]$ cd phantombot
  [isabell@stardust phantombot]$ chmod u+x launch-service.sh launch.sh ./java-runtime-linux/bin/java

Now we are ready to launch PhantomBot again. You can run the bot with:

.. code-block:: console
  [isabell@stardust phantombot]$ supervisorctl start phantombot
  [isabell@stardust phantombot]$
  
.. _PhantomBot: https://phantom.bot/
.. _GitHub: https://github.com/PhantomBot/PhantomBot/releases/latest
.. _GNU General Public License v3 (GPL-3): https://www.gnu.org/licenses/gpl-3.0.html

----`

Tested with PhantomBot 3.1.2 on Uberspace 7.6.2.

.. author_list::
