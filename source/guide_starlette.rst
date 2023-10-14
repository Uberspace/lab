.. highlight:: console

.. author:: Lomion <lomion@sarkasti.eu>

.. tag:: lang-python
.. tag:: starlette
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/starlette.png
      :align: center

######
Starlette
######

.. tag_list::

Starlette_ is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.

----

.. note:: For this guide, you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`Supervisord <daemons-supervisord>` to set up your service

License
=======

All relevant legal information can be found here

  * https://github.com/encode/starlette/blob/master/LICENSE.md

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note:: For this guide we will use *mysite* as the project's name and will install it to ``~/mysiteproject``.

Installation
============

Install the latest Starlette version and ASGI server uvicorn.

::

 [isabell@stardust ~]$ pip3.11 install --user starlette uvicorn
 [isabell@stardust ~]$

.. hint::

  For additional dependencies look at https://www.starlette.io/#dependencies .

Create Project
--------------

We create an example app in ``~/mysiteproject/example.py``:

.. code-block:: python
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route


    async def homepage(request):
        return JSONResponse({'hello': 'world'})


    app = Starlette(debug=True, routes=[
        Route('/', homepage),
    ])


Setup Service
=============

Create Service
--------------

Noe we continue with setting it up as a service.

Create ``~/etc/services.d/mysite.ini`` with the following content:

.. code-block:: ini
    :emphasize-lines: 2,3

    [program:mysite]
    directory=%(ENV_HOME)s/mysiteproject
    command=python3.11 /home/sarkasti/.local/bin/uvicorn --host 0.0.0.0 example:app
    startsecs=15

After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

::

  [isabell@stardust ~]$ supervisorctl reread
  mysite: available
  [isabell@stardust ~]$ supervisorctl update
  mysite: updated process group
  [isabell@stardust ~]$ supervisorctl status
  mysite                            RUNNING   pid 26020, uptime 0:03:14
  [isabell@stardust ~]$

Your service should be in the state ``RUNNING``. If it still is in ``STARTING`` instead, no worries! You might just have to wait sometime and try the command again (up to 15 seconds). It might already run fine anyway though. Otherwise check the logs in ``~/logs/supervisord.log``.

Configure Web Backend
---------------------

.. note::

    Uvicorn is running Starlette on port 8000 by default.

.. include:: includes/web-backend.rst

Your backend should now point to the service; let's check it:

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ uberspace web backend list
    / http:8000 => OK, listening: PID 23161, python3.11 /home/sarkasti/.local/bin/uvicorn --host 0.0.0.0 example:app

    [isabell@stardust ~]$


Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!


----

Tested with Django 0.31.1, Python 3.11, Uberspace 7.15

.. author_list::
