.. highlight:: console

.. author:: René Nowak <rene-n@gmx.net>

.. tag:: blog
.. tag:: web
.. tag:: lang-python
.. tag:: comment

.. sidebar:: Logo

  .. image:: _static/images/isso.svg
      :align: center

##########
Isso
##########

.. tag_list::

Isso_ is a simple, self-hosted commenting server which can easily be included inside blogging platforms such as :lab:`Ghost <guide_ghost>` or :lab:`Wordpress <guide_wordpress>`.

Users can format comments by using Markdown. Isso has spam protection and an admin panel to administrate comments. 

The Isso Server is written in Python and the client side is realized by a small javascript. Comments are stored inside a sqlite database.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager :manual_anchor:`pip <lang-python.html#pip>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`

License
=======

All relevant legal information can be found here

  * https://github.com/posativ/isso/blob/master/LICENSE

Prerequisites
=============

We're using :manual:`Python <lang-python>` in the version 3.6.8:

::

 [isabell@stardust ~]$ python3 -V
 Python 3.6.8
 [isabell@stardust ~]$

Your commenting server URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$


Connect a web backend to the Isso Server port you want to use and which will be created later in this guide:

::

 [isabell@stardust ~]$ uberspace web backend set comments.isabell.uber.space --http --port 1234
 [isabell@stardust ~]$


Installation
============

Install Isso:

::

 [isabell@stardust ~]$ pip3.6 install isso --user
 Collecting isso
 [...]
 Successfully installed Jinja2-2.11.1 MarkupSafe-1.1.1 bleach-3.1.4 cffi-1.14.0 html5lib-1.0.1 isso-0.12.2 itsdangerous-1.1.0 misaka-2.1.1 pycparser-2.20 six-1.14.0 webencodings-0.5.1 werkzeug-1.0.1

 [isabell@stardust ~]$


Configuration
=============

Configure Isso
-------------------

Create and open the file ``~/etc/isso/user.cfg`` and configure it according to your needs. Check out the Isso server-manual_ for explanations of all possibilities:

::

 [general]
 dbpath = /home/isabell/etc/isso/comments.db
 host = https://isabell.uber.space/

 [server]
 listen = http://0.0.0.:1234/

The minimum settings are a link to the sqlite database as well as the host domain and the ip of the local host. The host domain is from where you want to access the isso server - be aware that the comment domain has to be a sub domain of the blog domain (read about CORS_ for more information).
The port can be any free port of your uberspace (you have chosen that port during the web backend configuration, mentioned above).


Run ``isso -c ~/etc/isso/user.cfg run`` to let Isso check and load the configurations. If everything is set up correctly you should see the following output:

::

 [isabell@stardust ~]$ isso -c ~/etc/isso/user.cfg run
 2020-04-04 13:27:56,086 INFO: connected to https://isabell.uber.space/
 [isabell@stardust ~]$

If you get any error message your configation settings are not correct.

.. note:: Currently Isso has an issue with the latest version of the module ``werkzeug``. If the code from above fails with the error message ``"ImportError: cannot import name 'SharedDataMiddleware'"`` you can use the following workaround until the issue gets fixed.

  * uninstall current version of ``werkzeug``:
    ::
     [isabell@stardust ~]$ pip3 uninstall werkzeug
     Uninstalling Werkzeug-1.0.1:
     [...]
     Successfully uninstalled Werkzeug-1.0.1
     [isabell@stardust ~]$

  * install a compatible version of ``werkzeug``:
    ::
     [isabell@stardust ~]$ pip3 install Werkzeug==0.16.1 --user
     Collecting Werkzeug==0.16.1
     [...]
     Successfully installed Werkzeug-0.16.1
     [isabell@stardust ~]$



Setup daemon
------------
Create and open the file ``~/etc/services.d/isso.ini`` to enter the following lines:

::

 [program:isso]
 command = /home/isabell/.local/bin/isso -c /home/isabell/etc/isso/user.cfg run
 autostart = true
 autorestart = true

Afterwards tell supervisord to read and load the updated configuration:

::

 [isabell@stardust ~]$ supervisorctl reread
 isso: available
 [isabell@stardust ~]$ supervisorctl update
 isso: added process group
 [isabell@stardust ~]$ supervisorctl status
 isso                             RUNNING   pid 12882, uptime 0:01:18
 [isabell@stardust ~]$


Finishing installation
======================

Now you can include Isso to your website by following the client-manual_. 
If you enabled the admin functionality inside the configuration you can access the admin panel by adding the path ``/admin``.


Security
--------

Use a strong password and salt value inside the server configuration (refer to Isso server-manual_).


Updates
=======

.. note:: Check for updates_ regularly to stay informed about the newest version.

When an update is available you can update it by running:

::

 [isabell@stardust ~]$ pip3 install --user --upgrade isso


.. _updates: https://github.com/posativ/isso/releases
.. _Isso: https://posativ.org/isso/
.. _server-manual: https://posativ.org/isso/docs/configuration/server/
.. _client-manual: https://posativ.org/isso/docs/configuration/client/
.. _CORS: https://de.wikipedia.org/wiki/Cross-Origin_Resource_Sharing

----

Tested with Isso 0.11.1, Uberspace 7.5.1.1

.. author_list::