.. highlight:: console

.. author:: Jan Klomp <https://klomp.de>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: rss
.. tag:: web
.. tag:: feedreader

.. sidebar:: About

  .. image:: _static/images/tt-rss.png
      :align: center

#############
Tiny Tiny RSS
#############

.. tag_list::

`Tiny Tiny RSS`_ is an open source multiuser web-based news feed reader and aggregator (RSS/Atom). TTRSS is a server side AJAX powered application, the user only needs a web browser or one of the available Android clients. It supports multiple ways to share stuff, many plugins and themes, a JSON-based API and much more. The background service polls for subscribed web feeds at regular intervalls.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Tiny Tiny RSS is free software, licensed under GNU GPLv3, all relevant legal information can be found here

  * https://www.gnu.org/licenses/gpl-3.0.html

Prerequisites
=============

Tiny Tiny RSS needs :manual:`PHP <lang-php>` version 5.6 or newer:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your website domain needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

We're using Git to clone the current version from Tiny Tiny RSS into the subdirectory ``ttrss`` from your :manual:`DocumentRoot <web-documentroot>`. Always use the latest Git code from master branch.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USERNAME/html/
 [isabell@stardust html]$ git clone https://git.tt-rss.org/fox/tt-rss.git ttrss
 Clonig into 'ttrss'...
 remote: Enumerating objects: xxxxx, done.
 [...]
 Resolving deltas: 100% (xxxxx,xxxxx), done.
 [isabell@stardust html]$
 
It's time to create an :manual_anchor:`additional database <database-mysql.html#additional-databases>` database called ``$username_ttrss`` for Tiny Tiny RSS.

::

 [isabell@stardust html]$ mysql -e "create database $username_ttrss"
 [isabell@stardust html]$

Now point your browser to your uberspace url or domain (e.g. ``https://isabell.uber.space/ttrss``) and follow the instructions to complete the installation.

Database settings:
  * Database type: ``MySQL``
  * Username: ``$username``
  * Password: ``your_MySQL_password`` (you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now; if you don't, have a look again at the top)
  * Database name: ``$username_ttrss``
  * Host name: ``localhost``
  * Port: ``3306``
  
Other settings:
  * Tiny Tiny RSS URL: ``https://$username.uber.space/ttrss``
  
After that you can click on the button ``Test configuration``. All tests should be succeeded.

Finally you have to click on ``initialize the database`` and when this step is done *don't forget to click on* ``Save configuration``.

Open your Tiny Tiny RSS installation on ``https://$username.uber.space/ttrss`` and login with default credentials (username: ``admin``, password: ``password``).

.. warning:: *Change your default password now*!

With the admin account you can create new user logins for the everyday use of Tiny Tiny RSS.

Configuration
=============

Configure update daemon 
-----------------------

The update daemon is the recommended way to automatically update the subscribed RSS or Atom feeds. We're using :manual:`supervisord <daemons-supervisord>` to create the required service.

Create a subdirectory ``scripts`` into your :manual:`home directory <basics-home>` and put a new shell script ``ttrss.sh`` with the following content into it:

::

 #!/bin/bash
 cd /var/www/virtual/$username/html/ttrss/
 exec php ./update_daemon2.php --daemon 2>&1
 
Make the script executable:

::

 [isabell@stardust ~]$ chmod u+rwx ~/scripts/ttrss.sh
 [isabell@stardust ~]$
 
Create a file ``ttrss.ini`` in the directory ``~/etc/services.d/`` with the following content:

::

 [program:ttrss]
 command=/home/$username/scripts/ttrss.sh
 autostart=yes
 autorestart=yes
 
Ask :manual:`supervisord <daemons-supervisord>` to look for the new ``ttrss.ini`` file, then start the daemon and check the status:

::

 [isabell@stardust ~]$ supervisorctl reread
 my-daemon: available
 [isabell@stardust ~]$ supervisorctl update
 my-daemon: added process group
 [isabell@stardust ~]$ supervisorctl status ttrss
 ttrss          RUNNING   pid 3771, uptime 0 days, 00:00:22
 [isabell@stardust ~]$
 
 
Now Tiny Tiny RSS runs with its own service on the server and all subscribed feeds will be updated.

Security
========

.. note:: 
  * Change the default admin password after the installation! 
  * Create one ore more user logins for the everyday use of Tiny Tiny RSS. 
  * Check for updates in the update feed_ regularly to stay informed about the newest version (see below).

Updates
=======

Updating Tiny Tiny RSS is done easy with Git:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USERNAME/html/ttrss/
 [isabell@stardust ttrss]$ git pull origin master
  * branch                master     -> FETCH_HEAD
 Already up to date.
 [isabell@stardust ttrss]$
 
Afterwards when logging in to Tiny Tiny RSS you may be redirected to the database updater. Log in with admin credentials and follow instructions.
 

.. _Tiny Tiny RSS: https://tt-rss.org
.. _feed: https://git.tt-rss.org/fox/tt-rss/commits/master

----

Tested with Tiny Tiny RSS v20.06-c352e872e , Uberspace 7.7.1.2

.. author_list::

