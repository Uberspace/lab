.. highlight:: console

.. author:: Sebastian Burschel <https://github.com/SeBaBu/>

.. tag:: web
.. tag:: file-storage
.. tag:: webdav

.. sidebar:: About

  .. image:: _static/images/wsgidav.png
      :align: center

############
WsgiDAV
############

.. tag_list::



----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

MIT license.

  * https://github.com/mar10/wsgidav/blob/master/LICENSE


Installation
============

Use pip3 to install wsgidav:

::

 [isabell@stardust ~]$ pip3 install wsgidav cheroot --user

Create the data folder:

::

 [isabell@stardust ~]$ mkdir ~/webdav


Add additional folders you want to access via webdav with:

::

 [isabell@stardust ~]$ mkdir ~/webdav/<newfoldername>

config file
======================

.. note::

    Only use spaces to indent in the config file! No tabs!


The following template is the minimum to get wsgidav up and running. You have to change provider_mapping, user_mapping and the port (if another service is already running on 8080).
If you miss some functionality or want more information, take a look at the sample file and the explanation of the configuration options:
https://wsgidav.readthedocs.io/en/latest/user_guide_configure.html#sample-wsgidav-yaml


Config file path:

::

 ~/.wsgidav/wsgidav.yaml
 


Config file:

::

 server: "cheroot"
 server_args:
     numthreads: 256
 host: 0.0.0.0
 port: 8080
 block_size: 8192
 add_header_MS_Author_Via: true
 hotfixes:
     winxp_accept_root_share_login: false
     win_accept_anonymous_options: false
     unquote_path_info: false
     re_encode_path_info: null
     emulate_win32_lastmod: true
 
 middleware_stack:
     - wsgidav.debug_filter.WsgiDavDebugFilter
     - wsgidav.error_printer.ErrorPrinter
     - wsgidav.http_authenticator.HTTPAuthenticator
     - wsgidav.dir_browser.WsgiDavDirBrowser
     - wsgidav.request_resolver.RequestResolver
 
 
 mount_path: null
 provider_mapping:
     "/": "/home/isabell/webdav/"
     "/firstpath": "/home/isabell/webdav/<newpath>"
 # Adds folder "/home/isabell/webdav/<newpath>" to URL https://isabell.uber.space/firstpath
	
 simple_dc:
     user_mapping:
         "*":  # default (used for all shares that are not explicitly listed). Keep this one!
             "isabell":
                 password: "<password>" # Change it!
                 roles: ["editor"]
         "/firstpath": # The mount_path this user has access to.
             "isabellscousin": # Username
                 password: "<password>" # Password. Change it!
 # Here you can add additional users (same indent)

 http_authenticator:
     accept_basic: true
     accept_digest: true
     default_to_digest: true
     trusted_auth_header: null
     domain_controller: null
 
 nt_dc:
     preset_domain: null
     preset_server: null
 pam_dc:
     service: "login"
     encoding: "utf-8"
     resetcreds: true
 verbose: 3
 logger_format: "%(asctime)s.%(msecs)03d - <%(thread)05d> %(name)-27s %(levelname)-8s: %(message)s"
 logger_date_format: "%H:%M:%S"
 error_printer:
     catch_all: false
 debug_methods: []
 debug_litmus: []
 dir_browser:
     enable: true
     ignore:
         - ".DS_Store"  # macOS folder meta data
         - "Thumbs.db"  # Windows image previews
         - "._*"  # macOS hidden data files
     icon: true
     response_trailer: true
     show_user: true
     show_logout: true
     davmount: false
     ms_mount: false
     ms_sharepoint_support: true
 
 property_manager: true
 mutable_live_props:
     - "{DAV:}getlastmodified"
 lock_manager: true




Configure web server
====================

.. note::

    wsgidav is running on port 8080.

.. include:: includes/web-backend.rst

Configure ``supervisord``
=========================

Create ``~/etc/services.d/wsgidav.ini`` with the following content:

.. code-block:: ini

 [program:wsgidav]
 command=wsgidav -c /home/isabell/.wsgidav/wsgidav.yaml
 directory = /home/isabell/webdav
 autostart=yes
 autorestart=yes

Start Service
=============

.. include:: includes/supervisord.rst

Now go to ``https://<username>.uber.space`` (would be ``https://isabell.uber.space`` in our example) and see if it works. Enjoy!


----

Tested with wsgidav 3.0.0, Uberspace 7.3.4.2

.. author_list::
