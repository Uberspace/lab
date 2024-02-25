.. highlight:: console

.. author:: Mirko Reul <https://mirkoreul.de>

.. tag:: lang-python

.. sidebar:: Logo

  .. image:: _static/images/otree-logo.png
      :align: center

#######
oTree
#######

.. tag_list::

oTree_ is an open-source platform for web-based interactive tasks, such as lab experiments and multiplayer games, written in Python.


----

.. note:: For this guide you should be familiar with the basic concepts of:

  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`Domains <web-domains>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Python <lang-python>`

License
=======

oTree is licenced under the MIT open source licence. The authors ask that you cite their paper:

  * Licence: http://opensource.org/licenses/MIT
  * Paper: http://dx.doi.org/10.1016/j.jbef.2015.12.001

Prerequisites
=============

Database
----------

oTree uses PostgreSQL to store data in production mode.
If you haven't set it up yet, initialize and configure :lab:`PostgreSQL <guide_postgresql>` first.

Create a separate user and database for oTree:

.. code-block:: console

   [isabell@stardust ~]$ createuser otree -P
   [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=otree --template=template0 otree
   [isabell@stardust ~]$

Take note of the passphrase for the ``otree`` user. We will refer to it below as ``POSTGRESQL_PW``.

Web domain
----------

Setup a domain to access your oTree apps:

.. code-block:: console

   [isabell@stardust ~]$ uberspace web domain add otree.example.org
   [isabell@stardust ~]$


Web backend
----------

.. include:: includes/web-backend.rst

For this guide, we will be using the oTree default port ``8000`` and the domain ``otree.example.org``.


Installation
============

Create and enter a new directory for the oTree app:

.. code-block:: console

   [isabell@stardust ~]$ mkdir otree
   [isabell@stardust ~]$ cd otree
   [isabell@stardust otree]$

oTree is installed via the Python package manager ``pip``.
First, you should create and activate a virtual environment to separate the installation
from any other Python packages that may be installed in your home directory:

.. code-block:: console

   [isabell@stardust otree]$ python3.10 -m venv venv
   [isabell@stardust otree]$ source venv/bin/activate
   (venv) [isabell@stardust otree]$

Second, install otree and its dependencies:

.. code-block:: console

   (venv) [isabell@stardust otree]$ pip3.10 install otree
   (venv) [isabell@stardust otree]$

Configuration
============

oTree
----------

If you already have an oTree project, you should copy it into the ``otree`` directory.
If you don't have an oTree project yet, you can create one with:

.. code-block:: console

   (venv) [isabell@stardust otree]$ otree startproject myproject
   ? Include sample games? (y or n): y
   ✔ Created project folder.
   ℹ Enter "cd myproject" to move inside the project folder, then start the server with "otree devserver".
   (venv) [isabell@stardust otree]$

Next, install additional packages required by the project.
By default, oTree lists these packages in ``myproject/requirements.txt``:

.. code-block:: console

   (venv) [isabell@stardust otree]$ pip3.10 install -r myproject/requirements.txt
   (venv) [isabell@stardust otree]$

The ``psycopg2`` library is used to connect to the PostgreSQL database.
If you were to start oTree in production mode now, you may get the following error:

.. code-block:: python

    ImportError: /home/isabell/otree/venv/lib64/python3.10/site-packages/psycopg2/_psycopg.cpython-310-x86_64-linux-gnu.so: undefined symbol: PQconninfo

Though not recommended by the developers of Psycopg2_, a workaround is to install the ``psycopg2-binary`` package:

.. code-block:: console

   (venv) [isabell@stardust otree]$ pip3.10 install psycopg2-binary
   (venv) [isabell@stardust otree]$

You can now exit the virtual environment with:

.. code-block:: console

   (venv) [isabell@stardust otree]$ deactivate
   [isabell@stardust otree]$


Set up the daemon
----------

Before running oTree in production, generate up to three additional secret keys,
depending on your needs:

.. code-block:: console

   [isabell@stardust]$ openssl rand -hex 16 # OTREE_ADMIN_PASSWORD: admin login
   [isabell@stardust]$ openssl rand -hex 8 # OTREE_SECRET_KEY: (optional) participant URL secret
   [isabell@stardust]$ openssl rand -hex 32 # OTREE_REST_KEY: (optional) key for the REST API
   [isabell@stardust]$

Which secret keys are required depends on your app, check the oTree_ documentation for details.

To run oTree in production mode with ``supervisord``, create a new file at ``/home/$USER/etc/services.d/otree.ini``
with the following contents: 

.. code-block:: ini
 :emphasize-lines: 4-7

   [program:otree]
   directory=%(ENV_HOME)s/otree/myproject
   environment=
      PATH="%(ENV_HOME)s/otree/venv/bin:%(ENV_PATH)s",
      DATABASE_URL="postgres://otree:POSTGRESQL_PW@localhost:5432/otree",
      OTREE_SECRET_KEY="OTREE_SECRET_KEY",
      OTREE_ADMIN_PASSWORD="OTREE_ADMIN_PASSWORD",
      OTREE_REST_KEY="OTREE_REST_KEY",
      OTREE_PRODUCTION="1",
      OTREE_AUTH_LEVEL="DEMO"
   command=%(ENV_HOME)s/otree/venv/bin/otree prodserver 8000
   startsecs=30

Modify the file as follows:
   * ``environment``: add your passphrases as indicated, or remove variabes you don't need. You may also want to set ``AUTH_LEVEL="STUDY"`` for production usage.
   * ``directory``: path to the oTree app that you wish to run.
   * ``command``: path to oTree, as installed via ``pip`` in your virtual environment.

.. include:: includes/supervisord.rst

You should now be able to access your oTree app by navigating to ``https://otree.example.org``.

Tested with Uberspace v7.15.9, oTree v5.10.4.

.. _oTree: https://www.otree.org/
.. _Psycopg2: https://pypi.org/project/psycopg2/
