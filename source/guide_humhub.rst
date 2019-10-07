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

HumHub_ is a free social network software and framework built to give you the tools to make teamwork easy and successful. 

The software is based on top of the Yii_ framework and therefore written in PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

HumHub is released under a dual license, on one hand the AGPL V3 license and on the other hand a commercial license. The license_ and terms_ can be found on the Humhub website.

Prerequisites
=============

We're using PHP in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`DocumentRoot <web-documentroot>` and download the latest release_, then unzip it into the ``html`` directory:

.. code-block:: console
 :emphasize-lines: 2,5

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget --output-document=humhub.zip "https://humhub.org/en/download/start?version=1.3.15&type=zip&ee=0"
 […]
 [isabell@stardust isabell]$ unzip humhub.zip
 [isabell@stardust isabell]$ cd humhub-1.3.15
 [isabell@stardust humhub-1.3.15]$ mv * /var/www/virtual/$USER/html/
 [isabell@stardust humhub-1.3.15]$

Database Setup
----------------------

Humhub saves your data in a MySQL database. Please use an :manual_anchor:`additional database <database-mysql.html#additional-databases>`. You need to create this database before you enter the database credentials in the web-installer.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_humhub"
 [isabell@stardust ~]$

Configuration
=============

Point your browser to your domain (e.g. isabell.uber.space) to set up and configure your HumHub installation. Check the  documentation_ for further questions.


Updates
=======

Check the news_ regularly to stay informed about the newest version. You will be additionally notified about available updates in the built in humhub update module. You can update the installation via the update module which can be found in the humhub administration menue.


.. _HumHub: https://humhub.org
.. _news: https://www.humhub.org/de/news
.. _AGPLv3: http://www.gnu.org/licenses/agpl-3.0.en.html
.. _Yii: https://www.yiiframework.com/
.. _release: https://humhub.org/en/download
.. _documentation: http://docs.humhub.org/index.html
.. _license: https://humhub.org/en/licences
.. _terms: https://humhub.org/en/legal/terms


----

Tested with HumHub 1.3.15, Uberspace 7.1.13

.. author_list::
