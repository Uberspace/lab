.. highlight:: console

.. author:: Jan Philip Bernius <https://janphilip.bernius.net>

.. tag:: lang-ruby
.. tag:: web

##########
Guillotine
##########

.. tag_list::

Guillotine_ is a simple URL Shortener written in Ruby and powers GitHubs URL Shortener Git.io_.
It supports multiple storage adapters, including :manual:`MySQL <database-mysql>`, :lab:`PostgreSQL <guide_postgresql>`, SQLite, :lab:`Redis <guide_redis>`, Riak and Cassandra.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Ruby <lang-ruby>` and its package manager :manual_anchor:`gem <lang-ruby.html#gem>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Guillotine is released under the `MIT License`_.

Prerequisites
=============

We're using :manual:`Ruby <lang-ruby>` in the stable version 2.6:

.. code-block:: console

  [isabell@stardust ~]$ uberspace tools version use ruby 2.6
  Selected Ruby version 2.6
  The new configuration is adapted immediately. Patch updates will be applied automatically.

  [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your Short URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Install Dependencies
--------------------

Use ``gem`` to install the latest versions of the Guillotine, Sequel and mysql2 gems:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ gem install guillotine sequel mysql2
  Fetching sinatra-1.4.8.gem
  Fetching addressable-2.3.8.gem
  Fetching rack-1.6.11.gem
  Fetching tilt-2.0.9.gem
  Fetching rack-protection-1.5.5.gem
  Fetching guillotine-1.4.2.gem
  WARNING:  You don't have /home/isabell/.gem/ruby/2.6.0/bin in your PATH,
  	  gem executables will not run.
  Successfully installed rack-1.6.11
  Successfully installed rack-protection-1.5.5
  Successfully installed tilt-2.0.9
  Successfully installed sinatra-1.4.8
  Successfully installed addressable-2.3.8
  Successfully installed guillotine-1.4.2
  Fetching sequel-5.22.0.gem
  Successfully installed sequel-5.22.0
  Fetching mysql2-0.5.2.gem
  Building native extensions. This could take a while...
  Successfully installed mysql2-0.5.2
  8 gems installed

  [isabell@stardust ~]$

Create App File
---------------

Create a directory for the application:

.. code-block:: console
  :emphasize-lines: 1-2

  [isabell@stardust ~]$ mkdir ~/guillotine
  [isabell@stardust ~]$

Add the following content to ``~/guillotine/app.rb`` to set up the connection to the MySQL database using the Sequel adapter. Make sure to adapt your MySQL credentials.

.. code-block:: ruby
  :emphasize-lines: 6

  require 'guillotine'
  require 'sequel'

  module MyApp
    class App < Guillotine::App
      db = Sequel.connect("mysql2://isabell:MySuperSecretPassword@127.0.0.1:3306/isabell")
      adapter = Guillotine::Adapters::SequelAdapter.new(db)
      set :service => Guillotine::Service.new(adapter)

      post "/" do
        status, head, body = settings.service.create(params[:url], params[:code])

        if loc = head['Location']
          body = head['Location'] = File.join(request.base_url, loc)
        end

        # Show shortened URL in Body
        [status, head, simple_escape(body)]
      end
    end
  end

.. note:: This file can be used as a configuration point.
  The Katana_  project provides an example for possible extensions.

Create Rackup config file
-------------------------

Add the following content to ``~/guillotine/config.ru``:

.. code-block:: ruby

  require "rubygems"
  require File.expand_path("../app.rb", __FILE__)

  run MyApp::App


Set up Database
---------------

Initialize the database for Guillotine:

.. code-block:: console
  :emphasize-lines: 1-9

  [isabell@stardust ~]$ mysql <<__SQL__
  USE $USER;
  CREATE TABLE IF NOT EXISTS \`urls\` (
    \`url\` varchar(255) DEFAULT NULL,
    \`code\` varchar(255) DEFAULT NULL,
    UNIQUE KEY \`url\` (\`url\`),
    UNIQUE KEY \`code\` (\`code\`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
  __SQL__
  [isabell@stardust ~]$

Configure web server
--------------------

.. note::

    Guillotine is running on port 9292.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/guillotine.ini`` with the following content:

.. code-block:: ini

  [program:guillotine]
  environment=APP_ENV=production
  directory=%(ENV_HOME)s/guillotine
  command=/opt/uberspace/etc/%(ENV_USER)s/binpaths/ruby/rackup config.ru --host 0.0.0.0 --port 9292

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Create short URL
================

Use your HTTP tool of choice (e.g. ``curl``) to make a POST request to create a short URL.

.. code-block:: console
  :emphasize-lines: 1-2

  [isabell@stardust ~]$ curl https://isabell.uber.space \
    --form "url=https://uberspace.de"
  https://isabell.uber.space/D_deZA
  [isabell@stardust ~]$

Define your own short code like so:

.. code-block:: console
  :emphasize-lines: 1-3

  [isabell@stardust ~]$ curl https://isabell.uber.space \
    --form "url=https://lab.uberspace.de" \
    --form "code=lab"
  https://isabell.uber.space/lab
  [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use :manual_anchor:`gem <lang-ruby.html#gem>` to update dependencies like so:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ gem update
  Updating installed gems
  Updating addressable
  Fetching addressable-2.6.0.gem
  Fetching public_suffix-3.1.1.gem
  WARNING:  You don't have /home/isabell/.gem/ruby/2.6.0/bin in your PATH,
  	  gem executables will not run.
  Successfully installed public_suffix-3.1.1
  Successfully installed addressable-2.6.0
  Updating bigdecimal
  Fetching bigdecimal-1.4.4.gem
  Building native extensions. This could take a while...
  Successfully installed bigdecimal-1.4.4
  Updating csv
  Fetching csv-3.1.1.gem
  Successfully installed csv-3.1.1
  Updating fileutils
  Fetching fileutils-1.2.0.gem
  Successfully installed fileutils-1.2.0
  Updating io-console
  Fetching io-console-0.4.8.gem
  Building native extensions. This could take a while...
  Successfully installed io-console-0.4.8
  Updating json
  Fetching json-2.2.0.gem
  Building native extensions. This could take a while...
  Successfully installed json-2.2.0
  Updating rack
  Fetching rack-2.0.7.gem
  Successfully installed rack-2.0.7
  Updating rack-protection
  Fetching rack-protection-2.0.5.gem
  Successfully installed rack-protection-2.0.5
  Updating rdoc
  Fetching rdoc-6.1.1.gem
  Successfully installed rdoc-6.1.1
  Updating rexml
  Fetching rexml-3.2.2.gem
  Successfully installed rexml-3.2.2
  Updating rss
  Fetching rss-0.2.8.gem
  Successfully installed rss-0.2.8
  Updating sinatra
  Fetching sinatra-2.0.5.gem
  Fetching mustermann-1.0.3.gem
  Successfully installed mustermann-1.0.3
  Successfully installed sinatra-2.0.5
  Gems updated: addressable public_suffix bigdecimal csv fileutils io-console json rack rack-protection rdoc rexml rss mustermann sinatra
  [isabell@stardust ~]$

Restart the Service for the update to take effect.

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ supervisorctl restart guillotine
  guillotine: stopped
  guillotine: started
  [isabell@stardust ~]$

Check the status and logs to verify that Guillotine started successfully after the update.

.. code-block:: console
  :emphasize-lines: 1,3

  [isabell@stardust ~]$ supervisorctl status guillotine
  guillotine                       RUNNING   pid 26020, uptime 0:03:14
  [isabell@stardust ~]$ supervisorctl tail -5000 guillotine stderr
  [2019-08-01 16:48:56] INFO  WEBrick::HTTPServer#start done.
  [2019-08-01 16:48:56] INFO  WEBrick 1.4.2
  [2019-08-01 16:48:56] INFO  ruby 2.6.2 (2019-03-13) [x86_64-linux]
  [2019-08-01 16:48:56] INFO  WEBrick::HTTPServer#start: pid=26020 port=9292
  [isabell@stardust ~]$


.. _Guillotine: https://github.com/technoweenie/guillotine
.. _MIT License: https://github.com/technoweenie/guillotine/blob/master/LICENSE
.. _feed: https://github.com/technoweenie/guillotine/releases.atom
.. _Git.io: https://git.io
.. _Katana: https://github.com/mrtazz/katana

----

Tested with Ruby 2.6.2, Guillotine 1.4.2, Uberspace 7.3.4

.. author_list::
