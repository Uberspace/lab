.. highlight:: console

.. author:: Torben <https://entorb.net/contact.php?origin=UberspaceLab>

.. tag:: lang-python
.. tag:: streamlit
.. tag:: web
.. tag:: audience-developers

#########
Streamlit
#########

.. tag_list::

Streamlit_ is a high-level Python Web framework focussing on data visualization.

----

.. note:: For this guide, you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`Supervisord <daemons-supervisord>` to set up your service

License
=======

All relevant legal information can be found in the `terms of use`_.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

For this guide we will use *mysiteproject* as the project's name and will install it to ``~/mysiteproject``.

Installation
============

Install the latest Streamlit version.

.. code-block:: console

  [isabell@stardust ~]$ pip3.11 install --user streamlit
  [isabell@stardust ~]$

Create Project
--------------

Create a directory for your project. We use `~/mysiteproject` for this guide.

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/mysiteproject
  [isabell@stardust ~]$ mkdir ~/mysiteproject/.streamlit
  [isabell@stardust ~]$

.. warning:: While it does not matter how you name it and where you put it, we suggest that you do **not** put this directory under any path served to the web (e.g. ``~/html``), to avoid exposing your files.

Configuration
=============

Create ``~/mysiteproject/.streamlit/config.toml``

.. code-block:: 

  [browser]
  gatherUsageStats = false

  [server]
  headless = true
  port = 8501
  baseUrlPath = ""

See Streamlit `configuration documentation`_ for more information.

Example App
===========

Create ``~/mysiteproject/app.py``

.. code-block:: python

  import streamlit as st
  st.title("Test")

Add Web Backend
===============

.. note:: Streamlit is running on port 8501.

.. include:: includes/web-backend.rst

Setup Service
=============

Create ``~/etc/services.d/mysiteproject.ini`` with the following content:

.. code-block:: ini
  :emphasize-lines: 2,3

  [program:mysiteproject]
  directory=%(ENV_HOME)s/mysiteproject
  command=streamlit run app.py

After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service.

.. include:: includes/supervisord.rst

Configure Web Backend
---------------------

.. note:: Streamlit is running on port 8501.

.. include:: includes/web-backend.rst

Your backend should now point to the service.

.. _Streamlit: https://docs.streamlit.io/
.. _terms of use: https://streamlit.io/terms-of-use
.. _configuration documentation: https://docs.streamlit.io/develop/api-reference/configuration/config.toml

----

Tested with Streamlit 1.40.2, Python 3.11, Uberspace 7.16

.. author_list::
