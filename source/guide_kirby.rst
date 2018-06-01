.. sectionauthor:: Daniel Kratz <uberlab@danielkratz.com>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/kirby.svg 
      :align: center

#########
Kirby
#########

Kirby_ is a modern, fast, flexible, file-based (no database) content management system written in PHP. 

The idea behind Kirby is to provide a tool for developing websites or applications that is both easy to use for developers and at the same time gives you all the freedom you want to structure your content and render your output.

Kirby was released for the first time in 2009 and is actively developed by the Bastian Allgeier GmbH. Although the code of Kirby is available for download, a per website license_ is required to use it in production. 

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

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install and update Kirby we use the Kirby CLI_, which is a command line interface to manage Kirby installations more efficiently. You can install it via Composer. 

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ composer global require getkirby/cli:1.4.0
  Changed current directory to /home/isabell/.config/composer
  ./composer.json has been updated
  Loading composer repositories with package information
  Updating dependencies (including require-dev)
  Nothing to install or update
  Generating autoload files
 [isabell@stardust ~]$

.. warning:: Please note that we are installing the latest release tag (1.4.0) instead of master, since the master branch contains a bug_ which would prevent the CLI from running on Uberspace 7. 

To install the Kirby Starterkit_ into your `document root`_, you just need to use the ``kirby install`` command. 

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust ~]$ kirby install html
  Installing Kirby...
  ======================================================================> 100%
  Extracting files
  Kirby is installed!
 [isabell@stardust ~]$

That's all the magic. If you visit your previously set up domain you should see a working website with demo contents from the Starterkit. 

Configuration
============

When you're ready to launch your website with Kirby you need to purchase a license_. To use your license edit the configuration file ``~/html/site/config/config.php`` and fill in your licence key.

.. code-block:: php

  c::set('license', 'your license key');

.. warning:: Please be aware that one license is valid for a single website only. So you need to purchase additional licences for multiple websites. This is no legal advice. Please review the `license options <https://getkirby.com/buy>`_ and the `licence agreement <https://getkirby.com/license>`_ for yourself and contact the developer if you're not sure. 


Best practices
============

If you want to avoid the demo code and contents of the Kirby Starterkit, there is a minimal setup available known as Plainkit_. You can install it by appending the kit parameter to the install command ``kirby install html --kit plainkit``. However, the use is only recommended for users who are already familiar with Kirby. 

Tuning
============

For larger sites you can switch on Kirby's cache. The cache stores the entire result of a rendered page. As long as the cache is valid, visitors will be served the cached version which is faster than to regenerate it.

The cache can be activated by editing the ``config.php``:

.. code-block:: php

  c::set('cache', true);

.. note:: Kirby is using a simple file cache by default. Please make sure that ``~/html/site/cache`` is writable in order to make the cache work. If you've not changed the write permissions this should work out of the box.

If you need dynamic output on individual pages you can ignore them from being cached, by adding their URI to the cache.ignore array in the ``config.php``:

.. code-block:: php

  c::set('cache.ignore', array(
    'search'
  ));

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Kirby's `releases <https://github.com/getkirby/starterkit/releases>`_ for the latest versions. If a newer
version is available, you should update your installation. 

To update Kirby you just need to use the ``kirby update`` command in the directory of your installation. 

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ kirby update
  Updating Kirby...
  [...]
  Kirby has been updated to 64.8.6
 [isabell@stardust ~]$

If you've enabled the cache, you might need to empty the cache directory to be sure nothing breaks. Delete all contents from ``~/html/site/cache`` in order to do so.

.. warning:: Kirby and especially **Plugins** are **not** updated automatically, so make sure to regularly check any update options.


.. _Kirby: https://getkirby.com/
.. _PHP: http://www.php.net/
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _feed: https://github.com/getkirby/starterkit/releases.atom
.. _download: https://getkirby.com/docs/installation/download
.. _license: https://getkirby.com/buy
.. _Plainkit: https://github.com/getkirby/plainkit
.. _Starterkit: https://github.com/getkirby/starterkit
.. _CLI: https://github.com/getkirby/cli
.. _bug: https://github.com/getkirby/cli/issues/36

----

Tested with Kirby 2.5.10 and Uberspace 7.1.5