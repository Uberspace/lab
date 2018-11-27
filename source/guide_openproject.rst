.. highlight:: console

.. author:: Frank Stollmeier <fjanks@directbox.com>

.. sidebar:: Logo

  .. image:: _static/images/openproject.png
      :align: center

############
OpenProject
############

OpenProject_ is a web-based project management system for location-independent team collaboration. 
The functions include scheduling of work packages, task lists, wikis, forums, document management, time tracking, cost reporting, integration of git repositories, bug tracking, and others.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * MySQL_
  * supervisord_


Prerequisites
=============

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst


Installation
============

Download OpenProject and install packages
-----------------------------------------

In this example, we use the "community edition" of OpenProject, which comes with some common plugins included. If you prefer to install plain OpenProject without any plugins, replace the url below by ``https://github.com/opf/openproject.git``.

.. code-block:: console 
    :emphasize-lines: 2
    
    [isabell@stardust ~]$ 
    [isabell@stardust ~]$ git clone https://github.com/opf/openproject-ce.git --branch stable/8 --depth 1
    [isabell@stardust ~]$ cd openproject-ce
    [isabell@stardust openproject-ce]$ git checkout stable/8
    [isabell@stardust openproject-ce]$ gem install bundler
    [isabell@stardust openproject-ce]$ bundle install --deployment --without postgres sqlite development test therubyracer docker
    [isabell@stardust openproject-ce]$ npm install
    [isabell@stardust openproject-ce]$


Setup MySQL database
--------------------

Create a new database with the name <username>_openproject (replace <username> with your username): 

.. code-block:: console 
    :emphasize-lines: 2
    
    [isabell@stardust ~] mysql
    MariaDB [(none)]> CREATE DATABASE <username>_openproject CHARACTER SET utf8;
    MariaDB [(none)]> quit;
    [isabell@stardust ~] 

.. include:: includes/my-print-defaults.rst

Now we tell OpenProject to use our new database. First, make a copy of the example configuration file:

.. code-block:: console

    [isabell@stardust ~]$ cp ~/openproject-ce/config/database.yml.example ~/openproject-ce/config/database.yml
    
Open ``~/openproject-ce/config/database.yml`` and search for the "production"-block:

.. code-block:: none
  :emphasize-lines: 3,5,6,8

  production:
    adapter: mysql2
    database: <databasename>
    host: localhost
    username: <username>
    password: <password>
    # For MySQL 5.6 or older, set encoding to utf8.
    encoding: utf8

In this block, replace <databasename> with the name of the database that we created in the previous step ("<username>_openproject" if you chose the same name as in the example), replace <username> and <password> with your MySQL credentials, and set the encoding to utf8.

.. warning:: The yml-files are sensitive to whitespace.

Initialize MySQL database
-------------------------

The following commands will prepare the mysql-database for OpenProject:

  .. code-block:: console 
  
    [isabell@stardust ~]$ cd ~/openproject-ce
    [isabell@stardust openproject-ce]$ RAILS_ENV="production" ./bin/rake db:create
    [isabell@stardust openproject-ce]$ RAILS_ENV="production" ./bin/rake db:migrate
    [isabell@stardust openproject-ce]$ RAILS_ENV="production" ./bin/rake db:seed
    [isabell@stardust openproject-ce]$ RAILS_ENV="production" ./bin/rake assets:precompile
    [isabell@stardust openproject-ce]$ 


Setup mails
-----------

OpenProject can send emails to users, e.g. to notify them about events regarding their work packages or about changes on wiki pages that the user is watching. 
First, make a copy of the example configuration file:

.. code-block:: console

    [isabell@stardust ~]$ cp ~/openproject-ce/config/configuration.yml.example ~/openproject-ce/config/configuration.yml
    
Open the file ``~/openproject-ce/config/configuration.yml`` and append the following block:

.. code-block:: none
  :emphasize-lines: 3,4,6,7,8
  
  production:
    email_delivery_method: "smtp"
    smtp_address: "<hostname>"
    smtp_port: 587
    smtp_authentication: :login
    smtp_domain: '<hostname>'
    smtp_user_name: '<username>'
    smtp_password: '<password>'
    protocol: https
  rails_cache_store: :memcache

In this block, replace <hostname> with your hostname (e.g. stardust.uberspace.de), set the smtp-port to 587, and enter your username and the password for your mailbox. The username includes the domain, e.g. ``isabell@uber.space``. The password is the same as your password for ssh.

.. warning:: The yml-files are sensitive to whitespace.


Enable file server
------------------

The Ruby server can either rely on another webserver like Apache or Nginx, or serve static files by itself. For the second method, we need to open ``~/openproject-ce/config/environments/production.rb`` and set the following value to true::

    config.public_file_server.enabled = true


Configuration
=============

Choose port
-----------

You will need a free port: 

.. include:: includes/generate-port.rst

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

The following command generates a secret token. The output is a long alphanumeric squence that you will need in the next step.

  .. code-block:: none

    [isabell@stardust ~]$ cd ~/openproject-ce
    [isabell@stardust openproject-ce]$ ./bin/rake secret
    secret_key
    [isabell@stardust openproject-ce]$     


Create the file ``~/etc/services.d/openproject-daemon.ini`` with the following content: 

  .. code-block:: ini
  
    [program:openproject-daemon]
    directory=/home/<username>/openproject-ce
    command=bash -c 'exec bundle exec unicorn --host 127.0.0.1 --port <portnumber> --env production'
    autostart=yes
    autorestart=yes
    environment=HOME=/home/<username>,RAILS_ENV=production,SECRET_KEY_BASE=<secret_key>

Replace <username> with your username (two times), replace <portnumber> with the free port, and replace <secret_key> with the key that was generated in the previous step.

The following commands tell supervisord about our new service and start the daemon:

  .. code-block:: console

    [isabell@stardust ~]$ supervisorctl reread
    [isabell@stardust ~]$ supervisorctl update
    [isabell@stardust ~]$ supervisorctl start openproject-daemon



Finishing installation
======================

Point your browser to https://isabell.stardust.space and login as user "admin" with the default password "admin". Before doing anything else, change this password!



.. _OpenProject: https://www.openproject.org
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html



----

Tested with OpenProject 8.1.0, Uberspace 7.1.17.0

.. authors::
