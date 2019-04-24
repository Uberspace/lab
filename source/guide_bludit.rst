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

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download and configure Bludit_.

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

Your first plugin you have to install, is the **Version** plugin. It will show you in the admin panel the current used version of bludit. When there will be a new version of bludit, the plugin show you an info and a link to the bludit site.
To install log into admin panel and go to **Plugins**. The last plugin at the list ist **Version**. Only click activate and wait a moment. There it is.

Update
------

1. First make a full backup from all files and folders and move it to your home folder.

.. code-block:: console
 :emphasize-lines: 2,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ tar cfvz 3.8.0_backup.tar.gz *
 bl-content/
 […]
 README.md
 [isabell@stardust html]$ mv 3.8.0_backup.tar.gz /home/isabell/
 [isabell@stardust html]$

2. Download the latest version from Bludit_ or Github_. In this example we´re download it from Github_.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/bludit/bludit/archive/3.8.1.tar.gz
 […]
 Saving to: ‘3.8.1.tar.gz’

    [   <=>                                 ] 1,026,715   1.70MB/s   in 0.6s

 2019-03-03 10:23:07 (1.70 MB/s) - ‘3.8.1.tar.gz’ saved [1026715]
 [isabell@stardust html]$

4. Extract the tar file.
Untar the archive and replace existing files. After this, delete the tar file.

.. warning:: The files in the directory ``/bl-content`` should not be deleted. There the user accounts and other important stuff are stored. For more information look at the next chapter.

.. code-block:: console
 :emphasize-lines: 1,5

 [isabell@stardust html]$ tar -xzvf 3.8.1.tar.gz --strip-components=1
 bludit-3.8.1/.github/
 […]
 bludit-3.8.1/install.php
 [isabell@stardust html]$ rm 3.8.1.tar.gz
 [isabell@stardust html]$

5. Log into the admin area and check your settings.


Important folders
-----------------

Folder structure of Bludit.

/html
    /bl-content/    « Databases and uploaded images

    /bl-kernel/     « Core of Bludit

    /bl-languages/  « Languages files

    /bl-plugins/    « Plugins

    /bl-themes/     « Themes


/bl-content/
**************

.. note:: This folder is very important, it is where Bludit stores all files, as well as databases and images. Before making some update it's highly recommended to make a backup of this folder.

.. important::

 **databases/**
    **plugins/ (Database: plugins)**
        - pages.php       (Database: pages)
        - security.php    (Database: black list, brute force protection, others)
        - site.php        (Database: site variables, name, description, slogan, others)
        - tags.php        (Database: tags)
        - users.php       (Database: users)

    **pages/ (Content: pages)**
        - about/index.txt
        - imprint/index.txt

    **tmp/ (Temp files)**

    **uploads/ (Uploaded files)**
        - profiles/       (Profiles images)
        - thumbnails/     (Thumbnails images)
        - example1.jpg
        - example2.png

    **workspaces/ (Workspaces for the plugins)**


/bl-kernel/
***********

This folder contains the core of Bludit.

/bl-languages/
**************

This folder contains all language files, each file is a JSON document, encoded in UTF-8.

/bl-languages/
++++++++++++++
    * bg_BG.json
    * cs_CZ.json
    * de_CH.json
    * en.json
    * es.json
    * ...

/bl-plugins/
************

This folder contains all plugins, you can download new plugins and upload here.

/bl-plugins/
++++++++++++
    * about/
    * disqus/
    * rss/
    * sitemap/
    * tinymce/
    * ...

/bl-themes/
***********

This folder contains all themes, you can download new themes and upload here.

/bl-themes/
+++++++++++
    * alternative/
    * blogx/
    * ...


Security
========

Password recovery for user *admin*
------------------------------------

When you forgot the admin password, you can reset it manually.

1. Download the file recovery.php_ from Bludit_ in your :manual:`document root <web-documentroot>`.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://raw.githubusercontent.com/bludit/password-recovery-tool/master/recovery.php
 […]
 Saving to: ‘recovery.php’

 100%[======================================>] 1,703       --.-K/s   in 0s

 2019-03-03 10:35:32 (139 MB/s) - ‘recovery.php’ saved [1703/1703]
 [isabell@stardust html]$

2. Open the file with your browser, https://isabell.uber.space/recovery.php
3. A new password for the admin user is generated and displayed on the browser.
4. Log in to the admin panel with the user *admin* and the new password generated.

.. note:: The script recovery.php is going to try to delete himself but if this doesn't happen we recommend delete the file recovery.php by hand.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ rm recovery.php
 [isabell@stardust html]$




.. _feed: https://github.com/bludit/bludit/releases.atom
.. _Bludit: https://www.bludit.com
.. _Github: https://github.com/bludit/bludit/releases
.. _recovery.php: https://raw.githubusercontent.com/bludit/password-recovery-tool/master/recovery.php

----

Tested with Bludit 3.8.0 "APA" (3.8.1 "APA" for update), Uberspace 7.2.2.2

.. author_list::
