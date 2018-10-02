.. highlight:: console

.. author:: Finn <mail@f1nn.eu>

.. sidebar:: About

  .. image:: _static/images/django.svg
      :align: center

##########
Django
##########

Django_ is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Python_ and its package manager pip
  * supervisord_

License
=======

All relevant legal information can be found here 

  * https://www.djangoproject.com/trademarks/

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

.. include:: includes/install-uwsgi.rst

Step 2
------
Install django

::

 [isabell@stardust ~]$ pip3.6 install django --user
 [isabell@stardust ~]$


Create a django project. We will use "MyDjangoProject" during this guide.

::

 [isabell@stardust ~]$ django-admin startproject MyDjangoProject
 [isabell@stardust ~]$

Migrate database

::

 [isabell@stardust ~]$ python3.6 ~/MyDjangoProject/manage.py migrate
 [isabell@stardust ~]$


Configuration
=============

Configure port
--------------

Since Django applications use their own webserver, you need to find a free port and bind your application to it.

.. include:: includes/generate-port.rst

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

To deploy your application with uwsgi, create a file at ``~/uwsgi/apps-enabled/myDjangoProject.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! (4 times)
.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: ini
  :emphasize-lines: 2,3,5,16,17

  [uwsgi]
  base = /home/<username>/MyDjangoProject/MyDjangoProject
  chdir = /home/<username>/MyDjangoProject

  http = :<yourport>
  master = true
  wsgi-file = %(base)/wsgi.py
  touch-reload = %(wsgi-file)

  app = wsgi

  #virtualenv = %(chdir)/venv

  plugin = python

  uid = <username>
  gid = <username>

Test installation
-----------------

Perform a CURL request to your custom port to see if your installation succeeded:

.. warning:: Replace ``<yourport>`` with your port!

::

 [isabell@stardust ~]$ curl -I localhost:<yourport>
 HTTP/1.1 200 OK
 Content-Type: text/html
 X-Frame-Options: SAMEORIGIN
 Content-Length: 16348
 [isabell@stardust ~]$

If you don't see ``HTTP/1.1 200 OK`` check your installation.



Finishing installation
======================

Point your browser to URL and create a user account.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!


.. _Django: https://www.djangoproject.com/
.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

----

Tested with Django 2.0.5, Uberspace 7.1.6

.. authors::
