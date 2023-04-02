.. author:: benks <uberspace@benks.io>

.. tag:: lang-php
.. tag:: web
.. tag:: mediaplayer
.. tag:: streaming
.. tag:: groupware

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ampache.png
      :align: center

#######
Ampache
#######

.. tag_list::


`Ampache`_ is a glossy multiuser Web-based Audio file manager / web Media Server published under AGPLv3.
If you want to try out Ampache without installing it first, visit the `demo-page`_:
A general Installation guide can be found on `Github`_.


----

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Clone ampache code from github and install necessary dependencies with composer.

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/
  [isabell@stardust isabell]$ git clone https://github.com/ampache/ampache.git
  [isabell@stardust isabell]$ cd ampache/
  [isabell@stardust ampache]$ composer install --prefer-source --no-interaction

Remove your empty DocumentRoot and link Ampache's public folder instead:

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/
  [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
  [isabell@stardust isabell]$ ln -s ampache/public html
  [isabell@stardust isabell]$


Configuration
=============

Now point your browser to your uberspace URL and follow the instructions.
You will need to enter the following information:

* Various

  * Web Path: /

* Database Connection

  * Database Name:	<username>_ampache
  * MySQL Hostname: localhost
  * MySQL Port (optional): leave this blank
  * MySQL Username: <username>
  * MySQL Password: <SQL-Password from above>

* Installation Type: default

After clicking the "create config" button you can create an admin account and start a possible update.

Now you can login as admin to create users with different roles, add catalogues, import audio files stored in your uberspace, include external webradios, install addons and brand your instance.


Updates
=======

.. note:: Check the changelog_ regularly to stay informed about the newest changes.

If you want to upgrade from an older version of Ampache it is recommended moving the old directory out of the way, extracting the new copy in its place and then copying the old /config/ampache.cfg.php, /rest/.htaccess, /channel/.htaccess, and /play/.htaccess files if any. All database updates will be handled by Ampache.


.. _`demo-page`: http://ampache.org/demo.html
.. _`Ampache`: http://ampache.org
.. _Github: https://github.com/ampache/ampache/wiki/Installation
.. _changelog: https://github.com/ampache/ampache/wiki/changelog

----

Tested with Ampache v5.5.5 and Uberspace v7.13, and PHP 8.1

.. author_list::
