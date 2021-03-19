.. highlight:: console

.. author:: Maximilian F. Kapfer <maximilian.kapfer@gmail.com>

.. sidebar:: Logo

  .. image:: _static/images/snibox.png
      :align: center

######
Snibox
######

Snibox is a self-hosted snippet manager. Developed to collect and organize code snippets. Supports various programming languages, markdown, plain text.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`Ruby <lang-ruby>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`


License
=======

Snibox is released under the MIT License. All relevant legal information can be found here:

  * https://opensource.org/licenses/MIT


Prerequisites
=============
For this service we need to use Ruby in the version 2.6 and PostgreSQL in the version 12.

::

 [isabell@stardust ~]$ uberspace tools version list ruby
    - 2.5
    - 2.6
    - 2.7
    - 3.0

 [isabell@stardust ~]$ uberspace tools version use ruby 2.6
    Selected ruby version 2.6
    The new configuration is adapted immediately. Patch updates will be applied automatically.

 [isabell@stardust ~]$ uberspace tools version list postgresql
    - 10
    - 11
    - 12
    - 13

 [isabell@stardust ~]$ uberspace tools version use postgresql 12
 Using 'postgresql' version: 13

Next, we need a running PostgreSQL database. A detailed description can be found in the
`PostgreSQL Guide <https://lab.uberspace.de/guide_postgresql.html>`_

If you want to use Snibox with your own domain you need to setup your domains_ first:

.. include:: includes/web-domain-list.rst

Installation
============

Step 1 - Download & Extract
---------------------------

::

 [isabell@stardust ~]$ git clone https://github.com/snibox/snibox.git
 [isabell@stardust ~]$ cd snibox/

Step 2 - Install bundler & dependencies
---------------------------------------

::

 [isabell@stardust snibox]$ gem install bundler:1.17.2
 [isabell@stardust snibox]$ bundle install



Configuration
=============

Step 1: Copy the example config file
------------------------------------

::

 [isabell@stardust snibox]$ cp .env.production.sample .env


Step 2: Generate a secret key for the service
---------------------------------------------

::

 [isabell@stardust snibox]$ ./bin/rake secret


Step 3: Edit the configuration
------------------------------

::

 [isabell@stardust snibox]$ vim .env

.. warning:: Be sure, to replace all values with correct data of your own Uberspace account!

::

 # Secrets -> Secret Key from above
 SECRET_KEY_BASE=3e84e3f85a79be7b2571eb832a31cf142583d47d60640f1b288d2cd616e5355f755c7f3b7ba9861dd890b50188c7e604c9101f592c245bff651464cf497a6ed8

 # Comment the line below if you serve static files using Nginx, etc
 RAILS_SERVE_STATIC_FILES=enabled

 # SSL
 FORCE_SSL=false

 # Database -> Your PostgreSQL database settings
 DB_NAME=isabell
 DB_USER=isabell
 DB_PASS=1234567890123456789012345678901234567890123456789012345678901234
 DB_HOST=localhost
 DB_PORT=5432

 # Mailgun. Required by 'Reset password feature'. Feel free to start without this setup.
 # -> Not needed settings for mail
 MAILGUN_SMTP_PORT=587
 MAILGUN_SMTP_SERVER=smtp.mailgun.org
 MAILGUN_SMTP_LOGIN=
 MAILGUN_SMTP_PASSWORD=
 MAILGUN_API_KEY=
 MAILGUN_DOMAIN=
 MAILGUN_PUBLIC_KEY=


Finishing installation
======================


Step 1 - Set Snibox to production
---------------------------------

::

  [isabell@stardust snibox]$ RAILS_ENV=production ./bin/rake db:setup
  [isabell@stardust snibox]$ RAILS_ENV=production ./bin/rake assets:precompile



Step 2 - Setup the web backend
----------------------------
To ensure a connection between Snibox you need to setup a backend connection to the port 3000:

::

 [isabell@stardust snibox]$ web backend set / --http --port 3000
 Set backend for / to port 3000; please make sure something is listening!
 You can always check the status of your backend using "uberspace web backend list".

 [isabell@stardust snibox]$ uberspace web backend list
 / http:3000 => OK, listening: PID 19995, puma 3.12.1 (tcp://0.0.0.0:3000) [snibox]




Step 3 - Create the snibox service
----------------------------------
Create the service file.

::

 [isabell@stardust snibox]$ vim ~/etc/services.d/snibox.ini

::

 [program:snibox]
 environment=RAILS_ENV=production
 command=/home/testy/snibox/bin/rails s

Load the configuration.

::

 [isabell@stardust snibox]$ supervisorctl reread

Update supervisorctl.

::

 [isabell@stardust snibox]$ supervisorctl update

Check if snibox is running.

::

 [isabell@stardust snibox]$ supervisorctl status
 postgresql                       RUNNING   pid 13101, uptime 10:04:45
 snibox                           RUNNING   pid 10247, uptime 0:00:05


Step 4 - Register new user
--------------------------
Visit your domain ``https://isabell.uber.space/register`` to register a new Snibox user.


Tested with Snibox v2019(latest), Uberspace 7.10.0

.. authors::
