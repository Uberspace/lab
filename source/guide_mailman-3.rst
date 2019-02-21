.. highlight:: console

.. author:: Richard Kroegel <info@kroegel.org>

.. sidebar:: Logo

  .. image:: _static/images/mailman.jpg
      :align: center

#########
Mailman 3
#########

`Mailman`_ is free software for managing electronic mail discussion and e-newsletter lists. Mailman is integrated with the web, making it easy for users to manage their accounts and for list owners to administer their lists. Mailman supports built-in archiving, automatic bounce processing, content filtering, digest delivery, spam filters, and more.

`Mailman 3`_ is a complete re-write of previous versions, consisting of a suite of programs that work together:

  * **Mailman Core**; the core delivery engine. This is where you are right now.
  * **Postorius**; the web user interface for list members and administrators.
  * **HyperKitty**; the web-based archiver
  * **Mailman client**; the official Python bindings for talking to the Core’s REST administrative API.

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

Your URL needs to be setup for web and mail:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$ uberspace mail domain list
 isabell.uber.space
 [isabell@stardust ~]$

Additionally, create a mailbox_ for Mailman to use to send e-mails. In this example, we are going to use ``forwarder@isabell.uber.space``.

Installation
============

Get Mailman 3
-------------
Install Mailman 3 and its dependencies via pip.

::

 [isabell@stardust ~]$ pip3.6 install --user mailman postorius hyperkitty mailman-hyperkitty whoosh
 [...]
 [isabell@stardust ~]$

Get Dart Sass
-------------
Postorius and HyperKitty are build using SASS_ stylesheets which have to be compiled/decompiled before use. As U7 does not provide an SASS compiler, we need to download the *Dart Sass* standalone binary. Get the link of the latest Dart Sass binary for **linux-x64** from https://github.com/sass/dart-sass/releases, download and extract the binaries:

::

 [isabell@stardust ~]$ wget https://github.com/sass/dart-sass/releases/download/9.99.9/dart-sass-9.99.9-linux-x64.tar.gz
 [isabell@stardust ~]$ tar xzvf dart-sass-9.99.9-linux-x64.tar.gz dart-sass
 [isabell@stardust ~]$ mv dart-sass ./bin/ 
 [isabell@stardust ~]$ rm dart-sass-9.99.9-linux-x64.tar.gz 
 [isabell@stardust ~]$


Get the mailman-suite example configuration
-------------------------------------------
To have a starting point for configuration, we use the mailman-suite_ example provided by the Mailman team and move it to a path where we can access it easily.

::

 [isabell@stardust ~]$ git clone https://gitlab.com/mailman/mailman-suite.git
 [isabell@stardust ~]$ mv mailman-suite/mailman-suite_project/ .
 [isabell@stardust ~]$ rm -rf mailman-suite
 [isabell@stardust ~]$ mv mailman-suite_project/ mailman-suite
 [isabell@stardust ~]$ 


Get and enable uwsgi
---------------------
.. include:: includes/install-uwsgi.rst

Get .qmail helper script
-------------------------
Mailman 3 uses LMTP to transfer emails locally. As qmail_ is not able to use this directly, we need to download a helper script from the mailman source:

::

 [isabell@stardust ~]$ cd bin
 [isabell@stardust bin]$ wget https://gitlab.com/mailman/mailman/raw/master/contrib/qmail-lmtp
 [isabell@stardust bin]$ chmod +x qmail-lmtp

Configuration
=============
Get a free port
---------------

We need to find a couple of free ports and bind your application to it.  Since Mailman Core itself exposes a REST interface, Postorius and HyperKitty run as Django applications with their own webserver and we need a LMTP port for local mail forwarding from qmail_ to Mailman, you will need to execute the following code multiple times (directly before you are going to change the respective configurations).

.. include:: includes/generate-port.rst


Configure Mailman Core
----------------------

At first, we need to configure the REST interface of the core component. To create a basic configuration, we need to run ``mailman info`` and get the path of the configuration file. The output should look like this:

:: 

 [isabell@stardust ~]$ mailman info
 GNU Mailman 3.2.0 (La Villa Strangiato)
 Python 3.6.7 (default, Dec  5 2018, 15:02:05)
 [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
 config file: /home/isabell/var/etc/mailman.cfg
 db url: sqlite:////home/isabell/var/data/mailman.db
 devmode: DISABLED
 REST root url: http://localhost:8001/3.1/
 REST credentials: restadmin:restpass
 [isabell@stardust ~]$ 

When the file is created, we need to add and change a couple of options in ``/home/isabell/var/etc/mailman.cfg``. The ``mta`` section contains the configuration related to sending and receiving mails. As we are using qmail_, the incoming MTA has to be set to null. In ``webservice`` section we configure the REST API server. As sometimes the paths where mailman stores its data can depend on the directory from where it is called, we manually define all necessary paths in ``paths.custom`` and force their usage in ``mailman``. A full overview of possible settings can be found in the `mailman docs schema.cfg`_.

.. code :: cfg

 [mta]
 incoming: mailman.mta.null.NullMTA
 lmtp_host: localhost
 smtp_host: stardust.uberspace.de
 # First free port
 lmtp_port: 9000
 smtp_port: 587 
 smtp_user: forwarder@isabell.uber.space
 smtp_pass: mailpassword

 [webservice]
 hostname: localhost
 # Second free port
 port: 9001
 use_https: no
 admin_user: restadmin
 admin_pass: restpass
 api_version: 3.1

 [paths.custom]
 var_dir: /home/isabell/var
 bin_dir: /home/isabell/.local/bin
 log_dir: /home/isabell/var/logs
 lock_dir: /home/isabell/var/locks
 data_dir: /home/isabell/var/data
 cache_dir: /home/isabell/var/cache
 etc_dir: /home/isabell/var/etc
 messages_dir: /home/isabell/var/messages
 archive_dir: /home/isabell/var/archives
 template_dir: /home/isabell/var/templates
 pid_file: /home/isabell/var/master.pid
 lock_file: /home/isabell/var/locks/master.lck

 [mailman]
 layout: custom

Daemonizing Mailman Core
------------------------

As we want to make sure that Mailman is started automatically, we need to set it up as a service. Due to mailman not having having the option to always run in foreground, we need some other means of controlling it.

Based on this `guide <https://serverfault.com/a/608073>`_, we can create a small bash mapper that starts mailman and then stays in the foreground while regularly checking mailman's pid file. It is also able to gracefully terminate mailman through supervisorctl. Long story short, create a file ``~/bin/mailman3-daemon`` and put in the following content:

.. code :: sh

 #! /usr/bin/env bash
 set -eu
 
 pidfile=/home/aobtest/var/master.pid
 command="/home/aobtest/.local/bin/mailman"
 arg_config="--config /home/aobtest/var/etc/mailman.cfg "
 
 # Proxy signals
 function kill_app(){
     $command $cmd_config stop
     kill $(cat $pidfile)
     exit 0 # exit okay
 }
 trap "kill_app" SIGINT SIGTERM
 
 # Stop mailman if running
 $command $arg_config stop
 
 # Start with force if not exited correctly
 $command $arg_config start --force
 sleep 2
 
 # Loop while the pidfile and the process exist
 while [ -f $pidfile ] && kill -0 $(cat $pidfile) ; do
     sleep 0.5
 done
 exit 1000 # exit unexpected
 
Afterwards, make it executable:

::

 [isabell@stardust ~]$ chmod +x ~/bin/mailman3-daemon
 [isabell@stardust ~]$

As last step, we need to create the supervisord config file for mailman in ``~/etc/services.d/mailman3.ini``:

.. code :: ini

 [program:mailman3]
 command=%(ENV_HOME)s/bin/mailman3-daemon
 autostart=true
 autorestart=true
 stderr_logfile = ~/var/logs/daemon_err.log
 stdout_logfile = ~/var/logs/daemon_out.log
 stopsignal=INT

Now we can tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 mailman3: available
 [isabell@stardust ~]$ supervisorctl update
 mailman3: added process group
 [isabell@stardust ~]$ supervisorctl status
 mailman3                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

Adjusting Django configuration
------------------------------

After the REST backend has been configured, we need to configure the Django frontends for Postorius and HyperKitty. The configuration is stored in ``/home/isabell/mailman-suite/settings.py``. As the default configuration contains a lot of pre-defined options, only changed or important settings are mentioned below (in order of appearance in the configuration file). To reduce the amount of lines, comments have been left out but can be found in the original file for reference.

.. code :: python

 [...]

 BASE_DIR = '/home/isabell/var/' 
 
 SECRET_KEY = 'change-this-on-your-production-server'
 
 DEBUG = True # Leave to True while debugging, but change to False in production
 
 ADMINS = (
      ('Isabell', 'isabell@uber.space'), 
 )

 ALLOWED_HOSTS = [
     "localhost",  # Archiving API from Mailman, keep it.
     # "lists.your-domain.org",
     # Add here all production URLs you may have.
     "isabell.uber.space", 
     # And more...
 ]

 # Second free port from above
 MAILMAN_REST_API_URL = 'http://localhost:9001' 
 MAILMAN_REST_API_USER = 'see_above'
 MAILMAN_REST_API_PASS = 'see_above'
 MAILMAN_ARCHIVER_KEY = '<SecretArchiverAPIKey>'
 MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')
 
 [...]

 USE_X_FORWARDED_HOST = True # Uncomment
 
 SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Uncomment
 SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SCHEME', 'https') # Uncomment
 
 [...]

 STATIC_ROOT = '/home/isabell/html/static/'

 [...]

 DEFAULT_FROM_EMAIL = 'forwarder@isabell.uber.space' 
 
 SERVER_EMAIL = 'isabell@uber.space'

 EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
 EMAIL_HOST = 'stardust.uberspace.de'
 EMAIL_PORT = 587
 EMAIL_USE_TLS = True
 # Use previously created mail user/password
 EMAIL_HOST_USER = 'forwarder@isabell.uber.space'
 EMAIL_HOST_PASSWORD = 'mailpassword'

 [...]

 COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', '/home/isabell/bin/sass {infile} {outfile}'),
    ('text/x-sass', '/home/isabell/bin/sass {infile} {outfile}'),
 )

 # Comment the following lines out to test sending mail
 #if DEBUG == True:
 #   EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
 #   EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')

Setting up Django
-----------------

After we have adjusted our configuration file, we need to compile and configure the Django project and create a super user to be used as web admin:

:: 

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.6 manage.py migrate
 [...]
 [isabell@stardust mailman-suite]$ python3.6 manage.py collectstatic
 [...]
 [isabell@stardust mailman-suite]$ python3.6 manage.py createsuperuser
 ? Username (leave blank to use 'isabell'): isabell
 ? Email address: isabell@uber.space
 ? Password:
 ? Password (again):
 ℹ Superuser created successfully.
 [isabell@stardust mailman-suite]$

When the Django is configured, we need to rename the example site to match our needs:

::

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.6 manage.py shell

 >>> from django.contrib.sites.models import Site
 >>> site = Site.objects.get(name='example.com')
 >>> site.name = 'Isabells Uberspace'
 >>> site.domain = 'isabell.uber.space'
 >>> site.save()
 >>> exit()

 [isabell@stardust mailman-suite]$

.. include:: includes/proxy-rewrite-static.rst

Please be sure to use the third free port, e.g. 9003!

Finally, to be able to call and execute our Django app, we need to create ``~/uwsgi/apps-enabled/mailman-suite.ini`` and add the following content.

.. code :: ini
 
 [uwsgi]
 chdir = /home/isabell/mailman-suite
 
 # Third free port
 http-socket = 0.0.0.0:9003
 master = true
 process = 2
 threads = 2
 wsgi-file = wsgi.py
 
 # your user name
 uid = isabell
 gid = isabell
 
 attach-daemon = ./manage.py qcluster

Generally, it might be necessary to reload *uwsgi* after changing the config change:

::

 [isabell@stardust ~]$ supervisorctl restart uwsgi
 uwsgi: stopped
 uwsgi: started
 [isabell@stardust ~]$
 
Setup .qmail-forwarder script
-----------------------------

Because Mailman_ doesn't handle our .qmail-configuration automatically, we need to help it create the necessary aliases. This needs to be done for each new mailinglist, so we will create an extra script to process this task. Create the file ``~/bin/mailman3-add-list.sh`` with the following content (this code was created originally 
for Mailman 2 and is based on the script provided in the official installation instructions). Make sure to change the ``p`` variable to your LMTP port:

.. code :: bash

 #!/bin/sh
 if [ $# = 1 ]; then
 i=$1
 # First free port
 p=9000
 echo Making links to $i in home directory...
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-admin
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-bounces
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-confirm
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-join
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-leave
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-owner
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-request
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-subscribe
 echo "|/home/isabell/bin/qmail-lmtp $p 1" > ~/.qmail-$i-unsubscribe
 fi

You still need to make the script executable:

::

 [isabell@stardust ~]$ chmod +x ~/bin/mailman-add-list.sh
 [isabell@stardust ~]$

After creating a list via the webinterface, you can then run this script to create the required .qmail-files (like ``mailman-add-list.sh listname`` if you stored it as ``~/bin/mailman-add-list.sh`` and want to create aliases for a list ``listname``).

Install cronjobs
----------------

`Mailman 3`_ offers a `cronjobs <https://manual.uberspace.de/daemons-cron.html?highlight=cron#cron>`_ to perform some maintenance actions at regular intervals. To install them for your user, run ``crontab -e`` and add the line ``@daily /home/isabell/.local/bin/mailman digests --send`` at the end of the file.

Using Mailman
=============

Now we are ready to use Mailman. Simply go to ``https://isabell.uber.space`` and log in with the superuser account we created earlier. You now will get an email to confirm the account to the address you initially specified. If you do not get one, check the ``~/var/email/`` dir - you might have forgotten to disable the debug setting in ``~/mailman-suite/settings.py`` (see above). Otherwise check the logs in ``~/mailman-suite/`` and ``~/var/logs/`` for clues. 

Now you can create a new list using the Postorious web UI. 

.. warning:: Don't forget to create the .qmail-aliases using the '~/bin/mailman3-add-list.sh' script afterwards!

This guide is based on the `official Mailman 3 installation instructions <http://docs.mailman3.org/en/latest/index.html>`_, the `official Mailman 3 documentation <https://mailman.readthedocs.io/en/latest/README.html>`_ as well as the great guides here at uberlab for `Django <./guide_django.html>`_ and, of course, `Mailman 2 <./guide_mailman.html>`_.

Tested with Django 2.1.7, HyperKitty 1.2.1, Mailman 3.2.0, Postorius 1.2.4 and uWSGI 2.0.18 on Uberspace 7.2.2.2.

.. _Mailman 3: http://www.mailman3.org/en/latest/
.. _Mailman: http://www.list.org/
.. _mailman-suite: https://gitlab.com/mailman/mailman-suite
.. _mailman docs schema.cfg: https://mailman.readthedocs.io/en/latest/src/mailman/config/docs/config.html#schema-cfg
.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _mailbox: https://manual.uberspace.de/en/mail-mailboxes.html#setup-a-new-mailbox
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt
.. _SASS: https://sass-lang.com/
.. _`macropin/docker-mailman`: https://github.com/macropin/docker-mailman/blob/master/mailman.sh
.. _qmail: https://manual.uberspace.de/en/basics-home.html?highlight=qmail#qmail


.. authors::
