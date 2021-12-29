.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-nodejs
.. tag:: privacy

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/embetty.png
      :align: center

#######
Embetty
#######

.. tag_list::

Embetty_ is a :manual:`Node.js <lang-nodejs>` proxy service that allows you to embed Tweets and videos from YouTube, Facebook, and Vimeo on your website without compromising your visitor's privacy. It is developed by `Heise online`_ and is released under the MIT license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

embetty.js
----------


Change to your :manual:`DocumentRoot <web-documentroot>` and download the current version of embetty.js from their github feed_ (use the current link, not the one from the snippet below!):

::

  [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
  [isabell@stardust html]$ wget https://github.com/heiseonline/embetty/releases/download/v0.0.1/embetty.js
  [...]
  [isabell@stardust ~]$

Please refer to Embetty's `quick start guide`_ for details.


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
  [...]
  added 182 packages
  [isabell@stardust ~]$
  


Configuration
=============

Change the configuration
------------------------

Setup daemon
------------

Create ``~/etc/services.d/embetty.ini`` with the following content:

.. warning:: Replace all place holders such as ``<username>`` with your actual values!

.. code-block:: ini
 :emphasize-lines: 3

 [program:embetty]
 command=embetty start
 startsecs=60
 environment=TWITTER_ACCESS_TOKEN_KEY="<accesstoken>",TWITTER_ACCESS_TOKEN_SECRET="<accesstokensecret>",TWITTER_CONSUMER_KEY="<consumerkey>",TWITTER_CONSUMER_SECRET="<consumersecret>"

.. note:: If you don't need Twitter support, you can leave out the ``TWITTER_`` variables.

In our example this would be:

.. code-block:: ini

 [program:embetty]
 command=embetty start
 startsecs=60
 environment=TWITTER_ACCESS_TOKEN_KEY="47114223-BZC77d4304f0EE547630e56f2d84c4fedf6a41QU3",TWITTER_ACCESS_TOKEN_SECRET="biQ1a114dabFBB10022291691e499c4b3a39402c8dZAH",TWITTER_CONSUMER_KEY="E4a38941Jb4efbac38GE854a62",TWITTER_CONSUMER_SECRET="d775b93f776dc6577B3f2C212aE080c24f308e28803d0877a2"


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::

    Embetty is running on port 3000. If you want to host Embetty on the same Uberspace as your website, use ``/embetty`` as URI.

.. include:: includes/web-backend.rst

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
.. _quick start guide: https://github.com/heiseonline/embetty#quick-start
.. _Twitter application: https://apps.twitter.com/
.. _feed: https://github.com/heiseonline/embetty-server/releases

----

Tested with Embetty 3.0.8, Uberspace 7.11.5

.. author_list::
