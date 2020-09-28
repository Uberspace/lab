.. highlight:: console

.. author:: Andreas Pabst

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-ruby
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/fluentd.png
      :align: center

##########
Fluentd
##########

.. tag_list::

Fluentd_ is an open source data collector for unified logging layer. It allows you to unify data collection and
consumption for a better use and understanding of data.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Ruby <lang-ruby>` and its package manager :manual_anchor:`gem <lang-ruby.html#gem>`
  * :manual:`supervisord <daemons-supervisord>`
  * Optional: :manual:`web backends <web-backends>`

License
=======

Fluentd_ is released under the Apache-2.0 License.

All relevant legal information can be found here

  * https://github.com/fluent/fluentd/blob/master/LICENSE
  * http://www.apache.org/licenses/LICENSE-2.0

Prerequisites
=============

We're using :manual:`Ruby <lang-ruby>` in the stable version 2.6:

::

 [isabell@stardust ~]$ uberspace tools version show ruby
 Using 'Ruby' version: '2.6'
 [isabell@stardust ~]$

Installation
============

Fluentd_ can be installed as a ruby gem:

::

 [isabell@stardust ~]$ gem install fluentd --no-doc
 Fetching http_parser.rb-0.6.0.gem
 Fetching concurrent-ruby-1.1.7.gem
 Fetching tzinfo-2.0.2.gem
 Fetching serverengine-2.2.1.gem
 Fetching sigdump-0.2.4.gem
 Fetching yajl-ruby-1.4.1.gem
 Fetching msgpack-1.3.3.gem
 Fetching cool.io-1.6.0.gem
 Fetching fluentd-1.11.2.gem
 Fetching tzinfo-data-1.2020.1.gem
 Fetching strptime-0.2.4.gem
 WARNING:  You don't have /home/isabell/.gem/ruby/2.6.0/bin in your PATH, gem executables will not run.
 Building native extensions. This could take a while...
 Successfully installed msgpack-1.3.3
 Building native extensions. This could take a while...
 Successfully installed yajl-ruby-1.4.1
 Building native extensions. This could take a while...
 Successfully installed cool.io-1.6.0
 Successfully installed sigdump-0.2.4
 Successfully installed serverengine-2.2.1
 Building native extensions. This could take a while...
 Successfully installed http_parser.rb-0.6.0
 Successfully installed concurrent-ruby-1.1.7
 Successfully installed tzinfo-2.0.2
 Successfully installed tzinfo-data-1.2020.1
 Building native extensions. This could take a while...
 Successfully installed strptime-0.2.4
 Successfully installed fluentd-1.11.2
 11 gems installed
 [isabell@stardust ~]$

.. note:: You can ignore the warning about the executables not being in the PATH, Uberspace already took care of that.

To verify the installation, check the version of fluentd:

::

 [isabell@stardust ~]$ fluentd --version
 fluentd 1.11.2
 [isabell@stardust ~]$

Configuration
=============

Create configuration
---------------------------
Create the default configuration in the ``~/fluentd`` directory.

::

 [isabell@stardust ~]$ fluentd --setup ~/fluentd
 Installed /home/isabell/fluentd/fluent.conf.
 [isabell@stardust ~]$

Edit the config file ``~/fluentd/fluent.conf`` and comment out the following lines:

.. code-block::

 ## match tag=system.** and forward to another fluent server
 #<match system.**>
 #  @type forward
 #  @id forward_output
 #
 #  <server>
 #    host 192.168.0.11
 #  </server>
 #  <secondary>
 #    <server>
 #      host 192.168.0.12
 #    </server>
 #  </secondary>
 #</match>


Setup daemon
------------

Create ``~/etc/services.d/fluentd.ini`` with the following content:

.. code-block:: ini

 [program:fluentd]
 directory=%(ENV_HOME)s/fluentd
 command=fluentd --config fluent.conf --no-supervisor
 startsecs=60

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Further adjust the configuration in ``~/fluentd/fluent.conf`` according to your needs (see configuration_).

Optional: Expose the HTTP Endpoint
-----------------------

To expose the fluentd http endpoint (default port 8888), configure a :manual:`web backend <web-backend>`:

::

  [isabell@stardust ~]$ uberspace web backend set /fluentd --http --port 8888 --remove-prefix
  Set backend for /fluentd to port 8888; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

You can then test this endpoint by sending a GET request to ``https://isabell.uber.space/fluentd/debug.test?json={%22test%22:%22message%22}``.
The json payload should then appear in the fluentd logs:

::

  [isabell@stardust ~]$ supervisorctl tail fluentd
  ...
  2020-09-09 12:10:46.630093423 +0200 debug.test: {"test":"message"}
  [isabell@stardust ~]$


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _Fluentd: https://www.fluentd.org/
.. _configuration: https://docs.fluentd.org/configuration
.. _feed: https://rubygems.org/gems/fluentd/versions.atom

----

Tested with Fluentd 1.11.2, Uberspace 7.7.6

.. author_list::
