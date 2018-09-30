.. author:: Theodor Müller <info@trilliarden.net>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/puma.png
      :align: center

#######
Puma
#######

Puma_ is a Ruby_ web server built for speed and parallelism. It is designed for running Rack_ apps only. It is licensed under the BSD 3-Clause license. This guide explains how to install Puma and run a minimal, custom Ruby application.

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * Ruby_
  * supervisord_

Installation
============

Use ``gem`` to install the latest version of Puma:

::

  [isabell@stardust ~]$ gem install puma
  Fetching: puma-3.12.0.gem (100%)
  Building native extensions. This could take a while...
  Successfully installed puma-3.12.0
  1 gem installed
  [isabell@stardust ~]$ 
  
Create a directory, and inside the directory a file ``rubyapp.ru`` for the application:

::

  [isabell@stardust ~]$ mkdir ~/rubyapp
  [isabell@stardust ~]$ touch ~/rubyapp/rubyapp.ru
  [isabell@stardust ~]$ 

Update the permissions so that the application file is executable:

::

  [isabell@stardust ~]$ chmod +x ~/rubyapp/rubyapp.ru 
  [isabell@stardust ~]$ 
  
This file is the Rackup file for the application. Add the following content to ``~/rubyapp/rubyapp.ru``, a simple Hello World application:

.. code-block:: none
  class HelloWorld
    def call(env)
      [200, {"Content-Type" => "text/plain"}, ["Hello World"]]
    end
  end

  run HelloWorld.new


Configuration
=============

Configure port
--------------

You need to find a free port to bind Puma to it.

.. include:: includes/generate-port.rst

Puma configuration file
-----------------------

Next, create a Puma configuration file, update the permissions as before,

::

  [isabell@stardust ~]$ touch ~/rubyapp/config.rb
  [isabell@stardust ~]$ chmod +x ~/rubyapp/config.rb
  [isabell@stardust ~]$

and add the following content:

.. code-block:: none
  #!/usr/bin/env puma

  # The directory to operate out of.
  directory '/home/isabell/rubyapp'

  # The path to the rackup file
  rackup '/home/isabell/rubyapp/rubyapp.ru'

  # Bind Puma to the port
  bind 'tcp://127.0.0.1:9000'


Setup supervisord
-----------------

Create ``~/etc/services.d/rubyapp.ini`` with the following content:

.. code-block:: ini
  [program:rubyapp]
  command=/opt/uberspace/etc/isabell/binpaths/ruby/puma --config /home/isabell/rubyapp/config.rb
  autostart=yes
  autorestart=yes

The ``--config`` parameter provides the path to the configuration file.

Tell ``supervisord`` to refresh its configuration and start the service:

::

  [isabell@stardust ~]$ supervisorctl reread
  rubyapp: available
  [isabell@stardust ~]$ supervisorctl update
  rubyapp: added process group
  [isabell@stardust ~]$ 

Setup .htaccess
---------------

Create the file ``~/html/.htaccess`` with the following content to forward requests from the outside to Puma:

.. code-block:: none
  DirectoryIndex disabled

  RewriteEngine On
  RewriteRule ^rubyapp/(.*) http://localhost:9000/$1 [P]

Logging
-------

If you want to enable logging, create a new directory for Puma logfiles:

::

  [isabell@stardust ~]$ mkdir /home/isabell/logs/puma
  [isabell@stardust ~]$

Edit the configuration file at ``~/rubyapp/config.ru`` and append the following line to redirect Puma's output and errors to log files:

.. code-block:: none
  stdout_redirect '/home/isabell/logs/puma/out.log', '/home/isabell/logs/puma/err.log', true

Restart Puma to reload the configuration file:

::

  [isabell@stardust puma]$ supervisorctl restart rubyapp
  rubyapp: stopped
  rubyapp: started
  [isabell@stardust puma]$ 


Test
----

To validate the installation, open a browser and visit ``isabell.uber.space/rubyapp/``. If everything is set up correctly, you will see "Hello World". 


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use ``gem`` to update Puma:

::

  [isabell@stardust puma]$ gem update puma
  (...)
  [isabell@stardust puma]$ 

Further Reading
===============

* Puma's readme_ on GitHub
* An example configuration_ file 


----

Tested with Puma 3.12, Uberspace 7.1.13.0


.. authors::

.. _Ruby: https://www.ruby-lang.org/
.. _Puma: https://puma.io
.. _Rack: https://rack.github.io
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _readme: https://github.com/puma/puma
.. _configuration https://github.com/puma/puma/blob/master/examples/config.rb
.. _feed: https://github.com/puma/puma/releases
