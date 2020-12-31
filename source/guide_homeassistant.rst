.. highlight:: console

.. author:: Dirk <https://github.com/universalappfactory/>

.. tag:: python
.. tag:: iot
.. tag:: mqtt
.. tag:: web

.. sidebar:: About

  .. image:: _static/images/homeassistant.png
      :align: center


#########
Home Assistant
#########

.. tag_list::

Open source home automation that puts local control and privacy first. Powered by a worldwide community of tinkerers and DIY enthusiasts. Perfect to run on a Raspberry Pi or a local server.
[1]_

home-assistant is written in python and licensed under the Apache License 2.0.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * :manual:`Domains <web-domains>`

License
=======

Home-assistant is written in python and licensed under the Apache License 2.0.
All relevant legal information can be found here:

  * https://github.com/home-assistant/core/blob/dev/LICENSE.md

Prerequisites
=============

Your domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Create a virtual environment and install packages
-------------------
Install the homeassistant in a virtual environment.
Python 3.8 or later is recommended, so we'll stick on 3.8.

.. code-block:: console
 :emphasize-lines: 1,2,3,4,5,6

 [isabell@stardust ~]$ mkdir /home/isabell/homeassistant
 [isabell@stardust ~]$ cd /home/isabell/homeassistant
 [isabell@stardust ~]$ python3.8 -m venv .
 [isabell@stardust ~]$ source ./bin/activate
 [isabell@stardust ~]$ python3.8 -m pip install wheel
 [isabell@stardust ~]$ python3.8 -m pip install homeassistant
 [isabell@stardust ~]$


First time startup
---------------
Now we can start the homeassistant for the first time in order to create all needed configuration files.
Just run the following command in the created homeassistant directory with active venv.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ hass

A directory containing config files is created at /home/isabell/.homeassistant. 
So you can terminate the homeassistant using Strg-C.


Configuration
=============

Configure homeassistant
-------------------

Now it's time to make a basic configuration.
Here_ you can find more about the homeassistant configuration.

.. _Here: https://www.home-assistant.io/docs/configuration/basic/

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ nano ~/.homeassistant/configuration.yaml

Modify external_url and internal_url.

.. code-block:: yaml
  :emphasize-lines: 8,9

  homeassistant:
  name: Home
  latitude: 32.87336
  longitude: 117.22743
  elevation: 430
  unit_system: metric
  time_zone: Europe/Berlin
  external_url: "isabell.uber.space"
  internal_url: "0.0.0.0:8123"
  allowlist_external_dirs:
  allowlist_external_urls:
  media_dirs:
  legacy_templates: false

Setup a web backend
-------------------

::

    [isabell@stardust ~]$ uberspace web backend set / --http --port 8123    
    [isabell@stardust ~]$

 
Create a supervisord service entry
-------------------
nano /home/isabell/etc/services.d/homeassistant.ini

.. code-block:: ini
  :emphasize-lines: 8,9

  [program:homeassistant]
  command=python -m homeassistant
  autostart=yes
  autorestart=yes
  environment = PATH="/home/isabell/homeassistant/bin"

.. include:: includes/supervisord.rst


Finishing installation
======================

Now your homeassistant should be running and you can point your webbrowser to the configured domain in order to make the initial homeserver setup.


Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!

And last but not least, don't forget to check out the security checklist:

  * https://www.home-assistant.io/docs/configuration/securing/

Updates
=======

.. note:: Check out the packageindex_ regularly to stay informed about the newest version.

.. _packageindex: https://pypi.org/project/homeassistant/

----

Tested with homeassistant 2020.12.2, Uberspace 7.8.1.0

.. author_list::

.. [1] https://www.home-assistant.io/, 30.12.2020
