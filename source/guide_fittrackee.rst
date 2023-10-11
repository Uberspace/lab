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
  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`Supervisord <daemons-supervisord>`
  * :lab:`Redis <guide_redis>`
  * :manual:`Domains (optional) <web-domains>`
  * :manual:`Mail (optional) <mail-access>`


License
=======

Fittrackee is open-sourced software licensed under the `AGPL license <https://github.com/SamR1/FitTrackee/blob/master/LICENSE>`_.

Prerequisites
=============

Mandatory `Prerequisites for Fittrackee <https://samr1.github.io/FitTrackee/en/installation.html#prerequisites>`_:

  * :manual:`Python <lang-python>` in the version >3.8.1. 
  * :manual:`PostgreSQL <guide_postgresql>` in the version 11+. 

Installation
============

Create folder
-------------

We do not install Fittrackee in the :manual:`DocumentRoot <web-documentroot>`. We install it in a separate folder. First we create this folder.

::

 [isabell@stardust ~]$ cd /home/isabell
 [isabell@stardust ~]$ mkdir fittrackee
 [isabell@stardust ~]$ 


Install Fittrackee
------------------

``cd`` into your empty Fittrackee folder and set up virtual environment for Python 3.9:

::

 [isabell@stardust ~]$ cd /home/isabell/fittrackee
 [isabell@stardust fittrackee]$ python3.9 -m venv fittrackee_venv
 [isabell@stardust fittrackee]$ ls
  fittrackee_venv
 [isabell@stardust ~]$ 


Activate the virtual environment and install Fittrackee:

::

 [isabell@stardust fittrackee]$ source fittrackee_venv/bin/activate
  (fittrackee_venv) [isabell@stardust fittrackee]$ pip3.9 install fittrackee
  (fittrackee_venv) [isabell@stardust fittrackee]$ 
  ..
  [notice] A new release of pip is available: 23.0.1 -> 23.2.1
  [notice] To update, run: pip install --upgrade pip


Then install version 1.26.6 of ``urllib3`` because otherwise you will get an error message later when setting up the database.

::

 (fittrackee_venv) [isabell@stardust fittrackee]$ pip3.9 install urllib3==1.26.6
 ...
 Successfully installed urllib3-1.26.6


Configuration
=============

PostgreSQL
----------

Please follow the :manual:`PostgreSQL <guide_postgresql>` guide to configurate PostgreSQL.


Web Backends
------------

With web backends you can connect Fittrackee running on port 5000 by default to the frontend to make it accessible from outside. 
Please follow the instructions :manual:`Web Backends <web-backends>`.


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

You need to create the necessary environment variables for Fittrackee. 
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

 [isabell@stardust ~]$ cd /home/isabell/fittrackee/
 [isabell@stardust fittrackee]$ source fittrackee_venv/bin/activate
 (fittrackee_venv) [isabell@stardust fittrackee]$ 


Set environment variables from file ``.env``.

::

 (fittrackee_venv) [isabell@stardust fittrackee]$ source /PathToYourEnvFile/.env

Initialize database schema

::

 (fittrackee_venv) [isabell@stardust fittrackee]$ ftcli db upgrade

Start the application

::

 (fittrackee_venv) [isabell@stardust fittrackee]$ fittrackee


Open your :manual:`domain <web-domains>` in web browser and register. Further information on Fittrackee can be found 
in `Fittrackees documentation <https://samr1.github.io/FitTrackee/en/installation.html>`_.

----

Tested with Fittrackee 0.7.23, Uberspace 7.15.5

.. _Fittrackee: https://github.com/SamR1/FitTrackee/

.. author_list::
