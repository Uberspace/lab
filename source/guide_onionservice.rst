.. highlight:: console

.. author:: @expiringplatform <vrhx4va7h145o5z9ptdq38vv@systemli.org>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: web

.. sidebar:: About



##########
Tor onion service
##########

.. tag_list::

This guide describes how to make your services available via a tor onion service that runs in the users uberspace. Note that uberspace also offers a onion service, depending on what you want to achieve you might not need to follow this guide to get what you want. Therefore read the about the :manual:`Tor Service <web-tor>` first.

.. manual: :manual_anchor:`tor-onion-service`

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`


Prerequisites
=============

Some service you want to connect to via the onion service should be setup and running. In this guide we will use port 80, on which the a webserver should be running by default.

Installation
============

Download tor
-------------------

Go to the tor download_ page and copy the download link for the latest stable version of the tor expert bundle for the OS GNU/Linux (x86_64)
::
 [isabell@stardust ~]$ curl --proto '=https' --tlsv1.2 -sSf https://archive.torproject.org/tor-package-archive/torbrowser/13.0.8/tor-expert-bundle-linux-x86_64-13.0.8.tar.gz -o tor.tar.gz
 [isabell@stardust ~]$ tar xvzf tor.tar.gz
 [isabell@stardust ~]$.

.. _download: https://www.torproject.org/download/tor/

Verify the signature (optional)
-------------------------------

To verify the integrity and authenticity of the download check the signatures as described in the docs_.

.. _docs: https://support.torproject.org/little-t-tor/verify-little-t-tor/




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
 startsecs=60
 environment=LD_LIBRARY_PATH=%(ENV_HOME)s/tor/


Finishing installation
======================

Start the service using:
::
 [isabell@stardust ~]$ supervisorctl reread
 [isabell@stardust ~]$ supervisorctl start tor-onion-service
 [isabell@stardust ~]$.

To view your automatically generated .onion hostname
::
 [isabell@stardust ~]$ cat ~/onionservice/hostname
 jv2h7lm5tir5dsr6ihqmut6elusip3ylef46lhaq6q3gsv5pi7ddrwqd.onion
 [isabell@stardust ~]$.

To test if everything is working, download and install torbrowser_ and visit your .onion domain.

.. _torbrowser: https://www.torproject.org/download/

Note that it may take a few minutes after starting the service until the onion service is reachable.


Best practices
==============


Security
--------

Users connecting to the onion service will look to the service that listens on the destination port like they would connect to it from localhost. If the application that is reachable via the .onion domains grants special permissions to connections from localhost, these permissions now apply to everyone who connects via the .onion service.


Read the tor FAQ_ and the tor browser manual_ to understand the security it can provide, the limitations and how to use it correctly:

.. _FAQ: https://support.torproject.org/faq/
.. _manual: https://tb-manual.torproject.org/

The folder ``~/onionservice`` contains the cryptographic keys of the onion service, which are critical for the security. Make sure to set restrictive permissions.

Updates
=======

.. note:: In this setup there are no automatic updates. To get informed about new tor releases you can subscribe to the Tor mailinglist_

.. _mailinglist: https://lists.torproject.org/cgi-bin/mailman/listinfo/tor-announce

Debugging
=========

If something fails with this specific error, you should have a look at this specific config, or just reload that service. Try to look into the log at this path.

If the service fails to start you can start the tor binary directly to see the thr error messages:
::
 [isabell@stardust ~]$ LD_LIBRARY_PATH=~/tor ~/tor/tor --torrc-file tor/torrc
 [isabell@stardust ~]$.


Backup
======

The folder ``~/onionservice`` should be backed up. It contains the long-term identity keys for the onion service, which are randomly generated when starting tor for the first time. When the keys are lost, the .onion domain is lost.

----

.. author_list::
