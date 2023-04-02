.. highlight:: console

.. author:: Michi <https://github.com/michi-zuri>
.. author:: Mike <https://github.com/fooforge>

.. tag:: console
.. tag:: lang-rust

.. sidebar:: Logo

  .. image:: _static/images/starship.svg
      :align: center

########
Starship
########

.. tag_list::

Starship_ is the minimal, blazing-fast, and infinitely customisable prompt for
any shell!


----

.. image:: _static/images/starship.png

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`shell <basics-shell>`

License
=======

Starship_ is free software, available under the permissive ISC License, which
is functionally equivalent to BSD 2-Clause and MIT licenses,
removing some language that is no longer necessary.

Prerequisites
=============

A `Nerd Font`_ installed and enabled in your terminal on your computer (for example, try the
FiraCode Nerd Font that can be downloaded from NerdFonts_).

Instructions for installing fonts depend on your local operating systems: `Windows 10`_,
macOS_. For Linux: read the manual that belongs to your distribution. Blink.sh_ should
work out of the box.

Installation
============

To install the prebuilt binary you first need to download the install script from the project's
website via ``curl``.

.. code-block:: console

 [isabell@stardust ~]$ curl -fsSL https://starship.rs/install.sh -o install-starship.sh
 isabell on stardust in ~

Once you have the file, in order to be able to run the script, you need to set the executable bit.

.. code-block:: console

 [isabell@stardust ~]$ chmod +x install-starship.sh
 isabell on stardust in ~

Afterwards, you can install Starship_ and run it.

.. code-block:: console

 [isabell@stardust ~]$ ./install-starship.sh --bin-dir ~/bin --yes
 [...]
 [isabell@stardust ~]$ eval "$(~/bin/starship init bash)"
 isabell on stardust in ~

To make the new prompt permanent, add a newline and the below eval statement to your ``~/.bashrc``:

.. code-block:: console

 eval "$(~/bin/starship init bash)"

That's it, you have successfully installed Starship_ to your Uberspace console:

.. code-block:: console

 [isabell@localhost ~]$ ssh isabell@stardust
 Welcome to Uberspace7!
 [...]
 isabell on stardust in ~

To start customizing your prompt, have a look at `Starship's Presets`_'. The configuration file lives
in ``~/.config/starship.toml``.

.. _Starship: https://starship.rs/
.. _`Starship's Presets`: https://starship.rs/presets/#presets
.. _`Nerd Font`: https://www.nerdfonts.com/
.. _NerdFonts: https://www.nerdfonts.com/font-downloads
.. _`Windows 10`: https://support.microsoft.com/en-us/help/314960/how-to-install-or-remove-a-font-in-windows
.. _macOS: https://support.apple.com/en-us/HT201749
.. _blink.sh: https://blink.sh/

Tested with Starship v1.3.0 and Uberspace version 7.12.

.. author_list::
