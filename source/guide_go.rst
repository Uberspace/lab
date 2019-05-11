.. highlight:: console

.. author:: Cornelius <https://github.com/ces92>

.. tag:: golang
.. tag:: go

.. sidebar:: Logo

  .. image:: _static/images/golang.svg
      :align: center

##########
Go
##########

.. tag_list::

Go_ is an open source programming language that makes it easy to build simple, reliable, and efficient software.

----

License
=======

All relevant legal information can be found here

  * https://golang.org/LICENSE


Installation
============

Step 1
------
Install Linuxbrew
::

 [isabell@stardust ~]$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
 [...]
 [isabell@stardust ~]$ Warning: /home/isabell/.linuxbrew/bin is not in your PATH.
 [isabell@stardust ~]$

Add Linuxbrew PATH to ``~/.bash_profile``:

::

 [isabell@stardust ~]$ test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
 [isabell@stardust ~]$

Reload the ``.bash_profile`` with:

::

 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$



Step 2
------
Install Go
::

 [isabell@stardust ~]$ brew install go
 [...]
 [isabell@stardust ~]$ 🍺  /home/qwerr/.linuxbrew/Cellar/go/1.12.4: 9,796 files, 454.7MB, built in 4 minutes 1 second
 [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use ``Linuxbrew`` to update Go:
::

 [isabell@stardust ~]$ brew update
 [isabell@stardust ~]$ brew upgrade go
 [...]
 [isabell@stardust ~]$

.. _Go: https://golang.org/
.. _feed: https://github.com/golang/go/releases.atom

----

Tested with Go 1.12.4, Uberspace 7.2.10

.. author_list::
