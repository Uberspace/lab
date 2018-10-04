.. highlight:: console

.. author:: Philipp Wensauer <mail@philippwensauer.com>
      
##########
SimpleID
##########

SimpleID is a simple, personal OpenID provider written in PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

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

``cd`` to your `document root`_, respectively the folder above, because not all files must/should be accessable via web, then download the latest release of *SimpleID* and extract it:

.. note:: The link to the lastest version can be found at SimpleID's `download page <http://simpleid.koinic.net/releases//>`_.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget http://downloads.sourceforge.net/simpleid/simpleid-1.0.2.tar.gz
 [isabell@stardust isabell]$ tar -xzf simpleid-1.0.2.tar.gz

Step 2 - Symlink
----------------

The folder containing the frontend needs to be accessible via web. To achieve this, a symlink is created linking to the www folder.

::

 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/simpleid/www/ ~/html/simpleid
 
Step 3 - Copy empty configuration
---------------------------------

::

 [isabell@stardust isabell]$ cp /var/www/virtual/$USER/simpleid/www/config.php.dist /var/www/virtual/$USER/simpleid/www/config.php

Step 4 - Cleanup
----------------
::

 [isabell@stardust isabell]$ rm simpleid-1.0.2.tar.gz
 
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

Before editing this file, we need to create a password/salt pair.

There are several ways to go, using the MD5, SHA1 and SHA256 algorithm and an optional salt. In this example we will use the SHA256 algorithm with a random salt.

First we'll generate a random salt to make this secure as possible. You are free to use any string as salt.

::

 [isabell@stardust ~]$ date +%s | sha256sum | base64 | head -c 16 ; echo
 Y2MyZTNkYzI0OTA3
 [isabell@stardust ~]$
 
With this generated hash and your password in mind we can create the SHA256 hash with 100,000 iterations for the identity file.

.. warning:: Replace ``<password>`` with your password, and ``<salt>`` with the generated salt or the one you decided to chose.

::

 [isabell@stardust ~]$ php -r 'echo hash_pbkdf2("sha256", "<password>", "<salt>", 100000).PHP_EOL;'

With our example values this would be

::

 [isabell@stardust ~]$ php -r 'echo hash_pbkdf2("sha256", "MySuperSecretPassword", "Y2MyZTNkYzI0OTA3", 100000).PHP_EOL;'
 1d62e170c8af2529b51f8450406e7f7280f5076da1c7e17bbd44575c8112f5b6
 [isabell@stardust ~]$

Then open the identity file you copied before to /var/www/virtual/$USER/simpleid/identities/<username>.identity in your favorite editor.

Search for the pass line and edit it as described.

.. code-block:: php

 pass="<hash>:pbkdf2:sha256:<salt>"

In our example we would use this passline:

.. code-block:: php

 pass="1d62e170c8af2529b51f8450406e7f7280f5076da1c7e17bbd44575c8112f5b6:pbkdf2:sha256:Y2MyZTNkYzI0OTA3"
 
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

Create the file index.htm with the following content:

.. code-block:: html

 <html>
   <head>
     <link rel="openid.server" href="https://isabell.uber.space/simpleid/" />
     <link rel="openid2.provider" href="https://isabell.uber.space/simpleid/" />
   </head>
 </html>

You are now ready to use your own OpenID provider. Just make sure you are using the right URL for authentication, https://<username>.uber.space/openid.

.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _PHP: https://manual.uberspace.de/en/lang-php.html

----

Tested with SimpleID 1.0.2, Uberspace 7.1.13.0

.. authors::
