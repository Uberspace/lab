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

`Mailman`_ is free software for managing electronic mail discussion and e-newsletter lists. Mailman is integrated with
the web, making it easy for users to manage their accounts and for list owners to administer their lists. Mailman
supports built-in archiving, automatic bounce processing, content filtering, digest delivery, spam filters, and more.

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

Domains
-------

Your URL needs to be setup for web and mail:

::

    [isabell@stardust ~]$ uberspace web domain list
    isabell.uber.space
    [isabell@stardust ~]$ uberspace mail domain list
    isabell.uber.space
    [isabell@stardust ~]$

Mailbox
-------

Create a :manual_anchor:`mailbox <mail-mailboxes.html#setup-a-new-mailbox>` just for Mailman to use to send
e-mails. In this example, we are going to use ``mailman3@isabell.uber.space``.


Set up Mailman Core
===================

Mailman Core is the component that processes incoming mails and sends out mails to the list members. You can use cli
commands to set up lists and manage them.

Get Mailman 3
-------------
Install Mailman 3 and its dependencies via pip.

::

    [isabell@stardust ~]$ pip3.8 install --user mailman
    [...]
    [isabell@stardust ~]$

Because of some package dependency issues
(see `this comment <https://github.com/Uberspace/lab/issues/1553#issuecomment-1691626761>`_ for more information)
we have to pin some package versions:

::

    [isabell@stardust ~]$ pip3.8 install --user "urllib3<2" "flufl.lock<8" "flufl.i18n<5" "importlib_resources<6.0"
    [...]
    [isabell@stardust ~]$


Configure Mailman Core
----------------------

Create the configuration file ``~/etc/mailman-core.cfg`` with the following content:

.. note::
    * Replace ``isabell`` and  ``stardust`` with your user- and hostname.
    * Set the correct password ``<mailbox-password>`` for the mailbox you created before.
    * Create a new random password for ``<rest-admin-password>``, you will need this again later.

.. code :: cfg

    [mta]
    incoming: mailman.mta.null.NullMTA
    lmtp_host: 0.0.0.0
    smtp_host: stardust.uberspace.de
    lmtp_port: 8024
    smtp_port: 587
    smtp_secure_mode: starttls
    smtp_user: mailman3@isabell.uber.space
    smtp_pass: <mailbox-password>
    max_recipients: 100

    [webservice]
    hostname: 0.0.0.0
    port: 8001
    use_https: no
    admin_user: restadmin
    admin_pass: <rest-admin-password>
    api_version: 3.1

    [paths.custom]
    etc_dir: /home/isabell/etc
    var_dir: /home/isabell/var
    bin_dir: /home/isabell/.local/bin

    queue_dir: $var_dir/queue
    list_data_dir: $var_dir/lists
    log_dir: $var_dir/logs
    data_dir: $var_dir/data
    cache_dir: $var_dir/cache
    messages_dir: $var_dir/messages
    archive_dir: $var_dir/archives
    template_dir: $var_dir/templates
    pid_file: $var_dir/master.pid
    lock_dir: $var_dir/locks
    lock_file: $lock_dir/master.lck

    [mailman]
    layout: custom

    [archiver.hyperkitty]
    class: mailman_hyperkitty.Archiver
    enable: yes
    configuration: $etc_dir/mailman-hyperkitty.cfg

.. note::
    The ``mta`` section contains the configuration related to sending and receiving mails. As we are using
    :manual_anchor:`qmail <basics-home.html#qmail>`, the incoming MTA has to be set to null.

    In ``webservice`` section we configure the REST API server. Because we install Mailman in a userspace,
    we need to tell it where to look for it's binaries and configuration using ``paths.custom``.

    A full overview of possible settings can be found in the `mailman docs schema.cfg`_.


Setting up .qmail
------------------

Mailman 3 uses LMTP to transfer emails locally. As :manual_anchor:`qmail <basics-home.html#qmail>` is not able to use
this directly, we need to download a helper script from the mailman source:

::

    [isabell@stardust ~]$ cd bin
    [isabell@stardust bin]$ wget https://gitlab.com/mailman/mailman/raw/master/contrib/qmail-lmtp
    [isabell@stardust bin]$ chmod +x qmail-lmtp
    [isabell@stardust bin]$

We then need to to forward incomind mails to the LMTP handler, replace the content of the main .qmail file
``~/.qmail-default`` with the following:

.. code :: bash

 |/home/isabell/bin/qmail-lmtp 8024 1 isabell.local.uberspace.de

(You need to replace ``isabell`` with your username twice.)

.. warning::
    This will forward **all** incoming emails of this Uberspace to Mailman, possibly resulting in the loss of
    other emails. To use individual mailaddresses on the same Uberspace (not recommended) set up individual
    ``.qmail-MAILBOXNAME`` files.

Daemonizing Mailman Core
------------------------

As we want to make sure that Mailman is started automatically, we need to set it up as a service, create a service
file ``~/etc/services.d/mailman-core.ini`` with the following content:

.. code :: ini

    [program:mailman-core]
    directory=%(ENV_HOME)s
    command=%(ENV_HOME)s/.local/bin/master -C %(ENV_HOME)s/etc/mailman-core.cfg
    autostart=true
    autorestart=true
    stderr_logfile = ~/logs/mailman-core_error.log
    stdout_logfile = ~/logs/mailman-core_stdout.log
    stopsignal=TERM
    startsecs=30

.. note ::

    Due to mailman executable not having the option to always run in foreground, we need some other means of
    controlling it. The process which we use here to control all forked processes is located at
    ``~/.local/bin/master``.

.. include:: includes/supervisord.rst

Using Mailman Core
------------------

You can now use the Mailman Core via CLI commands:

::

    [isabell@stardust ~]$ mailman status
    GNU Mailman is running (master pid: 1026)
    [isabell@stardust ~]$ mailman create test@isabell.uber.space -d
    Created mailing list: test@isabell.uber.space
    [isabell@stardust ~]$ mailman lists
    1 matching mailing lists found:
    test@isabell.uber.space

The commands must be executed in ``/home/isabell`` as working directory, you can get a list of all commands with
``mailman help``.


Add cronjob for daily digests
-----------------------------

Mailman offers a command to create daily digests that can be subscripted by mailing lists members.
Add this to your :manual_anchor:`crontab <daemons-cron.html#cron>` if you want to use the feature:

.. code-block:: bash

 @daily /home/$USER/.local/bin/mailman digests --send

.. tip::
    By now you have successfully installed the Mailman Core and can use it via the CLI, the upcoming part of the
    guide will show how to set up an additional web frontend.


Set up Mailman web
==================

In addition to control Mailman over CLI command there is also a powerful web frontend provided with the components of
``postorius`` and ``hyperkitty``.


Get postorius and hyperkitty
----------------------------
Install dependencies via pip:

::

    [isabell@stardust ~]$ pip3.8 install --user hyperkitty postorius mailman-hyperkitty uwsgi whoosh
    [...]
    [isabell@stardust ~]$


Get Dart Sass
-------------
Postorius and HyperKitty are build using SASS_ stylesheets which have to be compiled/decompiled before use. As U7
does not provide an SASS compiler, we need to download the *Dart-Sass* standalone binary.

Get the url of the latest Dart-Sass binary for **linux-x64** from the
`release page <https://github.com/sass/dart-sass/releases,>`_, download and extract the binaries:

::

 [isabell@stardust ~]$ wget https://github.com/sass/dart-sass/releases/download/1.17.2/dart-sass-1.17.2-linux-x64.tar.gz
 [isabell@stardust ~]$ tar xzvf dart-sass-1.17.2-linux-x64.tar.gz dart-sass
 [isabell@stardust ~]$ mv dart-sass ./bin/
 [isabell@stardust ~]$ rm dart-sass-1.17.2-linux-x64.tar.gz
 [isabell@stardust ~]$


Configure HyperKitty
--------------------

HyperKitty is the part of Mailman that takes care of archiving mail and provides a web frontend. It is invoked
by Mailman Core and used by the mailman-suite.

To configure HyperKitty, create the file ``~/etc/mailman-hyperkitty.cfg`` and add the following content:

.. code :: cfg

 [general]
 base_url: http://localhost:8000/hyperkitty/
 api_key: <hyperkitty-api-key>

Generate a random secure string and replace ``<hyperkitty-api-key>`` with it, you will need this key again later.


Get the mailman-suite
---------------------
To have a starting point for configuration, we use the Django mailman-suite_ example provided by the Mailman team and move
it to a path where we can access it easily.

::

 [isabell@stardust ~]$ git clone https://gitlab.com/mailman/mailman-suite.git
 [isabell@stardust ~]$ mv mailman-suite/mailman-suite_project/ .
 [isabell@stardust ~]$ rm -rf mailman-suite
 [isabell@stardust ~]$ mv mailman-suite_project/ mailman-suite
 [isabell@stardust ~]$


Configure the mailman-suite
---------------------------

As the mailman-suite is a Django project, we first need to adapt some custom configurations. Create a file
``~/mailman-suite/settings_local.py`` with the following content:

.. note::
    * Replace ``isabell`` with your username multiple times.
    * Replace ``stardust.uberspace.de`` with your hostname.
    * Replace ``<mailbox-password>`` with the one you have set up the mailman3 mailbox with.
    * Replace ``<rest-admin-password>`` with the one you created in the Mailman Core config.
    * Replace ``<hyperkitty-api-key>`` with the key you created before for HyperKitty.

.. code :: python

    BASE_DIR = '/home/isabell/var/'
    SECRET_KEY = '{{ django_secret_key }}'

    DEBUG = False

    ADMINS = (
         ('admin', 'isabell@uber.space'),
    )

    ALLOWED_HOSTS = [
        'localhost',  # Archiving API from Mailman, keep it.
        'isabell.uber.space', # Add your custom domain here if you have one
    ]

    MAILMAN_REST_API_URL = 'http://isabell.local.uberspace.de:8001'
    MAILMAN_REST_API_USER = 'restadmin'
    MAILMAN_REST_API_PASS = '<rest-admin-password>'
    MAILMAN_ARCHIVER_KEY = '<hyperkitty-api-key>'
    MAILMAN_ARCHIVER_FROM = ('127.0.0.1', '::1')

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Uncomment
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SCHEME', 'https') # Uncomment

    STATIC_ROOT = '/home/isabell/html/static/'

    DEFAULT_FROM_EMAIL = 'mailbox3@isabell.uber.space'
    SERVER_EMAIL = 'isabell@uber.space'

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'stardust.uberspace.de'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'mailman3@isabell.uber.space'
    EMAIL_HOST_PASSWORD = '<mailbox-password>'

    COMPRESS_PRECOMPILERS = (
       ('text/less', 'lessc {infile} {outfile}'),
       ('text/x-scss', '/home/isabell/bin/dart-sass/sass {infile} {outfile}'),
       ('text/x-sass', '/home/isabell/bin/dart-sass/sass {infile} {outfile}'),
    )

    Q_CLUSTER = {
        'timeout': 100,
        'retry': 200,
        'save_limit': 100,
        'orm': 'default',
        'workers': 4,
    }

Setting up the mailman-suite Django framework
---------------------------------------------

First migrate the database:

::

    [isabell@stardust ~]$ cd ~/mailman-suite
    [isabell@stardust mailman-suite]$ python3.8 manage.py migrate
    [...]
    [isabell@stardust mailman-suite]$

Then collect the static files to ``~/html/static``

::

    [isabell@stardust ~]$ cd ~/mailman-suite
    [isabell@stardust mailman-suite]$ python3.8 manage.py collectstatic
    [...]
    [isabell@stardust mailman-suite]$

Then create a superuser that can be used as first login in the frontend:

::

    [isabell@stardust ~]$ cd ~/mailman-suite
    [isabell@stardust mailman-suite]$ python3.8 manage.py createsuperuser
    ? Username (leave blank to use 'isabell'): isabell
    ? Email address: isabell@uber.space
    ? Password:
    ? Password (again):
    ℹ Superuser created successfully.
    [isabell@stardust mailman-suite]$

When Django is configured, we need to rename the example site to match our needs:

::

    [isabell@stardust ~]$ cd ~/mailman-suite
    [isabell@stardust mailman-suite]$ python3.8 manage.py shell

     >>> from django.contrib.sites.models import Site
     >>> site = Site.objects.get(name='example.com')
     >>> site.name = 'Isabells Mailinglists'
     >>> site.domain = 'isabell.uber.space'
     >>> site.save()
     >>> exit()


Daemonizing the mailman-suite
-----------------------------
We will use ``uwsgi`` as a server for the Django application. First create the apps folder:

::

    [isabell@stardust ~]$ mkdir -p ~/etc/uwsgi/apps-enabled
    [isabell@stardust ~]$

Then add mailman-suite to ``uwsgi``, therefore create the config file
``~/etc/uwsgi/apps-enabled/mailman-suite.ini`` and add the following content:

.. code :: ini

 [uwsgi]
 chdir = /home/isabell/mailman-suite

 http-socket = 0.0.0.0:8000
 master = true
 process = 2
 threads = 2
 wsgi-file = wsgi.py
 startsecs=30

 # your user name
 uid = isabell
 gid = isabell

 attach-daemon = python3.8 ./manage.py qcluster

Now we create a service for ``uwsgi`` to keep it up and running, create  ``~/etc/services.d/mailman-suite.ini``
with the following content:

.. code-block:: ini

    [program:mailman-suite]
    command=uwsgi --master --emperor %(ENV_HOME)s/etc/uwsgi/apps-enabled
    autostart=true
    autorestart=true
    stderr_logfile = ~/logs/mailman-suite_error.log
    stdout_logfile = ~/logs/mailman-suite_stdout.log
    stopsignal=INT
    startsecs=30

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs.


Add web backends for the mailman-suite
--------------------------------------

.. note::

    The mailman-suite is running on port **8000**

.. include:: includes/web-backend.rst

Additionally, serve static files using apache:

::

  [isabell@stardust ~]$ uberspace web backend set /static --apache
  Set backend for /static to apache.
  [isabell@stardust ~]$


Using Mailman web
=================

Now we are ready to use the Mailman web frontend. Simply go to ``https://isabell.uber.space`` and log in with the
superuser account we created earlier.

You now will get an email to confirm the account to the address you initially specified for the account.
You can then create and manage mailing lists with the Postorius web frontend.

.. note::
    With your first new list you will need to set up a mailserver domain if you have not done yet
    via the Mailman CLI.


Updates
=======
As Mailman 3 consists of multiple independent projects, there is no single RSS feed. To check for updates, you can use ``pip`` on your uberspace:

::

 [isabell@stardust ~]$ pip3.8 list --outdated --user
 [isabell@stardust ~]$

If there are outdated packages, update the mailman packages and their dependencies using:

::

 [isabell@stardust ~]$ pip3.8 install --user --upgrade mailman postorius hyperkitty mailman-hyperkitty whoosh uwsgi
 [isabell@stardust ~]$

.. note:: Even after ``pip --upgrade``, there might be outdated packages. This is the case if mailman's dependencies demand a specific version, e.g. `Django<2.2,>=1.11`, and is nothing to worry about.

Acknowledgements
================

.. note::
    This guide is based on the `official Mailman 3 installation instructions <http://docs.mailman3.org/en/latest/index.html>`_, the `official Mailman 3 documentation <https://mailman.readthedocs.io/en/latest/README.html>`_ as well as the great guides here at uberlab for :lab:`Django <guide_django.html>` and, of course, :lab:`Mailman 2 <guide_mailman.html>`. Without their previous work, this guide would have not been possible. A special thanks to `luto <https://github.com/luto>`_ for being challenging yet very helpful in overcoming some obstacles!

Tested with Django 2.1.8, HyperKitty 1.2.2, Mailman 3.2.2, Postorius 1.2.4 and uWSGI 2.0.18 on Uberspace 7.2.8.2.

.. _Mailman 3: http://www.mailman3.org/en/latest/
.. _Mailman: http://www.list.org/
.. _mailman-suite: https://gitlab.com/mailman/mailman-suite
.. _mailman docs schema.cfg: https://mailman.readthedocs.io/en/latest/src/mailman/config/docs/config.html#schema-cfg
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt
.. _SASS: https://sass-lang.com/


.. author_list::
