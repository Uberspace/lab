.. highlight:: console

.. author:: Jonas <https://github.com/jfowl>

.. tag:: lang-php

.. sidebar:: Logo

  .. image:: _static/images/grocy.svg
      :align: center

####
Grocy
####

.. tag_list::

Grocy is a web-based self-hosted groceries & household management solution for your home.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Git_
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

Step 1
-----

Download grocy to the root of your uberspace web directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://releases.grocy.info/latest -O grocy_latest.zip
 […]
 Saving to: ‘grocy_latest.zip’
 
 grocy_latest.zip        100%[===============================>]  54,83M  12,6MB/s    in 4,4s

 2020-08-26 12:09:31 (12,5 MB/s) - ‘grocy_latest.zip’ saved [57489683/57489683]
 [isabell@stardust isabell]$ 

Step 2
------

Unpack the downloaded grocy release

::

 [isabell@stardust isabell]$ unzip -q grocy_latest.zip
 [isabell@stardust isabell]$ rm grocy_latest.zip
 [isabell@stardust isabell]$ 


Step 3
------

Uberspace, by default, serves the `html` directory via http(s).
Therefore, we move everything from `public`, the directory that grocy want's us to serve, to public.

::

 [isabell@stardust isabell]$ mv public/* public/.htaccess html
 [isabell@stardust isabell]$ 



Step 4
------

Copy the default config file to `data/config.php` and edit it to your liking

::

 [isabell@stardust isabell]$ cp config-dist.php data/config.php
 [isabell@stardust isabell]$ nano data/config.php
 [isabell@stardust isabell]$ 


You will probably want to change the `CURRENCY` to `EUR` and `CULTURE` to `de`.



Finishing installation
======================

Point your Browser to your installation URL ``https://isabell.uber.space``.
This will take a moment, as grocy will need to create the default database at first.

When prompted for a login, use `admin` for both username and password. CHANGE THIS AS SOON AS POSSIBLE!


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Grocy comes with a handy update script, so just run this and copy the public files to html again.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ bash update.sh
 [isabell@stardust isabell]$ mkdir html
 [isabell@stardust isabell]$ mv public/* public/.htaccess html



.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _Grocy: https://grocy.info/
.. _feed: https://github.com/grocy/grocy/releases.atom
.. _MIT License: https://github.com/grocy/grocy/blob/master/LICENSE
.. _Github Repository: https://github.com/grocy/grocy/releases

----

Tested with Grocy 2.7.1, Uberspace 7.7.4.0

.. author_list::
