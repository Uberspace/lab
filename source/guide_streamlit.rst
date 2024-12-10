.. highlight:: console

.. author:: Torben <https://entorb.net/contact.php?origin=UberspaceLab>

.. tag:: lang-python
.. tag:: streamlit
.. tag:: web
.. tag:: audience-developers

######
Streamlit
######

.. tag_list::

Streamlit_ is a high-level Python Web framework focussing on data visualization. This guide is based on the :lab:`Django <guide_django>` guide.

----

.. note:: For this guide, you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`Supervisord <daemons-supervisord>` to set up your service

License
=======

All relevant legal information can be found here

  * https://streamlit.io/terms-of-use

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note:: For this guide we will use *mysiteproject* as the project's name and will install it to ``~/mysiteproject``.

Installation
============

Install the latest Streamlit version.

.. code-block:: console

  [isabell@stardust ~]$ pip3.11 install --user streamlit
  [isabell@stardust ~]$

Create Project
==============

Create a top-level directory for your project somewhere. We use `~/mysiteproject` for this guide.

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/mysiteproject
  [isabell@stardust ~]$ mkdir ~/mysiteproject/.streamlit
  [isabell@stardust ~]$

.. warning:: While it does not matter how you name it and where you put it, we suggest that you do **not** put this directory under any path served to the web (e.g. ``~/html``), to avoid exposing your files.

Configuration
=============

Create ``~/mysiteproject/.streamlit/config.toml``

.. code-block:: python

  [browser]
  gatherUsageStats = false

  [server]
  headless = true
  port = 8501
  baseUrlPath = ""

See `Streamlit configuration documentation <https://docs.streamlit.io/develop/api-reference/configuration/config.toml>`_ for more information.

Example App
===========
Create ``~/mysiteproject/app.py``

.. code-block:: python

  import streamlit as st
  st.title("Test")

start it manually
.. code-block:: console

  [isabell@stardust ~]$ cd mysiteproject
  [isabell@stardust ~/mysiteproject$]$ streamlit run app.py
  [isabell@stardust ~/mysiteproject$]$

close via ctrl+c

Add Web Backend
===============

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set / --http --port 8501
  Set backend for / to port 8501; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

Setup Service
=============

Create ``~/etc/services.d/mysiteproject.ini`` with the following content (take care to adapt the given directory and project name according to your chosen values):

.. code-block:: ini
  :emphasize-lines: 2,3

  [program:mysiteproject]
  directory=%(ENV_HOME)s/mysiteproject
  command=streamlit run app.py

After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

::

  [isabell@stardust ~]$ supervisorctl reread
  mysiteproject: available
  [isabell@stardust ~]$ supervisorctl update
  mysiteproject: updated process group
  [isabell@stardust ~]$ supervisorctl status
  mysiteproject                 RUNNING   pid 11137, uptime 0:04:25
  [isabell@stardust ~]$

Your service should be in the state ``RUNNING``. If it still is in ``STARTING`` instead, no worries! You might just have to wait sometime and try the command again (up to 15 seconds). It might already run fine anyway though. Otherwise check the logs in ``~/logs/supervisord.log``.

Configure Web Backend
---------------------

.. include:: includes/web-backend.rst

Your backend should now point to the service; let's check it:

.. code-block:: console
  :emphasize-lines: 1

  [isabell@stardust ~]$ uberspace web backend list
  / http:8501 => OK, listening: PID 11264, /usr/bin/python3.11 /home/isabell/.local/bin/streamlit run app.py

  [isabell@stardust ~]$

Finishing Installation
======================

Perform a CURL request to the configured URL, to see if your installation succeeded:

.. code-block:: console
  :emphasize-lines: 1,2

  [isabell@stardust ~]$ curl -I https://isabell.uber.space/mysiteproject
  HTTP/1.1 301 Moved Permanently
  Server: nginx
  Date: Mon, 09 Dec 2024 20:53:12 GMT
  Content-Type: text/html
  Content-Length: 162
  Connection: keep-alive
  Location: https://isabell.uber.space/mysiteproject

  [isabell@stardust ~]$

Documentation
=============

.. _official docs: https://docs.streamlit.io/

----

Tested with Streamlit 1.40.2, Python 3.11, Uberspace 7.15

.. author_list::
