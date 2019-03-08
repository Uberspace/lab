.. highlight:: console

.. author:: Christian <christian@kuntzsch.me>

.. sidebar:: About

  .. image:: _static/images/babybuddy.png
      :align: center

##########
Baby Buddy
##########

`Baby Buddy`_ is an open source activity management system for your infant child. It is designed to keep track of sleep, feedings, diaper changes and tummy time "[...] to learn about and predict baby's needs without (as much) guess work".
It is written in :manual:`Python <lang-python>` and based on the popular :lab:`Django-Framework <guide_django>`.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager :manual_anchor:`pip <lang-python.html#pip>`
  * :lab:`Django-Framework <guide_django>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://github.com/cdubz/babybuddy/blob/master/LICENSE

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

You need `pipenv`_, a package manager/virtual environment tool for Python, so install that:

::

 [isabell@stardust ~]$ pip3.6 install pipenv --user

.. include:: includes/install-uwsgi.rst

Installation
============

Step 1
------
During the installation process, you want to use Python in version 3.6. Set an alias for that:

::

 [isabell@stardust ~]$ alias python=python3.6
 [isabell@stardust ~]$ Python --version
 Python 3.6.7
 [isabell@stardust ~]$

Step 2
------
Baby Buddy will store its data in a :manual:`MySQL <database-mysql>` database. Create one with the name ``<username>_babybuddy``.

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_babybuddy DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
 [isabell@stardust ~]$

Step 3
------
Create two folders, one for the source code and one for the application's data.

::

 [isabell@stardust ~]$ mkdir -p ~/babybuddy/public ~/babybuddy/data/media
 [isabell@stardust ~]$

Clone the Baby Buddy source code from Github into the first folder.

::

 [isabell@stardust ~]$ git clone https://github.com/cdubz/babybuddy.git ~/babybuddy/public
 [...]
 remote: Total 4593 (delta 27), reused 80 (delta 19), pack-reused 4477
 Receiving objects: 100% (4593/4593), 8.15 MiB | 3.33 MiB/s, done.
 Resolving deltas: 100% (2734/2734), done.
 [isabell@stardust ~]$

Step 4
------
Install all the requirements. Since we are working with Python 3, we need to use a flag:

  * ``--three``: Use Python 3 when creating virtualenv

::

 [isabell@stardust ~]$ cd ~/babybuddy/public/
 [isabell@stardust ~/babybuddy/public]$ pipenv install --three
 [...]
   🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 39/39 — 00:00:54
 To activate this project's virtualenv, run pipenv shell.
 Alternatively, run a command inside the virtualenv with pipenv run.
 [isabell@stardust ~/babybuddy/public]$

Also, install the package ``mysqlclient``:

::

 [isabell@stardust ~/babybuddy/public]$ pipenv install mysqlclient --three
 [...]
   🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 40/40 — 00:00:02
 To activate this project's virtualenv, run pipenv shell.
 Alternatively, run a command inside the virtualenv with pipenv run.
 [isabell@stardust ~/babybuddy/public]$ cd
 [isabell@stardust ~]$

Step 5
------
Copy the template configuration file and adapt it based on the following example.

::

 [isabell@stardust ~]$ cp ~/babybuddy/public/babybuddy/settings/production.example.py ~/babybuddy/public/babybuddy/settings/production.py
 [isabell@stardust ~]$

.. warning:: Replace ``<secretkey>`` with a random sequence of characters!
.. warning:: Replace ``<host>`` with your host!
.. warning:: Replace ``<username>`` with your username!
.. warning:: Replace ``<databasepassword>`` with your database password!

.. code-block:: python
  :emphasize-lines: 6,8,16,17,18

   from .base import *
   
   # Production settings
   # See babybuddy.settings.base for additional settings information.
   
   SECRET_KEY = '<secretkey>'
   
   ALLOWED_HOSTS = ['<host>']
   
   # Database
   # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
   
   DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<username>_babybuddy',
        'USER': '<username>',
        'PASSWORD': '<databasepassword>',
        'HOST': '127.0.0.1',
        'PORT': '3306',
      }
   }
   
   # Static files
   
   MEDIA_ROOT = os.path.join(BASE_DIR, '../data/media')

To work correctly with the Uberspace Proxy, you need to add this option to the end of the file:

.. code-block:: python

   USE_X_FORWARDED_HOST = True

In our example, the file ``~/babybuddy/public/babybuddy/settings/production.py`` should look like this:

.. code-block:: python

   from .base import *

   # Production settings
   # See babybuddy.settings.base for additional settings information.

   SECRET_KEY = 'MyRandomSecretKey'

   ALLOWED_HOSTS = ['isabell.uber.space']

   # Database
   # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

   DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'isabell_babybuddy',
        'USER': 'isabell',
        'PASSWORD': 'MySuperSecretPassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
      }
   }

   # Static files

   MEDIA_ROOT = os.path.join(BASE_DIR, '../data/media')

   USE_X_FORWARDED_HOST = True

Step 6
------

Enter the virtual environment, initialize the database tables and exit the virtual environemt again:

::

 [isabell@stardust ~]$ cd ~/babybuddy/public/
 [isabell@stardust ~/babybuddy/public]$ pipenv shell
 Launching subshell in virtual environment…
  . /home/isabell/.local/share/virtualenvs/public-xxxxxx/bin/activate
 [isabell@stardust ~/babybuddy/public]$ export DJANGO_SETTINGS_MODULE=babybuddy.settings.production
 [isabell@stardust ~/babybuddy/public]$ python manage.py migrate
 [...]
 [isabell@stardust ~/babybuddy/public]$ exit && cd
 [isabell@stardust ~]$

Configuration
=============

Configure port
--------------

.. include:: includes/generate-port.rst

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup service
-------------

To deploy your application with uwsgi, create a file at ``~/uwsgi/apps-enabled/babybuddy.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! (4 times)
.. warning:: Replace ``<yourport>`` with your port!

.. note:: Find the location of the pipenv virtual environment for the ``virtualenv`` parameter with the following command:

 ::
 
  [isabell@stardust ~]$ cd ~/babybuddy/public/ && pipenv --venv
  /home/isabell/.local/share/virtualenvs/public-xxxxxx

.. code-block:: ini
  :emphasize-lines: 3,5,12,21,22

  [uwsgi]
  project = babybuddy
  base_dir = /home/<username>/babybuddy
  
  virtualenv = /home/<username>/.local/share/virtualenvs/public-xxxxxx
  chdir = %(base_dir)/public
  module =  %(project).wsgi:application
  env = DJANGO_SETTINGS_MODULE=%(project).settings.production
  master = True
  vacuum = True
  
  http = :<yourport>
  
  wsgi-file = %(base)/public/babybuddy/wsgi.py
  touch-reload = %(wsgi-file)
  
  app = wsgi
  
  plugin = python
  
  uid = <username>
  gid = <username>

Finishing installation
======================

Point your browser to https://isabell.uber.space and log in with the default credentials.

.. note:: Default credentials:

 * username ``admin``
 * password ``admin``

Best practices
==============

Security
--------

Change all default passwords.

.. _`Baby Buddy`: https://github.com/cdubz/babybuddy
.. _pipenv: https://github.com/pypa/pipenv