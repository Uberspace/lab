.. highlight:: console

.. author:: Philipp Wensauer <mail@philippwensauer.com>
.. tag:: lang-php
.. tag:: web
.. tag:: privacy

.. sidebar:: Logo

  .. image:: _static/images/simpleid.png
      :align: center

##########
SimpleID
##########

.. tag_list::

SimpleID is a simple, personal OpenID provider written in PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Your URL needs to be setup for web:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1 - Download & Extract
------------------------------

``cd`` to your :manual:`document root <web-documentroot>`, respectively the folder above, because not all files must/should be accessible via web, then download the latest release of *SimpleID* and extract it:

.. note:: The link to the latest version can be found at SimpleID's `download page <http://simpleid.koinic.net/releases/>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget http://downloads.sourceforge.net/simpleid/simpleid-42.23.1.tar.gz
 [isabell@stardust isabell]$ tar -xzf simpleid-42.23.1.tar.gz
 [isabell@stardust ~]$

Step 2 - Symlink
----------------

The folder containing the frontend needs to be accessible via web. To achieve this, a symlink is created linking to the www folder.

::

 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/simpleid/www/ ~/html/simpleid
 [isabell@stardust ~]$

Step 3 - Copy empty configuration
---------------------------------

::

 [isabell@stardust isabell]$ cp /var/www/virtual/$USER/simpleid/www/config.php.dist /var/www/virtual/$USER/simpleid/www/config.php
 [isabell@stardust ~]$

Step 4 - Cleanup
----------------
::

 [isabell@stardust isabell]$ rm simpleid-42.23.1.tar.gz
 [isabell@stardust ~]$

Configuration
=============

Define Base URL
---------------

Edit file ``/var/www/virtual/$USER/simpleid/www/config.php``.
The only change you really have to do is changing the SIMPLEID_BASE_URL, the other options are optional.

.. warning:: Replace ``<username>`` with your Uberspace username!

.. code-block:: php

 define('SIMPLEID_BASE_URL', 'https://<username>.uber.space/simpleid');

In our example this would be:

.. code-block:: php

 define('SIMPLEID_BASE_URL', 'https://isabell.uber.space/simpleid');

Create identity
---------------

You will need to create an identify file for every user of your SimpleID installation.

.. warning:: Replace ``<username>`` with the username you want to use for your SimpleID identity!

::

 [isabell@stardust isabell]$ cp /var/www/virtual/$USER/simpleid/identities/example.identity.dist /var/www/virtual/$USER/simpleid/identities/<username>.identity
 [isabell@stardust ~]$

Before editing this file, we need to create a password/salt pair.

There are several ways to go, using the MD5, SHA1 and SHA256 algorithm and an optional salt. In this example we will use the SHA256 algorithm with a random salt.

First we'll generate a random salt to make this secure as possible. You are free to use any string as salt.

::

 [isabell@stardust ~]$ pwgen 32 1
 MySuperSecretSalt
 [isabell@stardust ~]$

With this generated hash and your password in mind we can create the SHA256 hash with 100,000 iterations for the identity file.

.. warning:: Replace ``<password>`` with your password, and ``<salt>`` with the generated salt or the one you decided to chose.

::

 [isabell@stardust ~]$ php -r 'echo hash_pbkdf2("sha256", "<password>", "<salt>", 100000).PHP_EOL;'
 [isabell@stardust ~]$

With our example values this would be

::

 [isabell@stardust ~]$ php -r 'echo hash_pbkdf2("sha256", "MySuperSecretPassword", "MySuperSecretSalt", 100000).PHP_EOL;'
 5fd924625f6ab16a19cc9807c7c506ae1813490e4ba675f843d5a10e0baacdb8
 [isabell@stardust ~]$

Then open the identity file you copied before to /var/www/virtual/$USER/simpleid/identities/<username>.identity in your favorite editor.

Search for the pass line and edit it as described.

.. code-block:: php

 pass="<hash>:pbkdf2:sha256:100000:<salt>"

In our example we would use this passline:

.. code-block:: php

 pass="5fd924625f6ab16a19cc9807c7c506ae1813490e4ba675f843d5a10e0baacdb8:pbkdf2:sha256:100000:MySuperSecretSalt"

Since this is our first user, it should be set as administrator by changing

.. code-block:: php

 ;administrator=1

to (remove the ``;``)

.. code-block:: php

 administrator=1

The last thing is to set an `identifier <http://simpleid.koinic.net/docs/1/identity-requirements/#identifier>`_ using an unique URL.

.. warning:: Replace ``<username>`` with your Uberspace username!

.. code-block:: php

 identity="https://<username>.uber.space/openid/"

This will be the URL you'll have to use for registering with websites. We'll create the folder and fill it in a later step. In this example we will use:

.. code-block:: php

 identity="https://isabell.uber.space/openid/"

.. warning:: Don't forget the closing ``/`` or you'll get an error if you try to use the identity.

After saving the file, you should be able login for the first time at your SimpleID installation located at the defined Base URL ``https://<username>.uber.space/simpleid``.

Create identifier
-----------------

For finally using this identity you'll need to create a file at the URL we've defined in the .identity file.

::

 [isabell@stardust ~]$ mkdir ~/html/openid
 [isabell@stardust ~]$

Create the file ~/html/openid/index.htm with the following content:

.. code-block:: html

 <html>
   <head>
     <link rel="openid.server" href="https://isabell.uber.space/simpleid/" />
     <link rel="openid2.provider" href="https://isabell.uber.space/simpleid/" />
   </head>
 </html>

You are now ready to use your own OpenID provider. Just make sure you are using the right URL for authentication, https://<username>.uber.space/openid.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Follow the steps described in the UPGRADE.txt shipped with the newest version. There all steps described you'll have to perform to update your installation.

.. _feed: http://simpleid.koinic.net/releases/

----

Tested with SimpleID 1.0.2, Uberspace 7.1.13.0

.. author_list::
