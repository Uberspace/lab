.. author:: tobimori <tobias@moeritz.cc>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: ide
.. tag:: collaborative-editing 

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/code.svg
      :align: center

#############
code-server
#############

.. tag_list::

code-server_  is `VS Code`_ running on a remote server, in this guide your Uberspace, accessible through the browser.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

code-server_ is released under the `MIT License`_.

Prerequisites
=============

Setup your Domain:

.. include:: includes/web-domain-list.rst

Installation
=============

Create a new folder for code-server_ in your home directory and switch into it.

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/code-server && cd ~/code-server
  [isabell@stardust code-server]$ 


Then download the latest release_ for x86_64:

.. code-block:: console

  [isabell@stardust code-server]$ wget https://github.com/cdr/code-server/releases/download/3.1.0/code-server-3.1.0-linux-x86_64.tar.gz
  [...]
  ‘code-server-3.1.0-linux-x86_64.tar.gz’ saved
  [isabell@stardust code-server]$


Then extract the files in the current folder with ``tar``. Don't forget ``--strip-components=1`` to remove the ``code-server-3.1.0-linux-x86_64`` prefix from the path.

.. code-block:: console

  [isabell@stardust code-server]$ tar -xzf code-server-3.1.0-linux-x86_64.tar.gz --strip-components=1
  [isabell@stardust code-server]$

You can now delete the archive:

.. code-block:: console

  [isabell@stardust code-server]$ rm code-server-3.1.0-linux-x86_64.tar.gz
  [isabell@stardust code-server]$

Setup daemon
====================

.. note::

    Be aware that almost all configuration of code-server_ happens via command line arguments and so in this file.

Create ``~/etc/services.d/code-server.ini`` with the following content. 
Make sure to `<password>` with your password.

.. code-block:: ini
  :emphasize-lines: 3

  [program:code-server]
  command=%(ENV_HOME)s/code-server/code-server --host 127.0.0.1 --port 8080 --user-data-dir %(ENV_HOME)s/code-server --auth password
  environment=PASSWORD=<password>
  autorestart=true
  autostart=true

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.

Configure web backend
==========================

.. note::

    code-server_ is running on port 8080 in the default configuration. If you want or need to use another port, you can change that in the :manual:`supervisord <daemons-supervisord>` daemon file we created above.

.. include:: includes/web-backend.rst

.. _`VS Code`: https://code.visualstudio.com/
.. _code-server: https://github.com/cdr/code-server
.. _release: https://github.com/cdr/code-server/releases/latest
.. _MIT License: https://github.com/cdr/code-server/blob/master/LICENSE.txt

----

Tested with code-server 3.1.0 on Uberspace 7.5.1.

.. author_list::
