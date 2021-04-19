.. highlight:: console

.. author:: Christian Macht <https://github.com/cmacht/>

.. tag:: lang-python
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/fastapi.png
      :align: center

#######
FastAPI
#######

.. tag_list::

FastAPI_ is a modern, async web-framework for building APIs with Python 3.6+ making use of type hints. It is a microframework, in many ways quite `similar to Flask`_ and uses the MIT license_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python 3 <lang-python>` and its package manager :manual_anchor:`pip <lang-python.html#pip>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Installation
============

We are creating a very basic proof-of-concept API that will do a calculation and return the result as valid JSON.


Create application directory and files
--------------------------------------

::

  [isabell@stardust ~]$ mkdir ~/fastapi
  [isabell@stardust ~]$

Create a file ``~/fastapi/main.py`` with the following content:

.. code-block:: python

  #!/usr/bin/env python3.6
  import fastapi
  import uvicorn

  api = fastapi.FastAPI()

  @api.get('/')
  def calculate():
    answer = 24 + 18
    return {'answer': answer}

  # To test this app locally, uncomment this line:
  # uvicorn.run(api, host="localhost", port=8000)



Python Virtual Environment
--------------------------
To install the packages your application depends on, you want to use a virtual environment that is isolated from the system python's packages.
FastAPI requires Python 3.6+ so we are going to use the latest working version, which is Python 3.8 (due to a `dependency issue`_):

::

  [isabell@stardust ~]$ cd ~/fastapi
  [isabell@stardust fastapi]$ python3.8 -m venv .env
  [isabell@stardust fastapi]$ source .env/bin/activate
  (.env) [isabell@stardust fastapi]$

In your virtual environment, install the dependencies we are using in ``main.py``:

::

  (.env) [isabell@stardust fastapi]$ pip install fastapi uvicorn
  (.env) [isabell@stardust fastapi]$

.. note:: You can already check if your application is working by uncommenting the ``ucivorn.run()`` line and executing ``python main.py`` in the virtual environment. Open a second ssh connection and get the output with ``curl localhost:8000``

While uvicorn_ handles the asynchronous side of FastAPI, we want gunicorn_ as a well-tested and production-ready solution to run and manage multiple uvicorn workers. Install it with two dependencies in your virtual environment:

::

  (.env) [isabell@stardust fastapi]$ pip install gunicorn uvloop httptools
  (.env) [isabell@stardust fastapi]$

You can deactivate the virtual environment context like this:

::

  (.env) [isabell@stardust fastapi]$ deactivate
  [isabell@stardust fastapi]$



Configuration
=============

Incoming https requests are routed through :manual:`nginx <background-http-stack>` to a :manual:`web backend <web-backends>` where our application server is listening.
Let's get this working:

Gunicorn
--------
First, we are telling gunicorn to spin up several uvicorn processes and listen on port 8000 for incoming requests. Create the config file ``~/fastapi/conf.py``:

.. code-block:: python

  import os
  app_path = os.environ['HOME'] + '/fastapi'

  # Gunicorn configuration
  wsgi_app = 'main:api'
  bind = ':8000'
  chdir = app_path
  workers = 4
  worker_class = 'uvicorn.workers.UvicornWorker'
  errorlog =  app_path + '/errors.log'



This is a minimal working example based on gunicorn's `example config`_, you can find a comprehensive `list of options here`_.

.. note:: Test if everything is working with ``~/fastapi/.env/bin/gunicorn --config ~/fastapi/conf.py --check-config``. If there is no output, you're good.


Supervisord
-----------
Next, create a configuration for supervisord in ``~/etc/services.d/fastapi.ini``:

.. code-block:: ini

  [program:fastapi]
  directory=%(ENV_HOME)s/fastapi
  command=%(ENV_HOME)s/fastapi/.env/bin/gunicorn --config %(ENV_HOME)s/fastapi/conf.py

.. include:: includes/supervisord.rst

Web backend
-----------

.. note:: Gunicorn is set up to run on port 8000.

.. include:: includes/web-backend.rst



That's it
=========

This concludes the setup. Point your browser to :manual:`your url <web-domains>` and check that everything is running correctly.


.. _FastAPI: https://github.com/tiangolo/fastapi
.. _similar to Flask: https://fastapi.tiangolo.com/alternatives/#flask
.. _license: https://github.com/tiangolo/fastapi/blob/master/LICENSE
.. _dependency issue: https://github.com/MagicStack/httptools/issues/59
.. _uvicorn: https://www.uvicorn.org
.. _gunicorn: https://gunicorn.org/
.. _example config: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
.. _list of options here: https://docs.gunicorn.org/en/stable/settings.html#server-socket

----

.. author_list::
