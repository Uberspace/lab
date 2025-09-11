.. author:: Dan Untenzu <mail@pixelbrackets.de>
.. highlight:: console
.. tag:: lang-ruby
.. tag:: web
.. tag:: customer-management
.. tag:: audience-business

.. sidebar:: Logo

  .. image:: _static/images/redmine.svg
      :align: center

#######
Redmine
#######

.. tag_list::

Redmine_ is an Open Source, web-based project management and issue tracking service.

It is written using the Ruby on Rails framework and licensed under `GNU General Public License v2 <https://www.gnu.org/licenses/gpl-2.0.html>`_

This guide explains how to install Redmine on Uberspace.

----

.. error::

  This guide seems to be **broken** for all current versions of redmine, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1883


.. note:: For this guide you should be familiar with the basic concepts of

  * Ruby_
  * supervisord_
  * domains_

Prerequisites
=============

Checkout which `version of Ruby <https://redmine.org/projects/redmine/wiki/RedmineInstall>`_
is supported by your desired version of Redmine. Redmine version 6 for example
expects Ruby 3.1, 3.2 or 3.3.

Run ``uberspace tools version show ruby`` to show which Ruby version is currently
active on your Uberspace and ``uberspace tools version list ruby`` to list all
available ones.

To set Ruby version 3.2 you could run (but there is no need to do so if one of the above is already active):

.. code-block:: console

  [isabell@stardust ~]$ uberspace tools version use ruby 3.2
  Selected Ruby version 3.2
  [isabell@stardust ~]$

Ruby requires a database, so you should create an empty database now.

.. note::

  Use the collation ``utf8mb4``, otherwise Redmine will crash when users paste
  emojis in tickets.

.. code-block:: none

  [isabell@stardust ~] mysql -e "CREATE DATABASE ${USER}_redmine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  [isabell@stardust ~]

Your domain needs to be setup:

.. include:: includes/web-domain-list.rst

.. include:: includes/my-print-defaults.rst


Installation
============

This instruction follows the official installation_ guide of Redmine for almost all steps,
except for the step “Test the installation / Installing web server”.

Download_ and extract Redmine in the desired version. Ruby should not be stored
into your DocumentRoot. Instead you may create a subfolder ``redmine`` in the
`Home Directory`_ and place
all files in there.

.. code-block:: console

  [isabell@stardust ~]$ wget https://redmine.org/releases/redmine-6.0.6.tar.gz
  [isabell@stardust ~]$ tar xfv redmine-6.0.6.tar.gz
  [isabell@stardust ~]$ mv redmine-6.0.6 redmine
  [isabell@stardust ~]$ cd redmine
  [isabell@stardust redmine]$

Copy the file ``config/database.yml.example`` to ``config/database.yml`` and edit
the new file in order to configure your database settings for the "production" environment. You'll find your mysql password using ``my_print_defauls client``.

.. code-block:: yaml
  :emphasize-lines: 3,5,6

  production:
    adapter: mysql2
    database: isabell_redmine
    host: localhost
    username: isabell
    password: "my_secure_mysql_password"

Redmine uses Bundler to manage dependencies. Install Bundler running ``gem install bundler``.

.. note:: Package installation on recent versions of Redmine crashes because the `nokogiri` gem requires GLIBC_2.28 which is not available on U7.

To fix the issue one has to modify the `nokogiri` dependency in the Gemfile as follows:

.. code-block:: ruby

  gem 'nokogiri', '~> 1.18.3', force_ruby_platform: true


Install all dependencies running ``bundle install --without development test rmagick --path vendor/bundle``:

.. code-block:: console

  [isabell@stardust redmine]$ bundle install --without development test rmagick --path vendor/bundle
  Bundle complete!
  Gems in the groups development, test and rmagick were not installed.
  Bundled gems are installed into `./vendor/bundle`
  [isabell@stardust redmine]$

Create a secret token running ``bundle exec rake generate_secret_token``.

Create the database structure with the command ``RAILS_ENV=production bundle exec rake db:migrate``.

Redmine provides a set of default configuration data like a first admin user,
some access groups, default project settings etc. which may be added running
``RAILS_ENV=production bundle exec rake redmine:load_default_data``.

All file permission should be fine automatically on Uberspace.

The installation is now done, what's missing is the connection to the webserver.

Connecting the webserver
------------------------

A Ruby specialty is that it requires a so called »appserver« as connector
between your application and the webserver. The webserver, like Nginx or Apache,
will handle all incoming web request and pass only request for the Ruby app along
to the appserver. The appserver will then actually run your Rails app.

Ruby offers many appservers. You may use Puma_, which is documented extensively
in the UberLab as well.

.. code-block:: console

  [isabell@stardust redmine]$ gem install puma
  Building native extensions. This could take a while...
  Successfully installed puma
  1 gem installed
  [isabell@stardust redmine]$

.. tip::

  Use the installation with the ``gem`` command above and not with bundler,
  as suggested in the Redmine installation guide, since this may trigger a
  `bug <https://github.com/seuros/capistrano-puma/issues/237>`_.

Create a configuration file for Puma called ``config.rb`` and add the following
structure. Adapt the highlighted lines to your setup.

.. code-block:: none
  :emphasize-lines: 4,7

  #!/usr/bin/env puma

  # The directory of your Ruby app
  directory '/home/isabell/redmine'

  # The path to the Redmine rackup file
  rackup '/home/isabell/redmine/config.ru'

.. note::

    puma is running on port 9292.

.. include:: includes/web-backend.rst

You could now start Puma manually and everything would work. But to start it
automatically Uberspace offers the service supervisord_.

Create and edit the file ``~/etc/services.d/redmine-daemon.ini`` and add the following content to it.

.. code-block:: ini

  [program:redmine-daemon]
  command=/opt/uberspace/etc/%(ENV_USER)s/binpaths/ruby/puma --config %(ENV_HOME)s/redmine/config.rb --environment production
  autostart=yes
  autorestart=yes

The ``--config`` parameter provides the path to the Puma configuration file.
Be aware that the ``%(ENV_X)s`` is a Python syntax, which will expand to
``/home/isabell`` (so the »s« is part of the syntax, not of your path).

Lastly, tell supervisord to refresh its configuration and start new services by running ``supervisorctl update``.

Redmine should now be available on your configured domain.

Configuration
=============

If you've added the default configuration for Redmine, then you will have a
default profile with the following credentials.

- Name: *admin*
- Password: *admin*

Redmine will ask you to change the password right after you login for the first time.

Create some users first. The create some projects. Add members to your projects.

Best practices
==============

- Rename the ``admin`` user to any other username
- Set up groups for teams, and assign new tickets to teams instead of individuals
  so everybody can see them

Updates
=======

Check for new download_ versions regularly and follow the Security_ Advisories
to stay informed about important updates.

Follow the Redmine Upgrade_ Guide to update the application, which consists of
the same steps as the installation guide above, plus backup and restore of existing data.

----

Tested with Redmine 6.0.6, Ruby 3.2, Uberspace 7.16.7

.. author_list::

.. _Redmine: https://www.redmine.org/
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _Download: https://redmine.org/projects/redmine/wiki/Download/
.. _Installation: https://redmine.org/projects/redmine/wiki/RedmineInstall
.. _Security: https://www.redmine.org/projects/redmine/wiki/Security_Advisories
.. _Upgrade: https://www.redmine.org/projects/redmine/wiki/RedmineUpgrade
.. _Ruby: https://manual.uberspace.de/lang-ruby.html
.. _Puma: https://lab.uberspace.de/guide_puma.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _Home Directory: https://manual.uberspace.de/basics-home.html#home
.. _DocumentRoot: https://manual.uberspace.de/web-documentroot.html#documentroot
