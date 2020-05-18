.. highlight:: console

.. author:: YourName <YourURL/YourMail>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/loremipsum.png
      :align: center

##########
Loremipsum
##########

.. tag_list::

Loremipsum_ dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * http://www.loremipsum.com/legal/privacy

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your blog URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

Step 2
------

Configuration
=============

Configure Webserver
-------------------

Setup daemon
------------

Finishing installation
======================

Point your browser to URL and create a user account.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!

Tuning
======

Disable all plugins you don't need. Configure caching.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _Loremipsum: https://en.wikipedia.org/wiki/Lorem_ipsum
.. _feed: https://github.com/lorem/ipsum/releases.atom

----

Tested with Loremipsum 1.22.1, Uberspace 7.1.1

.. author_list::
