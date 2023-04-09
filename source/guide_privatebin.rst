.. highlight:: console

.. author:: Nepomacs <https://github.com/Nepomacs/>
.. author:: franok <https://franok.de>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: privacy
.. tag:: lang-php
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/privatebin.png
      :align: center

##########
PrivateBin
##########

.. tag_list::

PrivateBin is a minimalist, open source online pastebin where the server has zero knowledge of pasted data.

Data is encrypted and decrypted in the browser using 256bit AES in Galois Counter mode.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`domains <web-domains>`

License
=======

PrivateBin consists of PHP and JS code which was originally written by Sébastien Sauvage in 2012 and falls under the Zlib/libpng license.
All relevant legal information can be found in the Github_ repository of the project.


Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$



The domain you want to use must be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the source
-------------------

Check the Github_ release section and copy the release tag version of the `latest release`_. Set the variable PBIN_VERSION to the version you just copied.
Then ``cd`` to your ``~/html`` folder and use ``wget`` to download it.

.. code-block:: console
 :emphasize-lines: 3

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust ~]$ PBIN_VERSION=0.0.0
 [isabell@stardust html]$ wget https://github.com/PrivateBin/PrivateBin/archive/$PBIN_VERSION.tar.gz -O "PrivateBin-$PBIN_VERSION.tar.gz"
 […]
 Saving to: ‘PrivateBin-1.5.1.tar.gz’

 100%[=================================================>] 3,172,029   3.45MB/s   in 0.9s

 2022-11-17 16:27:44 (8.32 MB/s) - ‘PrivateBin-1.5.1.tar.gz’ saved [523648]
 [isabell@stardust html]$

Untar the archive and then delete it.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust html]$ tar -xzf PrivateBin-1.5.1.tar.gz --strip-components=1
 [isabell@stardust html]$ rm PrivateBin-1.5.1.tar.gz
 [isabell@stardust html]$


Activate the .htaccess file
-----------------------------
PrivateBin provides a .htaccess file, which blocks some known robots and link-scanning bots. Activate it by renaming it from ``.htaccess.disabled`` to ``.htaccess``.

.. code-block:: console

 [isabell@stardust html]$ mv .htaccess.disabled .htaccess
 [isabell@stardust html]$


Moving files outside of DocumentRoot
------------------------------------
It is recommended_ to move the configuration, data files, templates and PHP libraries outside of your document root. This is useful to secure your installation.
To do that, create a folder  ``privatebin-data`` in ``/home/isabell/`` and move the folders to the new location (remember to replace ``isabell`` with your own username!).
If not already there, go to the ``html`` directory before running ``mv``.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ mkdir /home/$USER/privatebin-data
 [isabell@stardust html]$ mv -t /home/$USER/privatebin-data cfg/ lib/ tpl/ vendor/
 [isabell@stardust html]$

Changing index.php
------------------

Now edit ``~/html/index.php``  to inform PrivateBin about the new location of the folders.

.. code-block:: php

 [...]
 // change this, if your php files and data is outside of your webservers document root
 define('PATH', '/home/isabell/privatebin-data/');
 [...]

Configuration
=============

Configure your PrivateBin Instance
----------------------------------

.. note:: You don't need to change any of the default settings as they are mostly secure.

You can find an example configuration file at ``cfg/conf.sample.php`` with the default settings. To change these, copy the sample file to ``cfg/conf.php`` and adapt the values as needed.

.. code-block:: console

 [isabell@stardust ~]$ cd /home/$USER/privatebin-data
 [isabell@stardust html]$ cp cfg/conf.sample.php cfg/conf.php
 [isabell@stardust html]$

The file is in ini format, meaning that lines beginning with semicolons ``;`` are comments,
configuration options are grouped in sections, marked by square brackets ``[`` and ``]``
and the option keys are separated by the values with equal signs ``=``.

A full list of the possible configuration values can be found here_.



Best practices
==============

Robots.txt
----------

PrivateBin comes with a ``robots.txt`` file in the root directory.
It disallows all robots from accessing your pastes.
If you followed this guide, it is already at the right place in your :manual:`DocumentRoot <web-documentroot>`.
However, if you installed PrivateBin into a subdirectory, you have to move ``robots.txt`` back into the DocumentRoot.
Of course also adjust the file if you already use a robots.txt.

Making your PrivateBin instance read-only
-----------------------------------------

If you want to limit write access to your PrivateBin instance, i.e. specify who can create content, you can configure the ``.htaccess`` file accordingly.
Choose a username that should have write access and provide it to the ``htpasswd`` command:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ htpasswd -c .htpasswd sample_user
 New password:
 Re-type new password:
 Adding password for user sample_user
 [isabell@stardust html]$
 
Further users can be added by omitting the ``-c`` flag:
.. code-block:: console
 
 [isabell@stardust html]$ htpasswd .htpasswd another-user
 New password:
 Re-type new password:
 Adding password for user another-user
 [isabell@stardust html]$
 
Edit the ``.htaccess`` file and add the following lines (exchange ``isabell`` by your username):

.. code-block:: text

 AuthType Basic
 AuthName "Login to PrivateBin"
 AuthUserFile /var/www/virtual/isabell/html/.htpasswd
 <LimitExcept GET>
    Require valid-user
 </LimitExcept>

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ htpasswd -c .htpasswd sample_user
 New password:
 Re-type new password:
 Adding password for user sample_user
 [isabell@stardust html]$

The .htaccess file should look like this:

.. code-block::

 [isabell@stardust html]$ cat .htaccess
 RewriteEngine on
 RewriteCond !%{HTTP_USER_AGENT} "Let's Encrypt validation server" [NC]
 RewriteCond %{HTTP_USER_AGENT} ^.*(bot|spider|crawl|https?://|WhatsApp|SkypeUriPreview|facebookexternalhit) [NC]
 RewriteRule .* - [R=403,L]
 
 AuthType Basic
 AuthName "Login to PrivateBin"
 AuthUserFile /var/www/virtual/isabell/html/.htpasswd
 <LimitExcept GET>
    Require valid-user
 </LimitExcept>
 
 <IfModule mod_php7.c>
 php_value max_execution_time 30
 php_value post_max_size 10M
 php_value upload_max_size 10M
 php_value upload_max_filesize 10M
 php_value max_file_uploads 100
 </IfModule>

The PrivateBin site is still visible to the public
When a user tries to publish content, a Basic-Auth popup will ask for username and password.
The generated links are accessible to everyone.


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the latest version.

Updating is quite easy. Just repeat all steps of the :lab_anchor:`Installation chapter <guide_privatebin.html#installation>`.
Your configuration file won't get overwritten.

Check the Release-Notes if the configuration changed between ``cfg/conf.sample.php`` and your ``conf.php``.
Also check ``.htaccess.disabled`` if further adjustments needed to be made.


.. _PHP: http://www.php.net/
.. _latest release: https://github.com/PrivateBin/PrivateBin/releases/latest
.. _Github: https://github.com/PrivateBin/PrivateBin
.. _feed: https://github.com/PrivateBin/PrivateBin/releases.atom
.. _recommended: https://github.com/PrivateBin/PrivateBin/blob/master/INSTALL.md#changing-the-path
.. _here: https://github.com/PrivateBin/PrivateBin/wiki/Configuration

----

Tested with PrivateBin 1.5.1, Uberspace 7.15.1, PHP 8.1

.. author_list::
