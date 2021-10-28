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

Additionally, create a :manual_anchor:`mailbox <mail-mailboxes.html#setup-a-new-mailbox>` for Mailman to use to send e-mails. In this example, we are going to use ``forwarder@isabell.uber.space``.

Installation
============

Get Mailman 3
-------------
Install Mailman 3 and its dependencies via pip.

::

 [isabell@stardust ~]$ pip3.8 install --user mailman hyperkitty postorius mailman-hyperkitty whoosh
 [...]
 [isabell@stardust ~]$

Get Dart Sass
-------------
Postorius and HyperKitty are build using SASS_ stylesheets which have to be compiled/decompiled before use. As U7 does not provide an SASS compiler, we need to download the *Dart Sass* standalone binary. Get the link of the latest Dart Sass binary for **linux-x64** from https://github.com/sass/dart-sass/releases, download and extract the binaries:

::

 [isabell@stardust ~]$ wget https://github.com/sass/dart-sass/releases/download/1.17.2/dart-sass-1.17.2-linux-x64.tar.gz
 [isabell@stardust ~]$ tar xzvf dart-sass-1.17.2-linux-x64.tar.gz dart-sass
 [isabell@stardust ~]$ mv dart-sass ./bin/
 [isabell@stardust ~]$ rm dart-sass-1.17.2-linux-x64.tar.gz
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
Install the required uwsgi package with pip.

::

 [isabell@stardust ~]$ pip3.8 install uwsgi --user
 [isabell@stardust ~]$

After that, continue with setting it up as a service.

Create  ``~/etc/services.d/uwsgi.ini`` with the following content:

.. code-block:: ini

  [program:uwsgi]
  command=uwsgi --master --emperor %(ENV_HOME)s/uwsgi/apps-enabled
  autostart=true
  autorestart=true
  stderr_logfile = ~/uwsgi/err.log
  stdout_logfile = ~/uwsgi/out.log
  stopsignal=INT

Create needed folders and files for uwsgi:

::

 [isabell@stardust ~]$ mkdir -p ~/uwsgi/apps-enabled
 [isabell@stardust ~]$ touch ~/uwsgi/err.log
 [isabell@stardust ~]$ touch ~/uwsgi/out.log
 [isabell@stardust ~]$

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs.

Get .qmail helper scripts
-------------------------
Mailman 3 uses LMTP to transfer emails locally. As :manual_anchor:`qmail <basics-home.html#qmail>` is not able to use this directly, we need to download a helper script from the mailman source:

::

 [isabell@stardust ~]$ cd bin
 [isabell@stardust bin]$ wget https://gitlab.com/mailman/mailman/raw/master/contrib/qmail-lmtp
 [isabell@stardust bin]$ chmod +x qmail-lmtp



Configuration
=============

Configure Mailman Core
----------------------

At first, we need to configure the REST interface of the core component. Create the file ``~/var/etc/mailman.cfg``, paste and adjust the following config. The ``mta`` section contains the configuration related to sending and receiving mails. As we are using :manual_anchor:`qmail <basics-home.html#qmail>`, the incoming MTA has to be set to null. In ``webservice`` section we configure the REST API server. As our mailman installation is user-based, we need to tell mailman where to look for it's binaries and configuration using ``paths.custom``. Change ``var_dir`` and ``bin_dir``. A full overview of possible settings can be found in the `mailman docs schema.cfg`_.

.. code :: cfg

 [mta]
 incoming: mailman.mta.null.NullMTA
 lmtp_host: 0.0.0.0
 smtp_host: stardust.uberspace.de
 lmtp_port: 8024
 smtp_port: 587
 smtp_user: forwarder@isabell.uber.space
 smtp_pass: mailpassword

 [webservice]
 hostname: 0.0.0.0
 port: 8001
 use_https: no
 admin_user: restadmin
 admin_pass: restpass
 api_version: 3.1

 [paths.custom]
 var_dir: /home/isabell/var
 bin_dir: /home/isabell/.local/bin

 queue_dir: $var_dir/queue
 list_data_dir: $var_dir/lists
 log_dir: $var_dir/logs
 lock_dir: $var_dir/locks
 data_dir: $var_dir/data
 cache_dir: $var_dir/cache
 etc_dir: $var_dir/etc
 messages_dir: $var_dir/messages
 archive_dir: $var_dir/archives
 template_dir: $var_dir/templates
 pid_file: $var_dir/master.pid
 lock_file: $lock_dir/master.lck

 [mailman]
 layout: custom

 [archiver.hyperkitty]
 class: mailman_hyperkitty.Archiver
 enable: yes
 configuration: /home/isabell/var/etc/mailman-hyperkitty.cfg



Configure HyperKitty
--------------------

HyperKitty is the part of mailman that takes care of archiving mail. It is configured independently and invoked by mailman core. ``~/var/etc/mailman.cfg`` points to the hyperkitty configuration file which needs to be created at the respective location ``~/var/etc/mailman-hyperkitty.cfg``. The following file can be adapted to your usage, make sure to generate a secret API key for your instance.

.. code :: cfg

 [general]

 base_url: http://localhost:8000/hyperkitty/
 api_key: SecretArchiverAPIKey


Daemonizing Mailman Core
------------------------

As we want to make sure that Mailman is started automatically, we need to set it up as a service. Due to mailman executable not having having the option to always run in foreground, we need some other means of controlling it. The process controlling all forked processes is located at ``~/.local/bin/master``. We therefore need to create the supervisord config file for mailman in ``~/etc/services.d/mailman3.ini`` as follows:

.. code :: ini

 [program:mailman3]
 enviroment=MAILMAN_VAR_DIR="%(ENV_HOME)s/var"
 directory=%(ENV_HOME)s
 command=%(ENV_HOME)s/.local/bin/master -C %(ENV_HOME)s/var/etc/mailman.cfg
 autostart=true
 autorestart=true
 stderr_logfile = ~/var/logs/daemon_err.log
 stdout_logfile = ~/var/logs/daemon_out.log
 stopsignal=TERM

Afterwards, create necessary folders and files:

::

 [isabell@stardust ~]$ mkdir -p ~/var/logs
 [isabell@stardust ~]$ touch ~/var/logs/daemon_err.log
 [isabell@stardust ~]$ touch ~/var/logs/daemon_out.log
 [isabell@stardust ~]$

.. include:: includes/supervisord.rst

Adjusting Django configuration
------------------------------

After the REST backend has been configured, we need to configure the Django frontends for Postorius and HyperKitty. The configuration is stored in ``~/mailman-suite/settings.py``. As the default configuration contains a lot of pre-defined options, only changed or important settings are mentioned below (in order of appearance in the configuration file). To reduce the amount of lines, comments have been left out but can be found in the original file for reference.

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

 MAILMAN_REST_API_URL = 'http://isabell.local.uberspace.de:8001'
 MAILMAN_REST_API_USER = 'restadmin'
 MAILMAN_REST_API_PASS = 'restpass'
 MAILMAN_ARCHIVER_KEY = 'SecretArchiverAPIKey'
 MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')

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
 EMAIL_HOST_PASSWORD = 'mailpassword'

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

 # Comment the following lines out to test sending mail
 #if DEBUG == True:
 #   EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
 #   EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')

Setting up Django
-----------------

After we have adjusted our configuration file, we need to compile and configure the Django project and create a super user to be used as web admin:

.. note:: In case you get an error message when like ``django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required (found 3.7.17).``, when running those `manage.py` commands, then you need a newer version of the sqlite library. Install ``pysqlite3-binary`` and create a symlink in order to override ``sqlite3``:

 .. code :: bash

  [isabell@stardust ~]$ pip3.8 install --user pysqlite3-binary
  [...]
  [isabell@stardust ~]$ ln -s pysqlite3 ~/.local/lib/python3.8/site-packages/sqlite3
  [isabell@stardust ~]$

 Now add this ``~/mailman-suite/settings.py`` in order to have use that version of the ``sqlite3`` instead of the built-in one.

 .. code :: python

  import sys
  sys.path = ['/home/isabell/.local/lib/python3.8/site-packages'] + sys.path

::

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.8 manage.py migrate
 [...]
 [isabell@stardust mailman-suite]$ python3.8 manage.py collectstatic
 [...]
 [isabell@stardust mailman-suite]$ python3.8 manage.py createsuperuser
 ? Username (leave blank to use 'isabell'): isabell
 ? Email address: isabell@uber.space
 ? Password:
 ? Password (again):
 ℹ Superuser created successfully.
 [isabell@stardust mailman-suite]$

When Django is configured, we need to rename the example site to match our needs:

::

 [isabell@stardust ~]$ cd mailman-suite
 [isabell@stardust mailman-suite]$ python3.8 manage.py shell

 >>> from django.contrib.sites.models import Site
 >>> site = Site.objects.get(name='example.com')
 >>> site.name = 'Isabells Uberspace'
 >>> site.domain = 'isabell.uber.space'
 >>> site.save()
 >>> exit()

 [isabell@stardust mailman-suite]$

To be able to call and execute our Django app, we need to create ``~/uwsgi/apps-enabled/mailman-suite.ini`` and add the following content.

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

 attach-daemon = python3.8 ./manage.py qcluster

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

Setting up .qmail
-----------------------------

Because Mailman_ doesn't handle our .qmail-configuration automatically, we need to adjust  ``~/.qmail-default`` to forward all incoming mails to our LMTP handler. Update it with the following content. Make sure that ``8024`` is the LMTP port your :lab_anchor:`Mailman Core <guide_mailman-3.html#configure-mailman-core>` is listening on and change your username twice:

.. code :: bash

 |/home/isabell/bin/qmail-lmtp 8024 1 isabell.local.uberspace.de

.. warning:: This will forward **all** emails without an individually specified ``.qmail`` file to Mailman, possibly resulting in the loss of emails!

To enable mail delivery for non-mailman addresses (such as ``info@isabell.uber.space``) you need to create individual ``.qmail-emailadress`` files such as ``.qmail-info``. If you just want to forward incoming mail to another email address, simply write one email address per line (see example below):

.. code :: bash

 isabell@example.com

If you want to use an :manual:`IMAP mailbox<mail-mailboxes>` on your uberspace, use the following as content of your .qmail file:

.. code :: bash

 |/usr/bin/vdeliver

.. note:: In case you want to keep the default configuration, do not change ``~/.qmail-default`` and create additional .qmail-files such as ``~/.qmail-listname`` and ``~/.qmail-listname-default`` containing ``|/home/isabell/bin/qmail-lmtp 8024 1 isabell.local.uberspace.de`` to forward only ``listname@isabell.uber.space`` and the related email commands (e.g. ``listname-subscribe@isabell.uber.space``) to mailman. **This needs to be done manually for every list created in the web interface!**

Install cronjobs
----------------

`Mailman 3`_ offers a :manual_anchor:`cronjobs <daemons-cron.html#cron>` to perform some maintenance actions at regular intervals. To install them for your user, run ``crontab -e`` and add the following line at the end of the file.

.. code-block:: bash

 @daily /home/$USER/.local/bin/mailman digests --send


Using Mailman
=============

Now we are ready to use Mailman. Simply go to ``https://isabell.uber.space`` and log in with the superuser account we created earlier. You now will get an email to confirm the account to the address you initially specified. If you do not get one, check the ``~/var/email/`` dir - you might have forgotten to disable the debug setting in ``~/mailman-suite/settings.py`` (see above). Otherwise check the logs in ``~/mailman-suite/`` and ``~/var/logs/`` for clues.

Now you can create a new list using the Postorius web UI.

.. warning:: Don't forget to create the .qmail-aliases if you chose not to use ``.qmail-default``!

Updates
=======
As Mailman 3 consists of multiple independent projects, there is no single RSS feed. To check for updates, you can use ``pip`` on your uberspace:

.. code :: bash

 [isabell@stardust ~]$ pip3.8 list --outdated --user
 [isabell@stardust ~]$

If there are outdated packages, update the mailman packages and their dependencies using:

.. code :: bash

 [isabell@stardust ~]$ pip3.8 install --user --upgrade mailman postorius hyperkitty mailman-hyperkitty whoosh uwsgi
 [isabell@stardust ~]$

.. note:: Even after ``pip --upgrade``, there might be outdated packages. This is the case if mailman's dependencies demand a specific version, e.g. `Django<2.2,>=1.11`, and is nothing to worry about.

Acknowledgements
================
This guide is based on the `official Mailman 3 installation instructions <http://docs.mailman3.org/en/latest/index.html>`_, the `official Mailman 3 documentation <https://mailman.readthedocs.io/en/latest/README.html>`_ as well as the great guides here at uberlab for :lab:`Django <guide_django.html>` and, of course, :lab:`Mailman 2 <guide_mailman.html>`. Without their previous work, this guide would have not been possible. A special thanks to `luto <https://github.com/luto>`_ for being challenging yet very helpful in overcoming some obstacles!

Tested with Django 2.1.8, HyperKitty 1.2.2, Mailman 3.2.2, Postorius 1.2.4 and uWSGI 2.0.18 on Uberspace 7.2.8.2.

.. _Mailman 3: http://www.mailman3.org/en/latest/
.. _Mailman: http://www.list.org/
.. _mailman-suite: https://gitlab.com/mailman/mailman-suite
.. _mailman docs schema.cfg: https://mailman.readthedocs.io/en/latest/src/mailman/config/docs/config.html#schema-cfg
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt
.. _SASS: https://sass-lang.com/


.. author_list::
