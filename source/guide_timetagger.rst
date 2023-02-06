.. highlight:: console

.. author:: Marvin Dickhaus <https://marvindickhaus.de>

.. tag:: lang-python
.. tag:: web
.. tag:: accounting
.. tag:: time-tracking

.. sidebar:: Logo

  .. image:: _static/images/timetagger.svg
      :align: center

##########
TimeTagger
##########

.. tag_list::

TimeTagger_ is a free, open source time-tracking software written in Python. It has an interactive user experience and powerful reporting.

.. note::
  This guide is based upon the `selfhost article`_ written by Almar Klein, the author of TimeTagger.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

TimeTagger is released under the `GPLv3 License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install TimeTagger we use :manual_anchor:`pip <lang-python.html#pip>`.

.. note:: The ``pip``-command defaults to pip from python 2.7. Please use a modern version of pip instead. See the :manual:`manual <lang-python/#update-policy>` for currently supported versions. In this guide, we use python3.9.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ pip3.9 install --user --upgrade timetagger
 Collecting timetagger
  Downloading timetagger-22.6.6-py3-none-any.whl (2.9 MB)
  […]
  Successfully installed MarkupSafe-2.1.1 asgineer-0.8.1 bcrypt-3.2.2 cffi-1.15.1 click-8.1.3 h11-0.13.0 itemdb-1.1.1 jinja2-3.1.2 markdown-3.4.1 pscript-0.7.7 pycparser-2.21 pyjwt-2.4.0 timetagger-22.6.6 uvicorn-0.18.2
  […]
 [isabell@stardust ~]$

Configuration
=============

Create main file
----------------

To configure TimeTagger we need to create our own main file.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ cp ~/.local/lib/python3.9/site-packages/timetagger/__main__.py ~/bin/mytimetagger.py
 [isabell@stardust ~]$

Next we select the port ``4800`` to serve TimeTagger from. It must be mapped in the backend.

.. include:: includes/web-backend.rst

First Run
---------

We can now start the app for the first time. Therefor replace the number after the colon with the port number you chose.

Right now a user account is still missing. The app provides a dialogue to generate the encrypted string where a user is stored in.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ python3.9 ~/bin/mytimetagger.py --bind=0.0.0.0:4800
 […]
 [INFO 2022-07-08 12:14:34] Collected 4 assets from /home/isabell/.local/lib/python3.9/site-packages/timetagger/pages/.
 [INFO 2022-07-08 12:14:34] Server is starting up

Finishing installation
======================

Now we can browse to https://isabell.uber.space/timetagger/cred to generate our preferred credentials. Choose a strong password. As a result you receive a string like ``isabell:$2a$08$SskWkSrYJnXvlwLPU7OAlecoCxMDs5vMr1Egs6INiqq1a4ZcH3wBa``.
We use this string and test the login by adding the credential to the startup script.

First stop the running python script by sending ``CTRL+C`` to the console.

.. code-block:: console
 :emphasize-lines: 2

 [INFO 2022-07-08 12:14:34] Server is starting up
 ^C[INFO 2022-07-08 12:44:39] Server is shutting down
 [isabell@stardust ~]$


.. note:: The credentials must be encapsulated by single quotation marks.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ python3.9 ~/bin/mytimetagger.py --bind=0.0.0.0:4800 --credentials='isabell:$2a$08$SskWkSrYJnXvlwLPU7OAlecoCxMDs5vMr1Egs6INiqq1a4ZcH3wBa'
 […]
 [INFO 2022-07-08 12:46:34] Collected 4 assets from /home/isabell/.local/lib/python3.9/site-packages/timetagger/pages/.
 [INFO 2022-07-08 12:46:34] Server is starting up

We should now be able to successfully login. Finally we setup a daemon to run TimeTagger automatically.

Set up the daemon
-----------------
Create the file ``~/etc/services.d/timetagger.ini`` with the following content:

.. note:: Replace the port and credentials with the credentials you previously created. Also, make sure to enter the correct home directory instead of isabell.

.. code-block:: ini
 :emphasize-lines: 2

 [program:timetagger]
 command=python3.9 %(ENV_HOME)s/bin/mytimetagger.py --bind=0.0.0.0:4800 --credentials='isabell:$2a$08$SskWkSrYJnXvlwLPU7OAlecoCxMDs5vMr1Egs6INiqq1a4ZcH3wBa'
 autostart=true
 autorestart=true
 startsecs=60

This will make sure that TimeTagger_ is automatically started if the host reboots.

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING`` after 60 seconds, something went wrong.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Updating is as simple as running pip again to update to the latest version and restarting the daemon.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ pip3.9 install --user --upgrade timetagger
 […]
 Successfully installed timetagger-22.6.6
 […]
 [isabell@stardust ~]$ supervisorctl restart timetagger
 timetagger: stopped
 timetagger: started
 [isabell@stardust ~]$

.. _TimeTagger: https://timetagger.app/
.. _feed: https://pypi.org/rss/project/timetagger/releases.xml
.. _GPLv3 License: https://opensource.org/licenses/GPL-3.0
.. _LICENSE: https://raw.githubusercontent.com/almarklein/timetagger/main/LICENSE
.. _Selfhost article: https://timetagger.app/articles/selfhost/

----

Tested with TimeTagger 22.6.6 and Uberspace 7.13

.. author_list::
