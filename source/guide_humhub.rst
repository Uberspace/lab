.. highlight:: console

.. author:: Christoph Reißig <https://reissig-stopp.de>

.. tag:: lang-php
.. tag:: web
.. tag:: social-intranet
.. tag:: social-collaboration
.. tag:: teamwork
.. tag:: business

.. sidebar:: Logo

  .. image:: _static/images/humhub-logo.png
      :align: center

######
HumHub
######

.. tag_list::

HumHub is a free social network software and framework built to give you the tools to make teamwork easy and successful. 

The software is based on top of the Yii_ framework and therefore written in PHP_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

HumHub is released under a dual license, on one hand the AGPL V3 license and on the other hand a commercial license. The licence and terms can be found on the website via

  * https://humhub.org/en/licences
  * https://humhub.org/en/legal/terms


Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`DocumentRoot <web-documentroot>` and download the latest release, then unzip it into the ``html`` directory:

.. code-block:: console
 :emphasize-lines: 1,2,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget --output-document=latest.zip https://humhub.org/en/download/start?version=latest&type=zip&ee=0
 […]
 [isabell@stardust isabell]$ unzip latest.zip
 [isabell@stardust isabell]$ ls
 humhub-latestversion
 [isabell@stardust isabell]$ cd /humhub-latestversion
 […]
 [isabell@stardust isabell]$ mv * /var/www/virtual/$USER/html/
 [isabell@stardust ~]$

Database Setup
----------------------

Humhub saves your data in a MySQL database. Please use an :manual_anchor:`additional database <database-mysql.html#additional-databases>`. You need to create this database before you enter the database credentials in the web-installer.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_humhub"
 [isabell@stardust ~]$

Configuration
=============

Point your browser to your domain (e.g. isabell.uber.space) to set up and configure your HumHub installation.

Step 1: Welcome Screen and System Check
---------------------------------------

On the fist screen of the webinstaller you are welcomed. You can only choose >>Next<< here. After that the configuration is checked to meet the system requirements.

When everything is fine proceed to the >>Next<< step.

If you are facing any problems have a look at http://docs.humhub.org/admin-installation.html for further problem solving instructions

Step 2: Database Configuration
------------------------------

Enter the following informations into the installer:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * the name of your newly created HumHub database (e.g. ``isabell_humhub``)

Then click >>Next<<.


Step 3: Social network Name
---------------------------------

Fill in the name of your social network, for example the name of your company or brand.

Then click >>Next<<.


Step 4: Admin Details
---------------------------------

Fill in the username, an admin email adress, your admin password and your first and lastname.

Then click >>Create Admin Account<<.

**That's it.** After successful account creation you can login using your admin account credentials.


Usage
=====

You can find the full documentation under

    * http://docs.humhub.org/index.html


Updates
=======

.. note:: Check the news feed_ regularly to stay informed about the newest version.

You will be additionally notified about available updates in the built in humhub update module.
You can update the installation via the update module which can be found in the humhub administration menue.


.. _HumHub: https://humhub.org
.. _news: https://www.humhub.org/de/news
.. _AGPLv3: http://www.gnu.org/licenses/agpl-3.0.en.html
.. _PHP: http://www.php.net/
.. _Yii: https://www.yiiframework.com/


----

Tested with HumHub 1.3.15, Uberspace 7.1.13

.. author_list::
