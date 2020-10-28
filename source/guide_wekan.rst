.. highlight:: console

.. author:: Andrej <https://github.com/schoeke>
.. tag:: lang-node
.. tag:: project-management
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/wekan.svg
      :align: center

########
Wekan
########

.. tag_list::

Wekan_ - Open Source kanban

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`node <lang-nodejs>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :lab:`MongoDB <guide_mongodb>`


License
=======

Wekan is released under the very permissive `MIT License`_. All relevant information can be found in the GitHub_ repository of the project.

Prerequisites
=============

We're using :manual:`Nodejs <lang-php>` in the stable version 12:

::

 [isabell@stardust ~]$ $ uberspace tools version use node 12
 Selected Node.js version 12
 The new configuration is adapted immediately. Minor updates will be applied automatically.
 [isabell@stardust ~]$

The domain you want to use should be already set up:

.. include:: includes/web-domain-list.rst

We'll also need :lab:`MongoDB <guide_mongodb>`, so follow the MongoDB guide and come back when it's running.

Let's create a new password for our database:

.. code-block:: bash

 [isabell@stardust ~]$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-15};echo;
 randompassword
 [isabell@stardust ~]$

Once we have that, let's create the database itself.

.. code-block:: none

 [isabell@stardust ~]$ mongo
 MongoDB shell version v4.4.1
 connecting to: mongodb://127.0.0.1:21017/admin
 Implicit session: session { "id" : UUID("6fd371f6-e1fa-461c-be0c-ea3cbe230a01") }
 MongoDB server version: 4.4.1
 > use wekan
 > db.createUser(
    {
      user: "wekan",
      pwd: "randompassword",
      roles: ["readWrite"]
    }
   )
 >

You can leave the mongo shell afterwards by pressing ``CTRL-D``.

Installation
============

Download and extract .ZIP archive
-----------------------------------

Check the Wekan website for the `latest release`_ and copy the download link to the wekan-*.*.zip file. Then use ``wget`` to download it. Replace the URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ wget https://releases.wekan.team/wekan-4.43.zip
 […]
 Saving to: ‘wekan-4.43.zip’

 100%[========================================================================================================================>] 3,172,029   3.45MB/s   in 0.9s

 2018-10-11 14:48:20 (3.45 MB/s) - 'wekan-4.43.zip' saved [3172029]
 [isabell@stardust ~]$

Unzip the archive and then delete it. Replace the version in the file name with the one you downloaded.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ unzip wekan-4.43.zip
 [isabell@stardust ~]$ rm wekan-4.43.zip
 [isabell@stardust ~]$


Install server
--------------

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd bundle/programs/server
 [isabell@stardust server]$ npm install node-gyp node-pre-gyp fibers
 [isabell@stardust server]$ cd ~
 [isabell@stardust ~]$




========

To work properly, Kanboard requires that a `background job`_ runs on a daily basis. Edit your cron tab using the ``crontab -e`` command and insert this cron job to execute the daily cronjob at 8am. Make sure to replace ``isabell`` with your own user name.

::

  0 8 * * * cd /var/www/virtual/$USER/html && ./cli cronjob >/dev/null 2>&1

Best practices
==============

Plugins
-------

Get an overview of all available Plugins_ for Kanboard and install them from the user interface. More (unofficial) plugins may also be available, just browse GitHub.


Email Notifications
-------------------
To receive `email notifications`_, users of Kanboard `must have`_:

* Activated notifications in their profile
* Have a valid email address in their profile
* Be a member of the project that will trigger notifications

Set the email address used for the "From" header by changing the value in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2

 // E-mail address used for the "From" header (notifications)
 define('MAIL_FROM', 'isabell@uber.space');

Specify the URL of your Kanboard installation in your Application Settings to display a link to the task in notifications: ``https://isabell.uber.space/``. By default, nothing is defined, so no links will be displayed in notifications.

.. note:: Don’t forget the ending slash ``/``.

Debugging
---------

Enable debug mode by setting the following two values in ``config.php``:

.. code-block:: ini
 :emphasize-lines: 2,5

 // Enable/Disable debug
 define('DEBUG', true);

 // Available log drivers: syslog, stderr, stdout, system or file
 define('LOG_DRIVER', 'file');

The file ``debug.log`` will be found in the ``data`` folder of your Kanboard directory.


Updates
=======

.. note:: Check the update Feed_ regularly to stay informed about the newest version.

Check the GitHub's Atom Feed_ for any new Kanboard releases and copy the link to the ``.tar.gz`` archive. In this example the version is v42.23.2, which does not exist of course. Change the version to the latest one in the highlighted lines.

.. code-block:: console
 :emphasize-lines: 2,3,4,5,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/kanboard/kanboard/archive/v42.23.2.tar.gz
 [isabell@stardust isabell]$ tar -xzf v42.23.2.tar.gz
 [isabell@stardust isabell]$ cp -r html/data/ html/plugins/ html/config.php kanboard-42.23.2/
 [isabell@stardust isabell]$ cp -r kanboard-42.23.2/* html/
 [isabell@stardust isabell]$ rm -rf kanboard-42.23.2 v42.23.2.tar.gz
 [isabell@stardust isabell]$

Check the `Kanboard documentation`_ if the configuration changed between ``config.default.php`` and your ``config.php`` (happens very rarely). Also check ``.htaccess`` if further adjustments needed to be made.

.. _Wekan: https://wekan.github.io/
.. _MIT License: https://github.com/kanboard/kanboard/blob/master/LICENSE
.. _Wekan documentation: https://github.com/wekan/wekan/wiki
.. _Github: https://github.com/wekan/wekan/
.. _latest release: https://releases.wekan.team/

----

Tested with Kanboard 1.2.6, Uberspace 7.1.14.0

.. author_list::
