.. highlight:: console

.. author:: Michael Behrisch <oss@behrisch.de>

.. tag:: lang-c
.. tag:: mail
.. tag:: mailinglist

#########
ezmlm-idx
#########

.. tag_list::

ezmlm_ is a set of programs to run mailing lists either from a web interface, via mail or from the command line.
It can be used as an alternative to Mailman.
This guide covers only the command line and the mail interface, not the web. It does not use a database but just
flat files. For using a database and the web see the detailed docs.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Mailing lists
  * Compiling a C program using Makefiles

License
=======

ezmlm_ was written by Fred Lindberg, Fred B. Ringel, and Bruce Guenter and released under GPLv2.


Installation
============

Step 1
------

Download the latest version of ezmlm_ from the website https://untroubled.org/ezmlm/, extract it and enter the directory:

::

 [isabell@stardust ~] wget https://untroubled.org/ezmlm/archive/7.2.2/ezmlm-idx-7.2.2.tar.gz
 [isabell@stardust ~] tar -xzf ezmlm-idx-7.2.2.tar.gz
 [isabell@stardust ~] cd ezmlm-idx-7.2.2/
 [isabell@stardust ezmlm-idx-7.2.2]

Step 2
------

Change the configuration by editing the ``conf-*`` files using a text editor. It is usually sufficient to change the following files: ``conf-bin`` to

::

 /home/isabell/bin

``conf-etc`` to

::

 /home/isabell/etc/ezmlm

``conf-lib`` to

::

 /home/isabell/lib/ezmlm

``conf-man`` to

::

 /home/isabell/man

Then run

::

 [isabell@stardust ezmlm-idx-7.2.2] make
 [...]
 [isabell@stardust ezmlm-idx-7.2.2] make man
 [...]
 [isabell@stardust ezmlm-idx-7.2.2] ./ezmlm-test
 getconfopt library:   OK
 ezmlm-make:           OK
 Using subdb plugin:   std
 [...]
 ezmlm-send:           OK
 ezmlm-send (from):    OK
 ezmlm-send trailer:   OK
 omitbottom (-manage): OK
 omitbottom (-get):    OK
 Cleaning up...
 [isabell@stardust ezmlm-idx-7.2.2]


The test call should show that everything is OK. Also ``man ezmlm-make`` should work.
If not, check the output of the respective commands for errors.


Configuration and Usage
=======================

General setup
-------------

ezmlm_ comes with templates for the administrative messages it sends. They are installed in the directory configured in ``conf-etc`` above. To change a message you can edit the files directly. To set a new default language change the ``default`` symbolic link to point to the subdirectory with the chosen language.
It is advisable to keep the lists in a separate directory where ezmlm_ will create subdirectories for every single list:

::

 [isabell@stardust ~] mkdir lists
 [isabell@stardust ~]

Adding / removing a mailing list
--------------------------------

Most administrative commands need to be done from the command line using different tools.
In order to add a remotely administered list (-r) without an archive (-A) with the list owner ``owner@domain.org`` and the list address ``mylist@isabell.uber.space`` you can do:

::

 [isabell@stardust ~] ezmlm-make -rA -5 owner@domain.org ~/lists/mylist ~/.qmail-mylist mylist isabell.uber.space
 [isabell@stardust ~]

This will add the directory ``~/lists/mylist`` where everything concerning this list will be stored and setup all necessary ``.qmail-mylist`` files.

To remove the list simply delete the directory ``~/lists/mylist`` and the ``.qmail-mylist*`` files.

::

 [isabell@stardust ~] rm -rf ~/lists/mylist ~/.qmail-mylist*
 [isabell@stardust ~]


Subscribing / Unsubscribing
---------------------------

Users can either subscribe thenselves to a list by writing an email to ``mylist-subscribe@isabell.uber.space`` or can be added from the command line:

::

 [isabell@stardust ~] ezmlm-sub ~/lists/mylist user@otherdomain.org
 [isabell@stardust ~]

To unsubscribe write an email to ``mylist-unsubscribe@isabell.uber.space`` or use:

::

 [isabell@stardust ~] ezmlm-unsub ~/lists/mylist user@otherdomain.org
 [isabell@stardust ~]


ezmlm_ can do many more things such as subscriber only lists, list moderation etc. Have a look at the man page for ezmlm-make or at the online documentation for details.


.. _ezmlm: https://untroubled.org/ezmlm/

.. author_list::
