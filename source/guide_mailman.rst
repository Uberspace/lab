.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>
.. author:: ezra <ezra@posteo.de>

.. tag:: lang-python
.. tag:: mail
.. tag:: mailinglist

.. sidebar:: Logo

  .. image:: _static/images/mailman.jpg
      :align: center

#########
Mailman 2
#########

.. tag_list::

Mailman_ is free software for managing electronic mail discussion and e-newsletter lists. Mailman is integrated with the web, making it easy for users to manage their accounts and for list owners to administer their lists. Mailman supports built-in archiving, automatic bounce processing, content filtering, digest delivery, spam filters, and more.

.. note:: This guide is for the older Mailman 2. Unless you have specific requirements, head over to the newer :lab:`Mailman 3 <guide_mailman-3>`!

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * Folder/File Permissions

License
=======

Mailman is released under the GNU General Public License

  * https://www.gnu.org/copyleft/gpl.html

Prerequisites
=============

Your URL needs to be setup for web and mail:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$ uberspace mail domain list
 isabell.uber.space
 [isabell@stardust ~]$

Mailman requires `dnspython`. Install it using `pip`:

::

 [isabell@stardust ~]$ pip install dnspython --user
 Collecting dnspython
   Using cached https://files.pythonhosted.org/packages/ec/d3/3aa0e7213ef72b8585747aa0e271a9523e713813b9a20177ebe1e939deb0/dnspython-1.16.0-py2.py3-none-any.whl
 Installing collected packages: dnspython
 Successfully installed dnspython
 [isabell@stardust ~]$ 

Installation
============

Step 1
------
Prepare the installation folders:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ mkdir mailman_source mailman
 [isabell@stardust isabell]$ chmod g+s mailman
 [isabell@stardust isabell]$

Step 2
------

Download the latest Mailman 2.1 version from https://ftp.gnu.org/gnu/mailman/ and extract the archive in your webroot (replace the version numbers accordingly):

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ wget https://ftp.gnu.org/gnu/mailman/mailman-2.1.29.tgz
 [isabell@stardust isabell]$ tar xzvf mailman-2.1.29.tgz -C mailman_source --strip-components=1
 [isabell@stardust isabell]$

Now run the configure script, telling Mailman where to install and what user/groups to use for its binaries. You need to change your Uberspace account name for each parameter (you can find a declaration for the parameters in the Mailman documentation_):

::


 [isabell@stardust ~]$ cd /var/www/virtual/$USER/mailman_source
 [isabell@stardust mailman_source]$ ./configure --with-username=$USER --with-groupname=$USER --prefix=/var/www/virtual/$USER/mailman/ --with-mail-gid=$USER --with-cgi-gid=$USER
 [...]
 config.status: creating build/cron/nightly_gzip
 config.status: creating build/cron/senddigests
 config.status: executing default commands
 configuration completed at Thu Nov 1 10:10:10 CET 2018
 [isabell@stardust mailman_source]$

After configuration is finished, you may compile and install the package by running

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/mailman_source
 [isabell@stardust mailman_source]$ make && make install
 Compiling /var/www/virtual/isabell/mailman/Mailman/versions.py ...
 Upgrading from version 0x0 to 0x2011df0
 getting rid of old source files
 no lists == nothing to do, exiting
 [isabell@stardust mailman_source]$


If compilation and installation finished without errors, we will no longer need the source files now, so clean them up:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm mailman-*.tgz
 [isabell@stardust isabell]$ rm -fvr mailman_source
 [isabell@stardust isabell]$


Step 3
------

We can continue by checking folder permissions in the installation folder:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/mailman
 [isabell@stardust mailman]$ bin/check_perms
 No problems found
 [isabell@stardust mailman]$

In case errors are found, you should definitely fix them before continuing.

Step 4
------

If you want the webinterface to be public available, we need to create a couple of SymLinks and an htaccess-file:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ ln -s /var/www/virtual/$USER/mailman/cgi-bin ./mailman
 [isabell@stardust html]$ ln -s /var/www/virtual/$USER/mailman/archives/public ./pipermail
 [isabell@stardust html]$ ln -s /var/www/virtual/$USER/mailman/icons ./icons
 [isabell@stardust html]$

Create the file ``/var/www/virtual/$USER/mailman/cgi-bin/.htaccess`` with the following content:

::

 Options +ExecCGI
 SetHandler cgi-script

Finally, we need to adjust file permissions for the Mailman_ cgi-scripts to run:

::

 [isabell@stardust ~]$ chmod -R 0755 /var/www/virtual/$USER/mailman/cgi-bin
 [isabell@stardust ~]$

Step 5
------

Because Mailman_ doesn't handle our .qmail-configuration automatically, we need to help it create the necessary aliases. This needs to be done for each new mailinglist, so we will create an extra script to process this task. Create the file ``~/bin/mailman-add-list.sh`` with the following content (this code is based on the script provided in the official installation instructions):

.. code :: bash

 #!/bin/sh
 if [ $# = 1 ]; then
 i=$1
 echo Making links to $i in home directory...
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman post $i" > ~/.qmail-$i
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman admin $i" > ~/.qmail-$i-admin
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman bounces $i" > ~/.qmail-$i-bounces
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman confirm $i" > ~/.qmail-$i-confirm
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman join $i" > ~/.qmail-$i-join
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman leave $i" > ~/.qmail-$i-leave
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman owner $i" > ~/.qmail-$i-owner
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman request $i" > ~/.qmail-$i-request
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman subscribe $i" > ~/.qmail-$i-subscribe
 echo "|preline /var/www/virtual/$USER/mailman/mail/mailman unsubscribe $i" > ~/.qmail-$i-unsubscribe
 fi

You still need to make the script executable:

::

 [isabell@stardust ~]$ chmod +x ~/bin/mailman-add-list.sh
 [isabell@stardust ~]$

After creating a list via the webinterface, you can then run this script to create the required .qmail-files (like ``mailman-add-list.sh listname`` if you stored it as ``~/bin/mailman-add-list.sh`` and want to create aliases for a list ``listname``).

Configuration
=============

By now we have installed all the necessary files - let's tell them what they should actually do.

Step 1
------

Create a :manual_anchor:`mailbox <mail-mailboxes.html#setup-a-new-mailbox>` for Mailman to use to send e-mails. In this example, we are going to use ``mailmanbox@isabell.uber.space``.

Step 2
------

Add the following options to the end of the file ``/var/www/virtual/$USER/mailman/Mailman/mm_cfg.py`` (change values accordingly!):

.. code:: python

 # configure default domains to use for the webinterface and e-mail addresses
 DEFAULT_URL_HOST = 'isabell.uber.space'
 DEFAULT_EMAIL_HOST = 'isabell.uber.space'

 # configure mailmans mailbox
 SMTP_AUTH = True
 SMTP_USE_TLS = True
 SMTPHOST = 'stardust.uberspace.de'
 SMTPPORT = '587'

 SMTP_USER = 'mailmanbox@isabell.uber.space'
 SMTP_PASSWD = 'MySuperSecretPassword'

 # tell mailman to use HTTPS
 DEFAULT_URL_PATTERN = 'https://%s/mailman/'

You can look up the meaning  and default value of each variable in the file ``Defaults.py`` in the same folder.

.. warning:: Do not modify the ``Defaults.py`` as it may be overwritten on updates!


Finishing Installation
======================

Install cronjobs
----------------

Mailman_ offers a couple of cronjobs to perform some maintenance actions at regular intervals. Additionally, there are some tasks that need to be run frequently (like checking mails). To install them for your user, run:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/mailman
 [isabell@stardust mailman]$ echo "* * * * * /var/www/virtual/$USER/mailman/bin/qrunner --runner=All --once" >> cron/crontab.in
 [isabell@stardust mailman]$ crontab cron/crontab.in
 [isabell@stardust mailman]$

Create the first mailinglist
----------------------------

Now we are ready to create the first mailing list! Simply run

::

 [isabell@stardust ~]$ /var/www/virtual/$USER/mailman/bin/newlist mailman
 Enter the email of the person running the list: isabell@uber.space
 Initial test password:
 [...]
 Hit enter to notify test owner...
 [isabell@stardust ~]$

and follow the on-screen instructions.

.. warning:: Don't forget to create the .qmail-aliases using the 'mailman-add-list.sh' script afterwards!

Redirect HTTP-requests
----------------------

If you don't want a pesky HTTP 403 (Forbidden) error when someone calls ``https://isabell.uber.space/mailman``, you can extend the ``.htaccess`` in ``/var/www/virtual/isabell/mailman/cgi-bin`` with the following lines and they will be redirected to the ``listinfo`` page:

::

 RewriteEngine on
 RewriteBase /
 RewriteCond %{REQUEST_URI} ^\/mailman\/$
 RewriteRule .* mailman/listinfo [R=301,L]

All done! Enjoy using your new list manager available at ``https://isabell.uber.space/mailman``!

This guide is based on the `official Mailman 2.1 installation instructions <https://www.gnu.org/software/mailman/mailman-install/front.html>`_.

.. _Mailman: http://www.list.org/
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt


.. author_list::
