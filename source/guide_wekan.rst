.. highlight:: console

.. author:: Andrej <https://github.com/schoeke>
.. tag:: lang-nodejs
.. tag:: project-management
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/wekan.svg
      :align: center

########
Wekan
########

.. tag_list::

Wekan_ - Open Source kanban

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`node <lang-nodejs>`
  * :manual:`domains <web-domains>`
  * :lab:`MongoDB <guide_mongodb>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`


License
=======

Wekan is released under the very permissive `MIT License`_. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

We're using :manual:`Nodejs <lang-php>` in the stable version 12:

::

 [isabell@stardust ~]$ $ uberspace tools version use node 12
 Selected Node.js version 12
 The new configuration is adapted immediately. Minor updates will be applied automatically.
 [isabell@stardust ~]$

The domain you want to use should be already set up:

.. include:: includes/web-domain-list.rst

We'll also need :lab:`MongoDB <guide_mongodb>`, so follow the MongoDB guide and come back when it's running.

Let's create a password for a new database:

.. code-block::

 [isabell@stardust ~]$ pwgen 15 1
 randompassword
 [isabell@stardust ~]$

Once we have that, let's create the new database for Wekan itself.

.. code-block::

 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.4.1
 connecting to: mongodb://127.0.0.1:21017/admin
 Implicit session: session { "id" : UUID("6fd371f6-e1fa-461c-be0c-ea3cbe230a01") }
 MongoDB server version: 4.4.1
 > use wekan
 > db.createUser(
    {
      user: "wekan",
      pwd: "randompassword",
      roles: ["readWrite"]
    }
   )
 > exit
 [isabell@stardust ~]$


Installation
============

Download and extract .ZIP archive
-----------------------------------

Check the Wekan website for the `latest release`_ and copy the download link to the ``wekan-*.*.zip`` file. Then use ``wget`` to download it. Replace the URL with the one you just copied.

.. warning:: Make sure to use the latest version from the `latest release`_ page, as Wekan is developed in a fast pace.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ wget https://releases.wekan.team/wekan-4.43.zip
 […]
 Saving to: ‘wekan-4.43.zip’

 100%[========================================================================================================================>] 3,172,029   3.45MB/s   in 0.9s

 2018-10-11 14:48:20 (3.45 MB/s) - 'wekan-4.43.zip' saved [3172029]
 [isabell@stardust ~]$

Unzip the archive and then delete it. Replace the version in the file name with the one you downloaded.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ unzip wekan-4.43.zip
 [isabell@stardust ~]$ rm wekan-4.43.zip
 [isabell@stardust ~]$


Install server
--------------

Change into the server folder of wekan and delete two files before installing all dependencies and compile the code using node.

.. code-block:: console

 [isabell@stardust ~]$ cd bundle/programs/server
 [isabell@stardust server]$ rm node_modules/.bin/node-gyp
 [isabell@stardust server]$ rm node_modules/.bin/node-pre-gyp
 [isabell@stardust server]$ npm install node-gyp node-pre-gyp fibers
 [isabell@stardust server]$ cd
 [isabell@stardust ~]$


Configuration
=============


Setup daemon
------------

Next, we set up the daemon so that wekan is started automatically. Create ``~/etc/services.d/wekan.ini`` with the following content:

.. code-block:: ini

  [program:wekan]
  environment=PORT="8080",MONGO_URL="mongodb://wekan:randompassword@127.0.0.1:27017/wekan",ROOT_URL="https://isabell.uber.space"
  directory=%(ENV_HOME)s/bundle
  command=node main.js
  autostart=yes
  autorestart=yes

Now let's start the service:

.. include:: includes/supervisord.rst


Configure Webserver
-------------------

Lastly, we connect the server to the web.

.. note:: For this guide, Wekan will run on port 8080.

.. include:: includes/web-backend.rst


Finishing installation
======================

Point your browser to your Uberspace URL and create a user account which will be also your admin account.

Tuning
======

There are many more options that can be set via environment variables. To get an overview, have a look at the `Wekan Wiki`_.

Updates
=======

To update, simply download the newest version from the `latest release`_ website, unpack and rebuild.

.. note:: Check the update feed_ regularly to stay informed about the newest version. Wekan is updated often.

.. _wekan: https://wekan.org/
.. _MIT License: https://github.com/wekan/wekan/blob/master/LICENSE
.. _Wekan Wiki: https://github.com/wekan/wekan/wiki
.. _Github: https://github.com/wekan/wekan
.. _latest release: https://releases.wekan.team/
.. _feed: https://github.com/wekan/wekan/releases.atom

Tested with Wekan 4.43, Uberspace 7.7.9.0

.. author_list::
