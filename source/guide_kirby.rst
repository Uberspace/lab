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

Kirby was released for the first time in 2009 and is actively developed by the Bastian Allgeier GmbH. Although the code is open source, a license is required for use in production. 

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

The installation of Kirby is quite easy. Just clone the Kirby Starterkit in your `document root`_. 

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ git clone --recursive https://github.com/getkirby/starterkit.git ~/html
  Cloning into 'html'...
  remote: Counting objects: 3749, done.
  remote: Compressing objects: 100% (69/69), done.
  remote: Total 3749 (delta 25), reused 92 (delta 25), pack-reused 3649
  Receiving objects: 100% (3749/3749), 7.74 MiB | 9.97 MiB/s, done.
  Resolving deltas: 100% (1035/1035), done.
 [isabell@stardust html]$

That's all the magic. If you visit your previously set up domain you should see a working website with demo contents from the Starterkit. 

.. note:: While we are cloning Kirby from Github you can alternatively just download_ the zip and upload the contents manually to your `document root`_.

To simplify future updates we are replacing the ``kirby`` and ``panel`` folders and add them again as Git submodules. Using this workflow, updates will need only two commands on the command line. 

First, we remove the existing folders from the filesystem. Then we stage the changes in Git to remove the folders from the repository index. 

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ rm -R panel kirby
 [isabell@stardust html]$ git add .
 [isabell@stardust html]$

Finally we are adding the components as Git submodules and try to update them just to be safe.

.. code-block:: console
 :emphasize-lines: 1,5,9

 [isabell@stardust html]$ git submodule add https://github.com/getkirby/kirby.git
  Cloning into '/var/www/virtual/isabell/html/kirby'...
  remote: Counting objects: 4344, done.
  [...]
 [isabell@stardust html]$ git submodule add https://github.com/getkirby/panel.git
  Cloning into '/var/www/virtual/isabell/html/panel'...
  remote: Counting objects: 11083, done.
  [...]
 [isabell@stardust html]$ git submodule update --init --recursive
 [isabell@stardust html]$

Configuration
============

When you're ready to launch your website with Kirby you need to purchase a license_. To use your license go to ``/site/config/config.php`` and fill in your licence key.

.. code-block:: php

  c::set('license', 'your license key');

Best practices
============

If you want to avoid the demo code and contents of the Kirby Starterkit, there is a minimal setup available known as Plainkit_. You can install it the same way as the Starterkit. However, the use is only recommended for users who are already familiar with Kirby. 

Tuning
============

For complex sites with lots of content or high amounts of traffic you can switch on Kirby's cache. The cache stores the entire result of a rendered page. As long as the cache is valid, visitors will be served the cached version which is pretty close in performance to a static html file.

The cache can be activated in ``/site/config/config.php``:

.. code-block:: php

  c::set('cache', true);

.. note:: Kirby is using a simple file cache by default. Please make sure that ``/site/cache`` is writable in order to make the cache work. If you've not changed the write permissions this should work out of the box.

If you need dynamic output on individual pages you can ignore them from being cached, by adding their URI to the cache.ignore array in ``/site/config/config.php``:

.. code-block:: php

  c::set('cache.ignore', array(
    'search'
  ));

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Kirby's `releases <https://github.com/getkirby/starterkit/releases>`_ for the latest versions. If a newer
version is available, you should update your installation. 

If you've followed this guide and are using Git submodules for the Kirby core and the panel, updating via the command line is very easy. Just checkout the submodules and pull the newest version from Github:


.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ git submodule foreach --recursive git checkout master
 [isabell@stardust html]$ git submodule foreach --recursive git pull
 [isabell@stardust html]$

If you've downloaded Kirby as a ZIP archive and uploaded it manually you can update by redownloading the package and just replace the ``kirby`` and ``panel`` folders with the ones from the new archive.

.. warning:: Kirby and especially **Plugins** are **not** updated automatically, so make sure to regularly check any update options.


.. _Kirby: https://getkirby.com/
.. _PHP: http://www.php.net/
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _feed: https://github.com/getkirby/starterkit/releases.atom
.. _download: https://getkirby.com/docs/installation/download
.. _license: https://getkirby.com/buy
.. _Plainkit: https://github.com/getkirby/plainkit

----

Tested with Kirby 2.5.10 and Uberspace 7.1.4