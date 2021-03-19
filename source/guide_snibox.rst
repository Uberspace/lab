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

 [isabell@stardust ~]$ uberspace tools version use ruby 2.6
    Selected ruby version 2.6
    The new configuration is adapted immediately. Patch updates will be applied automatically.

 [isabell@stardust ~]$ uberspace tools version use postgresql 12
 Using 'postgresql' version: 13

Next, we need a running PostgreSQL database. A detailed description can be found in the
:lab:`PostgreSQL Guide <guide_postgresql>`

If you want to use Snibox with your own domain you need to setup your domains first:

.. include:: includes/web-domain-list.rst

Installation
============

Download & Extract
------------------

::

 [isabell@stardust ~]$ git clone https://github.com/snibox/snibox.git
 Cloning into 'snibox'...
 remote: Enumerating objects: 2609, done.
 remote: Total 2609 (delta 0), reused 0 (delta 0), pack-reused 2609
 Receiving objects: 100% (2609/2609), 778.57 KiB | 15.57 MiB/s, done.
 Resolving deltas: 100% (1528/1528), done.
 [isabell@stardust ~]$ cd snibox/

Install bundler & dependencies
------------------------------

::

 [isabell@stardust snibox]$ gem install bundler:1.17.2
 [isabell@stardust snibox]$ bundle install



Configuration
=============

Copy the example config file
----------------------------

::

 [isabell@stardust snibox]$ cp .env.production.sample .env


Generate a secret key for the service
-------------------------------------

::

 [isabell@stardust snibox]$ ./bin/rake secret


Edit the configuration
----------------------

Use your favourite editor to edit ``~/snibox/.env`` with the following content:


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


Set Snibox to production
------------------------

::

  [isabell@stardust snibox]$ RAILS_ENV=production ./bin/rake db:setup
  [isabell@stardust snibox]$ RAILS_ENV=production ./bin/rake assets:precompile



Setup the web backend
---------------------

.. note::
    Snibox is running on port 3000.

.. include:: includes/web-backend.rst


Create the snibox service
-------------------------
Use your favourite editor to create ``~/etc/services.d/snibox.ini`` with the following content:

.. code-block:: ini

 [program:snibox]
 environment=RAILS_ENV=production
 command=/home/testy/snibox/bin/rails s
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If snibox is not in state RUNNING, check your configuration


Register new user
-----------------
Visit your domain ``https://isabell.uber.space/register`` to register a new Snibox user.


Tested with Snibox v2019(latest), Uberspace 7.10.0

.. authors::
