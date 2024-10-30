.. highlight:: console

.. spelling:word-list::
    Et
    voilà

.. author:: Direnc <direnc99@gmail.com>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web
.. tag:: self-hosting


.. sidebar:: Logo

  .. image:: _static/images/moodle.svg
      :align: center

######
Moodle
######

.. tag_list::

Moodle_ Moodle is an acronym for "Modular Object-Oriented Dynamic Learning Environment". It is a free and open-source learning management system (LMS) written in PHP and distributed under the GNU General Public License. More information on Wikipedia_ or the official Moodle_ page.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`cron <daemons-cron>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here:

  * https://docs.moodle.org/dev/License

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.3:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.3'
 [isabell@stardust ~]$

MySQL
-----

.. include:: includes/my-print-defaults.rst

We will create a separate database for Moodle:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_moodle"
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Data directory
--------------

Moodle saves files and data into a directory for persistency. Create the data directory:

::

 [isabell@stardust ~]$ mkdir ~/moodledata
 [isabell@stardust ~]$

Installation
============

Download
--------

First, download Moodle and extract it. For this, change into the ``~/html`` directory of your Uberspace.

Then download the latest version (Moodle-Download_ page) of the tgz archive and extract it. It is recommended to select the stable version.

Note that the download link on the page is actually a redirect. So instead of the link behind the button, use the direct link, e.g.: ``https://download.moodle.org/download.php/direct/stable404/moodle-latest-404.tgz``.

::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget -O moodle.tgz https://download.moodle.org/download.php/direct/stable404/moodle-latest-404.tgz
 [isabell@stardust html]$ tar --strip-components=1 --gzip --extract --file=moodle.tgz
 [isabell@stardust html]$ rm moodle.tgz
 [isabell@stardust html]$


Moodle requires `max_input_vars` to be set to 5000 or higher. To configure this, create the file ``~/etc/php.d/max_input_vars.ini`` with the following content:

.. code-block:: ini

 max_input_vars=5000


.. note:: After setting this PHP parameter, restart PHP to activate the changes.

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools restart php
 Your php configuration has been loaded.
 [isabell@stardust ~]$

Setup
-----

Now you should be able to access the setup process of the Moodle instance.

Visit your Uberspace domain in the browser of our choice – in this case ``isabell.uber.space``.

1. Choose any language and click "Next".
2. For the Data directory, choose the directory you created: ``/home/isabell/moodledata``.
3. For the Database driver, choose "MariaDB (native/mariadb)".
4. For the Database Settings, enter your information:

  1. Database name: ``isabell_moodle``
  2. Database user: ``isabell``
  3. Database password: ``MySuperSecretPassword``
  4. Database port: ``3306``

5. Read the copyright notice and only accept if you truly do. 🙂
6. All checks should be OK. At the end of the page, click "Continue".
7. This could take a while to finish. You should be redirected to the process page. Here you can watch the process while installing missing plugins. After all installations have finished, at the end of the page, click "Continue".
8. After that, you will be shown the admin user creation page. Enter your information here which you later will also use to login.
9. Enter a full and short name for your Moodle instance.
10. Et voilà, your Moodle instance is now installed.

Cronjob
-------

You should configure a cron job for Moodle. This script is critical for several features of Moodle, e.g. sending notification emails. Edit your crontab using the ``crontab -e`` and put the following content inside the crontab:

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

Moosh exposes its functions/features via a CLI that you can use to perform several lower level tasks such as performing actions on the database. You can download Moosh_ from the Moodle plugins page.

::

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget https://moodle.org/plugins/download.php/31885/moosh_moodle44_2024050100.zip
 [isabell@stardust bin]$ unzip moosh_moodle44_2024050100.zip
 [isabell@stardust bin]$

You can then either add the Moosh folder to your $PATH or execute Moosh via path. To use Moosh, you have to change into your Moodle installation folder, in our case ~/html. From there you can run moosh:

::

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ php ~/bin/moosh/moosh.php
 ...
 [isabell@stardust html]$

You can do a lot of things with Moosh. For more details, head over to Moosh_Documentation_.

Plugins
=======

Moodle has the feature of being extended by plugins. Check out the Moodle-Plugins_ page. Note that some plugins may require additional installation instructions.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _feed: https://github.com/moodle/moodle/releases.atom
.. _Wikipedia: https://en.wikipedia.org/wiki/Moodle
.. _Moodle: https://docs.moodle.org/en/About_Moodle
.. _Moodle-Download: https://download.moodle.org/releases/latest/
.. _Moodle-Docs: https://docs.moodle.org/en/Main_page
.. _Moodle-Plugins: https://moodle.org/plugins/
.. _Moosh: https://moodle.org/plugins/view.php?id=522
.. _Moosh_Documentation: http://moosh-online.com/

----

Tested with Moodle version 4.4.1, Uberspace 7.15.15, PHP 8.3

.. author_list::
