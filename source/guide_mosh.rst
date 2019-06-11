.. highlight:: console

.. author:: Daniel Hannaske <https://github.com/dahanbn/>

.. tag:: mosh
.. tag:: console
.. tag:: ssh

#######
Mosh
#######

.. tag_list::

Mosh_ (mobile shell) is a replacement for interactive SSH terminals. It's more robust and responsive, especially over Wi-Fi, cellular, and long-distance links. In short if you want to connect to your Uberspace from cellular networks in most cases it's more fun fun via Mosh_.

Mosh_ is already available in your Uberspace environment and you don't need to install it. You don't need to launch it as a daemon. Mosh_ doesn't listen on network ports or authenticate users. The client logs in to the server via SSH, and users present the same credentials (e.g., password, public key) as before. Then Mosh_ runs the mosh-server remotely and connects to it over UDP. 

Therefore you need to open a port in your Uberspace firewall. 

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * :manual:`Firewall Ports <basic-ports>`

License
=======

Mosh_ is free software, available for GNU/Linux, BSD, macOS, Solaris, Android, Chrome, and iOS under the OCB license.


Configuration and Usage
=======================

Step 1
------

Each uberspace can open 20 ports. The port numbers are generated automatically in the range from 20.000 to 61.000 and cannot be chosen arbitrarily. 

.. code-block:: bash
 
 [isabell@stardust ~] uberspace port add
 Port 40132 will be open for TCP and UDP traffic in a few minutes.
 

Step 2
------

Remember the opened port after running ``uberspace port add``. If you are unsure what ports are opened than ``uberspace port list`` will list you all opened port. You need to thell the port your local mosh client to successfully connect to your Uberspace.

.. code-block:: bash
 
 [isabell@stardust ~] uberspace port list
 40132

Step 3
------

Connect via your local mosh client to your Uberspace via ``mosh -p 40132 stardust.uberspace``.

.. code-block:: bash
 
 [isabell@localhost ~] mosh -p 40132 stardust.uberspace
 Welcome to Uberspace7!
 [...]


That's it, you have successfully configured your Uberspace to access it with Mosh_! Don't forget to close the port if you ever decide to discontinue to use Mosh_


.. _Mosh: https://mosh.org/

.. author_list::