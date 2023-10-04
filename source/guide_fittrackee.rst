.. highlight:: console
.. author:: Astrid Günther <https://astrid-guenther.de>

.. tag:: lang-python
.. tag:: fitness-tracker
.. tag:: sport-tracking-app
.. tag:: tacking
.. tag:: tacker
.. tag:: sport
.. tag:: fitness 
.. tag:: gpx   

.. sidebar:: Logo

  .. image:: _static/images/fittrackee.png
      :align: center

##########
Fittrackee
##########

.. tag_list::

Fittrackee_ allows you to track your outdoor activities (workouts) from gpx files and keep your data on your own server. 
It is a open source and decentralized sport tracking app. 

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :lab:`PostgreSQL <guide_postgresql>`
  * :manual:`firewall ports <basics-ports>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :lab:`Redis <guide_redis>`
  * :manual:`Domains <web-domains>`
  * :manual:`mail <mail-access>`


License
=======

Fittrackee is open-sourced software licensed under the `AGPL license <https://github.com/SamR1/FitTrackee/blob/master/LICENSE>`_.

Prerequisites
=============

Mandatory `Prerequisites for Fittrackee <https://samr1.github.io/FitTrackee/en/installation.html#prerequisites>`_:

:manual:`Python <lang-python>` in the version >3.8.1. 

If you don’t select a certain version, we're using version 2.7. To change the python version, run the relevant binary. 
So if you want to start a script with version 3.9, use the python3.9 binary:

::

 [ub@lupus ~]$ python --version
 Python 2.7.5
 [ub@lupus ~]$ python3.9 --version
 Python 3.9.18


:manual:`PostgreSQL <guide_postgresql>` in the version 11+. We're using version 15. This is fine:

::

 [ub@lupus ~]$ uberspace tools version show postgresql
 Using 'Postgresql' version: '15'


Installation
============

Create folder
-------------

.. note:: You should not install Fittrackee in your :manual:`DocumentRoot <web-documentroot>`. Instead we install it in a separate folder.

::

 $ ssh ub@lupus.uberspace.de
 [ub@lupus ~]$ cd /home/ub
 [ub@lupus ~]$ mkdir fittrackee
 [ub@lupus ~]$ 


Install Fittrackee
------------------

``cd`` into your empty Fittrackee directory and set up virtual environment for Python:

::

 [ub@lupus ~]$ cd /home/ub/fittrackee
 [ub@lupus fittrackee]$ python3.9 -m venv fittrackee_venv
 [ub@lupus fittrackee]$ ls
  fittrackee_venv
 [ub@lupus ~]$ 


Activate the virtual environment:

::

 [ub@lupus fittrackee]$ source fittrackee_venv/bin/activate
  (fittrackee_venv) [ub@lupus fittrackee]$ pip3.9 install fittrackee
  (fittrackee_venv) [ub@lupus fittrackee]$ 
  ..
  [notice] A new release of pip is available: 23.0.1 -> 23.2.1
  [notice] To update, run: pip install --upgrade pip

Following that, I update pip because I like to work with current versions.

::

 (fittrackee_venv) [ub@lupus fittrackee]$ pip install --upgrade pip
  Successfully installed pip-23.2.1
 (fittrackee_venv) [ub@lupus fittrackee]$ 

Then I install version 1.26.6 of ``urllib3`` because I know from experience that otherwise I will get an error message regarding the version later when setting up the database.

::

 (fittrackee_venv) [ub@lupus fittrackee]$ pip install urllib3==1.26.6
 ...
 Successfully installed urllib3-1.26.6


Configuration
=============

PostgreSQL
----------

It's mandatory that we set up PostgreSQL.

Please follow the :manual:`PostgreSQL <guide_postgresql>` guide to configurate PostgreSQL.


Optional: Web Backends
------------

Do you want the application to be accessible at https://subdomain.example.org and the address
https://subdomain.example.org to remain in the browser's address bar. So it should not just be a simple forwarding, but a DNS addressing. In this case, web backends come into play! 

Please follow the :manual:`Web Backends <web-backends>` guide to setup up Web Backends.


Optional: Redis
---------------

We need Redis for task queue (if email sending is enabled and for data export requests) and API rate limits. 

Please follow the :lab:`Redis <guide_redis>` guide to setup redis. By default, Redis does not run on a port with us, but provides a Unix socket under ``/home/$USER/.redis/sock``. Either one has to adjust the configuration of the Fittrackee application or change the Redis configuration from `port 0' to 6379. 


Optional: Emails
----------------

In order to be able to send e-mails from Fittrackee, you need an e-mail account, which you specify in the next step in the file ``.env``. Any account can be used for this purpose. If you like, you can create the account directly at Uberspace.

Please follow the :manual:`mail <mail-access>` guide to setup up Emails.


Environment variables for Fittrackee
------------------------------------

It is mandatory to create the necessary environment variables. 
You can use the `example file <https://github.com/SamR1/FitTrackee/blob/master/.env.example>`_ as a guide. 
Further explanations can be found in the `Fittrackee documentation <https://samr1.github.io/FitTrackee/en/installation.html#environment-variables>`_.

For an installation in our system it is important to customize the variables ``HOST`` and ``DATABASE_URL`` as follows:

::

 export HOST=0.0.0.0
 ...
 export DATABASE_URL=postgresql://fittrackee:fittrackee@localhost:5432/fittrackee
 ...

For more information about the available ports, see :manual:`firewall ports <basics-ports>`.


Set up and launch Fittrackee
----------------------------

Start virtual environment.

::

 [ub@lupus ~]$ cd /home/ub/fittrackee/
 [ub@lupus fittrackee]$ source fittrackee_venv/bin/activate
 (fittrackee_venv) [ub@lupus fittrackee]$ 


Set environment variables from file ``.env``.

::

 (fittrackee_venv) [ub@lupus fittrackee]$ source .env

Initialize database schema

::

 (fittrackee_venv) [ub@lupus fittrackee]$ ftcli db upgrade

Start the application

::

 (fittrackee_venv) [ub@lupus fittrackee]$ fittrackee

Open https://ub.uber.space/ and register.

A more detailed guide regarding Fittrackee can be found in the `documentation of Fittrackee <https://samr1.github.io/FitTrackee/en/installation.html#from-pypi>`_.




----

Tested with Fittrackee 0.7.23, Uberspace 7.15.5

.. _Fittrackee: https://github.com/SamR1/FitTrackee/

.. author_list::
