.. highlight:: console

.. author:: Lomion0815

.. tag:: web
.. tag:: lang-go
.. tag:: analytics

.. sidebar:: Logo

  .. image:: _static/images/goatcounter.svg
      :align: center

####
Goatcounter
####

.. tag_list::

Goatcounter_ is an open source web analytics platform available as a free, donation-supported hosted service or self-hosted app. 

It aims to offer easy to use and meaningful privacy-friendly web analytics as an alternative to Google Analytics or Matomo.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`

License
=======

All relevant legal information can be found here

  * https://github.com/arp242/goatcounter/blob/release-2.4/LICENSE

Prerequisites
=============

The host domain and a subdomain for goatcounter need to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 goatcounter.isabell.uber.space
 [isabell@stardust ~]$ uberspace web backend set goatcounter.isabell.uber.space/ --http --port 1235
 [isabell@stardust ~]$

Installation
============

Check the goatcounter releases page for the most recent Linux AMD64 download:

https://github.com/arp242/goatcounter/releases

Create a folder and download goatcounter:

::

 [isabell@stardust ~]$ mkdir ~/goatcounter
 [isabell@stardust ~]$ cd ~/goatcounter
 [isabell@stardust ~]$ wget https://github.com/arp242/goatcounter/releases/download/v2.4.1/goatcounter-v2.4.1-linux-amd64.gz
 [isabell@stardust ~]$ gzip -d goatcounter-v2.4.1-linux-amd64.gz
 [isabell@stardust ~]$ mv goatcounter-v2.4.1-linux-amd64 goatcounter
 [isabell@stardust ~]$ chmod +x goatcounter
 [isabell@stardust ~]$

Configuration
=============

Create database
---------------

::

 [isabell@stardust ~]$ ./goatcounter db create site -createdb -vhost goatcounter.isabell.uber.space -user.email <user>@uber.space

Make sure to use your own domain and email address. You will be asked to enter a password for the specified user which will be used to access the webpage later.

Test
----

Run ``./goatcounter  serve -listen :1235 -tls http`` to test your installation by accessing https://goatcounter.isabell.uber.space

Setup daemon
------------
Create ``~/etc/services.d/goatcounter.ini`` with the following content:

.. code-block:: ini

 [program:goatcounter]
 command = %(ENV_HOME)s/goatcounter/goatcounter serve -listen :1235 -tls http -db sqlite+%(ENV_HOME)s/goatcounter/db/goatcounter.sqlite3
 autostart = true
 autorestart = true

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

Finishing installation
======================

Now you can include Goatcounter (for details have a look into the Help menu of your installation).

Updates
=======

.. note:: Check for updates_ regularly to stay informed about the newest version.

When an update is available download a new release from the release page and follow the update instraction on the goatcounter-github_.

::

 [isabell@stardust ~]$ pip3 install --user --upgrade isso


.. _goatcounter: https://www.goatcounter.com/
.. _goatcounter-github: https://github.com/arp242/goatcounter

----

Tested with Goatcounter 2.4.1 and Uberspace 7.15.4

.. author_list::
