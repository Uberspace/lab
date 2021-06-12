.. highlight:: console

.. author:: Kevin Jost <https://github.com/systemsemaphore>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/shaarli.png
      :align: center

#######
Shaarli
#######

.. tag_list::

.. abstract::
  Shaarli_ is a minimalist link sharing service. It can be used to share, comment and save interesting links. It is designed to be personal (single-user), fast and handy.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`

License
=======

Shaarli_ is `Free Software <https://en.wikipedia.org/wiki/Free_software>`_. See `COPYING <https://github.com/shaarli/Shaarli/blob/master/COPYING>`_ for a detail of the contributors and licenses for each individual component.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

  [isabell@stardust ~]$ uberspace tools version show php
  Using 'PHP' version: '7.4'
  [isabell@stardust ~]$

Set up your domain:

.. include:: includes/web-domain-list.rst

Installation
============

Enter your document root, download the `latest <https://github.com/shaarli/Shaarli/releases>`_ release and unpack the downloaded archive:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ wget https://github.com/shaarli/Shaarli/releases/download/v0.12.1/shaarli-v0.12.1-full.tar.gz
  [isabell@stardust html]$ tar xvzf shaarli-v0.12.1-full.tar.gz --strip-components=1
  [isabell@stardust html]$

Finishing installation
======================

Once all files have been placed at the correct location, go to ``https://isabell.uber.space``.
Enter a username and a secure password, choose your preferred language and timezone, then click on "Install".

Updates
=======

.. note:: ALL data from Shaarli will be lost when updating, please make sure to backup before upgrading.

Shaarli stores user data and configuration under the data directory. Remember to backup this folder before upgrading Shaarli:

::

  [isabell@stardust ~]$ cp -r /var/www/virtual/isabell/html/data ~/shaarli-data-backup
  [isabell@stardust ~]$

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Shaarli's `releases <https://github.com/shaarli/Shaarli/releases>`_ for the latest version. If a newer
version is available, enter your document root, download the archive, unpack it and make sure to restore your backup:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ wget https://github.com/shaarli/Shaarli/releases/download/v0.X.Y/shaarli-v0.X.Y-full.tar.gz
  [isabell@stardust html]$ tar xvzf shaarli-v0.X.Y-full.tar.gz --strip-components=1
  [isabell@stardust html]$ cp -r ~/shaarli-data-backup/* /var/www/virtual/isabell/html/data/
  [isabell@stardust html]$

.. _Shaarli: https://github.com/shaarli/Shaarli#readme
.. _Documentation: https://shaarli.readthedocs.io/en/master/
.. _feed: https://github.com/shaarli/Shaarli/releases
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Shaarli 0.12.1, Uberspace 7.7.10.0

.. author_list::
