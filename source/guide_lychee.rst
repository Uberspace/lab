.. author:: TheForcer <https://github.com/TheForcer>

.. tag:: lang-php
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/lychee.png
      :align: center

#########
Lychee
#########

.. tag_list::

Lychee_ is a open source photo-management software written in PHP and distributed under the MIT license. It allows you to easily upload, sort and manage your photos, all while presenting those with a beautiful web interface.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Also, the domain you want to use for Lychee must be set up as well:

.. include:: includes/web-domain-list.rst

Installation
============

Clone the Lychee code from GitHub_:

::

 [isabell@stardust ~]$ git clone https://github.com/LycheeOrg/Lychee ~/html
 Cloning into '/home/isabell/html'...
 remote: Counting objects: 10458, done.
 remote: Compressing objects: 100% (8/8), done.
 remote: Total 10458 (delta 3), reused 7 (delta 2), pack-reused 10448
 Receiving objects: 100% (10458/10458), 5.74 MiB | 8.85 MiB/s, done.
 Resolving deltas: 100% (7144/7144), done.
 [isabell@stardust html]$

Now point your browser to your Lychee URL and follow the instructions.

You will need to enter the following information:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Lychee database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_lychee. Enter that, you can leave the prefix field empty.

For the last step you have to enter the username/password you want to use for the Lychee user.

Updates
=======

You can regularly check their GitHub's Atom Feed_ for any new Lychee releases.

If a new version is available, ``cd`` to your Lychee folder and do a simple ``git pull origin master``:

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust html]$ git pull origin master
 Already up to date.
 [isabell@stardust html]$


.. _Lychee: https://lychee.electerious.com/
.. _GitHub: https://github.com/LycheeOrg/Lychee/releases
.. _Feed: https://github.com/LycheeOrg/Lychee/releases.atom

----

Tested with Lychee 3.1.6, Uberspace 7.1.1

.. author_list::
