.. highlight:: console

.. spelling::
    bg
    BG

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. tag:: lang-php
.. tag:: web
.. tag:: cms
.. tag:: blog

.. sidebar:: Logo

  .. image:: _static/images/bludit.png
      :align: center

######
Bludit
######

.. tag_list::

Bludit_ is a web application to build your own website or blog in seconds. It's completely free and open source. Bludit is a Flat-File CMS, which means that it uses files in JSON format to store the content: you don't need to install or configure a database. You only need a web server with PHP support.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`Domains <web-domains>`

License
=======

Bludit_ is released under the MIT License.

All relevant legal information can be found here

  * https://tldrlegal.com/license/mit-license
  * https://docs.bludit.com/en/#license

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest version of Bludit from Github__.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/bludit/bludit/archive/refs/tags/3.14.1.tar.gz
 […]
 Saving to: ‘3.14.1.tar.gz’

    [    <=>                                ] 1,016,833   1.58MB/s   in 0.6s

 2022-12-15 20:02:16 (1.58 MB/s) - ‘3.14.1.tar.gz’ saved [1016833]
 [isabell@stardust html]$

Untar the archive and then delete it.

.. code-block:: console
 :emphasize-lines: 1,5

 [isabell@stardust html]$ tar -xzvf 3.14.1.tar.gz --strip-components=1
 bludit-3.14.1/.github/
 […]
 bludit-3.14.1/install.php
 [isabell@stardust html]$ rm 3.14.1.tar.gz
 [isabell@stardust html]$


Finishing installation
======================

Now point your Browser to your installation URL ``https://isabell.uber.space/install.php``.
Complete the form and follow the installation instructions.

You will need to enter the following information:

  * language: the language you prefer.
  * admin password: set up your admin password.


Tuning
======

For plugins, themes and other stuff go to Bludit_.


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Follow the Update instructions in the Bludit documentation__.

.. note:: The files in the directory ``/bl-content`` should not be deleted. There the user accounts and other important stuff is stored.




.. _feed: https://github.com/bludit/bludit/releases.atom
.. _Bludit: https://www.bludit.com
.. _Github: https://github.com/bludit/bludit/releases
.. _recovery.php: https://raw.githubusercontent.com/bludit/password-recovery-tool/master/recovery.php
.. _documentation: https://docs.bludit.com/

----

Tested with Bludit 3.14.1, Uberspace 7.14.0, PHP 8.1

.. author_list::
