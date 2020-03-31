.. author:: Daniel Kratz <https://danielkratz.com>

.. tag:: lang-php
.. tag:: web
.. tag:: shortlinks

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/yourls.png
      :align: center

#########
YOURLS
#########

.. tag_list::

YOURLS_ is a set of PHP scripts that will allow you to run Your Own URL Shortener with complete control over your data, detailed stats, plugins, and more.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

YOURLS is released under the `MIT License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install YOURLS we clone the current version from GitHub to your :manual:`DocumentRoot <web-documentroot>` using Git.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ git clone https://github.com/YOURLS/YOURLS .
 Cloning into '.'...
 remote: Enumerating objects: 27, done.
 […]
 [isabell@stardust ~]$

YOURLS saves all your data in a MySQL database which we have to create first. We suggest you use an :manual_anchor:`additional database <database-mysql.html#additional-databases>`. In this guide we create a new database called ``isabell_yourls``.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_yourls"
 [isabell@stardust ~]$


Configuration
=============

To configure YOURLS you need to setup your configuration file. Copy the sample configuration file and open it with a text editor of your choice.

.. code-block:: console

 [isabell@stardust ~]$ cp ~/html/user/config-sample.php ~/html/user/config.php
 [isabell@stardust ~]$

Edit the following parts of your configuration file:
 * change the values of ``YOURLS_DB_USER``, ``YOURLS_DB_PASS``, ``YOURLS_DB_NAME`` to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`
 * change the value of ``YOURLS_SITE`` to your previously set up domain including the protocol (in this case ``https://isabell.uber.space``)
 * replace the value of ``YOURLS_COOKIEKEY`` with a long random string which is used to secure cookies. You can generate a string using this webservice_ and copy it from there.
 * setup an admin account by editing the username and passwort in the ``yourls_user_passwords`` variable. Don't worry, YOURLS will hash these plain text passwords on the next login attempt. Please don't use ``admin`` as your username and set yourself a strong password.

Save the configuration file and point your browser to your website URL and append /admin (e.g. ``isabell.uber.space/admin``) to visit the YOURLS admin interface. On your first visit there is only one button called ``Install YOURLS``. CLick this button and the application will finish the setup.

That's it. You can now login using your account.

Best practices
==============

Privacy
--------

By default YOURLS logs every visit on a shortlink with the complete IP adress of the visitor. You might want to change that in regard to the GDPR.

In order to only save shortened IP adresses for your statistics you can install the plugin yourls-pseudonymize_. To install the plugin clone the plugin repository to ``/user/plugins`` using Git.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/user/plugins
 [isabell@stardust plugins]$ git clone https://github.com/ubicoo/yourls-pseudonymize
 Cloning into 'yourls-pseudonymize'...
 remote: Enumerating objects: 21, done.
 [isabell@stardust ~]$

Last but not least you need to activate the plugin in the "Manage Plugins" area of your YOURLS admin interface.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check YOURLS' releases_ for the latest versions. If a newer
version is available, you should update your installation.

To update YOURLS you can use Git to pull the newest release.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ git pull origin master
 From https://github.com/YOURLS/YOURLS
 * branch            master    -> FETCH_HEAD
 [...]
 [isabell@stardust ~]$

.. warning:: Your YOURLS instance is **not** updated automatically, so make sure to regularly check any update options.


.. _YOURLS: https://yourls.org/
.. _releases: https://github.com/YOURLS/YOURLS/releases
.. _feed: https://github.com/YOURLS/YOURLS/releases.atom
.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE: https://github.com/YOURLS/YOURLS/blob/master/LICENSE
.. _webservice: https://yourls.org/cookie
.. _yourls-pseudonymize: https://github.com/sas101/yourls-pseudonymize

----

Tested with YOURLS 1.7.4 and Uberspace 7.3.6

.. author_list::
