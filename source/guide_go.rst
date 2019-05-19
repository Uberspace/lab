.. highlight:: console

.. author:: Raphael Höser <raphael@hoeser.info

.. categorize your guide! refer to the manual for the current list of tags: https://manual.uberspace.de/tags
.. tag:: lang-go

.. sidebar:: About

  .. image:: _static/images/go.svg
      :align: center

###
Go
###

.. tag_list::

Go_, also known as Golang, is a statically typed, compiled programming language designed at Google by Robert Griesemer, Rob Pike, and Ken Thompson. Go_ is syntactically similar to C, but with memory safety, garbage collection, structural typing, and CSP-style concurrency.

License
=======

Golang is distrubuted under a BSD style license.

All relevant legal information can be found here

  * https://golang.org/LICENSE

Installation
============

Download go binary for linux, amd64
-----------------------------------

In this guide we install go 1.12.5. In the future you might want to change the version to the most current version.

Check the download_ page for the newest version.

::

 [isabell@stardust ~]$ wget -O ~/go.tar.gz https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz
 [isabell@stardust ~]$

Extract Go archive
------------------

We extract the go archive to the home directory as it creates a directory called "go" which we'll use as the go root directory.

::

 [isabell@stardust ~]$ tar -xzf go.tar.gz
 [isabell@stardust ~]$

Setup environment variables
---------------------------

To use go we need to add ~/go/bin to the path environment variable and persist that change for the next shell session (your next login to your uberspace).

Add the following to the end of your ~/.bashrc:

::

 export PATH=$PATH:$HOME/go/bin

After that reload your .bashrc:

::

 [isabell@stardust ~]$ source ~/.bashrc
 [isabell@stardust ~]$

Finishing installation
======================

Now you can test your go installation by running "go version" and building a test program.

Updates
=======

.. note:: Check the download_ page regularly to stay informed about the newest version.

.. _Go: https://golang.org/
.. _download: https://golang.org/dl/

To Update go you just need to delete ~/go and redo the installation without editing the .bashrc file (skip the step "Setup environment variables").

----

Tested with Go 1.12.5

.. author_list::
