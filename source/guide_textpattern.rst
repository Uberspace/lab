.. author:: Robert Wetzlmayr <https://wetzlmayr.at/> et al.

.. tag:: lang-php
.. tag:: blog
.. tag:: cms
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/textpattern-logo-portrait.png
      :align: center

#########
Textpattern CMS
#########

.. tag_list::

`Textpattern CMS <https://textpattern.com>`_ is a flexible, elegant, fast and easy-to-use content management system written in PHP and `distributed under the GNU General Public License Version 2 (GPLv2) <https://textpattern.com/license>`_.

Textpattern is maintained by `Team Textpattern <https://textpattern.com/about/contributors>`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use Textpattern with your own domain, you will need to set up your :manual:`domains <web-domains>` first:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your :manual:`document root <web-documentroot>` and remove ``html/nocontent.html`` and the now empty ``html`` folder:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm html/nocontent.html
 [isabell@stardust isabell]$ rm -r html/
 [isabell@stardust isabell]$

Then download the latest release of Textpattern, extract it, and then rename the extracted folder to ``html``:

.. note:: The link to the latest version can be found at `Textpattern's download page <https://textpattern.com/download>`_.

::

 [isabell@stardust isabell]$ wget https://textpattern.com/file_download/118/textpattern-4.8.8.zip
 [isabell@stardust isabell]$ unzip textpattern-4.8.8.zip
 […]
    creating: textpattern-4.8.8/themes/
   inflating: textpattern-4.8.8/themes/.htaccess
   inflating: textpattern-4.8.8/.htaccess
 [isabell@stardust isabell]$ mv textpattern-4.8.8 html
 [isabell@stardust isabell]$ 

Now point your browser to your uberspace URL or domain and `follow the instructions <https://docs.textpattern.com/setup/installing-the-software>`_.

You will need to enter the following information:

Database details
----------------

  * MySQL user name: ``isabell``
  * MySQL password: ``yourMySQLPassword`` (you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now)
  * MySQL server: ``localhost``
  * MySQL database: your Textpattern database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: ``isabell_textpattern``
  * Create database?: Let Textpattern create your database for you.
  * Table prefix (optional): Leave this field blank.

Create config.php file
----------------------

  * Create a new file named config.php within the directory ``/var/www/virtual/$USER/html/textpattern/``. Copy and paste the information provided in the current setup step into the file.

Create and populate database tables
-----------------------------------

  * Your full name, your email address, login name, password: up to you...
  * Site configurations: The setup defaults will suffice for a start. You can change them anytime later when your site design evolves.

Go!
---

  * The last stage presents you with a confirmation screen that includes a link to the administration login page for your new Textpattern site.
  * You may need to make some necessary adjustments upon your first login to the back end. Please visit the Diagnostics panel (Admin > Diagnostics) to carry out any necessary corrections. This is perfectly normal, and any warnings or errors can be easily resolved here.

----

Tested with Textpattern 4.8.8, Uberspace 7.15.6, PHP 8.1

.. author_list::
