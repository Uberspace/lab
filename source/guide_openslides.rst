.. highlight:: console

.. author:: GodMod <godmod@eqdkp-plus.eu>
.. tag:: lang-python
.. tag:: django
.. tag:: presentations
.. tag:: web
.. tag:: assemblies
.. tag:: meetings
.. tag:: audience-business

.. sidebar:: About

  .. image:: _static/images/openslides.svg
      :align: center

##########
OpenSlides
##########

.. tag_list::

OpenSlides is a free, web-based presentation and assembly system for managing and projecting agenda, motions, and elections of assemblies.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Web Backends <web-backends>`

License
=======

OpenSlides_ is released under the `MIT License`_.

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
Install the OpenSlides Python package:

::

 [isabell@stardust ~]$ pip3.9 install openslides --user
 [...]
 Running setup.py install for pyrsistent ... done
 Running setup.py install for PyPDF2 ... done
 Running setup.py install for roman ... done
 Running setup.py install for websockets ... done
 Running setup.py install for openslides ... done
 [...]
 [isabell@stardust ~]$

 Check if OpenSlides is installed by typing:

::

 [isabell@stardust ~]$ openslides --version
 3.3
 [isabell@stardust ~]$

Step 2
------

.. note::

    OpenSlides is running on port 8000.

.. include:: includes/web-backend.rst

Step 3
------
Start the OpenSlides binary:

::

 [isabell@stardust ~]$ openslides runserver 0.0.0.0:8000
 [2021-04-03 18:35:10 +0200] [16175] [INFO] openslides.utils.schema_version [SweN] No old schema version
 [...]
 Django version 2.2.19, using settings 'settings'
 Starting ASGI/Channels version 2.3.1 development server at http://0.0.0.0:8000/
 Quit the server with CONTROL-C.


Step 4
------
Now point your Browser to your installation URL ``https://isabell.uber.space``.

Use ``admin`` as username and ``admin`` as password for your first login. You should change this password at ``https://isabell.uber.space/users/password`` immediately after login!

Step 5
-------

Finally, you should set up a service that keeps OpenSlides alive while you are gone. Use `CTRL+C` to terminate the current running OpenSlides process. After that, create the file ``~/etc/services.d/openslides.ini`` with the following content:

.. code-block:: ini

 [program:openslides]
 command=openslides runserver 0.0.0.0:8000
 autostart=true
 autorestart=true
 stopsignal=INT

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configuration
=============

You can find the configuration file of OpenSlides at ``~/.config/openslides/settings.py``. There you can make settings for SMTP, Redis, SAML etc.


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, update the following command to update your OpenSlides python package:

::

 [isabell@stardust ~]$ pip install --upgrade openslides
 [isabell@stardust ~]$

Backup
======

Backup the following directories:

  * ``~/.local/share/openslides/``
  * ``~/.config/openslides/``

.. _OpenSlides: https://openslides.com/
.. _feed: https://github.com/OpenSlides/OpenSlides/releases.atom
.. _MIT License: https://github.com/OpenSlides/OpenSlides/blob/master/LICENSE

----

Tested with OpenSlides 3.3 and Uberspace 7.9.0.0

.. author_list::
