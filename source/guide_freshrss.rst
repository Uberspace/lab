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

FreshRSS_ is a multi-user self-hosted RSS feed aggregator.

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

We're using PHP in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use FreshRSS with your own domain, it needs to be set up.

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`DocumentRoot <web-documentroot>` and download the latest release from GitHub, then unzip it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/FreshRSS/FreshRSS/archive/master.zip
 --2018-09-24 14:30:37--  https://github.com/FreshRSS/FreshRSS/archive/master.zip
 Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
 […]
 Saving to: ‘master.zip’

     [   <=>                                                                                                                   ] 2,694,638   4.37MB/s   in 0.6s

 2018-09-24 14:30:38 (4.37 MB/s) - ‘master.zip’ saved [2694638]
 [isabell@stardust isabell]$ unzip master.zip
 […]
  inflating: FreshRSS-master/tests/app/Models/UserQueryTest.php
  inflating: FreshRSS-master/tests/bootstrap.php
  inflating: FreshRSS-master/tests/phpunit.xml


Now remove your ``html`` directory and create a symbolic link ``html -> FreshRSS-master/p/``:

.. warning:: Make sure ``html`` is empty before deleting it. If there are any files you want to keep in ``html``, you can also rename the folder instead of deleting it.

::

 [isabell@stardust isabell]$ mv html html.old
 [isabell@stardust isabell]$ ln -s FreshRSS-master/p/ html
 [isabell@stardust isabell]$ ls -l
 total 2636
 drwxrwxr-x. 11 isabell isabell    4096 Sep  9 11:03 FreshRSS-master
 lrwxrwxrwx.  1 isabell isabell      18 Sep 24 14:43 html -> FreshRSS-master/p/
 -rw-rw-r--.  1 isabell isabell 2694638 Sep 24 14:30 master.zip

Configuration
=============

Point your browser to your domain, e.g. ``https://isabell.uber.space`` and follow the instructions to set up FreshRSS. In step 3, we recommend to use a separate database such as ``<username>_freshrss``. Replace ``<username>`` with your actual user name.

Cron job
--------

To automatically update your feeds every ten minutes, set up a cron job like this using the ``crontab -e`` command.

::

 */10 * * * * php /var/www/virtual/$USER/FreshRSS-master/app/actualize_script.php > $HOME/logs/FreshRSS.log 2>&1

Updates
=======

Keep an eye on the FreshRSS releases feed, which has automatically been added as your first subscription in FreshRSS. When a new version is released, remove the previously downloaded ZIP archive and download the current release, then unzip it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm master.zip
 [isabell@stardust isabell]$ wget https://github.com/FreshRSS/FreshRSS/archive/master.zip
 --2018-09-24 14:30:37--  https://github.com/FreshRSS/FreshRSS/archive/master.zip
 Resolving github.com (github.com)... 192.30.253.112, 192.30.253.113
 […]
 Saving to: ‘master.zip’

     [   <=>                                                                                                                   ] 2,694,638   4.37MB/s   in 0.6s

 2018-09-24 14:30:38 (4.37 MB/s) - ‘master.zip’ saved [2694638]
 [isabell@stardust isabell]$ unzip -o master.zip -x FreshRSS-master/data/do-install.txt
 […]
  inflating: FreshRSS-master/tests/app/Models/UserQueryTest.php
  inflating: FreshRSS-master/tests/bootstrap.php
  inflating: FreshRSS-master/tests/phpunit.xml
 [isabell@stardust isabell]$

This will overwrite any changed files while keeping your current configuration.

.. _FreshRSS: https://freshrss.org/
.. _GNU AGPLv3: https://www.gnu.org/licenses/agpl-3.0.html

----

Tested with FreshRSS 1.11.2, Uberspace 7.1.12.0

.. author_list::
