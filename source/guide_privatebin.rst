.. highlight:: console

.. author:: Nepomacs <https://github.com/Nepomacs/>

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

.. abstract::
  PrivateBin is a minimalist, open source online pastebin where the server has zero knowledge of pasted data.

  Data is encrypted and decrypted in the browser using 256bit AES in Galois Counter mode.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`domains <web-domains>`

License
=======

PrivateBin consists of PHP and JS code which was originally written by Sébastien Sauvage in 2012 and falls unter the Zlib/libpng license.
All relevant legal information can be found in the Github_ repository of the project.


Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$



The domain you want to use must be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the source
-------------------

Check Github_ for the `latest release`_ and copy the download link to the .tar.gz file.
Then ``cd`` to your ``~/html`` folder and use ``wget`` to download it. Replace the URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://github.com/PrivateBin/PrivateBin/archive/1.3.4.tar.gz
 […]
 Saving to: ‘1.3.4.tar.gz’

 100%[=================================================>] 3,172,029   3.45MB/s   in 0.9s

 2020-11-22 16:27:44 (8.32 MB/s) - ‘1.3.4.tar.gz’ saved [523648]
 [isabell@stardust html]$

Untar the archive and then delete it. Replace the version in the file name with the one you downloaded.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust html]$ tar -xzf 1.3.4.tar.gz --strip-components=1
 [isabell@stardust html]$ rm 1.3.4.tar.gz
 [isabell@stardust html]$


Activate the .htaccess file
-----------------------------
PrivateBin provides a .htaccess file, which blocks some known robots and link-scanning bots. Activate it by renaming it from ``.htaccess.disabled`` to ``.htaccess``.

.. code-block:: console

 [isabell@stardust html]$ mv .htaccess.disabled .htaccess
 [isabell@stardust html]$


Moving files outside of DocumentRoot
------------------------------------
It is recommended_ to move the configuration, data files, templates and PHP libraries outside of your document root.
To do that, create a Folder  ``privatebin-data`` in ``/var/www/virtual/isabell/`` and move the folders to the new location.
If not already there, go to the ``html`` directory before running ``mv``.

.. code-block:: console

 [isabell@stardust html]$ mkdir ../privatebin-data
 [isabell@stardust html]$ mv -t ../privatebin-data cfg/ lib/ tpl/ vendor/
 [isabell@stardust html]$

Changing index.php
------------------

Now edit ``~/html/index.php``  to inform PrivateBin about to the new location of the folders.

.. code-block:: php

 [...]
 // change this, if your php files and data is outside of your webservers document root
 define('PATH', '../privatebin-data/');
 [...]

Configuration
=============

Configure your PrivateBin Instance
----------------------------------

.. note:: You don't need to change any of the default settings as they are mostly secure.

You can find an example configuration file at ``cfg/conf.sample.php`` with the default settings. To change these, copy the sample file
to ``cfg/conf.php`` and adapt the values as needed.

.. code-block:: console

 [isabell@stardust html]$ cp ../privatebin-data/cfg/conf.sample.php ../privatebin-data/cfg/conf.php
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


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Updating ist quite easy. Just repeat all steps of the :lab_anchor:`Installation chapter <guide_privatebin.html#installation>`.
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

Tested with PrivateBin 1.3.4, Uberspace 7.7.10

.. author_list::
