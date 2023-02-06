.. highlight:: console

.. author:: Jonas <https://github.com/jfowl>

.. tag:: lang-php

.. sidebar:: Logo

  .. image:: _static/images/grocy.svg
      :align: center

#####
Grocy
#####

.. tag_list::

Grocy_ is a web-based self-hosted groceries & household management solution for your home.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Domains <web-domains>`

License
=======

Grocy is released under the `MIT license`_.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download
--------

Download grocy:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ wget https://releases.grocy.info/latest -O grocy_latest.zip
 […]
 Saving to: ‘grocy_latest.zip’

 grocy_latest.zip        100%[===============================>]  54,83M  12,6MB/s    in 4,4s

 2020-08-26 12:09:31 (12,5 MB/s) - ‘grocy_latest.zip’ saved [57489683/57489683]
 [isabell@stardust isabell]$

Extract
-------

Unpack the downloaded grocy release:

::

 [isabell@stardust isabell]$ unzip -q grocy_latest.zip -d grocy
 [isabell@stardust isabell]$ rm grocy_latest.zip
 [isabell@stardust isabell]$


Expose
------

Remove the default page from your DocumentRoot and link it to grocy's public folder:

::

 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s grocy/public html
 [isabell@stardust isabell]$


Configure
---------

Copy the default config file to ``data/config.php``:

::

 [isabell@stardust isabell]$ cd grocy
 [isabell@stardust grocy]$ cp config-dist.php data/config.php
 [isabell@stardust grocy]$

Now use your preferred text editor and edit ``data/config.php`` to your liking.

You will probably want to change the ``CURRENCY`` and ``CULTURE`` to your language code (e.g. ``EUR`` for Euro and ``de`` for Germany).

The config file provide's more help about this in it's comments, so make sure to read them.

Finishing installation
======================

Point your Browser to your installation URL (e.g. ``https://isabell.uber.space``).
This will take a moment, as grocy will need to create the default database at first.

When prompted for a login, use ``admin`` for both username and password.

.. warning:: Change the default password as soon as possible, as it poses a security risk. If you don't, anyone can access your data and change your password for you.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Grocy comes with a handy update script, so just run this and copy the public files to html again.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/grocy
 [isabell@stardust grocy]$ bash update.sh
 [isabell@stardust grocy]$



.. _Grocy: https://grocy.info/
.. _feed: https://github.com/grocy/grocy/releases.atom
.. _MIT License: https://github.com/grocy/grocy/blob/master/LICENSE
.. _Github Repository: https://github.com/grocy/grocy/releases

----

Tested with Grocy 3.3.2, Uberspace 7.13.0, and PHP 8.1

.. author_list::
