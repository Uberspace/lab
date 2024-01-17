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


Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$






.. include:: includes/my-print-defaults.rst

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download tor
-------------------

Go to the tor download page
``https://www.torproject.org/download/tor/`` and copy the download link for the latest stable version of the tor expert bundle for the OS GNU/Linux (x86_64)
::
 [isabell@stardust ~]$ curl --proto '=https' --tlsv1.2 -sSf https://archive.torproject.org/tor-package-archive/torbrowser/13.0.8/tor-expert-bundle-linux-x86_64-13.0.8.tar.gz -o tor.tar.gz

optional: download and verify the signature https://archive.torproject.org/tor-package-archive/torbrowser/13.0.8/tor-expert-bundle-linux-x86_64-13.0.8.tar.gz.asc
TODO: describe how to verify signature https://support.torproject.org/little-t-tor/verify-little-t-tor/

$ gpg --auto-key-locate nodefault,wkd --locate-keys ahf@torproject.org
$ gpg --auto-key-locate nodefault,wkd --locate-keys dgoulet@torproject.org
$ gpg --auto-key-locate nodefault,wkd --locate-keys nickm@torproject.org

gpg --output ./tor.keyring --export 0x2133BC600AB133E1D826D173FE43009C4607B1FB

gpgv --keyring ./tor.keyring ~/Downloads/tor-0.4.6.10.tar.gz.sha256sum.asc ~/Downloads/tor-0.4.6.10.tar.gz.sha256sum

sha256sum -c tor-0.4.6.10.tar.gz.sha256sum
::
 tar xvzf tor.tar.gz

Configuration
=============

Configure tor as onion service
------------------------

Create the file ``~/tor/torrc`` and add the following lines:
::
  HiddenServiceDir onionservice
  HiddenServicePort 80 127.0.0.1:80

The first line determines where the configuration and keys for the onion service will be stored.
This directory contains the cryptographic keys of the onion service and should not be publily accessible.

Set up the daemon
-----------------


Create the file ``~/etc/services.d/tor-onion-service.ini`` with the following content:
::
 [program:tor-onion-service]
 command=%(ENV_HOME)s/tor/tor --torrc-file %(ENV_HOME)s/tor/torrc
 directory=%(ENV_HOME)s
 autorestart=yes
 environment=LD_LIBRARY_PATH=%(ENV_HOME)s/tor/


Finishing installation
======================


To view your automatically generated .onion hostname
::
 [isabell@stardust ~]$ cat ~/tor/onionservice/hostname

To test if all is working download and install tor browser and enter your .onion domain in the url bar
https://www.torproject.org/download/


Best practices
==============


Security
--------

Users connecting to the onion service will look to the service that listens on the destination port like they would connect to it from localhost. If the application that is reachable via the .onion domains grants special permissions to connections from localhost, these permissions now apply to everyone who connects via the .onion service.


Read about tor to understand the security it can provide, the limitations and how to use it correctly:
``https://support.torproject.org/faq/``
``https://tb-manual.torproject.org/``

The folder ``~/tor/onionservice`` contains the cryptographic keys of the onion service, which are critical for the security. Make sure to set restrictive permissions.

Tuning
======

Disable all plugins you don't need. Configure caching.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _Loremipsum: https://en.wikipedia.org/wiki/Lorem_ipsum
.. _feed: https://github.com/lorem/ipsum/releases.atom

Debugging
=========

If something fails with this specific error, you should have a look at this specific config, or just reload that service. Try to look into the log at this path.

Backup
======

The folder ``~/tor/onionservice`` should be backed up. It contains the long-term identity keys for the onion service, which are randomly generated when starting tor for the first time. When the keys are lost, the .onion domain is lost.

----

Tested with Loremipsum 1.22.1, Uberspace 7.1.1

.. author_list::
