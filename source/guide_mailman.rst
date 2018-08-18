.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

.. sidebar:: Logo

  .. image:: _static/images/mailman.jpg
      :align: center

###########
Mailman 2.1
###########

Mailman_ is free software for managing electronic mail discussion and e-newsletter lists. Mailman is integrated with the web, making it easy for users to manage their accounts and for list owners to administer their lists. Mailman supports built-in archiving, automatic bounce processing, content filtering, digest delivery, spam filters, and more.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Python_
  * supervisord_
  * Folder/File Permissions

License
=======

Mailman is released under the GNU General Public License

  * https://www.gnu.org/copyleft/gpl.html

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

Download the latest Mailman 2.1 version from https://ftp.gnu.org/gnu/mailman/ and extract the archive in your webroot

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell
 [isabell@stardust ~]$ wget https://ftp.gnu.org/gnu/mailman/mailman-2.1.29.tgz
 [isabell@stardust ~]$ tar xzvf mailman-2.1.29.tgz
 [isabell@stardust ~]$ cd mailman-2.1.29
 [isabell@stardust ~]$

Step 2
------
Create the installation folder

::

 [isabell@stardust ~]$ mkdir /var/www/virtual/isabell/mailman
 [isabell@stardust ~]$ chmod a+rx,g+ws /var/www/virtual/isabell/mailman

and run the configure script, telling Mailman where to install and what user/groups to use for its binaries:

::

 [isabell@stardust ~]$ ./configure --with-username=isabell --with-groupname=isabell \
  --prefix=/var/www/virtual/isabell/mailman/ \
  --with-mail-gid=isabell --with-cgi-gid=isabell
 [isabell@stardust ~]$

After configuration is finished, you may compile and install the package by running

::

 [isabell@stardust ~]$ make && make install

Step 3
------

If compilation and installation finished without errors, we can continue by checking folder permissions in the installation folder.

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/mailman
 [isabell@stardust ~]$ bin/check_perms

In case errors are found, you should definitely fix them before continuing.

Step 4
------

If you want the webinterface to be available publically, we need to create a couple of SymLinks and an htaccess-file.

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/html
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/mailman/cgi-bin ./mailman
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/mailman/archives/public ./pipermail
 [isabell@stardust ~]$ printf "Options +ExecCGI\nSetHandler cgi-script" > /var/www/virtual/isabell/mailman/cgi-bin/.htaccess

Finally, we need to adjust file permissions for the Mailman_ cgi-scripts to run:

::

 [isabell@stardust ~]$ chmod -R 0755 /var/www/virtual/isabell/mailman/cgi-bin

Step 5
------

Because Mailman_ doesn't handle our .qmail-configuration automatically, we need to help it create the necessary aliases. The following script is based on the script provided in the official installation instructions and may be used by placing it in your Uberspace home-folder:

::

 #!/bin/sh
 if [ $# = 1 ]; then
 i=$1
 echo Making links to $i in the current directory...
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman post $i" > .qmail-$i
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman admin $i" > .qmail-$i-admin
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman bounces $i" > .qmail-$i-bounces
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman confirm $i" > .qmail-$i-confirm
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman join $i" > .qmail-$i-join
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman leave $i" > .qmail-$i-leave
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman owner $i" > .qmail-$i-owner
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman request $i" > .qmail-$i-request
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman subscribe $i" > .qmail-$i-subscribe
 echo "|preline /var/www/virtual/`whoami`/mailman/mail/mailman unsubscribe $i" > .qmail-$i-unsubscribe
 fi

After creating a list via the webinterface, you can then run this script to create the required .qmail-files (like ``~/addlist.sh listname`` if you stored it as ``addlist.sh`` and want to create aliases for a list ``listname``).

Step 6
------

By now we have installed all the necessary files - let's tell them what they should actually do. In ``/var/www/virtual/isabell/mailman/Mailman``, you will find two important files for configuration: ``Defaults.py`` and ``mm_cfg.py``. In the former, you will be able to review every settings default value. In the latter, you can change the value of each setting.

For our Uberspace, we should set ``DEFAULT_URL_HOST`` and ``DEFAULT_EMAIL_HOST`` to the name of your Uberspace host (i.e. ``stardust.uberspace.de``).

You will also need to create a mailbox_ for Mailman to use and set the following options respectively:

::

 SMTP_AUTH = True
 SMTP_USE_TLS = True
 SMTPHOST = 'stardust.uberspace.de'
 SMTPPORT = '587'

 SMTP_USER = 'mailmanbox@isabell.uber.space'
 SMTP_PASSWD = 'betterPWthanThis'

Additionally, you may enable HTTPS for your interface by setting:

::

 DEFAULT_URL_PATTERN = 'https://%s/mailman'

and running

::

 [isabell@stardust ~]$ /var/www/virtual/isabell/mailman/bin/withlist -l -a -r fix_url

Step 7
------

Now we are ready to create the administrative (site-wide) mailing list! Simply run

::

 [isabell@stardust ~]$ /var/www/virtual/isabell/mailman/bin/newlist mailman

and follow the on-screen instructions. Don't forget to create the .qmail-aliases afterwards!

Step 8
------

Mailman_ offers a couple of cronjobs to perform some maintenance actions at regular intervals. To install them for your user, run:

::

 [isabell@stardust ~]$ crontab /var/www/virtual/isabell/mailman/cron/crontab.in

Step 9
------

Create ``~/etc/services.d/mailman.ini`` with the following content (insert your username!):

::

 [program:mailman]
 command=/var/www/virtual/isabell/mailman/bin/qrunner --runner=All

Tell supervisord_ to refresh and start the qrunner:

::

 [isabell@stardust ~]$ supervisorctl reread
 mailman: available
 [isabell@stardust ~]$ supervisorctl update
 mailman: added process group
 [isabell@stardust ~]$ supervisorctl status
 mailman                          RUNNING   pid 3226, uptime 0:03:42

If it is not in state ``RUNNING``, check your configuration and logs.

All done! Enjoy using your new list manager available at ``https://isabell.uber.space/mailman``!

This guide is based on the `official Mailman 2.1 installation instructions <https://www.gnu.org/software/mailman/mailman-install/front.html>`_.

.. _Mailman: http://www.list.org/
.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _mailbox: https://manual.uberspace.de/en/mail-mailboxes.html


.. authors::
