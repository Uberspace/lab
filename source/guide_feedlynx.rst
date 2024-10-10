.. author:: Jan Klomp <https://jan.klomp.de>

.. tag:: rss
.. tag:: web
.. tag:: reading-list
.. tag:: read-later
.. tag:: lang-rust

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/feedlynx.svg
      :align: center

########
Feedlynx
########

.. tag_list::


Feedlynx_ collects weblinks and generates a RSS feed with these links for your prefered RSS reader to read them later. Every time you transfer a link to *Feedlynx*, it fetches the URL to determine a title and description. With this information, *Feedlynx* generates a new entry to the feed.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

If you want to use *Feedlynx* with your own domain you need to setup your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

Installation
============

Create a directory for the application:

::

  [isabell@stardust ~]$ mkdir ~/feedlynx
  [isabell@stardust ~]$

Find the latest version from the release_ page, then download and extract it into the *Feedlynx* directory.

::

  [isabell@stardust ~]$ VERSION=0.3.0
  [isabell@stardust ~]$ wget -qO- https://releases.wezm.net/feedlynx/$VERSION/feedlynx-$VERSION-x86_64-unknown-linux-musl.tar.gz | tar xvz -C ~/feedlynx
  [isabell@stardust ~]$

Make the downloaded binary executable:

::

  [isabell@stardust ~]$ chmod u+x ~/feedlynx/feedlynx
  [isabell@stardust ~]$


Configuration
=============

Setup daemon
------------

Feedlynx requires two environment variables to be set:


``FEEDLYNX_PRIVATE_TOKEN`` used to authenticate requests to add a new link.
``FEEDLYNX_FEED_TOKEN`` used in the path to the generated feed.

Both of these tokens must be at least 32 characters long and hard to guess. Suitable values can be generated with ``feedlynx gen-token``, which will print a randomly generated token:

::

  [isabell@stardust ~]$ ~/feedlynx/feedlynx gen-token
  [isabell@stardust ~]$ VERY_LONG_FEED_TOKEN
  [isabell@stardust ~]$ ~/feedlynx/feedlynx gen-token
  [isabell@stardust ~]$ VERY_LONG_PRIVATE_TOKEN
  [isabell@stardust ~]$

Create ``~/etc/services.d/feedlynx.ini`` with the following content:

.. code-block:: ini

  [program:feedlynx]
  environment=FEEDLYNX_FEED_TOKEN="VERY_LONG_FEED_TOKEN",FEEDLYNX_PRIVATE_TOKEN="VERY_LONG_PRIVATE_TOKEN",FEEDLYNX_ADDRESS="0.0.0.0"
  directory=%(ENV_HOME)s/feedlynx/
  command=%(ENV_HOME)s/feedlynx/feedlynx feed.xml
  autostart=yes
  autorestart=yes
  startsecs=60

.. include:: includes/supervisord.rst

Write down the feed token and the private token, because you'll need them later for accessing the feed and adding links.


Web backend
-----------

.. note::

    The default port from *Feedlynx* is 8001, so we have to configure the web backend to this port.

.. include:: includes/web-backend.rst


Testing the installation
========================

Point your browser to your domain, for example https://isabell.uber.space, where the available RSS feed is shown. You can access the feed with your prefered RSS reader by adding your VERY_LONG_FEED_TOKEN to the feed url.

Adding links to the feed is possible via the API_, the browser extension_ or Apple Shortcuts_. You'll need the VERY_LONG_PRIVATE_TOKEN for that.


Updates
=======

.. note:: Check the *Feedlynx* release_ page regularly to stay informed about the newest version.


If there is a new version available, you only have to stop the service, exchange the binary file, make the file executable and start the service again.

.. code-block:: console

   [isabell@stardust ~]$ supervisorctl stop feedlynx
   feedlynx: stopped
   [isabell@stardust ~]$ rm ~/feedlynx/feedlynx
   [isabell@stardust ~]$ $VERSION=NEW_VERSION
   [isabell@stardust ~]$ wget -qO- https://releases.wezm.net/feedlynx/$VERSION/feedlynx-$VERSION-x86_64-unknown-linux-musl.tar.gz | tar xvz -C ~/feedlynx
   feedlynx
   [isabell@stardust ~]$ chmod u+x ~/feedlynx/feedlynx
   [isabell@stardust ~]$ supervisorctl start feedlynx
   feedlynx: started
   [isabell@stardust ~]$


.. _Feedlynx: https://github.com/wezm/feedlynx/
.. _release: https://github.com/wezm/feedlynx/releases
.. _API: https://github.com/wezm/feedlynx?tab=readme-ov-file#api
.. _extension: https://github.com/wezm/feedlynx-ext
.. _Shortcuts: https://github.com/wezm/feedlynx?tab=readme-ov-file#apple-shortcuts-ios-ipados-macos

----

Tested with Feedlynx v0.3.0 and Uberspace 7.16.1

.. author_list::
