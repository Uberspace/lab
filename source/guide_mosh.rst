.. highlight:: console

.. author:: Daniel Hannaske <https://github.com/dahanbn/>

.. tag:: console
.. tag:: ssh

####
Mosh
####

.. tag_list::

Mosh_ (mobile shell) is a replacement for interactive SSH terminals. It's more robust and responsive, especially over Wi-Fi, cellular, and long-distance links. In short if you want to connect to your Uberspace from cellular networks in most cases it's more fun fun via Mosh_.

Mosh_ is already available in your Uberspace environment and you don't need to install it. You don't need to launch it as a daemon. Mosh_ doesn't listen on network ports or authenticate users. The client logs in to the server via SSH, and users present the same credentials (e.g., password, public key) as before. Then Mosh_ runs the mosh-server remotely and connects to it over UDP. 

Therefore you need to open a port in your Uberspace firewall. 

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * :manual:`Firewall Ports <basics-ports>`

License
=======

Mosh_ is free software, available for GNU/Linux, BSD, macOS, Solaris, Android, Chrome, and iOS under the GPLv3 license.


Configuration
=============

.. include:: includes/open-port.rst

Best practices
==============

It's not necessary to configure Mosh as a daemon on your Uberspace.

.. code-block:: bash
 
 [isabell@localhost ~] mosh -p <your_port> <username>.uber.space
 Welcome to Uberspace7!
 [...]
 [isabell@stardust ~]$


That's it, you have successfully configured your Uberspace to access it with Mosh_! Don't forget to close the port if you ever decide to discontinue to use Mosh_


.. _Mosh: https://mosh.org/

.. author_list::
