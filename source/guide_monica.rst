.. highlight:: console

.. author:: Sebastian Krings <https://krin.gs>

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/monica.png
      :align: center

######
Monica
######

.. tag_list::

Monica_ is a management system for your personal relationships.
It can be used to organize friends and friendships in the same manner a CRM is used to organize customers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

Monica is released under the ``GNU Affero General Public License v3.0``. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the source
-------------------

To install Monica clone the official repository one level above your :manual:`DocumentRoot <web-documentroot>` using Git.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ git clone https://github.com/monicahq/monica.git
 Cloning into 'monica'...
 remote: Enumerating objects: [...], done.
 [...]
 [isabell@stardust isabell]$

Afterwards, checkout the branch corresponding to the latest release (see the `Monica releases page`_ for version numbers).
The example below uses version 3.5.0, which is the latest version at the time of writing.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/monica
 [isabell@stardust monica]$ git fetch
 [isabell@stardust monica]$ git checkout tags/v3.5.0
 [isabell@stardust monica]$

Provide a database
------------------

You can either use the default database provided with each Uberspace or create an :manual_anchor:`additional database <database-mysql.html#additional-databases>` just for Monica.
We suggest to use the second approach to separate your data as much as possible.

You can create an additional database using the command line as shown below.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_monica"
 [isabell@stardust ~]$

Setup Monica
------------

To configure Monica and provide it with the necessary information to access the database, copy the sample configuration file ``.env.example`` to ``.env``.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/monica
 [isabell@stardust ~]$ cp .env.example .env
 [isabell@stardust monica]$

Then edit the ``.env`` file as follows:
* Change the values of ``DB_DATABASE``, ``DB_USERNAME``, ``DB_PASSWORD`` to reflect your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`,
* Set ``APP_ENV`` to ``production``, and
* If you want send reminders via mail, set the variables starting with ``MAIL_`` to reflect an email account and SMTP server. To use your Uberspace mail account, use the :manual_anchor:`following settings <mail-access.html#smtp>`.

Once the configuration file has been changed, continue with the installation.
To do so, you can use Composer_ and yarn_:

.. code-block:: console
 :emphasize-lines: 1,2,7,11

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/monica
 [isabell@stardust monica]$ composer install --no-interaction --no-dev
 [...]
 91 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!
 > Illuminate\Foundation\ComposerScripts::postInstall
 [isabell@stardust monica]$ yarn install
 Successfully applied Snyk patches
 Done in 9.34s.
 Done in 35.24s.
 [isabell@stardust monica]$ yarn run production
 [...]
 webpack compiled successfully
 Done in 122.16s.

Now, generate an application key to be used, i.e., for encryption.
There will be two interactive promts in which you would need to confirm with ``yes``.

 .. code-block:: console
 :emphasize-lines: 1,7,10,13

 [isabell@stardust monica]$ php artisan key:generate
 **************************************
 *     Application In Production!     *
 **************************************

 Do you really wish to run this command? (yes/no) [no]:
 > yes

 Application key set successfully.
 [isabell@stardust monica]$ php artisan setup:production -v

 You are about to setup and configure Monica. Do you wish to continue? (yes/no) [no]:
 > yes

✓ Maintenance mode: on
 [...]
 [isabell@stardust monica]$

Configuration
=============

Set up a cronjob
----------------

To allow Monica to perform some processes in the background, set up a :manual:`cronjob <daemons-cron>`.
Note that cron does not expand variables such as ``$PATH`` and ``$USER`` in the :manual_anchor:`same way the shell does <daemons-cron.html#path>`.
Thus, make sure to replace ``ìsabell`` with the appropriate account name below.

Use ``crontab -e`` to edit your cron table and add the following line:
``* * * * *   /usr/bin/php /var/www/virtual/isabell/monica/artisan schedule:run >> /dev/null 2>&1``

Configure the web server
------------------------

To make Monica available via the URL of your Uberspace, remove your unused :manual:`DocumentRoot <web-documentroot>` and create a new symbolic link to the ``monica/public`` directory.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/monica/public html
 [isabell@stardust isabell]$

Finishing installation
----------------------

After the installation, there is no default account.
Instead, Monica offers to create an initial account upon the first visit.

Once the account has been created, it can be used to invite others to the Monica instance.

Best practices
==============

Signup without invititation is disabled by default.
For security reasons, we advise against opening up user registration.

If you need to enable it, you can open the configuration file ``.env`` again and set ``APP_DISABLE_SIGNUP=false``.
For the change to take effect, you have to run ``php artisan config:cache`` inside the installation folder.

Updates
=======

.. note:: Check the `Monica releases page`_ regularly for updates and new releases.

To update Monica, you need to fetch the latest version via git.
Afterwards, you can use Composer_ and yarn_ to update dependencies if necessary and migrate your database in case the schema has changed.
The example below uses v3.5.0 for the latest version.
Your output might differ and show a (later) version number.

.. code-block:: console
 :emphasize-lines: 1,2,6,8,13,17,21

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/monica
 [isabell@stardust monica]$ git fetch
 remote: Enumerating objects: 3957, done.
 [...]
 * [new tag]         v3.5.0                 -> v3.5.0
 [isabell@stardust monica]$ git checkout tags/v3.5.0
 [...]
 [isabell@stardust monica]$ composer install --no-interaction --no-dev
 [...]
 91 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!
 > Illuminate\Foundation\ComposerScripts::postInstall
 [isabell@stardust monica]$ yarn install
 Successfully applied Snyk patches
 Done in 9.34s.
 Done in 35.24s.
 [isabell@stardust monica]$ yarn run production
 [...]
 webpack compiled successfully
 Done in 122.16s.
 [isabell@stardust monica]$ php artisan monica:update --force
 [...]
 Monica v3.5.0 is set up, enjoy.
 [isabell@stardust monica]$


.. _Composer: https://getcomposer.org/
.. _yarn: https://yarnpkg.com
.. _LICENSE: https://github.com/monicahq/monica/blob/master/LICENSE.md
.. _Monica releases page: https://github.com/monicahq/monica/releases

----

Tested with Monica 3.5.0, Uberspace 7.12.0

.. author_list::
