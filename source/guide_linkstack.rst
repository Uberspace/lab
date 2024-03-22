.. highlight:: console

.. author:: Jan Klomp <https://jan.klomp.de>
.. author:: BabyFn0rd <https://github.com/BabyFnord/>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web
.. tag:: self-hosting
.. tag:: analytics

.. sidebar:: Logo

  .. image:: _static/images/linkstack.svg
      :align: center

##########
LinkStack
##########

.. tag_list::

LinkStack_ is a highly customizable link sharing and landing page platform with an easy to use interface and acts as a free opensource alternative to Linktree, Shorby, bio.fm etc.

----

.. note:: For this guide you should be familiar with the basic concepts of

    * :manual:`PHP <lang-php>`
    * :manual:`domains <web-domains>`
    * :manual:`MySQL <database-mysql>`

License
=======

*LinkStack* is licensed under the GNU General Public License v3.0. All relevant legal information can be found here:

  * https://github.com/LinkStackOrg/LinkStack/blob/main/LICENSE

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1 or above (tested working with PHP 8.3):

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

If you want to use *LinkStack* with your own domain you need to setup your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst

Setup a new MySQL database for *LinkStack*:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_linkstack"
 [isabell@stardust ~]$

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release of *LinkStack* and extract it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/linkstackorg/linkstack/releases/latest/download/linkstack.zip
 [...]
 2023-01-06 18:48:51 (23.3 MB/s) - ‘linkstack.zip’ saved [24926989/24926989]
 [isabell@stardust isabell]$ unzip linkstack.zip
 [...]
 extracting: linkstack/version.json
  inflating: linkstack/web.config
  inflating: linkstack/webpack.mix.js
  inflating: README.md
 [isabell@stardust isabell]$

Delete the empty ``/html`` directory and the downloaded zip file, then rename the ``linkstack`` directory to ``html`` :

::

 [isabell@stardust isabell]$ rm -rf html && rm linkstack.zip
 [isabell@stardust isabell]$ mv linkstack html
 [isabell@stardust isabell]$

.. note:: If you intend to access *LinkStack* using a subdomain, you need to edit ``linkstack/.htaccess`` and add ``RewriteBase /`` below ``RewriteEngine On``.

Configuration
=============

Browse to ``https://isabell.uber.space/`` and complete the setup process using MySQL as the database backend. Fill in the database credentials:

::

 Database host:     localhost
 Database port:     localhost
 Database name:     isabell_linkstack
 Database username: isabell
 Database password: MySuperSecretPassword

Create the default login ``your@domain.com`` with password ``YourPassword``, subsequently enter a ``Handle`` and ``Name``.

In case you want to edit the ``Terms``, ``Privacy`` and ``Contact`` pages, browse to the ``Footer Pages`` section in the Admin Panel.

If you're going to allow registrations, you may want to edit the SMTP settings for outgoing mails. Click on ``Config`` on the Admin Panel and edit the SMTP server settings according to your requirements.

For more configuration options please have a look to the *LinkStack* documentation_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

When a new version is released, you will also get an update notification on your Admin Panel. The easiest way to update your installation is to use the web updater by clicking on the update notification.

.. _LinkStack: https://github.com/LinkStackOrg/LinkStack/
.. _feed: https://github.com/LinkStackOrg/LinkStack/releases.atom
.. _documentation: https://docs.linkstack.org/

----

Tested with LinkStack v4.7.7, Uberspace 7.15.10

.. author_list::
