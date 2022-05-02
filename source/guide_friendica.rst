.. highlight:: console

.. author:: Tobias Quathamer <t.quathamer@mailbox.org>

.. tag:: lang-php
.. tag:: web
.. tag:: ActivityPub
.. tag:: fediverse
.. tag:: microblogging

.. sidebar:: About

  .. image:: _static/images/friendica.svg
      :align: center

#########
Friendica
#########

.. tag_list::

.. error::

  This guide seems to be **broken** for the current versions of XYZ, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1254

Friendica_ is a free and open-source distributed social network.
It has built-in support for ActivityPub (e.g. Funkwhale, Hubzilla,
Mastodon, Pleroma, Pixelfed), OStatus (e.g. StatusNet, GNU social,
Quitter) and diaspora* protocols.

It forms one part of the Fediverse, an interconnected and
decentralized network of independently operated servers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>` and its package manager :manual_anchor:`composer <lang-php#package-manager>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`Cron <daemons-cron>`
  * :manual:`Domains <web-domains>`
  * Git_

License
=======

Friendica_ is released under the `GNU Affero General Public License v3.0`_.
All relevant information can be found in the LICENSE_ file in the
repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for Friendica:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_friendica"
  [isabell@stardust ~]$

Your friendica URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note::
  Friendica should be installed in a domain of its own (or in a subdomain),
  not in a subdirectory of a domain.

  **Make a decision now, because you are going to have to stick with it.**

Installation
============

Download the source
-------------------

In order to simplify updates for friendica and the needed addons,
you can use the git repository instead of tarballs.
If you want the bleeding edge, you could even switch your friendica
installation to the next pre-release or development version.

For this guide, we'll use the stable branch of friendica.

First, go one level above your :manual:`DocumentRoot <web-documentroot>`
and use ``git clone`` to get the friendica repository as well as
the addons. Please note, that friendica currently does not support
composer v2, so you need to use composer v1, which is included in
the git repository in the directory :file:`bin`.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ git clone https://github.com/friendica/friendica.git -b stable
 [isabell@stardust isabell]$ cd friendica
 [isabell@stardust friendica]$ bin/composer.phar install --no-dev
 [isabell@stardust friendica]$ git clone https://github.com/friendica/friendica-addons.git -b stable addon
 [isabell@stardust friendica]$

Copy the file :file:`.htaccess-dist` to :file:`.htaccess`:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/friendica
 [isabell@stardust friendica]$ cp .htaccess-dist .htaccess
 [isabell@stardust friendica]$

Remove your empty DocumentRoot and create a new symbolic link
to the friendica directory:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/friendica html
 [isabell@stardust isabell]$

Optional: file storage backend
------------------------------

Friendica can use the database to store uploaded files
(like images) for posts. This is the default. However, you
might want to change this to a file system based storage.

It is recommended to setup a directory which is not reachable
from your public URL. Therefore, create a new directory outside
of your friendica installation:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ mkdir storage
 [isabell@stardust isabell]$

Finishing installation
======================

Point your browser to your uberspace URL or domain.
It may take a while to load during this installation run.

Page 1 -- System tests:
  The first page shows some system tests, which should all
  be green.

Page 2 -- Basic setup:
  This includes things like SSL, the hostname, and the
  installation path. The automatically detected values
  should be correct, you should not need to change
  anything here.

Page 3 -- Database Configuration:
  * Database host: ``localhost``
  * Database User: ``isabell``
  * Database Password: ``yourMySQLPassword``
  * Database Name: ``isabell_friendica``

Page 4 -- Server setup:
  Enter an e-mail address for the friendica site admin.
  You will register a user with this address later on, and that
  user will be granted admin rights for this friendica
  installation.
  Also, you can set a default timezone and system language for
  friendica.

After those setup steps, point your browser to the registration
page (``https://isabell.uber.space/register``) and sign up with
the same e-mail address that you've used in page 4 above.

Configure your account basics
-----------------------------

You should receive an e-mail with a provisional password.
Log on using your nickname or email address and that password.
Go to settings and change the provided password to one
of your choice.

Configure your site basics
--------------------------

Visit the site section of the admin menu to close
registration access to your new site -- this is a choice you
can revise later. For a small site for a group of friends or
a family, the best registration policy would be invite-only.

Go to the site section of the admin menu and enable searching
for updates in the advanced settings. This way, you'll be
notified of available updates on the overview page of the
admin menu.

If you've created a folder for uploaded files, go to the storage
section of the admin menu and enter the storage file path
into the textfield, e.g. :file:`/var/www/virtual/isabell/storage`.

Activate scheduled tasks
------------------------

The background tasks need to be run every 5--10 minutes. For a
small to medium site, an interval of 10 minutes is sufficient.

Add the following cronjob to your :manual:`crontab <daemons-cron>`
to run the worker every 10 minutes:

.. code-block:: none

 */10 * * * * cd /var/www/virtual/$USER/html && php bin/worker.php > /dev/null 2>&1

Updates
=======

If you want to update to the next stable version, you can
use git to download the necessary files. Please remember to
always keep your local base friendica and addon repository
clones on the same branch and pull them simultaneously:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/friendica
 [isabell@stardust friendica]$ git pull && cd addon && git pull && cd ..
 [isabell@stardust friendica]$ bin/composer.phar install --no-dev
 [isabell@stardust friendica]$

.. note:: Check the friendica blog_ regularly to stay informed
  about the newest version.
  It's also recommended to enable searching for updates in the
  admin menu (site > advanced settings).

Backup
======

This is a list of files you need to restore your friendica node:

- A dump of the database
- Configuration file: :file:`config/local.config.php`
- The :file:`.htaccess` file (if it was edited after copying
  the :file:`.htaccess-dist` file)
- If the file storage backend is set to filesystem, a copy of
  the root filesystem folder (e.g. :file:`/var/www/virtual/isabell/storage`).

.. _blog: https://friendi.ca/blog/
.. _Friendica: https://friendi.ca/
.. _GNU Affero General Public License v3.0: https://www.gnu.org/licenses/agpl-3.0.en.html
.. _Git: https://git-scm.com/
.. _LICENSE: https://github.com/friendica/friendica/blob/stable/LICENSE


----

Tested with Friendica 2021.09, Uberspace 7.12.0

.. author_list::
