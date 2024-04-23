.. author:: roang <https://github.com/Roang-zero1>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: irc

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/the-lounge.svg
      :align: center

##########
The Lounge
##########

.. tag_list::

`The Lounge`_ is an open source IRC web client written in JavaScript and distributed under the MIT License. This self hosted client stays always connected so you never miss out on the most important chats. Another goal of The Lounge is to bring modern chat features such as push notifications, link previews and many more to your IRC chats.

The Lounge is based on the project Shout_ from which it is a community driven fork.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in version 18:

::

 [isabell@stardusts ~]$ uberspace tools version use node 18
 Selected Node.js version 18
 The new configuration is adapted immediately. Minor updates will be applied automatically.
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
 + thelounge@4.4.1
 added 242 packages in 31.627s
 [isabell@stardusts ~]$

Verify installation
-------------------

::

 [isabell@stardusts ~]$ thelounge --version
 v4.4.1

Configuration
=============

Configure web server
--------------------

.. note::

    The Lounge is running on port 9000.

.. include:: includes/web-backend.rst

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
 startsecs=60
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Creating users
--------------

Since we do not run a public server we have to add users before we can use The Lounge:

.. code-block:: console
 :emphasize-lines: 2, 3

 [isabell@stardust ~]$ thelounge add isabell
 2021-10-21 11:46:33 [PROMPT] Enter password:
 2021-10-21 11:46:39 [PROMPT] Save logs to disk? (yes)
 2021-10-21 11:46:41 [INFO] User isabell created.
 2021-10-21 11:46:41 [INFO] User file located at  /home/isabell/.lounge/users/isabel.json.
 [isabell@stardust ~]$

If you need to change the password for a user this can be done with:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ thelounge reset isabell
 2021-10-21 11:47:02 [PROMPT] Enter new password:
 2021-10-21 11:47:06 [INFO] Successfully reset password for isabel.
 [isabell@stardust ~]$

If you need to change the settings for a user this can be done with:

::

 [isabell@stardust ~]$ thelounge edit isabell
 [isabell@stardust ~]$

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

 [isabell@stardust ~]$ npm update --global thelounge
 + thelounge@2.7.1
    added 4 packages, removed 22 packages and updated 12 packages in 3.176s
 [isabell@stardust ~]$

Afterwards you have to restart you supervisord for The Lounge:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl restart thelounge
 thelounge: stopped
 thelounge: started
 [isabell@stardust ~]$ supervisorctl status
 thelounge                        RUNNING   pid 11044, uptime 0:00:08
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

.. _The Lounge: https://thelounge.chat/
.. _the official documentation: https://thelounge.chat/docs/server/configuration.html
.. _Shout: http://shout-irc.com/
.. _release: https://github.com/thelounge/thelounge/releases
.. _feed: https://github.com/thelounge/thelounge/releases.atom

----

Tested with The Lounge 4.2.0, Uberspace 7.11.5

.. author_list::
