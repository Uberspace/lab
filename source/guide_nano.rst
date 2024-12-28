.. highlight:: console
.. author:: Marc Redwerkz <wzrd.pw>

.. tag:: text-editor

.. sidebar:: Logo

  .. image:: _static/images/nano.svg
      :align: center

.. spelling:wordlist:
  nano
  Nano
  nano-editor

########
GNU nano
########

.. tag_list::

GNU nano is a user-friendly text editor for Unix-like systems, known for its simplicity and ease of use.
It comes preinstalled on your Uberspace, but the version is outdated and lacks features like emoji support.

----

License
=======

nano_ is published under a `copyleft GNU General Public License`_.

Preinstalled version
====================

::

Check nano version by typing:

::

 [isabell@stardust ~]$ nano --version
 GNU nano version 2.3.1 (compiled 04:47:52, Jun 10 2014)
 (C) 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
 2008, 2009 Free Software Foundation, Inc.
 Email: nano@nano-editor.org    Web: http://www.nano-editor.org/
 Compiled options: --enable-color --enable-extra --enable-multibuffer --enable-nanorc --enable-utf
 [isabell@stardust ~]$

::

Prerequisites
=============

`$HOME/.local/bin`needs to be included in your `$PATH`. If it's not already, 
add this line to your shell config file ``$HOME/.bashrc`` or ``$HOME/.zshrc``:

.. code-block:: sh

  PATH="$HOME/.local/bin:$PATH"

.. note::

Make sure `$HOME/.local/bin` is added to the front of your $PATH.

Build from source
=================

Fetch latest version
--------------------

Scrape latest version from website

.. code-block:: console

[isabell@stardust ~]$ latest=$(curl -s "https://nano-editor.org" | grep -Po '\K[0-9]+(\.[0-9]+)+' | sort -r -V | head -n1)
[isabell@stardust ~]$
                               
Download source code
--------------------

Check current version of nano at downloads_

.. code-block:: console

[isabell@stardust ~]$ wget -O nano-${latest}.tar.xz https://nano-editor.org/dist/v8/nano-${latest}.tar.xz 
[...]
Saving to: ‘nano-8.3.tar.xz’

100%[=======================================================>] 1,681,216   --.-K/s   in 0.1s     

2024-12-28 19:55:23 (16.1 MB/s) - ‘nano-8.3.tar.xz’ saved [1681216/1681216]

[isabell@stardust ~]$

Extract source code
-------------------

Extract the downloaded source code:

.. code-block:: console

  [isabell@stardust ~]$ tar --extract --file nano-${latest}.tar.xz
  [isabell@stardust ~]$

Configure build
---------------

Set a `prefix` to a location in your home dir.
You can then run `make install` without sudo:
                               
.. code-block:: console

  [isabell@stardust ~]$ cd nano-${latest}
  [isabell@stardust ~]$ ./configure --prefix="$HOME/.local/nano"
  [...]
  
    The global nanorc file is: /home/isabell/.local/nano/etc/nanorc
    Syntaxes get installed in: /home/isabell/.local/nano/share/nano/
                               
  [isabell@stardust ~]$ 

Build and install binary
------------------------

Compile multiple jobs in parallel to speed up the process,
but note that using more jobs may actually slow it down:
                               
.. code-block:: console

  [isabell@stardust ~]$ make -j3 && make install  
  [isabell@stardust ~]$ nano --version
   GNU nano, version 8.3
   (C) 2024 the Free Software Foundation and various contributors
   Compiled options: --enable-utf8
  [isabell@stardust ~]$ 

.. note::

You may need to restart you shell or log out and in again.
                               
.. _nano https://nano-editor.org
.. _downloads: https://nano-editor.org/download.php
.. _copyleft: https://nano-editor.org/dist/latest/COPYING

----

Tested with nano 8.3, Uberspace 7.16.3

.. author_list::
