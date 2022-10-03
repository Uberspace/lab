.. highlight:: console

.. author:: on4r <https://github.com/on4r>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: web
.. tag:: file-storage
.. tag:: self-hosting

.. sidebar:: Logo

  .. image:: _static/images/filebrowser.png
      :align: center

############
File Browser
############

.. tag_list::

`File Browser`_ provides a file managing interface within a specified directory and it can be used to upload, delete, preview, rename and edit your files.
It allows the creation of multiple users and each user can have its own directory. It can be used as a standalone app or as a middleware.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

File Browser is licensed under the `Apache License 2.0`_

Installation
============

Download and extract the `latest release`_
------------------------------------------

.. code-block:: console

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ curl --location <url_of_linux_amd64_filebrowser> | tar -xzf - filebrowser

Initialize a new database
-------------------------

.. code-block:: console

 [isabell@stardust bin]$ cd ~
 [isabell@stardust ~]$ mkdir filebrowser && cd filebrowser
 [isabell@stardust filebrowser]$ filebrowser config init


Configuration
=============

.. note:: You have to be in the same directory as the *filebrowser.db* file which you created before, in order to configurate it or else it will create a new one.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser config set --address 0.0.0.0
 [isabell@stardust filebrowser]$ filebrowser config set --root $HOME/my_files

Create your admin account.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser users add '<username>' '<password>' --perm.admin

Create a new `uberspace web backend`_.

.. code-block:: console

 [isabell@stardust filebrowser]$ uberspace web backend set / --http --port 8080

Create your file folder (the one you specified via the ``--root`` option).

.. code-block:: console

 [isabell@stardust filebrowser]$ mkdir ~/my_files

At this point you should check if everything is working as expected by starting manually.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser --database $HOME/filebrowser/filebrowser.db

File Browser should now be running on port ``8080``.

.. note:: Changes to the configuration via the CLI can not be done while the server is running as the database access is blocked by the instance.

Add service
-----------

Create ``~/etc/services.d/filebrowser.ini`` with the following content:

.. code-block:: ini

 [program:filebrowser]
 directory=%(ENV_HOME)s/filebrowser
 command=filebrowser
 startsecs=30
 autostart=yes

.. include:: includes/supervisord.rst

**DONE!**

.. _`File Browser`: https://github.com/filebrowser/filebrowser
.. _`Apache License 2.0`: https://github.com/filebrowser/filebrowser/blob/master/LICENSE
.. _`latest release`: https://github.com/filebrowser/filebrowser/releases/latest
.. _`uberspace web backend`: https://manual.uberspace.de/web-backends.html
.. _service: https://manual.uberspace.de/daemons-supervisord

----

Tested with File Browser 2.22.4 on Uberspace 7.13.0

.. author_list::
