.. highlight:: console

.. author:: ezra <ezra@posteo.de>
.. author:: luto <m@luto.at>
.. author:: chriskbach <https://github.com/chriskbach/>

.. tag:: lang-python
.. tag:: django
.. tag:: ticketing
.. tag:: web
.. tag:: audience-business

.. sidebar:: About

  .. image:: _static/images/pretix.svg
      :align: center

##########
pretix
##########

.. tag_list::

pretix_ is an open source ticketing solution. It is written in Django_ and can be highly customized for the process of ticket sales.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here

  * https://pretix.eu/about/en/terms

Prerequisites
=============

Since `release 2023.6.0 <https://pretix.eu/about/en/blog/20230627-release-2023-6/>`_ pretix no longer supports MySQL or MariaDB, instead PostgreSQL is required. For setting up PostgreSQL follow this :lab:`UberLab guide <guide_postgresql>`.

As recommended in the Section `Database and user management <https://lab.uberspace.de/guide_postgresql/#database-and-user-management>`_ please set up a user ``isabell_pretix`` and database ``isabell_pretix_db`` for this project.

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

.. note:: pretix uses :lab:`Redis <guide_redis>` to manage background tasks, so it installs it using the default configuration.

Installation
============

Download & Install
------------------

Install pretix using the python package manager. Be sure to replace the pseudo branch number ``release/6.6.x`` here with the latest release branch from the Github repository at https://github.com/pretix/pretix/branches/active:

::

 [isabell@stardust ~]$ pip3.11 install pretix==4.20.0 gunicorn --user
 [...]
  Running setup.py install for static3 ... done
  Running setup.py install for slimit ... done
  Running setup.py install for future ... done
  Running setup.py install for dj-static ... done
  Running setup.py install for vobject ... done
  Running setup.py install for python-u2flib-server ... done
  Running setup.py install for jwcrypto ... done
  Running setup.py install for django-jquery-js ... done
  Running setup.py install for paypalrestsdk ... done
  Running setup.py install for paypal-checkout-serversdk ... done
 [...]
 Successfully installed BeautifulSoup4-4.12.2 Django-3.2.19 Pillow-9.5.0 PyJWT-2.6.0 aiohttp-3.8.4 aiosignal-1.3.1 amqp-5.1.1 arabic-reshaper-3.0.0 asgiref-3.7.2 async-timeout-4.0.2 attrs-23.1.0 babel-2.12.1 billiard-3.6.4.0 bleach-5.0.1 cbor2-5.4.6 [...]
 [isabell@stardust ~]$

Also, you need to create an extra data folder:

::

 [isabell@stardust ~]$ mkdir ~/pretix_data
 [isabell@stardust ~]$

Configuration
-------------
Now you need to set up the configuration, create the file ``~/.pretix.cfg`` and insert the following content:

.. warning:: Be sure, to replace all values with correct data of your own Uberspace account!

.. code-block:: ini
  :emphasize-lines: 2,3,5,9,10,11,15,16,17,18

    [pretix]
    instance_name=Isabells pretix
    url=https://isabell.uber.space
    currency=EUR
    datadir=/home/isabell/pretix_data
    trust_x_forwarded_proto=on

    [database]
    backend=postgresql
    name=isabell_pretix_db
    user=isabell_pretix
    password=MySuperSecretPassword
    host=localhost
    port=5432

    [celery]
    broker=redis+socket:///home/isabell/.redis/sock
    backend=redis+socket:///home/isabell/.redis/sock

    [mail]
    from=isabell@uber.space
    host=stardust.uberspace.de
    user=isabell@uber.space
    password=MySuperSecretPassword
    port=587
    tls=on


Initialize database
-------------------
Initialize the pretix_ database tables and generate the static files:

::

 [isabell@stardust ~]$ python3.11 -m pretix migrate
 Operations to perform:
  Apply all migrations: auth, badges, banktransfer, contenttypes, oauth2_provider, otp_static, otp_totp, paypal, pretixapi, pretixbase, pretixdroid, pretixhelpers, pretixmultidomain, sendmail, sessions, stripe, ticketoutputpdf
  Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0001_initial... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
 [...]

::

 [isabell@stardust ~]$ python3.11 -m pretix rebuild
 [...]
 File “/home/jupretix/.local/lib/python3.11/site-packages/django/contrib/sites/locale/be/LC_MESSAGES/django.po” is already compiled and up to date.
 File “/home/jupretix/.local/lib/python3.11/site-packages/django/contrib/sites/locale/id/LC_MESSAGES/django.po” is already compiled and up to date.
 File “/home/jupretix/.local/lib/python3.11/site-packages/django/contrib/sites/locale/it/LC_MESSAGES/django.po” is already compiled and up to date.
 processing file django.po in /home/jupretix/.local/lib/python3.11/site-packages/django/contrib/sites/locale/sl/LC_MESSAGES
 processing language es
 processing language tr
 processing language uk

 954 static files copied to '/home/jupretix/.local/lib/python3.11/site-packages/pretix/static.dist', 970 post-processed.
 Compressing... done
 Compressed 28 block(s) from 547 template(s) for 1 context(s).
 [isabell@stardust ~]$

Web Backend
-----------

.. note::

    Pretix is running on port 9000.

.. include:: includes/web-backend.rst

Service
-------

Finally, you should set up a service that keeps pretix_ alive while you are gone. Therefor create the file ``~/etc/services.d/pretix.ini`` with the following content:

.. code-block:: ini

 [program:pretix]
 command=gunicorn --reload --preload --bind 0.0.0.0:9000 --workers 2 pretix.wsgi --name pretix --max-requests 1200 --max-requests-jitter 50
 directory=%(ENV_HOME)s/pretix_data
 autostart=true
 autorestart=true
 stopsignal=INT

 [program:pretix_worker]
 command=celery -A pretix.celery_app worker -l info --concurrency 1
 directory=%(ENV_HOME)s/pretix_data
 autostart=true
 autorestart=true
 stopsignal=INT

.. include:: includes/supervisord.rst

If the two services are not in state RUNNING, check your configuration.

Cronjob
-------

Create a new cronjob using ``crontab -e``:

::

  18,48 * * * * cd ~/pretix_data && python3.11 -m pretix runperiodic

Accessing pretix
----------------

Now point your Browser to your installation URL ``https://isabell.uber.space``. You will find the administration panel at ``https://isabell.uber.space/control``.

Use ``admin@localhost`` as username and ``admin`` as password for your first login. You should change this password immediately after login!


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, install the new version like so:

::

 [isabell@stardust ~]$ pip3.11 install pretix==4.16.0
 [isabell@stardust ~]$

Then re-run the Initialize database steps and restart the service like so:

::

 [isabell@stardust ~]$ python3.11 -m pretix migrate
 [isabell@stardust ~]$ python3.11 -m pretix rebuild
 [isabell@stardust ~]$ supervisorctl restart pretix
 [isabell@stardust ~]$

.. _pretix: https://pretix.eu/
.. _Django:  https://www.djangoproject.com/
.. _Gunicorn: https://gunicorn.org/
.. _Github: https://github.com/pretix/pretix
.. _feed: https://github.com/pretix/pretix/releases.atom
.. _bullshit: https://bullenscheisse.de/2018/pretix-auf-einem-uberspace/

----

Tested with pretix 4.20.0 and Uberspace 7.15.1

.. author_list::

This guide was written with the help of a former text on "bullshit_", thanks to Nathan.
