.. author:: Salocin <hallo@uberspace.de>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/embetty.png
      :align: center

#######
Embetty
#######

Embetty_ is a Node.js_ proxy service that allows you to embed Tweets and videos from YouTube, Facebook, and Vimeo on your website without compromising your visitor's privacy. It is developed by `Heise online`_ and is released under the MIT license.

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * Node.js_
  * supervisord_

Prerequisites
=============

embetty.js
----------

Download a copy of embetty.js and place it in your DocumentRoot_. Please refer to Embetty's `quick start guide`_ for details.

Twitter credentials (optional)
------------------------------

.. note :: If you only want to embed videos, you can skip this step.

In order to access the tweets you want to embed, you need to set-up a `Twitter application`_. For ease of use, we'll assume that you're using the account that you want to use to access Twitter through Embetty to add the application.

After adding the Twitter application, click the `manage keys and access tokens` link in the Application's settings and click `Create my access token`. Write down:

- the Access Token, e.g. ``47114223-BZC77d4304f0EE547630e56f2d84c4fedf6a41QU3``
- and the Access Token Secret, e.g. ``biQ1a114dabFBB10022291691e499c4b3a39402c8dZAH``
- the Consumer Key (API Key), e.g. ``E4a38941Jb4efbac38GE854a62``
- the Consumer Secret (API Secret), e.g. ``d775b93f776dc6577B3f2C212aE080c24f308e28803d0877a2``

.. note:: Make sure you write down you own values and not our examples.

Installation
============

Use ``npm`` to install the latest version of Embetty server:

::

  [isabell@stardust ~]$ npm install -g @heise/embetty-server
  /home/isabell/bin/embetty-start -> /home/isabell/lib/node_modules/@heise/embetty-server/bin/embetty-start
  /home/isabell/bin/embetty -> /home/isabell/lib/node_modules/@heise/embetty-server/bin/embetty
  + @heise/embetty-server@1.0.0-beta.6
  added 182 packages in 10.878s
  [isabell@stardust ~]$ 

Configuration
=============

Configure port
--------------

Since Embetty uses its own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Change the configuration
------------------------

Setup daemon
------------

Create ``~/etc/services.d/embetty.ini`` with the following content:

.. warning:: Replace all place holders such as ``<username>`` with your actual values!

.. code-block:: ini
 :emphasize-lines: 2,3

 [program:embetty]
 command=/home/<username>/bin/embetty start
 environment=PORT="<port>",TWITTER_ACCESS_TOKEN_KEY="<accesstoken>",TWITTER_ACCESS_TOKEN_SECRET="<accesstokensecret>",TWITTER_CONSUMER_KEY="<consumerkey>",TWITTER_CONSUMER_SECRET="<consumersecret>"

.. note:: If you don't need Twitter support, you can leave out the ``TWITTER_`` variables and only set ``PORT``.

In our example this would be:

.. code-block:: ini

 [program:embetty]
 command=/home/<username>/bin/embetty start
 environment=PORT="9000",TWITTER_ACCESS_TOKEN_KEY="47114223-BZC77d4304f0EE547630e56f2d84c4fedf6a41QU3",TWITTER_ACCESS_TOKEN_SECRET="biQ1a114dabFBB10022291691e499c4b3a39402c8dZAH",TWITTER_CONSUMER_KEY="E4a38941Jb4efbac38GE854a62",TWITTER_CONSUMER_SECRET="d775b93f776dc6577B3f2C212aE080c24f308e28803d0877a2"

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 embetty: available
 [isabell@stardust ~]$ supervisorctl update
 embetty: added process group
 [isabell@stardust ~]$ supervisorctl status
 embetty                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$ 

If it's not in state RUNNING, check your configuration.

Setup .htaccess
---------------

Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: none
 :emphasize-lines: 4

 DirectoryIndex disabled

 RewriteEngine On
 RewriteRule ^embetty/(.*) http://localhost:<yourport>/$1 [P]

In our example this would be:

.. code-block:: none

 DirectoryIndex disabled

 RewriteEngine On
 RewriteRule ^embetty/(.*) http://localhost:9000/$1 [P]

Usage
=====

Please refer to Embetty's `quick start guide`_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use ``npm`` to update Embetty:

::

[isabell@stardust ~]$ npm upgrade -g @heise/embetty-server
[isabell@stardust ~]$ 


.. _Embetty: https://github.com/heiseonline/embetty
.. _Heise online: https://www.heise.de
.. _Node.js: https://manual.uberspace.de/en/lang-nodejs.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _quick start guide: https://github.com/heiseonline/embetty#quick-start
.. _DocumentRoot: https://manual.uberspace.de/en/web-documentroot.html
.. _Twitter application: https://apps.twitter.com/
.. _feed: https://github.com/heiseonline/embetty-server/releases

----

Tested with Embetty 1.0.0-beta.6, Uberspace 7.1.7.0

.. authors::
