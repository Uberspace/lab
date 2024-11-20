.. highlight:: console

.. author:: Nico Brünjes <https://nicobruenjes.dev>

.. tag:: blog
.. tag:: cms
.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/classicpress-logo-gradient.svg
      :align: center

############
ClassicPress
############

.. tag_list::

ClassicPress_ is a fork of WordPress, which aims to be a more stable and secure alternative to the popular CMS. It is fully compatible with many WordPress plugins and themes, but uses the TinyMCE classic editor as the default option and lacks the support of blocks and the block editor (a.k.a. Gutenberg).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`


Prerequisites
-------------

ClassicPress recommends :manual:`PHP <lang-php>` version 8.1 or 8.2. to be used:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

You will also need a database, where ClassicPress can store data. You
may use your default database (i.e. named isabell) or add a new
one to your account like this (the database requires your username as a prefix):

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE  ${USER}_classic_press"
 [isabell@stardust ~]$

Note your credentials and the database name for later use.

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download the source
-------------------

Change into the ``/tmp`` directory of your root folder, download the
latest ClassicPress version and unzip it.

.. code-block:: console

 [isabell@stardust html]$ cd ~/tmp
 [isabell@stardust tmp]$ wget https://www.classicpress.net/latest.zip
 [isabell@stardust tmp]$ unzip latest.zip
 [isabell@stardust tmp]$

There should be a directory ``ClassicPress-release-<release_number>``, i.e. ``ClassicPress-release-2.2.0`` in your ``tmp`` now. Let's copy its content to your web folder.

.. code-block:: console

 [isabell@stardust tmp]$ cp -r ClassicPress-release-2.2.0/* /var/www/virtual/isabell/html/
 [isabell@stardust tmp]$

Clean up your ``/tmp`` folder:

.. code-block:: console

 [isabell@stardust tmp]$ rm latest.zip
 [isabell@stardust tmp]$ rm -rf ClassicPress-release-2.2.0
 [isabell@stardust ~]$

The installation on the server side is now complete. The rest of the installation process
will happen in the browser.

Finishing installation
======================

Point your browser at your domains address, probably ``https://isabell.uber.space`` and follow the installation instructions.

1. Choose your language
2. It follows an information about what you will need to install
   ClassicPress.
3. Fill out the form like this:

   1. The name of the database we set up earlier
   2. The user name for that database (it's usually the same as your
      username here)
   3. The database password we acquired above
   4. The database host is ``localhost``
   5. The table prefix would be ``cp_`` (the default)

4. In the next step, you can start the database initialisation process
   with a click.
5. Next step: Set your blog and admin user:

   1. Enter the title you have chosen for your blog (you have chosen one,
      haven't you?)
   2. Choose a username for your user
   3. Choose a secure password (and store it in your password manager!)
   4. Enter an email that will be associated with your user
   5. Choose if your blog should be indexed by search engines (can be
      changed back later)

6. That's it, after sending the form, you may login into your freshly
   installed ClassicPress weblog.

Done.

Updates
=======

ClassicPress updates itself automatically, but you can also check for updates manually in the admin area. Plugins and Themes also have the option to update themselves but it needs to be activated for each.

Documentation
=============

Find more help on the `ClassicPress
Documentation <https://docs.classicpress.net/>`__ page.


.. _ClassicPress: https://www.classicpress.net/


----

Tested with ClassicPress 2.2.0, Uberspace  7.16.2

.. author_list::
