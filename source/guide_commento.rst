.. author:: hendrikmaus <https://github.com/hendrikmaus>

.. tag:: lang-go
.. tag:: web
.. tag:: blog

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/commento.png
      :align: center

########
Commento
########

.. tag_list::

Commento_ is an open source, fast, privacy-focused commenting platform written in golang.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

Install and configure a :lab:`Postgresql <guide_postgresql>` server.

Installation
============

Since Commento_ provides pre-compiled binaries, we can use those:

.. warning:: Check the `releases page <https://docs.commento.io/getting-started/self-hosting/releases.html>`_ before you continue.

.. code-block:: console

 [isabell@stardust ~]$ mkdir commento
 [isabell@stardust ~]$ cd commento
 [isabell@stardust commento]$ wget https://commento-release.s3.amazonaws.com/commento-linux-amd64-v1.7.0.tar.gz
 [isabell@stardust commento]$

Extract the tar archive:

.. code-block:: console

 [isabell@stardust commento]$ tar -xf commento-linux-amd64-v1.7.0.tar.gz
 [isabell@stardust commento]$

We do not need the tarball any longer, so delete it:

.. code-block:: console

 [isabell@stardust commento]$ rm commento-linux-amd64-v1.7.0.tar.gz
 [isabell@stardust commento]$

You will be left with a single executable binary, called ``commento`` as well as supporting files.

Create Commento Start Script
----------------------------

Make sure to have your PostgreSQL credentials ready. You will need an existing ``database``, ``port``, ``username`` and ``password``.

Create ``~/bin/commento_daemon`` and add the following content:

.. warning:: Replace replace all placeholders ``<*>`` with your values!

.. code-block:: bash

 #!/bin/sh
 set -ue

 export COMMENTO_ORIGIN=https://isabell.uber.space
 export COMMENTO_PORT=31380
 export COMMENTO_BIND_ADDRESS="0.0.0.0"
 export COMMENTO_POSTGRES=postgres://<username>:<password>@<host>:<port>/<database>?sslmode=disable
 exec ~/commento/commento

Make your script executable:

.. code-block:: bash

 [isabell@stardust ~]$ chmod +x ~/bin/commento_daemon
 [isabell@stardust ~]$

Setup Supervisor
----------------

Create ``~/etc/services.d/commento.ini`` with the following content:

.. code-block:: ini

 [program:commento]
 command=%(ENV_HOME)s/bin/commento_daemon

.. include:: includes/supervisord.rst

To stop and start the daemon to perform maintenance tasks, you can use ``supervisorctl stop`` and ``supervisorctl start``, respectively:

::

 [isabell@stardust ~]$ supervisorctl stop commento
 commento: stopped
 [isabell@stardust ~]$

::

 [isabell@stardust ~]$ supervisorctl start commento
 commento: started
 [isabell@stardust ~]$

Check out the :manual:`supervisord manual <daemons-supervisord>` for further details.

Configure Web Backend
---------------------

.. note::

    Commento is running on port 31380.

.. include:: includes/web-backend.rst

Now you should be able to access Commento at your defined domain in your browser.

Additional Notes
----------------

If you are the only user of the Commento instance, it would be advisable to disable the new owner sign up, after you registered your site.
Add this to your ``commento_daemon`` above the ``/home/isabell/commento/commento`` call:

.. note:: This doe not impact the commenting users of your site!

.. code-block:: bash

 export COMMENTO_FORBID_NEW_OWNERS=true

Then restart Commento:

::

 [isabell@stardust ~]$ supervisorctl retart commento
 commento: stopped
 commento: started
 [isabell@stardust ~]$

The form to sign up will still be visible, but cannot be submitted.

.. _Commento: https://commento.io

---

Tested with Commento 1.7.0 / Uberspace 7.3.6.1

.. author_list::
