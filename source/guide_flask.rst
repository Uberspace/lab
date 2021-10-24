.. highlight:: console

.. author:: Benjamin Wießneth <bwiessneth@gmail.com>

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

The name of the application you are going to set up is called **basic_flask_template**.
If you wish to use another name make sure to replace **basic_flask_template** in all of the following steps with the name of your choice.



Create application directory and files
--------------------------------------

::

  [isabell@stardust ~]$ mkdir basic_flask_template
  [isabell@stardust ~]$ mkdir basic_flask_template/templates
  [isabell@stardust ~]$ mkdir basic_flask_template/style
  [isabell@stardust ~]$

Create ``~/basic_flask_template/app.py`` with the following content:

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


Create a html template file ``~/basic_flask_template/templates/index.html`` with the following content:

.. code-block:: html

  <!-- templates/index.html -->
  <html>
    <head>
      <title>basic_flask_template</title>
      <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
      <h1>{{message}}</h1>
    </body>
  </html>


Create css file ``~/basic_flask_template/static/style.css`` with the following content:

.. code-block:: css

  h1 {
    color: blue;
  }


Setup python environment and install required packages
------------------------------------------------------

You definitely want to create a isolated python environment. That way the required packages you are going to install with ``pip`` are encapsulated form your systemwide python installation. For more info check https://virtualenv.pypa.io/en/latest/

::

  [isabell@stardust ~]$ cd basic_flask_template
  [isabell@stardust basic_flask_template]$ virtualenv -p python3 ENV
  [isabell@stardust basic_flask_template]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask_template]$ pip install Click==7.0 Flask==1.1.1 itsdangerous==1.1.0 Jinja2==2.10.3 MarkupSafe==1.1.1 uWSGI==2.0.18 Werkzeug==0.16.0
  (ENV) [isabell@stardust basic_flask_template]$

You can activate your new python environment like this:

::

  [isabell@stardust ~]$ cd basic_flask_template
  [isabell@stardust basic_flask_template]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask_template]$

Once you're done playing with it, deactivate it with the following command:

::

  (ENV) [isabell@stardust basic_flask_template]$ deactivate
  [isabell@stardust basic_flask_template]$



Setup nginx
-----------

.. note::

    Flask is running on port 1024.

.. include:: includes/web-backend.rst


Start your application
----------------------

Using Werkzeug for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use Werkzeug which get's shipped with Flask to spin up a small development server. But be aware: **Do not use it in a production deployment.** For more info head to https://www.palletsprojects.com/p/werkzeug/.

Note that if you run your application under a path different from ``/``, this
approach does not work because the requests don't match the configured routes
and because the server does not set the ``SCRIPT_NAME`` variable.
The proper fix is using a uWSGI deployment as we will do in the next step.

To start Werkzeug execute the following commands. It enables the virtual python environment and uses executes ``app.py``. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust ~]$ cd basic_flask_template
  [isabell@stardust basic_flask_template]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask_template]$ python app.py
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
  [isabell@stardust basic_flask_template]$
  [isabell@stardust basic_flask_template]$


Using UWSGI for production
^^^^^^^^^^^^^^^^^^^^^^^^^^

A more suited approach to serve your application would be to use uWSGI.
The uWSGI project aims at developing a full stack for building hosting services. For more info head to https://uwsgi-docs.readthedocs.io/en/latest/.

Create ini file ``~/basic_flask_template/uwsgi.ini`` with the following content:

.. code-block:: ini

  [uwsgi]
  module = app:app
  pidfile = basic_flask_template.pid
  master = true
  processes = 1
  http-socket = :1024
  chmod-socket = 660
  vacuum = true


If your application does not run under ``/`` but under, say, ``/your/path/``,
replace the ``module = ...`` line with

.. code-block:: ini

  mount = /your/path=app:app
  manage-script-name = true

To serve your application via uWSGI execute the following commands. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust ~]$ cd basic_flask_template
  [isabell@stardust basic_flask_template]$ source ENV/bin/activate
  [isabell@stardust basic_flask_template]$ uwsgi uwsgi.ini
  ℹ [uWSGI] getting INI configuration from uwsgi.ini
  ℹ *** Starting uWSGI 2.0.18 (64bit) on [Tue Jan 21 15:47:41 2020] ***
  ℹ ...
  ℹ *** uWSGI is running in multiple interpreter mode ***
  ℹ spawned uWSGI master process (pid: 23422)
  ℹ spawned uWSGI worker 1 (pid: 23455, cores: 1)
  [isabell@stardust basic_flask_template]$ ^C
  [isabell@stardust basic_flask_template]$

Setup daemon
^^^^^^^^^^^^

Create ``~/etc/services.d/flask.ini`` with the following content:

.. code-block:: ini

 [program:flask]
 directory=%(ENV_HOME)s/basic_flask_template
 command=%(ENV_HOME)s/basic_flask_template/ENV/bin/uwsgi uwsgi.ini

Now let's start the service:

.. include:: includes/supervisord.rst
