.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. sidebar:: Logo

  .. image:: _static/images/matomo.png
      :align: center

#########
Matomo
#########

Matomo_ (former known as Piwik) is an open source website tracking tool (like Google Analytics) written in PHP and distributed under the GNU General Public License v3.0 licence.

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

If you want to use Matomo with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

If you want to install Matomo into a subfolder of your domain, create a new folder and navigate to it:
::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust ~]$ mkdir matomo
 [isabell@stardust ~]$ cd matomo/
 [isabell@stardust matomo]$

If you want to install matomo into your `document root`_, just navigate with ``cd`` to your `document root`_.

Now download the latest version and extract it:

.. note:: The link to the lastest version can be found at Matomo's `download page <https://matomo.org/download/>`_.

::

 [isabell@stardust matomo]$ curl https://builds.matomo.org/piwik.zip -o matomo.zip && unzip matomo.zip && rm matomo.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 18.0M  100 18.0M    0     0  26.1M      0 --:--:-- --:--:-- --:--:-- 26.1M
  
 [...]
 
 [isabell@stardust matomo]$

This will create a ``piwik`` folder containing the files and directories. Now we will move the files from the ``piwik`` folder to the parent folder.

::

 [isabell@stardust matomo]$ cd piwik/ && mv * .. && cd .. && rm piwik -rf
 [isabell@stardust matomo]$

Now point your browser to your Matomo URL and follow the instructions of the Installer.

You will need to enter the following information:
  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Matomo database name: we suggest you use an additional_ database. For example: isabell_matomo
  * Administrator (*Super User*) username and password: choose a username (maybe not *admin*) and a strong password for the super user
  * Name and URL of the first website you want to track with Matomo (more can be added after installation)
  
Privacy
=======
Matomo can be configured to ensure that users' privacy is respected. This is required in some countries. A detailed guide for configuring privacy settings in Matomo can be found `here <https://matomo.org/docs/privacy/>`_.


Updates
=======

The easiest way to update Matomo is to use the web updater provided in the admin section of the Web Interface. Matomo will show you a hint if there is an update available.

.. note:: Check the `changelog <https://matomo.org/changelog/>`_ regularly to stay informed about new updates and releases.

.. _Matomo: https://matomo.org/
.. _PHP: https://manual.uberspace.de/en/lang-php.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases

----

Tested with Matomo 3.5.0, Uberspace 7.1.3

.. authors::