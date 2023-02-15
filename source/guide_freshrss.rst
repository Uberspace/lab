.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-php
.. tag:: web
.. tag:: rss

.. sidebar:: Logo

  .. image:: _static/images/freshrss.svg
      :align: center

########
FreshRSS
########

.. tag_list::

FreshRSS_ is a multiuser self-hosted RSS feed aggregator.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`PHP <lang-php>`
  * :manual:`cron <daemons-cron>`

License
=======

FreshRSS is free and open source software licensed under the `GNU AGPLv3`_.


Prerequisites
=============

We're using PHP in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use FreshRSS with your own domain, it needs to be set up.

.. include:: includes/web-domain-list.rst

Create a new MySQL database:

::

 [isabell@fairydust ~]$ mysql --verbose --execute="CREATE DATABASE ${USER}_freshrss"
 --------------
 CREATE DATABASE isabell_freshrss
 --------------

 [isabell@fairydust ~]$

Installation
============

``cd`` to your :manual:`DocumentRoot <web-documentroot>` and download the latest release from GitHub, then unzip it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/FreshRSS/FreshRSS/archive/edge.zip
 --2018-09-24 14:30:37--  https://github.com/FreshRSS/FreshRSS/archive/edge.zip
 Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
 […]
 Saving to: ‘edge.zip’

     [   <=>                    ] 2,694,638   4.37MB/s   in 0.6s

 2018-09-24 14:30:38 (4.37 MB/s) - ‘edge.zip’ saved [2694638]
 [isabell@stardust isabell]$ unzip edge.zip
 […]
   creating: FreshRSS-edge/tests/lib/PHPMailer/
  inflating: FreshRSS-edge/tests/lib/PHPMailer/PHPMailerTest.php
  inflating: FreshRSS-edge/tests/shellchecks.sh


Now remove your ``html`` directory and create a symbolic link ``html -> FreshRSS-edge/p/``:

::

 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s FreshRSS-edge/p/ html
 [isabell@stardust isabell]$ ls -l
 total 2636
 drwxrwxr-x. 11 isabell isabell    4096 Sep  9 11:03 FreshRSS-edge
 lrwxrwxrwx.  1 isabell isabell      18 Sep 24 14:43 html -> FreshRSS-edge/p/
 -rw-rw-r--.  1 isabell isabell 2694638 Sep 24 14:30 edge.zip

Configuration
=============

Point your browser to your domain, e.g. ``https://isabell.uber.space`` and follow the instructions to set up FreshRSS. In step 3, use ``MySQL`` as the database type and the database named ``<username>_freshrss`` you creataed earlier. Replace ``<username>`` with your actual user name.

Cron job
--------

To automatically update your feeds every ten minutes, set up a cron job like this using the ``crontab -e`` command.

::

 */10 * * * * php /var/www/virtual/$USER/FreshRSS-edge/app/actualize_script.php > $HOME/logs/FreshRSS.log 2>&1

Updates
=======

Keep an eye on the FreshRSS releases feed, which has automatically been added as your first subscription in FreshRSS. When a new version is released, remove the previously downloaded ZIP archive and download the current release, then unzip it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm edge.zip
 [isabell@stardust isabell]$ wget https://github.com/FreshRSS/FreshRSS/archive/edge.zip
 --2018-09-24 14:30:37--  https://github.com/FreshRSS/FreshRSS/archive/edge.zip
 Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
 […]
 Saving to: ‘edge.zip’

     [   <=>                                  ] 2,694,638   4.37MB/s   in 0.6s

 2018-09-24 14:30:38 (4.37 MB/s) - ‘edge.zip’ saved [2694638]
 [isabell@stardust isabell]$ unzip -o edge.zip -x FreshRSS-edge/data/do-install.txt
 […]
  inflating: FreshRSS-edge/tests/app/Models/UserQueryTest.php
  inflating: FreshRSS-edge/tests/bootstrap.php
  inflating: FreshRSS-edge/tests/phpunit.xml
 [isabell@stardust isabell]$

This will overwrite any changed files while keeping your current configuration.

.. _FreshRSS: https://freshrss.org/
.. _GNU AGPLv3: https://www.gnu.org/licenses/agpl-3.0.html

----

Tested with FreshRSS 1.20.0, Uberspace 7.13.0, and PHP 8.1

.. author_list::
