.. highlight:: console

.. author:: Benjamin Wießneth <bwiessneth@gmail.com>
.. author:: Christian Macht <github.com/cmacht>

.. tag:: lang-python
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/flask-logo.png
      :align: center

#####
Flask
#####

.. tag_list::

`Flask <https://flask.palletsprojects.com/en/2.0.x/>`_ is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

----

License
=======

All relevant legal information can be found here

* https://www.palletsprojects.com/governance/licenses-and-copyright/



Installation
============

The name of the application you are going to set up is called **basic_flask**.
If you wish to use another name make sure to replace **basic_flask** in all of the following steps with the name of your choice.



Create application directory and files
--------------------------------------

::

  [isabell@stardust ~]$ mkdir basic_flask
  [isabell@stardust ~]$ mkdir basic_flask/templates
  [isabell@stardust ~]$ mkdir basic_flask/style
  [isabell@stardust ~]$

Create ``~/basic_flask/app.py`` with the following content:

.. code-block:: python

  #!/usr/bin/env python3.6
  import os
  from flask import Flask
  from flask import render_template

  app = Flask(__name__)

  @app.route("/")
  def index():
    message = "Hello from project_name"
    return render_template('index.html', message=message)

  if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1024, debug=True)


Create an html template file ``~/basic_flask/templates/index.html`` with the following content:

.. code-block:: html

  <!-- templates/index.html -->
  <html>
    <head>
      <title>basic_flask</title>
      <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
      <h1>{{message}}</h1>
    </body>
  </html>


Create a css file ``~/basic_flask/static/style.css`` with the following content:

.. code-block:: css

  h1 {
    color: blue;
  }


Setup Python environment and install required packages
------------------------------------------------------

You definitely want to create an isolated Python environment. That way the required packages you are going to install with ``pip`` are encapsulated from your system's Python installation. We are using the ``venv`` module to first create a local environment called ``ENV`` (or whatever name you prefer) that we activate with ``source``. Once active, use the venv's ``pip`` to install ``flask`` and its dependencies as well as a local version of ``uwsgi``.

::

  [isabell@stardust ~]$ cd basic_flask
  [isabell@stardust basic_flask]$ python3 -m venv ENV
  [isabell@stardust basic_flask]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask]$ pip install flask uwsgi
  (ENV) [isabell@stardust basic_flask]$


Once you're done playing with it, you can deactivate the virtual environment:

::

  (ENV) [isabell@stardust basic_flask]$ deactivate
  [isabell@stardust basic_flask]$



Configuration
=============

Using Werkzeug for development
------------------------------

You can use Werkzeug which gets shipped with Flask to spin up a small development server. But be aware: **Do not use it in a production deployment.** For more info head to https://www.palletsprojects.com/p/werkzeug/.

Note that if you run your application under a path different from ``/``, this
approach does not work because the requests don't match the configured routes
and because the server does not set the ``SCRIPT_NAME`` variable.
The proper fix is using a uWSGI deployment as we will do in the next step.

To start Werkzeug execute the following commands. This enables the virtual Python environment and loads ``app.py``. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust ~]$ cd basic_flask
  [isabell@stardust basic_flask]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask]$ python app.py
   ℹ * Serving Flask app "app" (lazy loading)
   ℹ * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
   ℹ * Debug mode: on
   ℹ * Running on http://0.0.0.0:1024/ (Press CTRL+C to quit)
   ℹ * Restarting with stat
   ℹ * Debugger is active!
   ℹ * Debugger PIN: 000-000-000
  ^C
  [isabell@stardust basic_flask]$


Using uWSGI for production
--------------------------

A more suited approach to serve your application would be to use uWSGI.
The uWSGI project aims at developing a full stack for building hosting services. For more info head to https://uwsgi-docs.readthedocs.io/en/latest/.

Create the ini file ``~/basic_flask/uwsgi.ini`` with the following content:

.. code-block:: ini

  [uwsgi]
  module = app:app
  pidfile = basic_flask.pid
  master = true
  processes = 1
  http-socket = :1024
  chmod-socket = 660
  vacuum = true


If your application does not run under ``/`` but under, say, ``/your/path/``,
replace the ``module = ...`` line with:

.. code-block:: ini

  mount = /your/path=app:app
  manage-script-name = true

To serve your application via uWSGI execute the following commands. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust ~]$ cd basic_flask
  [isabell@stardust basic_flask]$ source ENV/bin/activate
  [isabell@stardust basic_flask]$ uwsgi uwsgi.ini
  ℹ [uWSGI] getting INI configuration from uwsgi.ini
  ℹ *** Starting uWSGI 2.0.20 (64bit) on [Tue Jan 21 15:47:41 2020] ***
  ℹ ...
  ℹ *** uWSGI is running in multiple interpreter mode ***
  ℹ spawned uWSGI master process (pid: 23422)
  ℹ spawned uWSGI worker 1 (pid: 23455, cores: 1)
  [isabell@stardust basic_flask]$ ^C
  [isabell@stardust basic_flask]$

Setup daemon
------------

When serving a website with Flask, we want to have uWSGI running all the time. To do this, uberspace uses :manual_anchor:`supervisord <daemons-supervisord>` to start and restart processes. Create ``~/etc/services.d/flask.ini`` with the following content:

.. code-block:: ini

 [program:flask]
 directory=%(ENV_HOME)s/basic_flask
 command=%(ENV_HOME)s/basic_flask/ENV/bin/uwsgi uwsgi.ini

Now let's start the service:

.. include:: includes/supervisord.rst



Setup nginx
-----------

.. note::

    Flask is running on port 1024.

Flask is now running on the server, but because of Uberspace's :manual_anchor:`network infrastructure <background-network>` can not yet be accessed from the web.

.. include:: includes/web-backend.rst


Best Practices
==============

uWSGI can be configured extensively and has its own page on `best practices <https://uwsgi-docs.readthedocs.io/en/latest/ThingsToKnow.html>`_. Further recommendations can also be found in this `write-up from EuroPython 2019 <https://www.techatbloomberg.com/blog/configuring-uwsgi-production-deployment/>`_.

.. author_list::