.. highlight:: console

.. author:: luto <http://luto.at>

.. tag:: lang-c
.. tag:: lang-scheme

###########
Chez Scheme
###########

.. tag_list::

.. abstract::
  `Chez Scheme`_ is a programming language, a dialect and implementation of the language Scheme which is a type of Lisp.

License
=======

All relevant legal information can be found here:

  * https://github.com/cisco/ChezScheme/blob/main/LICENSE

Installation
============

Download and extract the source:

::

 [isabell@stardust ~]$ wget https://github.com/cisco/ChezScheme/releases/download/v9.5.4/csv9.5.4.tar.gz
 [isabell@stardust ~]$ tar xf csv9.5.4.tar.gz
 [isabell@stardust ~]$ cd csv9.5.4/

Compile and install:

::

 [isabell@stardust csv9.5.4]$ ./configure --installprefix=$HOME
 [isabell@stardust csv9.5.4]$ make -j2
 (cd a6le && make build)
 (cd c && make)
 ln -s ../../c/statics.c statics.c
 ln -s ../../c/system.h system.h
 ln -s ../../c/types.h types.h
 (...)
 make restoreboot
 mv -f ../boot/a6le/sbb ../boot/a6le/petite.boot
 mv -f ../boot/a6le/scb ../boot/a6le/scheme.boot
 make resetbootlinks
 touch bootstrap
 [isabell@stardust csv9.5.4]$ make install
 (cd a6le && make install)
 (cd c && make)
 make[2]: Nothing to be done for 'doit'.
 (...)
 ./installsh -o "" -g "" -m 444 examples/* /home/dbcheck/lib/csv9.5.4/examples
 ./installsh -o "" -g "" -m 444 boot/a6le/kernel.o /home/dbcheck/lib/csv9.5.4/a6le
 [isabell@stardust csv9.5.4]$

Test the binary:

::

 [isabell@stardust csv9.5.4]$ scheme --version
 9.5.4

Remove the source files:

::

 [isabell@stardust csv9.5.4]$ cd ..
 [isabell@stardust ~]$ rm -rf csv9.5.4.tar.gz csv9.5.4/

Updates
=======

.. note:: `Release log`_ regularly to stay informed about the newest version.

To update an existing installation, rerun the installation steps.

.. _`Chez Scheme`: https://cisco.github.io/ChezScheme/
.. _`Release log`: https://github.com/cisco/ChezScheme/releases

----

Tested with ChezScheme 9.4.5, Uberspace 7.10.0

.. author_list::
