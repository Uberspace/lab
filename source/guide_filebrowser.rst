.. highlight:: console

.. author:: on4r <https://github.com/on4r>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: web
.. tag:: file-storage
.. tag:: self-hosting

.. sidebar:: Logo

  .. image:: _static/images/filebrowser.png
      :align: center

##########
File Browser
##########

.. tag_list::

filebrowser_ provides a file managing interface within a specified directory and it can be used to upload, delete, preview, rename and edit your files.
It allows the creation of multiple users and each user can have its own directory. It can be used as a standalone app or as a middleware.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

filebrowser is licensed under the `Apache License 2.0`_

Installation
============

Download and extract the `latest release`_
-------------------

.. code-block:: console

 [isabell@stardust ~]$ cd ~/bin
 [isabell@stardust bin]$ wget <url_of_linux_amd64_filebrowser>
 [isabell@stardust bin]$ tar -xzf linux-amd64-filebrowser.tar.gz

Initialize a new database
-------------------------

.. code-block:: console

 [isabell@stardust bin]$ cd ~
 [isabell@stardust ~]$ mkdir filebrowser && cd filebrowser
 [isabell@stardust filebrowser]$ filebrowser config init


Configuration
=============

.. note:: You have to be in the same directory as the *filebrowser.db* file which you created before, in order to configurate it or else it will create a new one.
.. note:: Check your running web backends (``uberspace web backend list``) and choose a free port between 1024 and 65535.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser config set --port 1337
 [isabell@stardust filebrowser]$ filebrowser config set --address 0.0.0.0
 [isabell@stardust filebrowser]$ filebrowser config set --baseurl /my_files
 [isabell@stardust filebrowser]$ filebrowser config set --root /home/<username>/html/my_files

Create your admin account.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser users add <username> <password> --perm.admin

Create a new `uberspace web backend`_.

.. code-block:: console

 [isabell@stardust filebrowser]$ uberspace web backend set /my_files --http --port 1337 --remove-prefix

Create your file folder (the one you specified via the ``--root`` option).

.. code-block:: console

 [isabell@stardust filebrowser]$ mkdir ~/html/my_files

At this point you should check if everything is working as expected by starting the filebrowser manually.

.. code-block:: console

 [isabell@stardust filebrowser]$ filebrowser --database $HOME/filebrowser/filebrowser.db

You should now be presented with a login mask under the path you specified before as ``--baseurl``. In our case this would be ``isabell.uber.space/my_files``

All fine? Then we can create a new service_.

.. code-block:: console

 [isabell@stardust filebrowser]$ touch ~/etc/services.d/filebrowser.ini

.. code-block:: ini

 [program:filebrowser]
 command=%(ENV_HOME)s/bin/filebrowser --database %(ENV_HOME)s/filebrowser/filebrowser.db
 autostart=yes

Now reread, start and check the service.

.. code-block:: console

 [isabell@stardust filebrowser]$ supervisorctl reread
 [isabell@stardust filebrowser]$ supervisorctl update
 [isabell@stardust filebrowser]$ supervisorctl status

**DONE!**

.. _filebrowser: https://github.com/filebrowser/filebrowser
.. _`Apache License 2.0`: https://github.com/filebrowser/filebrowser/blob/master/LICENSE
.. _`latest release`: https://github.com/filebrowser/filebrowser/releases/latest
.. _`uberspace web backend`: https://manual.uberspace.de/web-backends.html
.. _service: https://manual.uberspace.de/daemons-supervisord

----

Tested with filebrowser 2.22.4 on Uberspace 7.13.0

.. author_list::
