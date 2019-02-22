.. author:: roang <https://github.com/Roang-zero1>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/the-lounge.svg
      :align: center

##########
The Lounge
##########

`The Lounge`_ is an open source IRC web client written in JavaScript and distributed under the MIT License, this self hosted client stays always connected so you never miss out on the most important chats. Another goal of The Lounge is to bring modern chat features such as push notifications, link previews and many more to your IRC chats.

The Lounge is based on the project Shout_ from which it is a community driven fork.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Node.js_ and its package manager npm_
  * supervisord_
  * domains_

Prerequisites
=============

We're using Node.js_ in the stable version 8:

::

 [isabell@stardusts ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardusts ~]$

Your The Lounge URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install thelounge
-----------------

Use ``npm`` to install ``thelounge`` globally:

::

 [isabell@stardusts ~]$ npm install --global thelounge
 [...]
 + thelounge@2.7.0
 added 242 packages in 31.627s
 [isabell@stardusts ~]$

Verify installation
-------------------

::

 [isabell@stardusts ~]$ thelounge --version
 v2.7.0

Configuration
=============

Configure port
--------------

Since Node.js applications use their own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Create configuration file
-------------------------

Create the configuration directory:

::

 [isabell@stardusts ~]$ mkdir ~/.lounge
 [isabell@stardusts ~]$


To configure The Lounge you need to create the ``~/.lounge/config.js`` file with the following content:

.. code-block:: javascript
 :emphasize-lines: 6

 "use strict"

 module.exports = {
   public: false,
   host: '127.0.0.1',
   port: <yourport>,
   reverseproxy: true
 };

Alternatively you can download the full default configuration from the project repository:

.. warning:: If you choose this option change the values according to the config provided above.

::

 [isabell@stardusts ~]$ wget https://raw.githubusercontent.com/thelounge/thelounge/master/defaults/config.js > ~/.lounge/config.js
 [isabell@stardusts ~]$

From now on you can modify with the ``thelounge config`` command.

For a full list of all configuration options see `the official documentation`_.

Setup daemon
------------

Create ``~/etc/services.d/thelounge.ini`` with the following content:

.. code-block:: ini

 [program:thelounge]
 command=thelounge start
 autostart=yes
 autorestart=yes

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardusts ~]$ supervisorctl reread
 thelounge: available
 [isabell@stardusts ~]$ supervisorctl update
 thelounge: added process group
 [isabell@stardusts ~]$ supervisorctl status
 thelounge                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardusts ~]$

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Creating users
--------------

Since we do not run a public server we have to add users before we can use The Lounge:

.. code-block:: console
 :emphasize-lines: 2, 3

 [isabell@stardusts ~]$ thelounge add isabell
 2018-10-09 20:20:20 [PROMPT] Enter password:
 2018-10-09 20:20:22 [PROMPT] Save logs to disk? (yes)
 2018-10-09 20:21:12 [INFO] User isabel created.
 2018-10-09 20:21:12 [INFO] User file located at /home/isabell/.lounge/users/isabel.json.
 [isabell@stardusts ~]$

If you need to change the password for a user this can be done with:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardusts ~]$ thelounge reset isabell
 2018-10-09 20:22:02 [PROMPT] Enter new password:
 2018-10-09 20:22:06 [INFO] Successfully reset password for isabel.
 [isabell@stardusts ~]$

If you need to change the settings for a user this can be done with:

::

 [isabell@stardusts ~]$ thelounge edit isabell
 [isabell@stardusts ~]$

Launch The Lounge
-----------------

Point your browser to your The Lounge URL and enjoy.

Updates
=======

.. note:: Check the release_ page or update feed_ regularly to stay informed about the newest version.

Update
------

To get the latest version of The Lounge you can use the ``npm`` package manager:

::

 [isabell@stardusts ~]$ npm update --global thelounge
 + thelounge@2.7.1
    added 4 packages, removed 22 packages and updated 12 packages in 3.176s
 [isabell@stardusts ~]$

Afterwards you have to restart you supervisord for The Lounge:

.. code-block:: console

 [isabell@stardusts ~]$ supervisorctl restart thelounge
 thelounge: stopped
 thelounge: started
 [isabell@stardusts ~]$ supervisorctl status
 thelounge                        RUNNING   pid 11044, uptime 0:00:08
 [isabell@stardusts ~]$

If it's not in state RUNNING, check your configuration.

.. _The Lounge: https://thelounge.chat/
.. _the official documentation: https://thelounge.chat/docs/server/configuration.html
.. _Shout: http://shout-irc.com/
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _npm: https://manual.uberspace.de/en/lang-nodejs.html#npm
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _htaccess: https://manual.uberspace.de/en/web-documentroot.html#own-configuration
.. _apache: https://manual.uberspace.de/en/lang-nodejs.html#connection-to-webserver
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _release: https://github.com/thelounge/thelounge/releases
.. _feed: https://github.com/thelounge/thelounge/releases.atom

----

Tested with The Lounge 2.7.1, Uberspace 7.1.13.0

.. authors::
