.. highlight:: console

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. sidebar:: Logo

  .. image:: _static/images/bludit.png
      :align: center

######
Bludit
######

Bludit_ is a web application to build your own website or blog in seconds, it's completely free and open source. Bludit is a Flat-File CMS this means Bludit uses files in JSON format to store the content, you don't need to install or configure a database. You only need a web server with PHP support.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * Domains_

License
=======

Bludit_ are released under the MIT License. 

All relevant legal information can be found here 

  * https://tldrlegal.com/license/mit-license
  * https://docs.bludit.com/en/#license

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your `document root`_, then download and configure Bludit_.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/bludit/bludit/archive/3.8.0.tar.gz
 […]
 Saving to: ‘3.8.0.tar.gz’

    [    <=>                                ] 1,016,833   1.58MB/s   in 0.6s

 2019-02-27 20:02:16 (1.58 MB/s) - ‘3.8.0.tar.gz’ saved [1016833]
 [isabell@stardust html]$
 
Untar the archive and then delete it. 

.. code-block:: console
 :emphasize-lines: 1,5
 
 [isabell@stardust html]$ tar -xzvf 3.8.0.tar.gz --strip-components=1
 bludit-3.8.0/.github/
 […]
 bludit-3.8.0/install.php
 [isabell@stardust html]$ rm 3.8.0.tar.gz
 [isabell@stardust html]$ cd ~
 [isabell@stardust ~]$ 


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


1. First make a full backup from all files and folders.
2. Remember which version of Bludit_ you are using for a possible roll-back.
3. Download the latest version from Bludit_ or Github_ to your client.
4. Extract the zip file.
5. Replace existing files with the new files with your terminal or (s)ftp-client.

.. warning:: The files in the directory ``/bl-content/database/`` should not be deleted. There the user accounts are stored.

6. Log into the admin area and check your settings.



.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _Domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/bludit/bludit/releases.atom
.. _Bludit: https://www.bludit.com
.. _`document root`: https://manual.uberspace.de/en/web-documentroot.html
.. _Github: https://github.com/bludit/bludit/releases

----

Tested with Bludit 3.8.0 "APA", Uberspace 7.2.2.2

.. authors::
