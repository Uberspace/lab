.. highlight:: console

.. author:: michi <https://github.com/michi-zuri/>

.. tag:: console
.. tag:: rust

.. sidebar:: Logo

  .. image:: _static/images/starship.svg
      :align: center

####
Starship
####

.. tag_list::

Starship_ is the minimal, blazing-fast, and infinitely customizable prompt for
any shell!


----

.. image:: _static/images/starship.png

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`shell <basics-shell>`

License
=======

Starship_ is free software, available under the permissive ISC License, whcih
is functionally equivalent to BSD 2-Clause and MIT licenses,
removing some language that is no longer necessary.

Prerequisites
============

A NerdFont_ installed and enabled in your terminal on your computer (for example, try the
FiraCode Nerd Font that can be downloaded from NerdFonts_).

Installation
============
.. code-block:: console

 [isabell@stardust ~]$ cargo install starship
 [...]
 [isabell@stardust ~]$ eval "$(starship init bash)"
 isabell on stardust in ~
 >

To make the prompt permanent, add one line to your .bashrc:

.. code-block:: console

 isabell on stardust in ~
 > echo -e '\n' >> .bashrc
 isabell on stardust in ~
 > echo 'eval "$(starship init bash)"' >> .bashrc
 isabell on stardust in ~
 >

That's it, you have successfully installed Starship_ to your Uberspace console:

.. code-block:: console

 [isabell@localhost ~]$ ssh <username>@<username>.uber.space
 Welcome to Uberspace7!
 [...]
 isabell on stardust in ~
 >


.. _Starship: https://starship.rs/
.. _NerdFont: https://www.nerdfonts.com/
.. _NerdFonts: https://www.nerdfonts.com/font-downloads

.. author_list::
