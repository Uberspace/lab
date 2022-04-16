.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: web
.. tag:: lang-python

.. sidebar:: Logo


  .. image:: _static/images/searx.png
      :align: center

#####
Searx
#####

.. tag_list::

Searx_ (Wikipedia_) is a free and open-source metasearch engine which aggregate results from more than 70 search services (e.g. Google, Bing etc.) and to avoid user tracking and profiling by these ones.

There are public instances_ of searx available, to get a personal practice before you install your own.

----

License
=======

Searx is released under the `GNU Affero General Public License`_.


.. note:: For this guide you should be familiar with the uberspace basic concepts of

  * supervisord_
  * domains_
  * `web backends`_


Installation
============

Repository Cloning
------------------

We will prepare the destination for the searx repository:

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p ~/opt/searx/

And clone the repository from GitHub:

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/searx/searx.git ~/opt/searx/

Python Module Installation
--------------------------

.. note:: We are using Python 3.8 instead of the default Python 2 (or the ``python3`` alias, which links to Python 3.6), as some depencencies of searx require this. For this reason, all ``pip`` and ``python`` commands need a version postfix ``3.8`` like below. (``3.9`` should work as well.)

Some required Python modules are necessary and will be installed in your uberspace with ``pip3.8`` and the options ``--user``, ``--upgrade`` and ``--requirement``:

.. code-block:: console

 [isabell@stardust ~]$ pip3.8 install --user --upgrade --requirement ~/opt/searx/requirements.txt

Configuration
-------------

We create the configuration file destination directory:

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/etc/searx

And copy the example file with basic default settings to the new directory:

.. code-block:: console

 [isabell@stardust ~]$ cp ~/opt/searx/utils/templates/etc/searx/use_default_settings.yml ~/etc/searx/settings.yml

Now it's time to change some entries in the configuration file ``~/etc/searx/settings.yml`` with your favourite editor. But here are the aspects to consider:

1. You can change the name of your own searx instance. The standard name is "searx".

2. The port with ``8888`` will not be touched, but keep this number in your mind for later configurtations.

3. The bind address must be changed to ``0.0.0.0``, to work with `web backends`_ in a common way.

4. Searx requires for the own instance a secret key. This random number will be created with openssl (16 digits) and please save it temporarily:

.. code-block:: console

  [isabell@stardust ~]$ openssl rand -hex 16
  012345678901234x


.. code-block:: yaml
 :emphasize-lines: 5,13,14,15

  use_default_settings: True

  general:
      debug : False # Debug mode, only for development
      instance_name : "searx" # displayed name

  search:
      safe_search : 0 # Filter results. 0: None, 1: Moderate, 2: Strict
      autocomplete : "" # Existing autocomplete backends: "dbpedia", "duckduckgo", "google", "startpage", "swisscows", "qwant", "wikipedia" - leave blank to turn it off by default
      default_lang : "" # Default search language - leave blank to detect from browser information or use codes from 'languages.py'

  server:
      port : 8888
      bind_address : "0.0.0.0" # address to listen on
      secret_key : "012345678901234x" # change this with your own secret key!
      base_url : False # Set custom base_url. Possible values: False or "https://your.custom.host/location/"
      image_proxy : False # Proxying image results through searx

Supervisord Setup
-----------------

At first we must create the service file ``~/etc/services.d/searx.ini`` with the following content:

.. code-block::

  [program:searx]
  environment=SEARX_SETTINGS_PATH="%(ENV_HOME)s/etc/searx/settings.yml"
  autostart=yes
  autorestart=yes
  command=python3.8 %(ENV_HOME)s/opt/searx/searx/webapp.py

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Web Backend Setup
-----------------

.. note::

    Searx is running on port 8888.

.. include:: includes/web-backend.rst

Debugging
---------

In case of problems, the log file ``~/logs/supervisord.log`` is the first point for you.

Any configuration changes will be considered with a restart of the daemon:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart searx

Tuning
======
The basic configuration is quiet well. Nearly all aspects to change are possible from the searx front-end. These changes will be saved in a cookie, a temporary solution.

If you want to reduce the search services for example by default, than you have to change the standard configuration.

The official documentation_ is a good address. A bigger configuration file example is available at ``~/opt/searx/searx/setting.yml``.


.. _Searx: https://github.com/searx/searx
.. _Wikipedia: https://en.wikipedia.org/wiki/Searx
.. _GNU Affero General Public License: https://github.com/searx/searx/blob/master/LICENSE
.. _instances: https://searx.space/
.. _supervisord: https://manual.uberspace.de/daemons-supervisord/
.. _domains: https://manual.uberspace.de/web-domains/
.. _web backends: https://manual.uberspace.de/web-backends/
.. _documentation: https://searx.github.io/searx/
.. _web backend: https://manual.uberspace.de/web-backends/

----

Tested with Uberspace 7.9.0.0 and searx 0.18.0

.. author_list::
