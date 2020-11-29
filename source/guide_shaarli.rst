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

Clone the GitHub repository, install the 3rd-party PHP dependencies and copy the resulting shaarli directory to your document root:

.. code-block:: console

  [isabell@stardust ~]$ git clone -b latest https://github.com/shaarli/Shaarli.git ~/shaarli
  [isabell@stardust ~]$ cd ~/shaarli
  [isabell@stardust ~]$ composer install --no-dev --prefer-dist
  [isabell@stardust ~]$ make build_frontend
  [isabell@stardust ~]$ make translate
  [isabell@stardust ~]$ make htmldoc
  [isabell@stardust ~]$ rsync -avP ~/shaarli/ /var/www/virtual/isabell/html/
  [isabell@stardust ~]$ 

Finishing installation
======================

Once all files have been placed at the correct location, go to ``https://isabell.uber.space``.
Enter a username and a secure password, choose your preferred language and timezone, then click on "Install".

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Shaarli's `releases <https://github.com/shaarli/Shaarli/releases>`_ for the latest version. If a newer
version is available, you can upgrade by following these steps:

.. code-block:: console

  [isabell@stardust ~]$ cd /var/www/virtual/isabell/html/
  [isabell@stardust ~]$ git pull
  [isabell@stardust ~]$ composer install --no-dev
  [isabell@stardust ~]$ make translate
  [isabell@stardust ~]$ make build_frontend
  [isabell@stardust ~]$ 

.. _Shaarli: https://github.com/shaarli/Shaarli#readme
.. _Documentation: https://shaarli.readthedocs.io/en/master/
.. _feed: https://github.com/shaarli/Shaarli/releases
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Shaarli 0.12.1, Uberspace 7.7.10.0

.. author_list::
