.. highlight:: console

.. author:: Richard Kroegel <info@kroegel.org>

.. tag:: lang-python
.. tag:: django
.. tag:: mail
.. tag:: mailinglist

.. sidebar:: Logo

  .. image:: _static/images/mailman.png
      :align: center

#########
Mailman 3
#########

.. tag_list::

`Mailman`_ is free software for managing electronic mail discussion and e-newsletter lists. Mailman is integrated with the web, making it easy for users to manage their accounts and for list owners to administer their lists. Mailman supports built-in archiving, automatic bounce processing, content filtering, digest delivery, spam filters, and more.

`Mailman 3`_ is a complete re-write of previous versions, consisting of a suite of programs that work together:

  * **Mailman Core**; the core delivery engine. This is where you are right now.
  * **Postorius**; the web user interface for list members and administrators.
  * **HyperKitty**; the web-based archiver
  * **Mailman client**; the official Python bindings for talking to the Core’s REST administrative API.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`MySQL <database-mysql>`
  * Folder/File Permissions

----


License
=======

Mailman is released under the GNU General Public License

  * https://www.gnu.org/copyleft/gpl.html


Prerequisites
=============

Your Domain needs to be setup for :manual_anchor:`web <web-domains.html#setup>` and :manual_anchor:`mail <mail-domains.html#setup>`:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$ uberspace mail domain list
 isabell.uber.space
 [isabell@stardust ~]$

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Additionally, create a :manual_anchor:`mailbox <mail-mailboxes.html#setup-a-new-mailbox>` for Mailman to use to send e-mails. In this example, we are going to use ``forwarder@isabell.uber.space``.

::

 [isabell@stardust ~]$ uberspace mail user add forwarder
 Enter a password for the mailbox:
 Please confirm your password:
 New mailbox created for user: 'forwarder', it will be live in a few minutes...
 [isabell@stardust ~]$


And another one as :manual_anchor:`catch-all <mail-mailboxes.html#catch-all-mailbox>`. In this example, we are going to use ``catchallbox@isabell.uber.space``.

::

 [isabell@stardust ~]$ uberspace mail user add catchallbox
 Enter a password for the mailbox:
 Please confirm your password:
 New mailbox created for user: 'forwarder', it will be live in a few minutes...
 [isabell@stardust ~]$
 [isabell@stardust ~]$ uberspace mail catchall set catchallbox
 Mails, which cannot be matched to a mailbox, will be sent to catchallbox.
 [isabell@stardust ~]$


You may want to add a Sieve rule and an IMAP folder ``Mailman``. To do this use your preferred mail client or login via https://webmail.uberspace.de/ using ``catchallbox@isabell.uber.space``. Under ``Settings`` > ``Filters`` you can add a custom sieve filter like this:

.. code-block:: sieve

  require["fileinto","regex","envelope"];

  if anyof(
    address :domain :regex ["to","delivered-to"] "isabell.uber.space",
    envelope :domain :regex "to" "isabell.uber.space"
  )
  {
      fileinto "Mailman";
      stop;
  }


Update pip - the package installer for python - to the latest version to get the latest packages. Possible warnings about skipped site packages can be ignored:

::

 [isabell@stardust ~]$ pip3.11 install --upgrade pip
 Defaulting to user installation because normal site-packages is not writeable
 WARNING: Skipping /usr/lib/python3.11/site-packages/pip-22.0.4.dist-info due to invalid metadata entry 'name'
 WARNING: Skipping /usr/lib/python3.11/site-packages/pip-22.3.1.dist-info due to invalid metadata entry 'name'
 ...
 [notice] A new release of pip is available: 24.0 -> 24.2
 [notice] To update, run: python3.11 -m pip install --upgrade pip
 [isabell@stardust ~]$ pip3.11 --version
 pip 24.2 from /home/kimyah4p/.local/lib/python3.11/site-packages/pip (python 3.11)
 [isabell@stardust ~]$



Installation
============

Get Mailman3
-------------

Install all required python modules for mailman3 with mysql and uwsgi via pip.

::

 [isabell@stardust ~]$ pip3.11 install mailman hyperkitty postorius mailman-hyperkitty whoosh pymysql mysqlclient uwsgi
 [...]
 [isabell@stardust ~]$



Create the directories required for config, run time and logs:

::

 [isabell@stardust ~]$ mkdir -p ~/{etc,logs,tmp,var}/mailman
 [isabell@stardust ~]$


Create the mysql database:

::

 [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_mailman;"
 [isabell@stardust ~]$



Get Dart Sass
-------------
Postorius and HyperKitty are build using SASS_ stylesheets which have to be compiled/decompiled before use. As U7 does not provide an SASS compiler, we need to download the *Dart Sass* standalone binary. Get the link of the latest Dart Sass binary for **linux-x64** from https://github.com/sass/dart-sass/releases, download and extract the binaries:

::

 [isabell@stardust ~]$ wget https://github.com/sass/dart-sass/releases/download/1.77.8/dart-sass-1.77.8-linux-x64.tar.gz
 [isabell@stardust ~]$ tar xzvf dart-sass-1.77.8-linux-x64.tar.gz dart-sass
 [isabell@stardust ~]$ mv dart-sass ./bin/
 [isabell@stardust ~]$ rm dart-sass-1.77.8-linux-x64.tar.gz
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


Enable uwsgi
---------------------
Create needed folders and files for uwsgi:

::

 [isabell@stardust ~]$ mkdir -p ~/etc/uwsgi/apps-enabled
 [isabell@stardust ~]$ mkdir -p ~/logs/uwsgi/
 [isabell@stardust ~]$ touch ~/logs/uwsgi/err.log
 [isabell@stardust ~]$ touch ~/logs/uwsgi/out.log
 [isabell@stardust ~]$


Create  ``~/etc/services.d/uwsgi.ini`` with the following content:

.. code-block:: ini

  [program:uwsgi]
  command=uwsgi --master --emperor %(ENV_HOME)s/etc/uwsgi/apps-enabled
  autostart=true
  autorestart=true
  stderr_logfile = %(ENV_HOME)s/logs/uwsgi/err.log
  stdout_logfile = %(ENV_HOME)s/logs/uwsgi/out.log
  stopsignal=INT
  startsecs=30

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs.



Configuration
=============


Configure Mailman Core
----------------------

At first, we need to configure the REST interface of the core component. Create the file ``~/etc/mailman/mailman.cfg``, paste and adjust the following config. The ``mta`` section contains the configuration related to sending and receiving mails. In ``webservice`` section we configure the REST API server. As our mailman installation is user-based, we need to tell mailman where to look for it's binaries and configuration using ``paths.custom``. Adapt ``var_dir``, ``bin_dir``, ``tmp_dir``, ``etc_dir`` and ``log_dir`` to the conditions on your account. A full overview of possible settings can be found in the `mailman docs schema.cfg`_.

.. code :: cfg

 [mta]
 incoming: mailman.mta.null.NullMTA
 lmtp_host: 0.0.0.0
 smtp_host: stardust.uberspace.de
 lmtp_port: 8024
 smtp_port: 587
 smtp_secure_mode: starttls
 smtp_user: forwarder@isabell.uber.space
 smtp_pass: mailpassword
 max_recipients: 100

 [webservice]
 hostname: 0.0.0.0
 port: 8001
 use_https: no
 admin_user: restadmin
 admin_pass: restpass
 api_version: 3.1

 [paths.custom]
 var_dir: /home/isabell/var/mailman
 bin_dir: /home/isabell/.local/bin
 etc_dir: /home/isabell/etc/mailman
 log_dir: /home/isabell/logs/mailman
 tmp_dir: /home/isabell/tmp/mailman

 queue_dir: $var_dir/queue
 list_data_dir: $var_dir/lists
 lock_dir: $var_dir/locks
 data_dir: $var_dir/data
 cache_dir: $var_dir/cache
 messages_dir: $var_dir/messages
 archive_dir: $var_dir/archives
 template_dir: $var_dir/templates
 pid_file: $var_dir/master.pid
 lock_file: $var_dir/master.lck

 [mailman]
 layout: custom

 class: mailman_hyperkitty.Archiver
 enable: yes
 configuration: /home/isabell/etc/mailman/mailman-hyperkitty.cfg



Configure HyperKitty
--------------------

HyperKitty is the part of mailman that takes care of archiving mail. It is configured independently and invoked by mailman core. ``~/var/etc/mailman.cfg`` points to the hyperkitty configuration file which needs to be created at the respective location ``~/etc/mailman/mailman-hyperkitty.cfg``. The following file can be adapted to your usage, make sure to generate a secret API key for your instance.

.. code :: cfg

 [general]

 base_url: http://localhost:8000/hyperkitty/
 api_key: SecretArchiverAPIKey


Daemonizing Mailman Core
------------------------

Prepair necessary log files:

::

 [isabell@stardust ~]$ touch ~/logs/mailman/daemon_err.log
 [isabell@stardust ~]$ touch ~/logs/mailman/daemon_out.log
 [isabell@stardust ~]$


As we want to make sure that Mailman is started automatically, we need to set it up as a service. Due to mailman executable not having the option to always run in foreground, we need some other means of controlling it. The process controlling all forked processes is located at ``~/.local/bin/master``. We therefore need to create the supervisord config file for mailman in ``~/etc/services.d/mailman3.ini`` as follows:

.. code :: ini

 [program:mailman3]
 directory=%(ENV_HOME)s
 command=%(ENV_HOME)s/.local/bin/master -C %(ENV_HOME)s/etc/mailman/mailman.cfg
 autostart=true
 autorestart=true
 stderr_logfile = %(ENV_HOME)s/logs/mailman/daemon_err.log
 stdout_logfile = %(ENV_HOME)s/logs/mailman/daemon_out.log
 stopsignal=TERM
 startsecs=30


.. include:: includes/supervisord.rst

Adjusting Django configuration
------------------------------

First create your own random SECRET_KEY to replace the default one:

::

 [isabell@stardust ~]$ pwgen --secure --symbols --capitalize --numerals 32 1
 i~Bzl3K!,9u0?.TETt51RmOLGK3/1jd,
 [isabell@stardust ~]$


After the REST backend has been configured, we need to configure the Django frontends for Postorius and HyperKitty. The configuration is stored in ``~/mailman-suite/settings.py``. As the default configuration contains a lot of pre-defined options, only changed or important settings are mentioned below (in order of appearance in the configuration file). To reduce the amount of lines, comments have been left out but can be found in the original file for reference.

.. code :: python

 [...]

 BASE_DIR = '/home/isabell/var/mailman'

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


 MAILMAN_REST_API_URL = 'http://isabell.local.uberspace.de:8001'
 MAILMAN_REST_API_USER = 'restadmin'
 MAILMAN_REST_API_PASS = 'restpass'
 MAILMAN_ARCHIVER_KEY = 'SecretArchiverAPIKey'
 MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')

 [...]

 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'isabell_mailman',
        'USER': 'isabell',
        'PASSWORD': '<your mysql password>',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}  # Enable utf8 4-byte encodings.
    }
 }

 [...]

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
 EMAIL_HOST_PASSWORD = 'forwarder_password'

 [...]

 COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', '/home/isabell/bin/dart-sass/sass {infile} {outfile}'),
    ('text/x-sass', '/home/isabell/bin/dart-sass/sass {infile} {outfile}'),
 )

 [...]

 Q_CLUSTER = {
     'timeout': 100,
     'retry': 200,
     'save_limit': 100,
     'orm': 'default',
     'workers': 4,
 }

 LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
     'handlers': {
         'mail_admins': {
             'level': 'ERROR',
             'filters': ['require_debug_false'],
             'class': 'django.utils.log.AdminEmailHandler'
         },
        	'file':{
             'level': 'INFO',
             'class': 'logging.handlers.WatchedFileHandler',
             'filename': '/home/isabell/logs/mailman/mailmansuite.log',  # Adapt
	     'formatter': 'verbose',
         },
  [...]

 # Comment the following lines out to test sending mail
 #if DEBUG == True:
 #   EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
 #   EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')

Setting up Django
-----------------

After we have adjusted our configuration file, we need to compile and configure the Django project and create a super user to be used as web admin:


::

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.11 manage.py migrate
 [...]
 [isabell@stardust mailman-suite]$ python3.11 manage.py collectstatic
 [...]
 [isabell@stardust mailman-suite]$ python3.11 manage.py createsuperuser
 ? Username (leave blank to use 'isabell'): isabell
 ? Email address: isabell@uber.space
 ? Password:
 ? Password (again):
 ℹ Superuser created successfully.
 [isabell@stardust mailman-suite]$

When Django is configured, we need to rename the example site to match our needs:

::

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.11 manage.py shell

 >>> from django.contrib.sites.models import Site
 >>> site = Site.objects.get(name='example.com')
 >>> site.name = 'Isabells Uberspace'
 >>> site.domain = 'isabell.uber.space'
 >>> site.save()
 >>> exit()

 [isabell@stardust mailman-suite]$


To be able to call and execute our Django app, we need to create ``~/etc/uwsgi/apps-enabled/mailman-suite.ini`` and add the following content.

.. code :: ini

 [uwsgi]
 chdir = /home/isabell/mailman-suite

 http-socket = 0.0.0.0:8000
 master = true
 process = 2
 threads = 2
 wsgi-file = wsgi.py

 # your user name
 uid = isabell
 gid = isabell

 attach-daemon = python3.11 ./manage.py qcluster

Generally, it might be necessary to reload *uwsgi* after changing the config change:

::

 [isabell@stardust ~]$ supervisorctl restart uwsgi
 uwsgi: stopped
 uwsgi: started
 [isabell@stardust ~]$

.. note::

    mailman is running on port 8000.

.. include:: includes/web-backend.rst

Additionally, serve static files using apache:

::

  [isabell@stardust ~]$ uberspace web backend set /static --apache
  Set backend for /static to apache.
  [isabell@stardust ~]$


Install cronjobs
----------------

`Mailman 3`_ offers a :manual_anchor:`cronjobs <daemons-cron.html#cron>` to perform some maintenance actions at regular intervals. To install them for your user, run ``crontab -e`` and add the following line at the end of the file.

.. code-block:: bash

 @daily /home/$USER/.local/bin/mailman digests --send


Setup fetchmail
===============

Next, we add a ``fetchmailrc`` to, e.g., ``~/etc/fetchmailrc`` This file may look like this:

.. code:: ini

  #actually we use the idle option, but this has still effects in case of an error
  set daemon 60
  set no syslog
  #has no effect with --nodetach, but ensures that we log to the same file, when we debug manually
  set logfile /home/isabell/logs/mailman/fetchmail_out.log
  #fetchmail tries to send bounce mails via the lmtp connection (i.e., to mailman3)
  #this will definitely fail, so we provide a global alternative:
  set no bouncemail
  set postmaster isabell@uber.space

  #BEGIN/END are only for readability and not part of fetchmails free form syntax
  #but this synatx is very prone to subtile errors, so a littly structure might help

  poll stardust.uberspace.de
    #BEGIN server options
    port 993
    protocol imap
    #these are specific to qmail, need to be changed, when the MDA changes
    #alternatively both might be "emulatable" with sieve later
    qvirtual isabell-
    envelope Delivered-To
    #your mailing list's domain must have one
    #of the domains in the next line as suffix:
    localdomains isabell.uber.space
    #END of server options
    #
    #BEGIN user options
    username isabell-catchallbox
    #for whatever reason 'ssl' is a user option and must come *after* username
    ssl
    idle
    password "<password_for_catchallbox>"
    no fetchall
    folder Mailman
    #this specifies mailmans *L*MTP server with port 8024:
    smtphost isabell.local.uberspace.de/8024
    #but now we tell fetchmail, that this is actually LMTP:
    lmtp
    #deduce the receiver from the envelope
    to *
    #END user options

This file still contains two options that are qmail specific. The option ``qvirtual isabell-`` tells fetchmail to strip all prefixes added by qmail and only use the remaining part as the recipient address. The ``envelope`` options tells fetchmail where to get the original envelope headers that where processed by the MDA. Eech MDA has different headers where they store this information and ``Delivered-To`` is qmail's way of passing the information. When Uberspace finally switches to some other MDA, you can drop the ``qvirtual`` option and alter ``Delivered-To``. Note that sieve filters can set addtionial headers based on the envelope, so you might also be able to emulate qmails behavior with sieve later.

Fechmail requires the fetchmailrc must have no more than -rwx------ (0700) permissions.

::

 [isabell@stardust ~]$ chmod 0700 ~/etc/fetchmailrc
 [isabell@stardust ~]$


Prepair necessary log files:

::

 [isabell@stardust ~]$ touch ~/logs/mailman/fetchmail_err.log
 [isabell@stardust ~]$ touch ~/logs/mailman/fetchmail_out.log
 [isabell@stardust ~]$

Finally, we also need an supervisord unit file for fetchmail, which we will place at ``~/etc/services.d/fetchmail.ini``:

.. code:: ini

  [program:fetchmail]
  directory=%(ENV_HOME)s
  command=/usr/bin/fetchmail --nodetach -vvv -f %(ENV_HOME)s/etc/fetchmailrc
  autostart=true
  autorestart=true
  stderr_logfile=%(ENV_HOME)s/logs/mailman/fetchmail_err.log
  stdout_logfile=%(ENV_HOME)s/logs/mailman/fetchmail_out.log
  stopsignal=TERM
  # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
  startsecs=30

Most of this is pretty much standard, but note the ``--nodetach`` option. This stops fetchmail from forking and exiting. As ``--nodetach`` disables fetchmail's logfile option, we let supervisord forward its output to the same file (except for errors). You can omit the ``-vvv`` verbosity option later, but it is very helpful for debugging fetchmail's deduction rules for adresses which can be quite surprising. Finally we start fetchmail:

.. code-block:: bash

  supervisorctl reread
  supervisorctl update
  supervisorctl start fetchmail


The error log will contain unsuccessful tries to connect to `isabell.local.uberspace.de:8024` via (its) IPv6 (address).
This error is *not* ciritcal, as a IPv4 connection will be established direcly after this failure.


Using Mailman
=============

Now we are ready to use Mailman. Simply go to ``https://isabell.uber.space`` and log in with the superuser account we created earlier. You now will get an email to confirm the account to the address you initially specified. If you do not get one, check the ``~/var/email/`` dir - you might have forgotten to disable the debug setting in ``~/mailman-suite/settings.py`` (see above). Otherwise check the logs in ``~/mailman-suite/`` and ``~/var/logs/`` for clues.

Now you can create a new list using the Postorius web UI.


Updates
=======
As Mailman 3 consists of multiple independent projects, there is no single RSS feed. To check for updates, you can use ``pip`` on your uberspace:

.. code :: bash

 [isabell@stardust ~]$ pip3.11 list --outdated
 [isabell@stardust ~]$

If there are outdated packages, update the mailman packages and their dependencies using:

.. code :: bash

 [isabell@stardust ~]$ pip3.11 install --upgrade mailman postorius hyperkitty mailman-hyperkitty whoosh uwsgi
 [isabell@stardust ~]$

.. note:: Even after ``pip --upgrade``, there might be outdated packages. This is the case if mailman's dependencies demand a specific version, e.g. `Django<2.2,>=1.11`, and is nothing to worry about.

Acknowledgements
================
This guide is based on the `official Mailman 3 installation instructions <http://docs.mailman3.org/en/latest/index.html>`_, the `official Mailman 3 documentation <https://mailman.readthedocs.io/en/latest/README.html>`_ as well as the great guides here at uberlab for :lab:`Django <guide_django.html>` and, of course, :lab:`Mailman 2 <guide_mailman.html>`. Without their previous work, this guide would have not been possible. A special thanks to `luto <https://github.com/luto>`_ for being challenging yet very helpful in overcoming some obstacles!

Tested with Django 4.2.16, HyperKitty 1.3.9, Mailman 3.3.9, Postorius 1.3.10 and uWSGI 2.0.26 on Uberspace 7.16.0.

.. _Mailman 3: http://www.mailman3.org/en/latest/
.. _Mailman: http://www.list.org/
.. _mailman-suite: https://gitlab.com/mailman/mailman-suite
.. _mailman docs schema.cfg: https://mailman.readthedocs.io/en/latest/src/mailman/config/docs/config.html#schema-cfg
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt
.. _SASS: https://sass-lang.com/


.. author_list::
