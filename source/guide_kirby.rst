.. author:: Daniel Kratz <uberlab@danielkratz.com>
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

License
=======

Kirby is licensed under the `Kirby End User License Agreement`_ which you can find on the official website. You need to purchase a license_ to use Kirby with your website.

.. warning:: Please be aware that one license is valid for a single website only. So you need to purchase additional licenses for multiple websites. This is no legal advice. Please review the `license options`_ and the `Kirby End User License Agreement`_ for yourself and contact the developer if you’re not sure.

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

To install Kirby we create a new Kirby Starterkit project using Composer (which is a dependency manager for PHP).

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust ~]$ composer create-project getkirby/starterkit html
  Installing getkirby/starterkit (3.0.0)
   - Installing getkirby/starterkit (3.0.0): Downloading (100%)
  Created project in html
  Loading composer repositories with package information
  Updating dependencies (including require-dev)
  [...]
 [isabell@stardust ~]$

That's all the magic. If you visit your previously set up domain you should see a working website with demo contents from the Starterkit.

Configuration
=============

Visit your domain followed by ``/panel`` (e.g. ``isabell.uber.space/panel``) to visit the admin panel and create your admin account. Please use a strong password for this.

When you're ready to launch your website with Kirby you need to purchase a license_. To register your license login to the admin panel, click register in the upper right corner and enter the neccessary information.

Please make sure to deactivate the debug mode for your site when going live. Edit the ``site/config/config.php`` file and set the ``debug`` option to ``false`` to achieve that.


Best practices
==============

If you want to avoid the demo code and contents of the Kirby Starterkit, there is a minimal setup available known as Plainkit_. You can install it by changing the composer command to ``composer create-project getkirby/plainkit html``. However, the use is only recommended for users who are already familiar with Kirby.

Tuning
============

For larger sites you can switch on Kirby's cache. The cache stores the entire result of a rendered page. As long as the cache is valid, visitors will be served the cached version which is faster than to regenerate it.

The cache can be activated by adding the ``cache`` option to the ``site/config/config.php`` file:

.. code-block:: php

  return [
    'cache' => [
        'pages' => [
            'active' => true,
        ]
    ]
  ];

.. note:: Kirby is using a simple file cache by default. Please make sure that ``~/html/site/cache`` is writable in order to make the cache work. If you've not changed the write permissions this should work out of the box.

If you need dynamic output on individual pages you can ignore them from being cached, please switch to the Kirby docs_ to find out how to achieve this.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Kirby's releases_ for the latest versions. If a newer
version is available, you should update your installation.

To update Kirby you just need to use the command ``composer update getkirby/cms`` in the directory of your installation.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ composer update getkirby/cms
  Loading composer repositories with package information
  Updating dependencies (including require-dev)
  [...]
 [isabell@stardust ~]$

If you've enabled the cache, you might need to empty the page cache directory to be sure nothing breaks. Delete all contents from ``~/html/site/cache/pages`` in order to do so.

.. warning:: Kirby and especially **Plugins** are **not** updated automatically, so make sure to regularly check any update options.


.. _Kirby: https://getkirby.com/
.. _PHP: http://www.php.net/
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _releases: https://github.com/getkirby/kirby/releases
.. _feed: https://github.com/getkirby/kirby/releases.atom
.. _download: https://getkirby.com/docs/installation/download
.. _license: https://getkirby.com/buy
.. _Plainkit: https://github.com/getkirby/plainkit
.. _Starterkit: https://github.com/getkirby/starterkit
.. _Kirby End User License Agreement: https://getkirby.com/license
.. _license options: https://getkirby.com/buy
.. _docs: https://getkirby.com/docs/guide/cache

----

Tested with Kirby 3.0.0 and Uberspace 7.2.1

.. authors::
