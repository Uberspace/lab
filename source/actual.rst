.. author:: knhash <https://knhash.in>

.. tag:: accounting
.. tag:: personal-finance
.. tag:: web

.. sidebar:: Logo

    .. image:: _static/images/actual.png
      :align: center

.. highlight:: console

###########
Actual
###########

.. tag_list::

`Actual Budget`_ is a super fast and privacy-focused app for managing your finances. At its heart is the well proven and much loved Envelope Budgeting methodology.

**You own your data** and can do whatever you want with it. Featuring multi-device sync, optional end-to-end encryption and so much more.

Here is the code `Repository`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`the shell <basics-shell>`
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============
Your website domain or subdomain needs to be setup up:

.. include:: includes/web-domain-list.rst


Installation
============

This installation broadly follows the `Quick Start Guide`_.

First you need to clone the Actual Server project to your machine, you can do this using Git.

::

  [isabell@stardust ~]$ git clone https://github.com/actualbudget/actual-server.git

Once you have it cloned, navigate to the directory where you cloned the project

::

  [isabell@stardust ~]$ cd actual-server

Install all the dependencies using `yarn`

::

  [isabell@stardust ~]$ yarn install


Configuration
=============

Setup daemon
------------
Create ``~/etc/services.d/actual.ini`` with the following content:

.. code-block:: ini

  [program:actual]
  directory=%(ENV_HOME)s/actual-server
  command=yarn start
  autostart=true
  autorestart=true
  stopsignal=INT

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::

    Actual is running on port ``5006``.

.. include:: includes/web-backend.rst


Updates
=======

When we publish a new release, you’ll need to follow these steps to update:

1. Stop the server if it’s running. You can use the keyboard shortcut ``Ctrl C`` (even on macOS) to stop the server, or close the terminal window it’s running from.
2. Run ``git pull`` from the directory you cloned the project into. This will download the latest server code.
3. Run ``yarn install`` from that same directory. This will download the latest web client code, along with any updated dependencies for the server.
4. Restart the server by running ``supervisorctl restart actual``.


.. _Actual Budget: https://actualbudget.org/
.. _Repository:  https://github.com/actualbudget/actual-server
.. _Quick Start Guide: https://actualbudget.org/docs/install/local

----

Tested with Actual 23.12.0, Uberspace 7.15.4

.. author_list::
