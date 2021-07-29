.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: wiki
.. tag:: web
.. tag:: lang-javascript

.. sidebar:: Logo

  .. image:: _static/images/tiddlywiki.svg
      :align: center

##########
TiddlyWiki
##########

.. tag_list::

TiddlyWiki_ is a personal wiki and a non-linear notebook for organising and sharing complex information.

License
=======

TiddlyWiki_ is published under a `permissive BSD 3-Clause License`_.

Prerequisites
=============

If you want to use TiddlyWiki with your own domain you need to setup your domain first:

.. include:: includes/web-domain-list.rst

Installation
============

Install the Node package
------------------------
TiddlyWiki is installed via Nodes package manager `npm`:

::

 [isabell@stardust ~]$ npm install -g tiddlywiki
 [...]
 + tiddlywiki@5.1.23
 added 1 package from 1 contributor in 5.102s
 [isabell@stardust ~]$

Check if TiddlyWiki is installed by typing:

::

 [isabell@stardust ~]$ tiddlywiki --version
 5.1.23
 [isabell@stardust ~]$

Create a new wiki
-----------------
The following commands creates a folder in your home directory for TiddlyWiki. After that, a new wiki folder (named ``mynewwiki`` in this example) containing server-related components is created.

::

 [isabell@stardust ~]$ mkdir tiddlywiki
 [isabell@stardust ~]$ cd tiddlywiki
 [isabell@stardust tiddlywiki]$ tiddlywiki mynewwiki --init server
 Copied edition 'server' to mynewwiki
 [isabell@stardust tiddlywiki]$ ls
 mynewwiki
 [isabell@stardust tiddlywiki]$

Setup a web backend
-------------------

.. note::

    TiddlyWiki is running on port 8080.

.. include:: includes/web-backend.rst

Configure permissions
---------------------
By default, anonymous users can read and edit the tiddlers.

To restrict the permissions, add a users file named ``myusers.csv`` into the `tiddlywiki` folder:

::

 [isabell@stardust ~]$ cd tiddlywiki
 [isabell@stardust tiddlywiki]$ touch myusers.csv

Use your favorite editor to add a comma seperated list of usernames and passwords (as cleartext) into the created file. The first header row ``username,password`` must be added.

::

 username,password
 jane,do3
 andy,sm1th
 roger,m00re

You can assign the users to the group ``readers`` (reading access only) or to the group ``writers`` (writing access) in the service configuration (see next step).

Setup TiddlyWiki as service
---------------------------

You should set up a service that keeps TiddlyWiki alive while you are gone. Create the file ``~/etc/services.d/tiddlywiki.ini`` with the following content:

.. code-block:: ini

 [program:tiddlywiki]
 command=tiddlywiki %(ENV_HOME)s/tiddlywiki/mynewwiki --listen host=0.0.0.0 credentials=%(ENV_HOME)s/tiddlywiki/myusers.csv readers=jane,andy writers=andy
 autostart=true
 autorestart=true
 stopsignal=INT

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.


Access your TiddlyWiki
----------------------
Now point your Browser to your installation URL ``https://isabell.uber.space``.


Update
======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Use the `npm` tool to update the TiddlyWiki installation:

::

 [isabell@stardust ~]$ servicectl stop tiddlywiki
 tiddlywiki: stopped
 [isabell@stardust ~]$ npm update -g tiddlywiki
 [...]
 [isabell@stardust ~]$ servicectl start tiddlywiki
 tiddlywiki: started
 [isabell@stardust ~]$

Backup
======

Backup the following directories:

  * ``~/tiddlywiki/``

Debugging
=========

In case of problems, the log file ``~/logs/supervisord.log`` is the first point for you.

Moreover, the ``tiddlywiki`` binary offers the ``--verbose`` parameter.


.. _TiddlyWiki: https://tiddlywiki.com/
.. _permissive BSD 3-Clause License: https://github.com/Jermolene/TiddlyWiki5/blob/master/license
.. _feed: https://github.com/Jermolene/TiddlyWiki5/releases.atom


----

Tested with TiddlyWiki 5.1.23, Uberspace 7.9.0.0

.. author_list::
