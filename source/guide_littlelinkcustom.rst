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

License
=======

*LittleLink Custom* is licensed under the GNU General Public License v3.0. All relevant legal information can be found here:

  * https://github.com/JulianPrieber/littlelink-custom/blob/main/LICENSE

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

If you want to use *LittleLink Custom* with your own domain you need to setup your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of *LittleLink Custom* and extract it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/JulianPrieber/littlelink-custom/releases/latest/download/littlelink-custom.zip
 ...
 [isabell@stardust html]$ unzip littlelink-custom.zip
 ...
 [isabell@stardust ~]$

Move the extracted files and directories to the document root, then delete the empty source directory, the downloaded zip file and the ``nocontent.html`` file:

::

 [isabell@stardust ~]$ mv littlelink-custom/* littlelink-custom/.[!.]* .
 [isabell@stardust ~]$
 [isabell@stardust ~]$ rm littlelink-custom.zip
 [isabell@stardust ~]$
 [isabell@stardust ~]$ rm -r littlelink-custom
 [isabell@stardust ~]$
 [isabell@stardust ~]$ rm nocontent.html
 [isabell@stardust ~]$

Configuration
=============

Open your webbrowser and go to ``https://isabell.uber.space/``, then log in to your installation with the default login ``admin@admin.com`` and password ``12345678``.

.. warning:: Change the default password of the default administrator account now!

On the Admin Panel, click on the ``Profile`` section located on the sidebar on the left-hand side of your screen. There you can enter a new and secure password.

Maybe you want to edit the ``Terms``, ``Privacy`` and ``Contact`` pages. You'll find them on the Admin Panel in the ``Pages`` section. On the bottom of the page you can also allow or reject registrations for other users.

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

Tested with LittleLink Custom v2.8.2, Uberspace 7.13.0

.. author_list::
