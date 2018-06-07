.. author:: tpraxl <kontakt@macrominds.de>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/rust-logo-blk.svg
      :align: center

###########
Rust Server
###########

It couldn't be simpler to run a Rust web server on Uberspace.

Install Cargo, checkout your server code, install the server as a supervisord_ service and start it. Done.

----

.. note:: For this guide you might want to be familiar with the basic concepts of

  * Rust_
  * htaccess_
  * supervisord_

Prerequisites
=============

We need to install Rust_ first:

::

 [rust@taylor ~]$ curl https://sh.rustup.rs -sSf | sh
 [rust@taylor ~]$ # Choose 1) for the default installation option that also sets up your PATH
 [rust@taylor ~]$ source ~/.cargo/env

Providing a Rust Server
=======================

To simplify this recipe, just follow the thruster-intro-tutorial_ to create your Hello World Server.

Connect it to the outside world
===============================

.. warning:: Replace ``<ubername>`` with your Uberspace name!

::

  [rust@taylor ~]$ vim /var/www/virtual/<ubername>/html/.htaccess

.. warning:: Replace ``4321`` with the port of your server (``4321`` is the port used in the thruster-intro-tutorial)

.. code-block:: apacheconf

  RewriteEngine On
  # Using this rule, everything under <ubername>.uber.space/rust will be mapped to your Rust server
  RewriteRule ^rust/(.*) http://localhost:4321/$1 [P]

Test your setup
===============

::

  [rust@taylor ~]$ # replace ~/thruster-intro with your server project directory
  [rust@taylor ~]$ cd ~/thruster-intro
  [rust@taylor thruster-intro]$ cargo run
      Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
       Running `target/debug/thruster-intro`


Now visit ``https://<ubername>.uberspace.de/rust/hello`` . If everything went well (it should have)
then you can see the message ``Hello World!``.

Install as a service
====================

Press CTRL+C to stop your test.

::

  [rust@taylor thruster-intro]$ cargo install
    Installing thruster-intro v0.1.0 (file:///home/rust/thruster-intro)
     Compiling libc v0.2.41
     […]
     Compiling thruster-intro v0.1.0 (file:///home/rust/thruster-intro)
      Finished release [optimized] target(s) in 41.11 secs
    Installing /home/rust/.cargo/bin/thruster-intro
  [rust@taylor thruster-intro]$ which thruster-intro
  ~/.cargo/bin/thruster-intro
  [rust@taylor thruster-intro]$ vim ~/etc/service.d/thruster.ini

.. warning:: Replace ``<ubername>`` with your Uberspace name!

.. code-block:: ini

  [program:thruster]
  command=/home/<ubername>/.cargo/bin/thruster-intro

::

  [rust@taylor ~]$ supervisorctl reread
  [rust@taylor ~]$ supervisorctl update

.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _htaccess: https://manual.uberspace.de/en/web-documentroot.html#own-configuration
.. _Rust: https://www.rust-lang.org
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _thruster-intro-tutorial: https://medium.com/@MertzAlertz/wicked-fast-web-servers-in-rust-4947688426bc

----

.. authors::
