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

 [isabell@stardust ~]$ mysql --verbose --execute="CREATE DATABASE ${USER}_freshrss"
 --------------
 CREATE DATABASE isabell_freshrss
 --------------

 [isabell@stardust ~]$

Installation
============

``cd`` to your :manual:`DocumentRoot <web-documentroot>` and download the latest release from GitHub, then unzip it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/FreshRSS/FreshRSS/archive/latest.zip
 --2018-09-24 14:30:37--  https://github.com/FreshRSS/FreshRSS/archive/latest.zip
 Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
 […]
 Saving to: ‘latest.zip’

     [   <=>                    ] 2,694,638   4.37MB/s   in 0.6s

 2018-09-24 14:30:38 (4.37 MB/s) - ‘latest.zip’ saved [2694638]
 [isabell@stardust isabell]$ unzip latest.zip
 […]
   creating: FreshRSS-latest/tests/lib/PHPMailer/
  inflating: FreshRSS-latest/tests/lib/PHPMailer/PHPMailerTest.php
  inflating: FreshRSS-latest/tests/shellchecks.sh


Configuration
=============

You can setup your FreshRSS installation using FreshRSS's command line interface (CLI):

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ cd FreshRSS-latest
 [isabell@stardust FreshRSS-latest]$ ./cli/do-install.php --default_user <yourfreshrssusername>  --base_url https://isabell.uber.space --title FreshRSS --api_enabled --db-type mysql --db-host localhost:3306 --db-user ${USER} --db-password "<yourmysqlpassword>" --db-base  ${USER}_freshrss 
 FreshRSS install…
 ℹ️ Remember to create the default user: isabell     ./cli/create-user.php --user isabell --password 'password' --more-options
 ℹ️ Remember to re-apply the appropriate access rights, such as:  sudo chown -R :www-data . && sudo chmod -R g+r . && sudo chmod -R g+w ./data/
 [isabell@stardust FreshRSS-latest]$ ./cli/create-user.php --user <yourfrehrssusername> --password <yourfreshrsspassword>
 FreshRSS creating user “isabell”…
 ℹ️ Remember to refresh the feeds of the user: isabell       ./cli/actualize-user.php --user isabell
 ℹ️ Remember to re-apply the appropriate access rights, such as:  sudo chown -R :www-data . && sudo chmod -R g+r . && sudo chmod -R g+w ./data/
 [isabell@stardust FreshRSS-latest]$

Make sure to replace the usernames, password, and base URL, so instead of ``<yourfreshrssusername>`` use the user name of your choice, etc.

Cron job
--------

To automatically update your feeds every ten minutes, set up a cron job like this using the ``crontab -e`` command.

::

 */10 * * * * php /var/www/virtual/$USER/FreshRSS-edge/app/actualize_script.php > $HOME/logs/FreshRSS.log 2>&1

Web Access
==========

Remove your ``html`` directory and create a symbolic link ``html -> FreshRSS-latest/p/``:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s FreshRSS-latest/p/ html
 [isabell@stardust isabell]$ ls -l
 total 2636
 drwxrwxr-x. 11 isabell isabell    4096 Sep  9 11:03 FreshRSS-latest
 lrwxrwxrwx.  1 isabell isabell      18 Sep 24 14:43 html -> FreshRSS-latest/p/
 -rw-rw-r--.  1 isabell isabell 2694638 Sep 24 14:30 latest.zip


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
