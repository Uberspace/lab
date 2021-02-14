.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: web
.. tag:: python

.. sidebar:: Logo


  .. image:: _static/images/searx.png
      :align: center

#####
searX
#####

.. tag_list::

Searx_ (Wikipedia_) is a free and open-source metasearch engine which aggregate results from more than 70 search services (e.g. Google, Bing etc.) and to avoid user tracking and profiling by these ones.

There are public instances_ of searx available, to get a personal practice before you install your own.

License
=======

Searx is released under the `GNU Affero General Public License`_.

----

.. note:: For this guide you should be familiar with the uberspace basic concepts of

  * supervisord_
  * domains_
  * `web backends`_

Installation
============

Step 1 - Repository Cloning
---------------------------

We will prepare the destination for the searx repository:

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p ~/opt/searx/

And clone the repository from GitHub:

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/searx/searx.git ~/opt/searx/

Step 2 - Python Module Installation
-----------------------------------

----

.. note:: Here we use python 3. This is the reason, that these guide consider this version aspect to the installation tool like ``pip`` and later to ``python`` it self.

Some python modules are necessary and will be installed in your uberspace with ``pip3`` and the option ``--user``:

.. code-block:: console

 [isabell@stardust ~]$ pip3 install --user requests pyyaml pygments werkzeug babel flask flask_babel lxml langdetect python-dateutil

Step 3 - Searx Configuration
----------------------------

We create the configuration file destination directory:

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/etc/searx

And copy the example file with basic default settings to the new directory:

.. code-block:: console

 [isabell@stardust ~]$ cp ~/opt/searx/utils/templates/etc/searx/use_default_settings.yml ~/etc/searx/settings.yml

Now it's time to change some entries in the configuration file:

1. Searx requires for the own instance a secret key. This random number will be created with openssl (16 digits) and placed direct in the config file via sed, the stream editor.

.. code-block:: console

 [isabell@stardust ~]$ sed -i -e "s/ultrasecretkey/`openssl rand -hex 16`/g" ~/etc/searx/settings.yml


2. You can change the name of your own searx instance. The standard name is "searx".

3. The bind address must be changed to ``0.0.0.0``, to work with `web backends`_ in a common way.

----

.. note:: The port with ``8888`` will not be touched, but keep this number in your mind for later configurtations.

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
    secret_key : "01234567890123456" # change this!
    base_url : False # Set custom base_url. Possible values: False or "https://your.custom.host/location/"
    image_proxy : False # Proxying image results through searx

# uncomment below section if you have running morty proxy
#result_proxy:
#    url : http://127.0.0.1:3000/
#    key : !!binary "your_morty_proxy_key"


Step 4 - Supervisord Setup
--------------------------

At first we must create the service file ``~/etc/services.d/searx.ini`` and the following content:

.. warning:: The PATH variable consider the installed Python modules regarding to the version 3.6 at this time point. Please have a look in the directory ``~/.local/lib/`` to be sure which version is the actual ones.

.. code-block::
 :emphasize-lines: 2

[program:searx]
environment =
 PATH="%(ENV_HOME)s/opt/searx/:%(ENV_HOME)s/.local/lib/python3.6/:%(ENV_PATH)s",
 SEARX_SETTINGS_PATH="%(ENV_HOME)s/etc/searx/settings.yml"
autostart=yes
autorestart=yes
command=python3 %(ENV_HOME)s/opt/searx/searx/webapp.py


We must report to supervisord that there is a new ini file to consider:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 searx: available


 And then to start the daemon:

 .. code-block:: console

 [isabell@stardust ~]$ supervisorctl update
 searx: added process group


At this time point, searx should be run in the background.

Step 5 - Domain Setup
---------------------

This guide consider a subdomain ``searx.isabell.example`` for your own searx instance.

.. code-block:: console

 [isabell@stardust ~]$ uberspace web domain add searx.isabell.example

.. note:: Please be sure, that your new subdomain is configured at your domain provider too.

If you want to find out that everthing is maintained for the web server on your Uberspace account, use the command:

.. code-block:: console

[isabell@stardust ~]$ uberspace web domain list
isabell.example
searx.isabell.example
isabell.uber.space

Step 6 - Web Backend Setup
--------------------------

This step is important, that your running searx instance is reachable from outside.

If this your first time to use web backends, you have to set it up:

.. code-block:: console

[isabell@stardust ~]$ uberspace web backend

Manage backends in web server configuration.

Possible commands:
  del — Delete web backend for a given domain and path.
  list — List all configured web backends.
  set — Set web backend for a given domain and path.


The following command supports the incomming request with the address http://searx.isabell.example and route this to the searx-daemon, listening on port ``8888``.

.. code-block:: console

[isabell@stardust ~]$ uberspace web backend set searx.isabell.example --http --port 8888

Step 7 - Debugging
------------------

In case of problems, the log file ``~/logs/supervisord.log`` is the first point for you.

Any configuration changes will be considered with a restart of the daemon:

.. code-block:: console

[isabell@stardust ~]$ supervisorctl restart searx

Tuning
======
The basic configuration is quiet well. Nearly all aspects to change are prossible from the searx front-end. These changes will be saved in a cookie, a temporary solution.

If you want to reduce the search services for example by default, than you have to change the standard configuration.

The official documentation_ is a good address. A bigger configuration file example is available at ``~/opt/searx/searx/setting.yml``


.. _Searx: https://github.com/searx/searx
.. _Wikipedia: https://en.wikipedia.org/wiki/Searx
.. _GNU Affero General Public License: https://github.com/searx/searx/blob/master/LICENSE
.. _instances: https://searx.space/
.. _supervisord: https://manual.uberspace.de/daemons-supervisord/
.. _domains: https://manual.uberspace.de/web-domains/
.. _web backends: https://manual.uberspace.de/web-backends/
.. _documentation: https://searx.github.io/searx/

----

Tested with Uberspace 7.9.0.0 and searx 0.18.0

.. author_list::
