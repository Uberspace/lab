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

.. note:: In most cases it will work totally fine to (cross-) compile your application for GOOS=linux and GOARCH="amd64" on your local device and upload the result to your uberspace as this wouldn't need a go installation on your uberspace (see `cross compiling go`_ for a guide). If that doesn't work for you, feel free to follow this guide.

Installation
============

Download go binary for linux, amd64
-----------------------------------

In this guide we install go 1.12.5. In the future you might want to change the version to the most current version.

Check the download_ page for the newest version.

::

 [isabell@stardust ~]$ wget -O ~/go.tar.gz https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz
 --2019-05-23 13:16:46--  https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz
 Resolving dl.google.com (dl.google.com)... 74.125.206.93, 74.125.206.190, 74.125.206.136, ...
 Connecting to dl.google.com (dl.google.com)|74.125.206.93|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 127938445 (122M) [application/octet-stream]
 Saving to: ‘/home/isabell/go.tar.gz’
 
 100%[=====================================================>]  127,938,445  148MB/s   in 0.8s
 
 2019-05-23 13:16:47 (148 MB/s) - ‘/home/isabell/go.tar.gz’ saved [127938445/127938445]
 
 [isabell@stardust ~]$

Extract Go archive
------------------

We extract the go archive to the home directory as it creates a directory called "go" which we'll use as the go root directory.

::

 [isabell@stardust ~]$ tar -xzf go.tar.gz
 [isabell@stardust ~]$

Setup environment variables
---------------------------

To use go we need to add ``~/go/bin`` to the path environment variable and persist that change for the next shell session (your next login to your uberspace).

Add the following to the end of your ``~/.bashrc``:

::

 export PATH=$PATH:$HOME/go/bin

After that reload your ``.bashrc``:

::

 [isabell@stardust ~]$ source ~/.bashrc
 [isabell@stardust ~]$

Finishing installation
======================

Now you can test your go installation by running "go version" and building a test program.

::

 [isabell@stardust ~]$ go version
 go version go1.12.5 linux/amd64
 [isabell@stardust ~]$


Updates
=======

.. note:: Check the download_ page regularly to stay informed about the newest version.

.. _Go: https://golang.org/
.. _download: https://golang.org/dl/
.. _`cross compiling go`: https://golangcookbook.com/chapters/running/cross-compiling/

To Update go you just need to delete ~/go and redo the installation without editing the .bashrc file (skip the step "Setup environment variables").

----

Tested with Go 1.12.5

.. author_list::
