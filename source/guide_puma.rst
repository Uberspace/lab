.. author:: Theodor Müller <info@trilliarden.net>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/puma.png
      :align: center

####
Puma
####

Puma_ is a Ruby_ web server built for speed and parallelism. It is designed for running Rack_ apps only. It is licensed under the BSD 3-Clause license. This guide explains how to install Puma and run a minimal, custom Ruby application.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Ruby_
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

We're using Ruby_ in the stable version 2.5:

.. code-block:: console

  [isabell@stardust ~]$ uberspace tools version show ruby
  Using 'Ruby' version: '2.5'
  [isabell@stardust ~]$

If you want to use Puma with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

Use ``gem`` to install the latest version of Puma:

.. code-block:: console

  [isabell@stardust ~]$ gem install puma
  Fetching: puma-3.12.0.gem (100%)
  Building native extensions. This could take a while...
  Successfully installed puma-3.12.0
  1 gem installed
  [isabell@stardust ~]$

Create a directory, and inside the directory a file ``rubyapp.ru`` for the application:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/puma
  [isabell@stardust ~]$ touch ~/puma/rubyapp.ru
  [isabell@stardust ~]$

This file is the Rackup file for the application. Add the following content to ``~/puma/rubyapp.ru``, a simple Hello World application:

.. code-block:: ruby

  class HelloWorld
    def call(env)
      [200, {"Content-Type" => "text/plain"}, ["Hello World"]]
    end
  end

  run HelloWorld.new

Create the folder for logs:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/logs/puma
  [isabell@stardust ~]$

Configuration
=============

Puma configuration file
-----------------------

Next, create a Puma configuration file:

.. code-block:: console

  [isabell@stardust ~]$ touch ~/puma/config.rb
  [isabell@stardust ~]$

... and add the following content. Adapt the highlighted lines to your setup.

.. code-block:: none
  :emphasize-lines: 4,7,13

  #!/usr/bin/env puma

  # The directory to operate out of.
  directory '/home/isabell/puma'

  # The path to the rackup file
  rackup '/home/isabell/puma/rubyapp.ru'

  # Bind Puma to the port
  bind 'tcp://0.0.0.0:9000'

  # Enable logging
  stdout_redirect '/home/isabell/logs/puma/out.log', '/home/isabell/logs/puma/err.log', true

Setup supervisord
-----------------

Create ``~/etc/services.d/puma.ini`` with the following content. Adapt the highlighted lines to your setup.

.. code-block:: ini
  :emphasize-lines: 2

  [program:puma]
  command=/opt/uberspace/etc/isabell/binpaths/ruby/puma --config %(ENV_HOME)s/puma/config.rb
  autostart=yes
  autorestart=yes

The ``--config`` parameter provides the path to the configuration file.

Tell ``supervisord`` to refresh its configuration and start the service:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl reread
  puma: available
  [isabell@stardust ~]$ supervisorctl update
  puma: added process group
  [isabell@stardust ~]$

Configure web server
--------------------

.. note::

    puma is running on port 9000.

.. include:: includes/web-backend.rst

Test
----

To validate the installation, open a browser and visit ``isabell.uber.space``. If everything is set up correctly, you will see "Hello World".


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use ``gem`` to update Puma:

.. code-block:: console

  [isabell@stardust ~]$ gem update puma
  (...)
  [isabell@stardust ~]$

Further Reading
===============

* Puma's readme_ on GitHub
* An example configuration_ file

----

Tested with Puma 3.12, Uberspace 7.1.17


.. author_list::

.. _Ruby: https://www.ruby-lang.org/
.. _Puma: https://puma.io
.. _Rack: https://rack.github.io
.. _readme: https://github.com/puma/puma
.. _configuration: https://github.com/puma/puma/blob/master/examples/config.rb
.. _feed: https://github.com/puma/puma/releases
