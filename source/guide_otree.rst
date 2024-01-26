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
The oTree documentation recommends deployment via Heroku for simplicity, however this may no longer be the best option
for some users since the removal of free plans from the platform.

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

Take note of the passphrase for the ``otree`` user:

.. code-block:: console

   [isabell@stardust ~]$ POSTGRESQL_PW=YOUR-POSTGRESQL_PW


Web domain
----------

Setup a domain to access your oTree apps:

.. code-block:: console

   [isabell@stardust ~]$ uberspace web domain add otree.example.org


Web backend
----------

.. include:: includes/web-backend.rst

For this guide, we will be using the oTree default port ``8000`` and the domain ``otree.example.org``.


Installation
============

oTree
----------

Create and enter a new directory for the oTree app:

.. code-block:: console

   [isabell@stardust ~]$ mkdir otree
   [isabell@stardust ~]$ cd otree

oTree is installed via the Python package manager ``pip``.
First, you should create and activate a virtual environment to separate the installation
from any other Python packages that may be installed in your home directory:

.. code-block:: console

   [isabell@stardust otree]$ python3.10 -m venv venv
   [isabell@stardust otree]$ source venv/bin/activate

Second, install otree and its dependencies:

.. code-block:: console

   (venv) [isabell@stardust otree]$ pip3.10 install otree

If you already have an oTree project, you should copy it into the ``otree`` directory.
If you don't have an oTree project yet, you can create one with:

.. code-block:: console
   (venv) [isabell@stardust otree]$ otree startproject myproject
   Include sample games? (y or n): y
   Created project folder.
   Enter "cd myproject" to move inside the project folder, then start the server with "otree devserver".

Next, install additional packages required by the project.
By default, oTree lists these packages in ``myproject/requirements.txt``:

.. code-block:: console
   (venv) [isabell@stardust otree]$ pip3.10 install -r myproject/requirements.txt

The ``psycopg2`` library is used to connect to the PostgreSQL database.
If you were to start oTree in production mode now, you may get the following error:

.. code-block:: bash
    ImportError: /home/mirko/otree/venv/lib64/python3.10/site-packages/psycopg2/_psycopg.cpython-310-x86_64-linux-gnu.so: undefined symbol: PQconninfo

Though not the recommended by the developers of Psycopg2_, a workaround is to install the ``psycopg2-binary`` package:

.. code-block:: console
   (venv) [isabell@stardust otree]$ pip3.10 install psycopg2-binary

You can now exit the virtual environment with:

.. code-block:: console
   (venv) [isabell@stardust otree]$ deactivate


Run Service
----------

Before running oTree in production, generate up to three additional secret keys,
depending on your needs:

.. code-block:: console
   [isabell@stardust]$ OTREE_ADMIN_PASSWORD=$(openssl rand -hex 16) # admin login
   [isabell@stardust]$ OTREE_SECRET_KEY=$(openssl rand -hex 8) # participant URL secret
   [isabell@stardust]$ OTREE_REST_KEY=$(openssl rand -hex 32) # REST API

Which secret keys are required depends on your app, check the oTree_ documentation for details.

To run oTree in production mode with ``supervisord``, create a new file at ``/home/etc/services.d/otree.ini``
by running:

.. code-block:: console
   [isabell@stardust]$ cat <<EOF >> /home/isabell/etc/services.d/otree.ini
   [program:otree]
   directory=%(ENV_HOME)s/otree/myproject
   environment=
      DATABASE_URL="postgres://otree:$(echo $POSTGRESQL_PW)@localhost:5432/otree",
      OTREE_SECRET_KEY=$OTREE_SECRET_KEY,
      OTREE_ADMIN_PASSWORD=$OTREE_ADMIN_PASSWORD,
      OTREE_REST_KEY=$OTREE_REST_KEY,
      OTREE_PRODUCTION=1,
      OTREE_AUTH_LEVEL=STUDY
   command=%(ENV_HOME)s/otree/venv/bin/otree prodserver 8000
   startsecs=30
   EOF

Note:
   * ``environment``: change variables as per your needs, and make sure your passphrases are correct. You may also want to set ``AUTH_LEVEL="STUDY"`` for production usage.
   * ``directory``: path to the oTree app that you wish to run.
   * ``command``: path to oTree, as installed via ``pip`` in your user directory.

.. include:: includes/supervisord.rst

Tested with Uberspace v7.15.9, oTree v5.10.4.

.. _oTree: https://www.otree.org/
.. _Psycopg2: https://pypi.org/project/psycopg2/
