.. highlight:: console

.. author:: Tobias Bell <uberspace@tobiasbell.de>

.. sidebar:: About

  .. image:: _static/images/ttrss.png
      :align: center

##############
Tiny Tiny RSS
##############

Tiny Tiny RSS is a free and open source web-based news feed (RSS/Atom) reader and
aggregator, designed to allow you to read news from any location, while feeling as
close to a real desktop application as possible.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * supervisord_
  * domains_
  * git_
  * PHP_
  * cron_

License
=======

The software is licensed under the GPL. All relevant information can be found in the repository of the project. 

  * https://git.tt-rss.org/git/tt-rss

Prerequisites
=============

We're using PHP in the latest stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

The URL where you want to run Tiny Tiny RSS needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Clone the Tiny Tiny RSS repository
----------------------------------

As Tiny Tiny RSS uses a rolling release model with the git master branch as current stable version, we
wil use git to download the software. So go to the webroot and clone Tiny Tiny RSS into the subfolder tt-rss

::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ git clone https://tt-rss.org/git/tt-rss.git .
 Cloning into '.'...
 remote: Counting objects: 59813, done.
 remote: Compressing objects: 100% (23687/23687), done.
 remote: Total 59813 (delta 32579), reused 59789 (delta 32557)
 Receiving objects: 100% (59813/59813), 74.56 MiB | 1.28 MiB/s, done.
 Resolving deltas: 100% (32579/32579), done.
 [isabell@stardust html]$

Configuration
=============

Setup your database
-------------------

It's a good idea to create the tables under a separate database.

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE <username>_tt_rss"

Replace <username> with your own user. 

Configure database and domain
-----------------------------

Now you should reach your installation under the URL ``https://<username>.uber.space/tt-rss`` (would be ``https://isabell.uber.space/tt-rss`` in our example).
Open the URL and set the Database settings to your MySQL hostname, username and password: the hostname is localhost and you should know your MySQL credentials by now. If you don’t, start reading again at the top.

Under other settings the domain https://isabell.uber.space should be shown.
Now click on `Test Configuration`. If everything worked you should see the messages
 * Configuration check succeeded.
 * Database test succeeded.

Click on `Initialize Database`. After that the generated configuration will be shown. Click on `Save configuration` to save it.
If you need to change it afterwards you will find it under ``~/html/config-php``.

 Configure users
 ---------------

 Now you can reach Tiny Tiny RSS under https://isabell.uber.space for the first time. Log in with 

  * User: admin
  * Password: password

You will be greeted by a dialog to change the default password. Do that and optionally add one or more users with restricted rights
for capturing and reading RSS feeds.

Setup daemon to fetch RSS feeds
-------------------------------
Create ``~/etc/services.d/ttrss.ini`` with the following content:

.. code-block:: ini

 [program:ttrss]
 directory=/home/<username>/html/
 command=/home/<username>/html/update_daemon2.php --quiet
 redirect_stderr=true

In our example this would be:

.. code-block:: ini

 [program:ttrss]
 directory=/home/isabell/html/
 command=/home/isabell/html/update_daemon2.php --quiet
 redirect_stderr=true

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 ttrss: available
 [isabell@stardust ~]$ supervisorctl update
 ttrss: added process group
 [isabell@stardust ~]$ supervisorctl status
 ttrss                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Setup automatic update
----------------------

To update your installation you just need to do a ``git pull`` and restart the RSS update daemon. So let's automate this.
Create the file ``~/bin/ttrss-update`` with the content

.. warning:: Replace ``<isabell>`` with your username!

::

 #/bin/sh
 cd /home/isabell/html
 git pull
 supervisorctl restart ttrss

Then make it executable

::

 [isabell@stardust ~]$ chmode +x ~/bin/ttrss-update

Now add a line to your crontab to update it daily.

::

 [isabell@stardust ~]$ crontab -e

Add the following line to the crontab and save it

.. warning:: Replace ``<isabell>`` with your username!

::

 @daily /home/isabell/bin/ttrss-update

If you don't want to get a mail for each update you need to add the line ``MAILTO=""`` to your crontab.

Finishing installation
======================

Point your browser to https://isabell.uber.space logon and add your first RSS feed!


.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _git: https://git-scm.com/
.. _cron: https://manual.uberspace.de/en/daemons-cron.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials

----

Tested with Tiny Tiny RSS `f5302247c6 <https://git.tt-rss.org/fox/tt-rss/commit/f5302247c6eecba217f35173b3f038cc828a7402>`_, Uberspace 7.1.1

.. authors::
