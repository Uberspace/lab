.. author:: logazer <https://logazer.de>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: wiki

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/wikijs.svg
      :align: center

#######
Wiki.js
#######

.. tag_list::

Wiki.js_ is a self-hosted open source wiki software with version tracking written in JavaScript and distributed under the AGPLv3 License.

It is highly extensible via a variety of modules, allowing for different ways of handling authentication, storage, and connecting various databases as well as a optional search engine of your choice.

Wiki.js has a WYSIWYG editor as well as support for markdown, html. Migration from MediaWiki is currently being developed.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

.. note:: If you already use PostgreSQL, you can skip the next two steps and take a look at :ref:`tuning`.

You need a database for Wiki.js:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_wiki"
  [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your wiki URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Create a ``wiki`` directory in your home.

::

  [isabell@stardust ~]$ mkdir ~/wiki
  [isabell@stardust ~]$

Download the latest `release <https://github.com/Requarks/wiki/releases/latest>`_ from GitHub,
apparently there is no direct URL to the latest archive file. For this matter, you can use `gitreleases.dev <https://gitreleases.dev>`_
which resolves to the latest archive file, which also comes in handy later for :ref:`updates`

::

  [isabell@stardust ~]$ wget https://github.com/Requarks/wiki/releases/download/2.1.113/wiki-js.tar.gz
  [...]
  Saving to: ‘wiki-js.tar.gz’
  [isabell@stardust ~]$

Extract the dowloaded archive to the ``wiki`` directory you created earlier.

::

  [isabell@stardust ~]$ tar xzf wiki-js.tar.gz -C ~/wiki
  [isabell@stardust ~]$

Configuration
=============

``cd`` into ``wiki`` and create a copy of the sample configuration file.

::

  [isabell@stardust ~]$ cd ~/wiki
  [isabell@stardust wiki]$ cp config.sample.yml config.yml
  [isabell@stardust wiki]$

Now edit the ``config.yml`` file. In the section ``db`` change ``user``,
``pass`` and ``db`` according to your credentials and database name.
``type`` can be set to **mariadb** because your Uberspace is using MariaDB.

.. code-block:: none
 :emphasize-lines: 3,6,7,8

 [...]
 db:
  type: mariadb
  host: localhost
  port: 3306
  user: isabell
  pass: MySuperSecretPassword
  db: isabell_wiki
 [...]

Configure web server
--------------------

.. note::

    Wiki.js is running on port 3000.

.. include:: includes/web-backend.rst

You can directly configure the backend to use a sub domain of choice
(e.g. **wiki.yourdomain.com**), if that domain is configured.
Using a different path than ``/`` (e.g. **yourdomain.com/wiki**)
whatsoever doesn't work, Wiki.js seems unable to resolve this correctly, even with ``--remove-prefix``

Setup daemon
------------

Create ``~/etc/services.d/wiki.ini`` with the following content:

.. code-block:: ini

 [program:wiki]
 directory=%(ENV_HOME)s/wiki
 command=env NODE_ENV=production /bin/node server

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Point your browser to your wiki URL and create a user account. Be sure to set the correct URL if it's asked for.
Now, you should be up and running. Enjoy!

.. _tuning:

Tuning
======================

Wiki.js is recommending PostgreSQL for best performance. You would just have to :lab:`set up PostgreSQL <guide_postgresql>`, create a database and
change the ``config.yml`` file accordingly, the rest of the process stays the same.

.. _updates:

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Update via script
-----------------

For a simple updating process you can use the following script. It could be extended and used in a :manual:`cronjob <daemons-cron>` etc.

If you did choose a different directory, be sure to change ``WIKIDIR`` to your need.
The script can also rollback to the last version before the update using the ``--rollback`` as only argument.
In order for this to work, a backup must exist in ``~/tmp/wiki.bak`` which is automatically created before every update.

.. warning:: As ``~/tmp/`` is **not persistent**, the rollback can only be used immediately after a failed update, not after a long period of time.

.. code-block:: console
 :emphasize-lines: 4

 #!/bin/bash
 # created by peleke.de (Ghost Guide), customized by logazer

 WIKIDIR=~/wiki
 PACKAGE_VERSION_OLD=$(sed -nE 's/^\s*"version": "(.*?)",$/\1/p' $WIKIDIR/package.json)
 CURRENT_WIKI=$(curl -s https://api.github.com/repos/Requarks/wiki/releases/latest | grep tag_name | head -n 1 | cut -d '"' -f 4)
 CURRENT_WIKI_DOWNLOAD="https://gitreleases.dev/gh/Requarks/wiki/latest/wiki-js.tar.gz"

 if [[ $1 == "--rollback" ]]
 then
  if [[ -d ~/tmp/wiki.bak ]]
  then
   PACKAGE_VERSION_BACKUP=$(sed -nE 's/^\s*"version": "(.*?)",$/\1/p' ~/tmp/wiki.bak/package.json)
   echo "Stopping Wiki.js ..."
   supervisorctl stop wiki
   echo "Rolling back to $PACKAGE_VERSION_BACKUP ..."
   rm -rf $WIKIDIR/* && cp -r ~/tmp/wiki.bak/* $WIKIDIR
   echo "Rollback complete ..."
   echo "Starting Wiki.js. This may take a few seconds ..."
   supervisorctl start wiki
   exit 0
  else
   echo "No Backup found :("
   exit 1
  fi
 fi

 if [[ $CURRENT_WIKI != $PACKAGE_VERSION_OLD ]]
 then
  read -r -p "Do you want to update Wiki.js $PACKAGE_VERSION_OLD to version $CURRENT_WIKI? [Y/n] " response
  if [[ $response =~ ^([yY]|"")$ ]]
  then
   echo "Updating Wiki.js ..."
   echo "Downloading version $CURRENT_WIKI ..."
   (cd ~/tmp/ && curl --progress-bar -LO $CURRENT_WIKI_DOWNLOAD)
   echo "Stopping Wiki.js ..."
   supervisorctl stop wiki
   echo "Removing version $PACKAGE_VERSION_OLD ..."
   cp $WIKIDIR/config.yml ~/tmp/config.yml.bak
   rm -rf ~/tmp/wiki.bak
   cp -r $WIKIDIR ~/tmp/wiki.bak
   rm -rf $WIKIDIR/*
   echo "Extracting version $CURRENT_WIKI ..."
   tar xzf ~/tmp/wiki-js.tar.gz -C $WIKIDIR && rm ~/tmp/wiki-js.tar.gz
   cp ~/tmp/config.yml.bak $WIKIDIR/config.yml && rm ~/tmp/config.yml.bak

   PACKAGE_VERSION=$(sed -nE 's/^\s*"version": "(.*?)",$/\1/p' $WIKIDIR/package.json)
   echo "Wiki.js $PACKAGE_VERSION_OLD has been updated to version $PACKAGE_VERSION"
   echo "Starting Wiki.js. This may take a few seconds ..."
   supervisorctl start wiki
   supervisorctl status
   echo "If something seems wrong, please check the logs: 'supervisorctl tail wiki'"
   echo "To rollback the update to the last version, use the option '--rollback'"
  fi
 else
  echo "Wiki.js $PACKAGE_VERSION_OLD is already up-to-date, no update needed."
 fi


.. _Wiki.js: https://wiki.js.org
.. _feed: https://github.com/Requarks/wiki/releases/

----

Tested with Wiki.js 2.1.113, Uberspace 7.3.11.0

.. author_list::
