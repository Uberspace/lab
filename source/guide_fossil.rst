.. author:: tux0r <https://tuxproject.de>

.. tag:: lang-c
.. tag:: audience-developers
.. tag:: version-control

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/fossil.png
      :align: center

######
Fossil
######

.. tag_list::

Fossil_ is a simple, high-reliability, distributed SCM system with a built-in web interface, including a wiki, a ticket system, a forum and more.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Your Fossil web URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Fossil is distributed as a single binary, which in this case is the server and the client component. Download Fossil's latest release_ and extract it.

::

  [isabell@stardust ~]$ mkdir ~/fossil
  [isabell@stardust ~]$ wget https://fossil-scm.org/home/uv/fossil-linux-x64-2.24.tar.gz
  [...]
  [isabell@stardust ~]$ tar -xzf fossil-linux-x64-2.24.tar.gz -C ~/fossil/
  [isabell@stardust ~]$ rm fossil-linux-x64-2.24.tar.gz
  [isabell@stardust ~]$

Configuration
=============

Create a repository root
------------------------

Each Fossil repository is a self-contained :manual:`SQLite <database-sqlite>` database. The Fossil server needs to know where your repositories are. In this example, we use ``~/repos``:

::

   [isabell@stardust ~]$ mkdir ~/repos
   [isabell@stardust ~]$


Configure web server
--------------------

.. include:: includes/web-backend.rst

.. note::

    Fossil will be running on port 8008. You can choose any other valid port in the next step.


Setup daemon
------------

To start the Fossil server automatically and run it in the background, create ``~/etc/services.d/fossil.ini`` with the following content:

.. code-block:: ini

  [program:fossil]
  command=%(ENV_HOME)s/fossil/fossil server %(ENV_HOME)s/repos --repolist --port 0.0.0.0:8008 --remove-prefix

.. include:: includes/supervisord.rst


Setup a test repository (optional)
----------------------------------

To see if everything is working, you can create a test repository here:

::

   [isabell@stardust ~]$ cd ~/repos
   [isabell@stardust ~]$ ../fossil/fossil init test.fossil
   [isabell@stardust ~]$


Finishing installation
======================

Point your browser to the URL you set up, e. g. ``https://isabell.uber.space``. If you created the test repository in the previous step, you should already see it.

Updates
=======

.. note:: Fossil must be updated manually.

.. _Fossil: https://fossil-scm.org/
.. _release: https://fossil-scm.org/home/uv/download.html

----

Tested with Fossil 2.24 on Uberspace 7.16.0

.. author_list::
