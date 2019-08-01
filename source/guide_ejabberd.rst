.. author:: fm0de

.. tag:: XMPP
.. tag:: Jabber
.. tag:: Instant Messanging

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ejabberd.png
      :align: center

########
ejabberd
########

.. tag_list::


`ejabberd <https://www.process-one.net/en/ejabberd/>`_ is a distributed, fault-tolerant technology that allows the creation of large-scale instant messaging applications. The server can reliably support thousands of simultaneous users on a single node and has been designed to provide exceptional standards of fault tolerance. As an open source technology, based on industry-standards, ejabberd can be used to build bespoke solutions very cost effectively.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`firewall ports <basics-ports>`
  * :manual:`web backends <web-backends>`

Prerequisites
=============

Domain
------

Your ejabberd domain needs to be setup. ejabberd defaults to the subomains
``upload.isabell.example``, ``conference.isabell.example`` , ``pubsub.isabell.example`` and ``proxy.isabell.example``

.. include:: includes/web-domain-list.rst


Erlang
------

ejabberd is written in Erlang see the `ejabberd documentation <https://docs.ejabberd.im/admin/installation/#requirements>`_ for the recomended version.
Easy installation of Erlang is done via `kerl <https://github.com/kerl/kerl>`_:
::

    [isabell@stardust ~]$ cd ~/bin
    [isabell@stardust bin]$ curl -O https://raw.githubusercontent.com/kerl/kerl/master/kerl
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
    100 66523  100 66523    0     0   331k      0 --:--:-- --:--:-- --:--:--  333k
    [isabell@stardust bin]$ chmod +x kerl
    [isabell@stardust ~]$ cd
    [isabell@stardust ~]$ kerl build 21.2
    Downloading otp_src_21.2.tar.gz to /home/isabell/.kerl/archives
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
    100   162  100   162    0     0    749      0 --:--:-- --:--:-- --:--:--   753
    100 81.3M  100 81.3M    0     0  2437k      0  0:00:34  0:00:34 --:--:-- 2401k
    Getting checksum file from erlang.org...
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   162  100   162    0     0    677      0 --:--:-- --:--:-- --:--:--   677
    100 32058  100 32058    0     0  69397      0 --:--:-- --:--:-- --:--:-- 69397
    Verifying archive checksum...
    Checksum verified (8a797dfe4cfb1bbf1b007f01b2f5a1ad)
    Extracting source code
    Building Erlang/OTP 21.2 (21.2), please wait...
    APPLICATIONS DISABLED (See: /home/isabell/.kerl/builds/21.2/otp_build_21.2.log)
    * jinterface     : No Java compiler found
    * odbc           : ODBC library - link check failed

    APPLICATIONS INFORMATION (See: /home/isabell/.kerl/builds/21.2/otp_build_21.2.log)
    * wx             : wxWidgets not found, wx will NOT be usable

    DOCUMENTATION INFORMATION (See: /home/isabell/.kerl/builds/21.2/otp_build_21.2.log)
    * documentation  :
    * fop is missing.
    * Using fakefop to generate placeholder PDF files.

    Erlang/OTP 21.2 (21.2) has been successfully built
    [isabell@stardust ~]$ kerl install 21.2 ~/erlang/builds/21.2/
    Installing Erlang/OTP 21.2 (21.2) in /home/isabell/erlang/builds/21.2...
    You can activate this installation running the following command:
    . /home/isabell/erlang/builds/21.2/activate
    Later on, you can leave the installation typing:
    kerl_deactivate
    [isabell@stardust ~]$. ~/erlang/builds/21.2/activate
    [isabell@stardust ~]$

Add your erlang installation to your .bash_profile:
::

    [isabell@stardust ~]$ echo ". ~/erlang/builds/21.2/activate #activate Erlang on shell" >> .bash_profile
    [isabell@stardust ~]$


LibYAML
-------
ejabberd needs `LibYAML <https://pyyaml.org/wiki/LibYAML>`_ for compilation:
::

    [isabell@stardust ~]$ wget https://pyyaml.org/download/libyaml/yaml-0.2.2.tar.gz
    --2019-07-10 09:28:21--  https://pyyaml.org/download/libyaml/yaml-0.2.2.tar.gz
    Auflösen des Hostnamen »pyyaml.org (pyyaml.org)«... 185.199.109.153, 185.199.108.153
    Verbindungsaufbau zu pyyaml.org (pyyaml.org)|185.199.109.153|:443... verbunden.
    HTTP-Anforderung gesendet, warte auf Antwort... 200 OK
    Länge: 609359 (595K) [application/gzip]
    In »»yaml-0.2.2.tar.gz«« speichern.

    100%[====================================================================================>] 609.359     --.-K/s   in 0,008s

    2019-07-10 09:28:21 (77,1 MB/s) - »»yaml-0.2.2.tar.gz«« gespeichert [609359/609359]

    [isabell@stardust ~]$ tar xf yaml-0.2.2.tar.gz
    [isabell@stardust ~]$ cd yaml-0.2.2/
    [isabell@stardust yaml-0.2.2]$./configure --prefix=/home/$USER/ejabberd
    checking for a BSD-compatible install... /usr/bin/install -c
    checking whether build environment is sane... yes
    checking for a thread-safe mkdir -p... /usr/bin/mkdir -p
    checking for gawk... gawk
    checking whether make sets $(MAKE)... yes
    checking whether make supports nested variables... yes
    checking for gcc... gcc
    checking whether the C compiler works... yes
    checking for C compiler default output file name... a.out
    checking for suffix of executables...
    checking whether we are cross compiling... no
    checking for suffix of object files... o
    checking whether we are using the GNU C compiler... yes
    checking whether gcc accepts -g... yes
    checking for gcc option to accept ISO C89... none needed
    checking whether gcc understands -c and -o together... yes
    checking for style of include used by make... GNU
    checking dependency style of gcc... gcc3
    checking how to run the C preprocessor... gcc -E
    checking whether ln -s works... yes
    checking whether make sets $(MAKE)... (cached) yes
    checking build system type... x86_64-pc-linux-gnu
    checking host system type... x86_64-pc-linux-gnu
    checking how to print strings... printf
    checking for a sed that does not truncate output... /usr/bin/sed
    checking for grep that handles long lines and -e... /usr/bin/grep
    checking for egrep... /usr/bin/grep -E
    checking for fgrep... /usr/bin/grep -F
    checking for ld used by gcc... /usr/bin/ld
    checking if the linker (/usr/bin/ld) is GNU ld... yes
    checking for BSD- or MS-compatible name lister (nm)... /usr/bin/nm -B
    checking the name lister (/usr/bin/nm -B) interface... BSD nm
    checking the maximum length of command line arguments... 1572864
    checking how to convert x86_64-pc-linux-gnu file names to x86_64-pc-linux-gnu format... func_convert_file_noop
    checking how to convert x86_64-pc-linux-gnu file names to toolchain format... func_convert_file_noop
    checking for /usr/bin/ld option to reload object files... -r
    checking for objdump... objdump
    checking how to recognize dependent libraries... pass_all
    checking for dlltool... no
    checking how to associate runtime and link libraries... printf %s\n
    checking for ar... ar
    checking for archiver @FILE support... @
    checking for strip... strip
    checking for ranlib... ranlib
    checking command to parse /usr/bin/nm -B output from gcc object... ok
    checking for sysroot... no
    checking for a working dd... /usr/bin/dd
    checking how to truncate binary pipes... /usr/bin/dd bs=4096 count=1
    checking for mt... no
    checking if : is a manifest tool... no
    checking for ANSI C header files... yes
    checking for sys/types.h... yes
    checking for sys/stat.h... yes
    checking for stdlib.h... yes
    checking for string.h... yes
    checking for memory.h... yes
    checking for strings.h... yes
    checking for inttypes.h... yes
    checking for stdint.h... yes
    checking for unistd.h... yes
    checking for dlfcn.h... yes
    checking for objdir... .libs
    checking if gcc supports -fno-rtti -fno-exceptions... no
    checking for gcc option to produce PIC... -fPIC -DPIC
    checking if gcc PIC flag -fPIC -DPIC works... yes
    checking if gcc static flag -static works... no
    checking if gcc supports -c -o file.o... yes
    checking if gcc supports -c -o file.o... (cached) yes
    checking whether the gcc linker (/usr/bin/ld -m elf_x86_64) supports shared libraries... yes
    checking whether -lc should be explicitly linked in... no
    checking dynamic linker characteristics... GNU/Linux ld.so
    checking how to hardcode library paths into programs... immediate
    checking whether stripping libraries is possible... yes
    checking if libtool supports shared libraries... yes
    checking whether to build shared libraries... yes
    checking whether to build static libraries... yes
    checking for doxygen... true
    checking for ANSI C header files... (cached) yes
    checking for stdlib.h... (cached) yes
    checking for an ANSI C-conforming const... yes
    checking for size_t... yes
    checking that generated files are newer than configure... done
    configure: creating ./config.status
    config.status: creating yaml-0.1.pc
    config.status: creating include/Makefile
    config.status: creating src/Makefile
    config.status: creating Makefile
    config.status: creating tests/Makefile
    config.status: creating include/config.h
    config.status: executing depfiles commands
    config.status: executing libtool commands
    [isabell@stardust yaml-0.2.2]$ make    
    Making all in include                                                                                                           [...]
    mv -f .deps/run-emitter-test-suite.Tpo .deps/run-emitter-test-suite.Po
    /bin/sh ../libtool  --tag=CC   --mode=link gcc  -g -O2   -o run-emitter-test-suite run-emitter-test-suite.o ../src/libyaml.la 
    libtool: link: gcc -g -O2 -o .libs/run-emitter-test-suite run-emitter-test-suite.o  ../src/.libs/libyaml.so -Wl,-rpath -Wl,/home/ejabberd/ejabberd/lib
    make[1]: Leaving directory `/home/ejabberd/yaml-0.2.2/tests'
    [isabell@stardust yaml-0.2.2]$ make install
    Making install in include
    [...]
    Making install in tests
    make[1]: Entering directory `/home/ejabberd/yaml-0.2.2/tests'
    make[2]: Entering directory `/home/ejabberd/yaml-0.2.2/tests'
    make[2]: Nothing to be done for `install-exec-am'.
    make[2]: Nothing to be done for `install-data-am'.
    make[2]: Leaving directory `/home/ejabberd/yaml-0.2.2/tests'
    make[1]: Leaving directory `/home/ejabberd/yaml-0.2.2/tests'
    [ejabberd@stardust yaml-0.2.2]$ 

Installation
============

Provide the LibYAML path to the compiler:
::

    [isabell@stardust ejabberd-19.05]$ export CFLAGS=-I/home/isabell/ejabberd/include
    [isabell@stardust ejabberd-19.05]$ export CPPFLAGS=-I/home/isabell/ejabberd/include
    [isabell@stardust ejabberd-19.05]$ export LDFLAGS=-L/home/isabell/ejabberd/lib
    [isabell@stardust ejabberd-19.05]$

Download and install ejabberd:
::

    [isabell@stardust ~]$ wget https://github.com/processone/ejabberd/archive/19.05.tar.gz
    --2019-07-10 09:48:53--  https://github.com/processone/ejabberd/archive/19.05.tar.gz
    Auflösen des Hostnamen »github.com (github.com)«... 140.82.118.4
    Verbindungsaufbau zu github.com (github.com)|140.82.118.4|:443... verbunden.
    HTTP-Anforderung gesendet, warte auf Antwort... 302 Found
    Platz: https://codeload.github.com/processone/ejabberd/tar.gz/19.05[folge]
    --2019-07-10 09:48:53--  https://codeload.github.com/processone/ejabberd/tar.gz/19.05
    Auflösen des Hostnamen »codeload.github.com (codeload.github.com)«... 140.82.114.10
    Verbindungsaufbau zu codeload.github.com (codeload.github.com)|140.82.114.10|:443... verbunden.
    HTTP-Anforderung gesendet, warte auf Antwort... 200 OK
    Länge: nicht spezifiziert [application/x-gzip]
    In »»19.05.tar.gz«« speichern.

        [    <=>                                                                              ] 1.865.845   1,51MB/s   in 1,2s

    2019-07-10 09:48:55 (1,51 MB/s) - »19.05.tar.gz« gespeichert [1865845]

    [isabell@stardust ~]$ tar xf 19.05.tar.gz
    [isabell@stardust ~]$ cd ejabberd-19.05/
    [isabell@stardust ejabberd-19.05]$./autogen.sh
    [isabell@stardust ejabberd-19.05]$ ./configure --enable-user=$USER --prefix=/home/$USER/ejabberd
    checking whether make sets $(MAKE)... yes
    checking for a BSD-compatible install... /usr/bin/install -c
    checking for a sed that does not truncate output... /usr/bin/sed
    checking for erl... /home/isabell/erlang/builds/21.2/bin/erl
    checking for erlc... /home/isabell/erlang/builds/21.2/bin/erlc
    checking for epmd... /home/isabell/erlang/builds/21.2/bin/epmd
    checking for erl... /home/isabell/erlang/builds/21.2/bin/erl
    checking for erlc... /home/isabell/erlang/builds/21.2/bin/erlc
    checking Erlang/OTP version... ok
    checking for Erlang/OTP root directory... /home/isabell/erlang/builds/21.2
    checking for escript... /home/isabell/erlang/builds/21.2/bin/escript
    checking for make... make
    allow this system user to start ejabberd: isabell
    configure: creating ./config.status
    config.status: creating Makefile
    config.status: creating vars.config
    config.status: creating src/ejabberd.app.src
    [isabell@stardust ejabberd-19.05]$

Install it:
::

    [isabell@stardust ejabberd-19.05]$ make install

Make the controll script available:

.. code-block:: console

   [isabell@stardust ~]$ ln -s ~/ejabberd/sbin/ejabberdctl ~/bin/ejabberdctl
   [isabell@stardust ~]$


Configuration
=============

Open Firewall Ports
-------------------
ejabberd needs 4 open ports for c2s, s2s, http and proxy connections.

.. include:: includes/open-port.rst

As standard ports can not always be used on uberspace an external domain is needed and SRV records must be set for c2s and s2s connections. Refer to the `XMPP wiki <https://wiki.xmpp.org/web/SRV_Records>`_ for setup and point them to the corresponding ports.

Change the configuration
------------------------

A standard config file is provided at ``~/ejabberd/etc/ejabberd/ejabberd.yaml`` where the ports, domain and administrator need to be set:

Change the host configuration to listen for the correct domain:

.. code-block:: ini
 :emphasize-lines: 2

  hosts:
  - "isabell.example"

Provide location of your keys and certificates for TLS transport:

.. note:: The list can be expanded with certfiles for each domain and subdomain.
.. code-block:: ini
 :emphasize-lines: 2,3

  certfiles:
    - "/home/isabell/etc/certificates/isabell.example.crt"
    - "/home/isabell/etc/certificates/isabell.example.key"


Change the port numbers to your open ports according to your SRV records:

.. code-block:: ini
 :emphasize-lines: 3,11

  listen:
    -
      port: <c2s-port>
      ip: "::"
      module: ejabberd_c2s
      max_stanza_size: 262144
      shaper: c2s_shaper
      access: c2s
      starttls_required: true
    -
      port: <s2s-port>
      ip: "::"
      module: ejabberd_s2s_in
      max_stanza_size: 524288

Change the ``<http-port>`` and disable TLS as it is going to be provided through web backends and disable the last two listeners:

.. code-block:: ini
 :emphasize-lines: 2,5,13-23

    -
      port: <http-port>
      ip: "::"
      module: ejabberd_http
    #  tls: true
      request_handlers:
        "/admin": ejabberd_web_admin
        "/api": mod_http_api
        "/bosh": mod_bosh
        "/captcha": ejabberd_captcha
        "/upload": mod_http_upload
        "/ws": ejabberd_http_ws
    #-
    #  port: 5280
    #  ip: "::"
    #  module: ejabberd_http
    #  request_handlers:
    #    "/admin": ejabberd_web_admin
    #-
    #  port: 1883
    #  ip: "::"
    #  module: mod_mqtt
    #  backlog: 1000

Add your admin user:

.. code-block:: ini
 :emphasize-lines: 2-4

  acl:
    admin:
      user:
        - "admin@isabell.uber.space"
    local:
      user_regexp: ""
    loopback:
      ip:
        - "127.0.0.0/8"
        - "::1/128"

Remove the port from the put_url and provide configuration for mod_http_upload:

.. code-block:: ini
 :emphasize-lines: 2-9

    mod_http_upload:
      put_url: "https://@HOST@/upload"
      file_mode: "0640"
      dir_mode: "2750"
      max_size: 104857600 # 100 MB
      access: local
      thumbnail: false
      docroot: "/home/isabell/ejabberd/upload"
      secret_length: 40

Disable mod_mqtt:

.. code-block:: ini
 :emphasize-lines: 1

    #mod_mqtt: {}

Configure mod_proxy65:

.. code-block:: ini
 :emphasize-lines: 2,4-7

    mod_proxy65:
    #   access: local
      max_connections: 5
      host: "proxy.isabell.example"
      name: "File Transfer Proxy"
      ip: "::"
      port: <proxy-port>

ejabberd defaults to plain text passwords so the following two lines need to be added to enable scram:

.. code-block:: ini

   auth_method: internal
   auth_password_format: scram


For additional options visit the `ejabberd documentation <https://docs.ejabberd.im/admin/configuration/>`_

Configure web backend
---------------------

.. note::

    ejabberd is listening on  ``<http-port>``.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/ejabberd.ini`` with the following content:

.. code-block:: ini

  [program:ejabberd]
  command=/home/isabell/ejabberd/sbin/ejabberdctl foreground
  autostart=yes
  autorestart=yes
  stopasgroup=true
  killasgroup=true
  stopsignal=INT


.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Register your administrator user:

.. code-block:: console

   [isabell@stardust ~]$ ejabberdctl register admin isabell.example <password>
   [isabell@stardust ~]$


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check ejabberd's `releases <https://github.com/processone/ejabberd/releases>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop ejabberd`` and repeat the "Installation" step followed by ``supervisorctl start ejabberd`` to restart ejabberd.

.. _Documentation: https://docs.ejabberd.im/
.. _feed: https://github.com/processone/ejabberd/releases.atom
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with ejabberd 19.05, erlang 21.2 and Uberspace 7.3.3.0

.. author_list::
