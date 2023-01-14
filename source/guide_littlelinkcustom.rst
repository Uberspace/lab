.. highlight:: console

.. author:: Jan Klomp <https://klomp.de>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web
.. tag:: self-hosting
.. tag:: analytics

.. sidebar:: Logo

  .. image:: _static/images/littlelinkcustom.svg
      :align: center

##########
LittleLink Custom
##########

.. tag_list::

LittleLinkCustom_ is a highly customizable link sharing and landing page platform with an easy to use interface and acts as a free opensource alternative to Linktree, Shorby, bio.fm etc.

----

.. note:: For this guide you should be familiar with the basic concepts of

    * :manual:`PHP <lang-php>`
    * :manual:`domains <web-domains>`
    * :manual:`MySQL <database-mysql>`

License
=======

*LittleLink Custom* is licensed under the GNU General Public License v3.0. All relevant legal information can be found here:

  * https://github.com/JulianPrieber/littlelink-custom/blob/main/LICENSE

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

If you want to use *LittleLink Custom* with your own domain you need to setup your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for *LittleLink Custom*:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_llcustom"
 [isabell@stardust ~]$

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of *LittleLink Custom* and extract it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/JulianPrieber/littlelink-custom/releases/latest/download/littlelink-custom.zip
 [...]
 2023-01-06 18:48:51 (23.3 MB/s) - ‘littlelink-custom.zip’ saved [24926989/24926989]
 [isabell@stardust isabell]$ unzip littlelink-custom.zip
 [...]
 extracting: littlelink-custom/version.json
  inflating: littlelink-custom/web.config
  inflating: littlelink-custom/webpack.mix.js
  inflating: README.md
 [isabell@stardust isabell]$

Delete the ``nocontent.html`` file, the empty ``/html`` directory and the downloaded zip file, then rename the ``littlelink-custom`` directory to ``html`` :

::

 [isabell@stardust isabell]$ rm html/nocontent.html; rmdir html/
 [isabell@stardust isabell]$ rm littlelink-custom.zip
 [isabell@stardust isabell]$ mv littlelink-custom html
 [isabell@stardust isabell]$


Configuration
=============

Open your webbrowser and go to ``https://isabell.uber.space/``, then click trough the setup process. It's recommend using MySQL as the database backend. Fill in the database credentials:

::

 Database host:     localhost
 Database port:     3306
 Database name:     isabell_llcustom
 Database username: isabell
 Database password: MySuperSecretPassword

During the setup process you have to create the default login ``admin@admin.com`` with password ``12345678``. Don't forget to fill in the ``Handle`` and ``Name`` fields also.

.. warning:: Change the default password of the default administrator account now!

On the Admin Panel, click on the ``Account Settings`` section located on the sidebar on the left-hand side of your screen. There you can enter a new and secure password.

Maybe you want to edit the ``Terms``, ``Privacy`` and ``Contact`` pages. You'll find them on the Admin Panel in the ``Footer Pages`` section.

If you're going to allow registrations, you may want to edit the SMTP settings for outgoing mails. Click on ``Config`` on the Admin Panel and edit the SMTP server settings according to your requirements.

For more configuration options please have a look to the Configuration_ section of the *LittleLink Custom* documentation.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

When a new version is released, you will also get an update notification on your Admin Panel. The easiest way to update your installation is to use the web updater by clicking on the update notification.

.. _LittleLinkCustom: https://littlelink-custom.com/
.. _feed: https://github.com/JulianPrieber/littlelink-custom/releases.atom
.. _Configuration: https://littlelink-custom.com/docs/d/configuration-getting-started/

----

Tested with LittleLink Custom v3.2.3, Uberspace 7.14.0

.. author_list::
