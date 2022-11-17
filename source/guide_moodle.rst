.. highlight:: console

.. spelling::
    Et
    voilà

.. author:: Direnc <direnc99@gmail.com>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web
.. tag:: self-hosting


.. sidebar:: About

  .. image:: _static/images/moodle.svg
      :align: center

##########
Moodle
##########

.. tag_list::

Moodle_ Moodle is an acronym for "Modular Object-Oriented Dynamic Learning Environment." It is a free and open-source learning management system (LMS) written in PHP and distributed under the GNU General Public License. More information on Wikipedia_ or the official Moodle_ page.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`cron <daemons-cron>`
  * :manual:`php <php-lang>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://docs.moodle.org/dev/License

Prerequisites
=============

We're using :manual:`php <lang-php>` in the stable version 8.0:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.0'
 [isabell@stardust ~]$

MySQL
-----

.. include:: includes/my-print-defaults.rst

We will create a separate database for moodle:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_moodle"
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

You can also setup your own :manual_anchor:`domain <web-domains.html>`. Note that you will have to create a separate folder for your domain as described in :manual_anchor:`DocumentRoot <web-documentroot.html>`.

Moodledata
----------
Moodle saves files and data into a folder for persistency. Create the moodledata folder:

::

 [isabell@stardust ~]$ mkdir ~/moodledata
 [isabell@stardust ~]$

Installation
============

Download
--------
First, download Moodle and extract it. For this, change into the html directory of your Uberspace.

Then download the latest version (Moodle-Download_ page) of the tgz archive and extract it. It is best to select the stable version. 

Note that the download link on the page is actually a redirect. So instead of the link behind the button, use the direct link e.g.: ``https://download.moodle.org/download.php/direct/...``.

::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget -O moodle.tgz https://download.moodle.org/download.php/direct/stable38/moodle-latest-38.tgz
 [isabell@stardust html]$ tar --strip-components=1 --gzip --extract --file=moodle.tgz
 [isabell@stardust html]$ rm moodle.tgz
 [isabell@stardust html]$

The ``--strip-components=1`` option will unpack the contents of the moodle folder inside the archive into the current folder. You could also unpack the archive with its subdirectory if you plan to use it with your own domain:

::

 [isabell@stardust html]$ tar --gzip --extract --file=moodle.tgz
 [isabell@stardust html]$


Moodle requires `max_input_vars` to be set to 5000 or higher. To configure this, create the file ``~/etc/php.d/max_input_vars.ini`` with the following content:

.. code-block:: ini

 max_input_vars=5000
 
 
.. note:: After setting this PHP parameter, restart PHP to activate the changes

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$
 

Initialize
----------
Now you should be able to access the initialization process of the Moodle instance.

Visit your Uberspace domain in the browser of our choice - in this case, ``isabell.uber.space``.

1. Choose any language and click ``Next``
2. For the ``Data directory``, choose the moodledata folder you created. ``/home/isabell/moodledata``
3. For the Database driver, choose ``MariaDB (native/mariadb)``
4. For the Database Settings, enter your information:

  1. ``Database name``: ``isabell_moodle``
  2. ``Database user``: ``isabell``
  3. ``Database password``: ``MySuperSecretPassword``
  4. ``Database port``: ``3306``

5. Read the Copyright notice and only accept if you truly do :)
6. The checks should now show all OK. At the end of the page, click on ``Continue``.
7. This could take a while to finish. You should be redirected to the process page. Here you can watch the process while installing missing plugins. After all installations have finished, at the end of the page, click on ``Continue``
8. After that, you will be shown the admin user creation page. Enter your information here which you later will also use to login.
9. Enter a full and short name for your Moodle instance.
10. Et voilà, your Moodle is now installed.

Cronjob
-------
You should configure a cron task for Moodle. This script is critical for several features of Moodle e.g. sending notification emails. Edit your cron tab using the ``crontab -e`` and put the following content inside crontab:

.. code-block:: text

 PATH=/home/isabell/bin:/usr/bin:/bin
 MAILTO=""
 */5 * * * * php /home/isabell/html/admin/cli/cron.php

This configures cron to execute the script every 5 minutes. If you want details on what exactly is executed, you can change the ``MAILTO`` variable to your email address.



Best practices
==============

Documentation
-------------

Moodle has extensive documentation. Check it out under Moodle-Docs_.

Moosh
-----
Moosh exposes its functions/features via a CLI that you can use to perform several lower level tasks such as performing actions on the database. You can download Moosh_ from the moodle plugins page.

::

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget https://moodle.org/plugins/download.php/20823/moosh_moodle38_2019121900.zip
 [isabell@stardust bin]$ unzip moosh_moodle38_2019121900.zip
 ...
 creating: moosh/Moosh/Command/Moodle30/Category/
 inflating: moosh/Moosh/Command/Moodle30/Category/CategoryDelete.php
 inflating: moosh/Moosh/MoodleMetaData.php
 [isabell@stardust bin]$

You can then either add the moosh folder to your $PATH or execute moosh via path. To use moosh, you have to change into your moodle installation folder, in our case ~/html. From there you can run moosh:

::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ php ~/bin/moosh/moosh.php
 ...
 [isabell@stardust html]$

You can do a lot of things with moosh. For more details, head over to Moosh_Documentation_

Tuning
======

Moodle has the feature of being extended by plugins. check out the Moodle-Plugins_ page. Note that some plugins may have additional installation instructions.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _feed: https://github.com/moodle/moodle/releases.atom
.. _Wikipedia: https://en.wikipedia.org/wiki/Moodle
.. _Moodle: https://docs.moodle.org/38/en/About_Moodle
.. _Moodle-Download: https://download.moodle.org/releases/latest/
.. _Moodle-Docs: https://docs.moodle.org/38/en/Main_page
.. _Moodle-Plugins: https://moodle.org/plugins/
.. _Moosh: https://moodle.org/plugins/view.php?id=522
.. _Moosh_Documentation: http://moosh-online.com/

----

Tested with Moodle version 4.0.5, Uberspace 7.13, PHP 8.0

.. author_list::
