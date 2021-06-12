.. highlight:: console

.. author:: Michael Behrisch <oss@behrisch.de>

.. tag:: lang-c
.. tag:: mail
.. tag:: mailinglist

#########
ezmlm-idx
#########

.. tag_list::

.. abstract::
  ezmlm_ is a set of programs to run mailing lists either from a web interface, via mail or from the command line.
  It can be used as an alternative to Mailman.
  This guide covers only the command line and the mail interface, not the web. It does not use a database but just
  flat files. For using a database and the web see the detailed docs.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Mailing lists
  * Compiling a C program using Makefiles


.. note:: When adding yourself to the list and test sending emails, be aware that GMail silently drops mails sent by yourself when they arrive again via the mailing list. One could think that there is a flaw in the uberspace qmail configuration sending out emails!


License
=======

ezmlm_ was written by Fred Lindberg, Fred B. Ringel, and Bruce Guenter and released under GPLv2.


Installation
============

Download the latest version of ezmlm_ from the website https://untroubled.org/ezmlm/, extract it and enter the directory:

::

 [isabell@stardust ~] wget https://untroubled.org/ezmlm/archive/7.2.2/ezmlm-idx-7.2.2.tar.gz
 [isabell@stardust ~] tar -xzf ezmlm-idx-7.2.2.tar.gz
 [isabell@stardust ~] cd ezmlm-idx-7.2.2/
 [isabell@stardust ezmlm-idx-7.2.2]

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


The test call should show that everything is OK. Now create directories and install everything in the correct locations

::

 [isabell@stardust ezmlm-idx-7.2.2] mkdir -p $HOME/{lib,etc}
 [isabell@stardust ezmlm-idx-7.2.2] make install
 [...]
 [isabell@stardust ezmlm-idx-7.2.2]

You can run ezmlm-test again if you wish. Now also ``man ezmlm-make`` should work.
If not, check the output of the respective commands for errors.


Configuration and Usage
=======================

It is advisable to keep the lists in a separate directory where ezmlm_ will create subdirectories for every single list:

::

 [isabell@stardust ~] mkdir lists
 [isabell@stardust ~]

Adding / removing a mailing list
--------------------------------

The tool to add a list and to change options afterwards is `ezmlm-make`. It needs four arguments:

1. the directory inside above created ``~/lists``
2. the prefix for .qmail-files
3. the local alias (the part before the ``@``)
4. the hostname (the part after the ``@``)

List-specific settings need to be passed as command line options. Here are some of the most common ones:

``-u``
    User posts. Only addresses that are subscribed to the list may send messages.
``-m``
    Message moderation. Every mail must be approved by a moderator.
``-s``
    Subscription moderation. Every new subscriber must be approved by a moderator.
``-5 owner@domain.org``
    Set the address of the list owner.
``-a``
    Create a list archive.

.. note:: A common setup is to allow subscribers to post to the list and hold messages by any other address in moderation. For this setup you need to apply both ``-u`` and ``-m``.

To **turn off** options, the according **capitalized** option must be used.

The command to add a new list ``mylist@isabell.uber.space`` with the list owner ``owner@domain.org`` without an archive (-A) that allows subscribers to post (-u) and holds foreign senders in moderation (-m) looks like this:

::

 [isabell@stardust ~] ezmlm-make -A -u -m -5 owner@domain.org ~/lists/mylist ~/.qmail-mylist mylist isabell.uber.space
 [isabell@stardust ~]

This will add the directory ``~/lists/mylist`` where everything concerning this list will be stored and setup all necessary ``.qmail-mylist…`` files.

To remove the list simply delete the directory ``~/lists/mylist`` and the ``.qmail-mylist*`` files.

::

 [isabell@stardust ~] rm -rf ~/lists/mylist ~/.qmail-mylist*
 [isabell@stardust ~]


Change options
--------------

If you want to change any of the options, use the option ``-+``. Note that all the other arguments from the creation are required here as well. To turn the archive back on, you need to do:

::

 [isabell@stardust ~] ezmlm-make -+ -a ~/lists/mylist ~/.qmail-mylist mylist isabell.uber.space
 [isabell@stardust ~]



Subscribing / Unsubscribing
---------------------------

Users can either subscribe themselves to a list by writing an email to ``mylist-subscribe@isabell.uber.space`` or can be added from the command line:

::

 [isabell@stardust ~] ezmlm-sub ~/lists/mylist user@otherdomain.org
 [isabell@stardust ~]

To unsubscribe write an email to ``mylist-unsubscribe@isabell.uber.space`` or use:

::

 [isabell@stardust ~] ezmlm-unsub ~/lists/mylist user@otherdomain.org
 [isabell@stardust ~]


ezmlm_ can do many more things such as subscriber only lists, list moderation etc. Have a look at the man page for ezmlm-make or at the online documentation for details.



Moderators
----------

Moderators will receive mails if messages are held for moderation (``-m``). Adding moderators is similar to adding subscribers using ``ezmlm-sub`` and ``ezmlm-unsub``, with one additional argument ``mod``:

::

 [isabell@stardust ~] ezmlm-sub ~/lists/mylist mod moderator@theirdomain.org
 [isabell@stardust ~]



Allow other addresses
---------------------

Allowing and removing other addresses to bypass moderation on a subscriber-only list (``-m -u``) is also similar to adding subscribers, with one additional argument ``allow``:

::

 [isabell@stardust ~] ezmlm-sub ~/lists/mylist allow alloweduser@otherdomain.org
 [isabell@stardust ~]


Language and custom messages
----------------------------

ezmlm_ comes with templates for the administrative messages it sends. They are installed in the directory configured in ``conf-etc`` above. To change a message you can edit the files directly. To set a new default language change the ``default`` symbolic link to point to the subdirectory with the chosen language.

To set another language (e.g. ``de``), use the ``-C`` option:

::

 [isabell@stardust ~] ezmlm-make -C ~/etc/ezmlm/de ~/lists/mylist ~/.qmail-mylist mylist isabell.uber.space
 [isabell@stardust ~]



.. _ezmlm: https://untroubled.org/ezmlm/


.. author_list::
