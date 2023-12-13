.. highlight:: console

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. tag:: lang-php
.. tag:: web
.. tag:: forum

.. sidebar:: Logo

  .. image:: _static/images/flatboard.png
      :align: center

#########
Flatboard
#########

.. tag_list::

Flatboard_ is a simple, lightweight, modern and fast flat-file forum, using JSON and Markdown or BBcode.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`

License
=======

Flatboard_ is released under the `MIT License`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.2:

::

 [isabell@stardust ~]$ uberspace tools version use php 8.2
 Selected PHP version 8.2
 [isabell@stardust ~]$

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download and configure Flatboard_.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget http://flatboard.free.fr/uploads/plugins/flatboard_latest.zip
 [...]
 Saving to: ‘flatboard_latest.zip’
 2019-03-03 16:47:53 (19.0 MB/s) - ‘flatboard_latest.zip’ saved [1280825/1280825]
 [isabell@stardust html]$

Unzip the archive and then delete it.

.. code-block:: console
 :emphasize-lines: 1,5

 [isabell@stardust html]$ unzip flatboard_latest.zip
 Archive:  flatboard_latest.zip
  inflating: flatboard.zip
  inflating: index.php
 [isabell@stardust html]$ rm flatboard_latest.zip
 [isabell@stardust html]$


Finishing installation
======================

Now point your Browser to your installation URL ``https://isabell.uber.space/index.php``.
Complete the form and follow the installation instructions.

You will need to enter the following information:

  * language: the language you prefer (English, French, Russian).

Then push the Unzip-Button.

  * title: title of your forum
  * description: what is your forum about
  * E-Mail: your admin e-mail address
  * administrator: set up your admin password
  * language: the language you prefer (English, French, German, Russian, Italian) « Yes, the question is double.

Updates
=======

.. note:: Check the update feed_ or twitter_ regularly to stay informed about the newest version.

1. First make a backup from ``/data`` folder and move it to your ``/home`` folder.

.. code-block:: console
 :emphasize-lines: 2,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ tar cfvz flatforum-data_backup.tar.gz *
 data/
 [...]
 data/key.php
 [isabell@stardust html]$ mv flatforum-data_backup.tar.gz $HOME
 [isabell@stardust html]$

2. Download the latest version from Flatboard_.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://flatboard.org/download.php?file=flatboard_latest.zip
 [...]
 Saving to: ‘flatboard_latest.zip’

 100%[============================================================================================>] 1,280,825   --.-K/s   in 0.06s

 2019-03-03 16:47:53 (19.0 MB/s) - ‘flatboard_latest.zip’ saved [1280825/1280825]
 [isabell@stardust html]$

3. Extract the zip file.

Unzip the archive, copy new files and folders and then delete it.

.. code-block:: console
 :emphasize-lines: 1,5,6,7,13,14,15,16

 [isabell@stardust html]$ unzip flatboard_latest.zip -d UPDATE
 Archive:  flatboard_latest.zip
  inflating: flatboard.zip
  inflating: index.php
 [isabell@stardust html]$ cd UPDATE
 [isabell@stardust UPDATE]$ rm flatboard_latest.zip
 [isabell@stardust UPDATE]$ unzip flatboard.zip
 Archive:  flatboard.zip
   creating: flatboard/
  inflating: flatboard/README.md
  [...]
  inflating: flatboard/view.php
 [isabell@stardust UPDATE]$ cd flatboard
 [isabell@stardust UPDATE]$ cp -r * /var/www/virtual/$USER/html/
 [isabell@stardust UPDATE]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ rm -rf UPDATE
 [isabell@stardust html]$ rm install.php
 [isabell@stardust html]$

4. Clear plugin and theme cache.

Delete all files stocked in ``data/plugin`` folder and go to your plugins page to activate your plugins again.

::

 [isabell@stardust html]$ cd data/plugin
 [isabell@stardust plugin]$ rm -rf *
 [isabell@stardust plugin]$ cd /var/www/virtual/$USER/html/

Delete the ``theme/YourTheme/cache/`` folder. In this example ``bootstrap`` theme is used.

::

 [isabell@stardust html]$ cd theme/bootstrap/
 [isabell@stardust bootstrap]$ rm -rf cache
 [isabell@stardust bootstrap]$

5. Log into the admin area and check your settings.



.. _feed: https://github.com/Fred89/flatboard/commits
.. _twitter: https://twitter.com/flatboardoffic1
.. _Flatboard: https://flatboard.org/
.. _License: https://github.com/Fred89/flatboard/blob/master/LICENSE

----

Tested with Flatboard 3.1, Uberspace 7.15.6

.. author_list::
