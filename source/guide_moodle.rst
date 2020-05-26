.. highlight:: console

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

We're using :manual:`php <lang-php>` in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

MySQL
-----

.. include:: includes/my-print-defaults.rst

We will create a seperate database for moodle:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_moodle"
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

You can also setup your own :manual_anchor:`domain <web-domains.html>`. Note that you will have to create a seperate folder for your domain as described in :manual_anchor:`DocumentRoot <web-documentroot.html>`.

Moodledata
----------
Moodle saves files and data into a folder inter alia for persistency. We have to create this folder and give its path to Moodle later on.

::

 [isabell@stardust ~]$ mkdir ~/moodledata
 [isabell@stardust ~]$

Installation
============

Step 1
------
First, we're going to download Moodle and extract it. For this, we should first change into the html directory of your account.

Then we're going to download the latest version (Moodle-Download_ page) of the tgz archive and extract it. I would advise you to select the stable version. Note that the downloadlink on the page is actually a redirect. So instead of the link behind the button, use the direct link e.g.: ``https://download.moodle.org/download.php/direct/...``.

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

Step 2
------
Now we should be able to access the initialization process of the Moodle instance. Here, we used the uberspace domain, so our address is the one mentionend here:

.. include:: includes/web-domain-list.rst

We visit the page in the browser of our choice.

1. Choose any language and click ``Next``
2. For the ``Data directory``, we choose the moodledata folder we created. ``/home/isabell/moodledata``
3. For the Database driver, we choose ``MariaDB (native/mariadb)``
4. For the Database Settings, we enter our information:

  1. ``Database name``: ``isabell_moodle``
  2. ``Database user``: ``isabell``
  3. ``Database password``: ``MySuperSecretPassword``
  4. ``Database port``: ``3306``

5. Read the Copyright notice and only accept if you truly do :)
6. The checks should now show all OK. At the end of the page, we click on ``Continue``.
7. This could take a while to finish. We should shortly after be redirected to the process page. We can watch the process while installing missing plugins. After all installations have finished, at the end of the page we click on ``Continue``
8. After that, we should be shown the admin user creation page. We enter our information here which we later will also use to login.
9. Enter a full and short name for your Moodle instance.
10. Et voila, our Moodle is now installed.

Step 3
------
We definitely should configure a cron task for Moodle. This script is critical for several features of Moodle e.g. sending notification emails. Enter

::

 [isabell@stardust ~]$ crontab -e
 no crontab for isabell - using an empty one
 [isabell@stardust ~]$

And put the following content inside crontab:

.. code-block:: text

 PATH=/home/isabell/bin:/usr/bin:/bin
 MAILTO=""
 */5 * * * * php /home/isabell/html/admin/cli/cron.php

This configures cron to execute the script every 5 minutes. If you want details on what exactly is executed, you can change the ``MAILTO`` variable to your email address.

Check if your crontab has been saved:

::

 [isabell@stardust ~]$ crontab -l
 PATH=/home/isabell/bin:/usr/bin:/bin
 MAILTO=""
 */5 * * * * php /home/isabell/html/admin/cli/cron.php
 [isabell@stardust ~]$

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

Tested with Moodle version 3.8.2, Uberspace 7.5.1

.. author_list::
