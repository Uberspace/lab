.. sectionauthor:: Daniel Kratz <uberlab@danielkratz.com>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/neos.png 
      :align: center

#########
Neos
#########

Neos_ is an open source Content Application Platform based on its own PHP framework Flow and distributed under the GPLv3 licence. 

The system is best known for it's intuitive approach of editing content directly in the website (also known as frontend editing) and the mighty marketing features like content dimensions which allow to display optimized contents for different target audiences. 

Neos (formerly TYPO3 Neos) was released for the first time in 2013. It is maintained by the Neos-Team and Contributors.



----

.. note:: For this guide you should be familiar with the basic concepts of 

  * PHP_
  * MySQL_ 
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.1: 

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Since Neos uses the subdirectory Web/ as web root you should not install Neos in your `document root`_. Instead we install it next to that and then use a symlink to make it accessible.

``cd`` to one level above your `document root`_, then use the dependency manager Composer to create a new project based on the Neos base distribution:

.. note:: Composer will install all neccessary dependencies Neos needs to run. This can take some time.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ composer create-project neos/neos-base-distribution Neos
 Neos
 Installing neos/neos-base-distribution (42.23.1)
   - Installing neos/neos-base-distribution (42.23.1): Downloading (100%)
 Created project in Neos
 Loading composer repositories with package information
 Updating dependencies (including require-dev)
 [...]

 [isabell@stardust isabell]$

Remove your unused `document root`_ and create a new symbolic link to the Neos/Web directory:

.. warning:: Please make sure your document root is empty before removing it. This step will delete all contained files if any.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -rf html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/Neos/Web html
 [isabell@stardust isabell]$

Configuration
============

Point your browser to your website URL and append /setup (e.g. isabell.uber.space/setup) to use the web based installer.

After setting some things up automatically, the setup will ask you for a setup password. You need to get this from a file in your Neos installation first: 

::

 [isabell@stardust isabell]$ cat /var/www/virtual/$USER/Neos/Data/SetupPassword.txt
 The setup password is:

 Z3pyq1Sp

 After you successfully logged in, this file is automatically deleted for security reasons.
 Make sure to save the setup password for later use.

Step 1: After you logged in using your setup password Neos will check for supported image manipulation libraries. Fortunately on Uberspace 7 there are multiple libraries preinstalled. Neos will use "imagick" as standard. You can change that later manually.

Step 2: To configure your database, you need to enter the following information:

  * your preffered database driver. You can use the preselected ``MySQL/MariaDB via PDO``.
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Neos database name: we suggest you use an additional_ database. For example: isabell_neos. The installer will create this database for you if you select ``[New Database]`` and enter the name for the new database.

Step 3: Create an administrator account. Please don't use ``admin`` as your username and set yourself a strong password.

Step 4: Create a new site by importing an existing/demo package or creating a new one. 

Step 5: You have successfully installed Neos on Uberspace 7!

Tuning
============

Please note that Neos is not running in "Production" context by default. If you're ready to go live and want full speed, you should change your FLOW_CONTEXT environment variable to "Production".

You can do this by uncommenting the line ``SetEnv FLOW_CONTEXT Production`` in your .htaccess file under ``/var/www/virtual/$USER/Neos/Web/.htaccess``

Updates
=======


.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Neos' `releases <https://github.com/neos/neos/releases>`_ for the latest versions. If a newer
version is available, you should manually update your installation. 

By using composer, you can update an existing installation to a specific version, without having to create a new project. But you have to follow version specific update instructions which you can find at the end of the official download_ page on the Neos website.

.. warning:: Neos, Flow and especially **additional packages** are **not** updated automatically, so make sure to regularly check any update options.


.. _Neos: https://www.neos.io/
.. _PHP: http://www.php.net/
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _feed: https://github.com/neos/neos/releases.atom
.. _download: https://www.neos.io/download-and-extend.html

----

Tested with Neos 3.3.9 and Uberspace 7.1.1 