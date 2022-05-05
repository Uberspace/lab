.. author:: André Jaenisch <https://jaenis.ch>

.. tag:: lang-php
.. tag:: web
.. tag:: fediverse
.. tag:: ActivityPub

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/castopod.svg
      :align: center

########
Castopod
########

.. tag_list::

Castopod_ is a free and open-source podcast hosting platform.

It forms one part of the Fediverse, an interconnected and
decentralized network of independently operated servers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>` and its package manager :manual_anchor:`composer <lang-php#package-manager>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`Cron <daemons-cron>`
  * :manual:`domains <web-domains>`

License
=======

Castopod_ is released under the `GNU Affero General Public License v3.0`_.
All relevant information can be found in the LICENSE.md_ file in the
repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.1
 Selected PHP version 8.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.

 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for Castopod:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_castopod"
  [isabell@stardust ~]$

Your castopod URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note::
  Castopod should be installed in a domain of its own (or in a subdomain),
  not in a subdirectory of a domain.

Installation
============

First, go one level above your :manual:`DocumentRoot <web-documentroot>`
and download the latest version. Make sure, it is a Castopod Package and not
the source code. At time of this writing this is v1.0.0-beta.14.

TODO: the permalink to latest version requires login:
https://docs.gitlab.com/ee/user/project/releases/#permanent-link-to-latest-release

Download the source
-------------------

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ wget https://code.castopod.org/adaures/castopod/uploads/48710de086e7b4dfa23f894e81e15365/castopod-1.0.0-beta.14.tar.gz
  [isabell@stardust isabell]$

Unpack and symlink
------------------

Unpack the tarball and remove the downloaded file.

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ tar --extract --verbose --ungzip --file castopod-1.0.0-beta.14.tar.gz
  [isabell@stardust isabell]$ rm castopod-1.0.0-beta.14.tar.gz
  [isabell@stardust isabell]$

Remove your empty DocumentRoot and create a new symbolic link
to the castopod directory:

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER
  [isabell@stardust isabell]$ rm --force html/nocontent.html; rmdir html
  [isabell@stardust isabell]$ ln --symbolic /var/www/virtual/$USER/castopod/public html
  [isabell@stardust isabell]$

Update .htaccess
----------------

Open the .htaccess file in html and remove unsupported lines: All and FollowSymLinks.

TODO: Codeblock needed here?

Finishing installation
======================

Before finishing the installation via wizard, set up some cronjobs for
various background processes:

For social features to work properly, this task is used to broadcast social activities
to your followers on the fediverse:

.. code-block:: none

   */10 * * * * cd /var/www/virtual/$USER/html && php index.php scheduled-activities

For having your episodes be broadcasted on open hubs upon publication using WebSub:

.. code-block:: none

   */10 * * * * cd /var/www/virtual/$USER/html && php index.php scheduled-websub-publish

Point your browser to your uberspace URL or domain.
You will see an error page. Add ``cp-install`` to the URL and finish the
instructions there. Make sure to pick a different value for Admin-Gateway and
Admin-Gateway.

Fixing file permissions
-----------------------

The permissions of the files are not correct. Follow
:manual_anchor:`DocumentRoot <web-documentroot#permissions>` to update them.

Security
========

After installation and updates, ensure that the file permissions are correct.
All files must be readonly except the following, who also need writing permissions:

/var/www/virtual/$USER/castopod/writable
/var/www/virtual/$USER/castopod/public/media

Updates
=======

If there is a new release available, move your /var/www/virtual/$USER/castopod/.env and
/var/www/virtual/$USER/castopod/public/media outside of those directories.
Then delete all other files there. Follow the installation instructions from above.
Move the files back to their original place.

Sometimes there are additional update instructions you have to follow. For example, .sql
files containing migrations.

TODO: Document how to run these without phpMyAdmin!

If you picked Redis as Caching mechanism, clear the cache.

Enjoy your new version!

.. note:: Check the releases_ regularly to stay informed about the newest version.


.. _releases: https://code.castopod.org/adaures/castopod/-/releases
.. _GNU Affero General Public License v3.0: https://www.gnu.org/licenses/agpl-3.0.en.html

Backup
======

Make sure to back up /var/www/virtual/$USER/castopod/.env and
/var/www/virtual/$USER/castopod/public/media as well as regular database dumps.

----

Tested with Castopod v1.0.0-beta.14, Uberspace 7.12.1

.. author_list::

