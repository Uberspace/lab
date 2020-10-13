.. highlight:: console

.. author:: jorsn <johannes@jorsn.eu>

.. tag:: office-suite
.. tag:: collaborative-editing
.. tag:: spreadsheet
.. tag:: presentation
.. tag:: web
.. tag:: docker
.. tag:: udocker

.. sidebar:: About

  .. image:: _static/images/libreoffice.svg
  .. image:: _static/images/collabora-code.svg
      :align: center

##################
LibreOffice Online
##################

.. tag_list::

`LibreOffice Online <LOOL_>`_ is a free online office suite based on the
desktop office suite LibreOffice. It comprises a word processor, a spreadsheet
and a presentation software. For usage it must be integrated with a file host
which provides file access via WOPI or WebDAV, such as :lab:`Nextcloud
<guide_nextcloud>` and :lab:`Seafile <guide_seafile>`, or via the local file
system.

`LibreOffice Online`_ is prebuilt as Linux distribution packages and as Docker
images. This guide covers installing, configuring and running the latter. As
Docker is not supported in Uberspace, `udocker`_ is used instead. It is a tool
for running docker containers using fake `chroot`_ techniques.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`

License
=======

LibreOffice and LibreOffice Online are licensed under the `MPL-2.0 and LGPL v3+
<https://www.libreoffice.org/download/license/>`_.

`Collabora Online Development Edition <CODE_>`_ (CODE) is a distribution of
LibreOffice Online. It is licensed `like the latter <CODE_>`_, and its Logo is
published under `CC0 <https://creativecommons.org/share-your-work/public-domain/cc0>`_.

`udocker`_ is licensed under the `Apache License 2.0
<https://github.com/indigo-dc/udocker/blob/master/LICENSE>`_.

Licensing information about containers on Dockerhub in general is available in Section 6 of its
`Terms of Service <Docker Terms of Service_>`_.

Prerequisites
=============

Setup the domain where your office installation will be accessible.

.. include:: includes/web-domain-list.rst

Then, install the latest stable version of `udocker`_:

::

  [isabell@stardust ~]$ curl https://raw.githubusercontent.com/indigo-dc/udocker/master/udocker.py > $HOME/bin/udocker
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100  338k  100  338k    0     0   522k      0 --:--:-- --:--:-- --:--:--  521k
  [isabell@stardust ~]$ chmod 0740 $HOME/bin/udocker
  [isabell@stardust ~]$ udocker install
  Info: setup repo: /home/isabell/.udocker
  Info: udocker command line interface 1.1.4
  Info: searching for udockertools 1.1.4
  Info: installing udockertools 1.1.4
  Info: installation of udockertools successful
  [isabell@stardust ~]$ 

This installs the binaries and libraries needed by udocker into ``$HOME/.udocker/``.

Installation
============

There are three officially endorsed docker distributions of LibreOffice:

  * `LibreOffice Online`_, by `The Document Foundation
    <https://www.documentfoundation.org/>`_ is the basis for all three. There
    is no official stable build, but an unstable docker image
    `libreoffice/online <https://hub.docker.com/r/libreoffice/online>`_.
  * `Collabora Office Development Edition <CODE_>`_ (CODE) is a more
    conservative development version of LibreOffice Online by Collabora_
    provided as docker image `collabora/code
    <https://hub.docker.com/r/collabora/code>`_.
  * `LibreOffice Powered by CIB`_ is a commercially supported distribution with
    the stable docker image `cibsoftware/libreoffice-online
    <https://hub.docker.com/r/cibsoftware/libreoffice-online>`_. It is not
    covered in this guide, as there is no reliable licensing information
    available for it, and it reqires a manual tweak (remove ``su``)
    in the startup script to run with `udocker_`.

On first sight, the main differences are the sizes of the docker images
and slightly different default configurations and look-and-feels. However, the new
*notebookbar* (ribbon-styled) design `introduced in CODE 6.4
<https://www.collaboraoffice.com/press-releases/code-6-4-0-release/>`_ does not
yet work correctly in the `libreoffice/online`_ docker image at the time of
writing (2020-10-14).

In the following, LibreOffice refers to any of the three distributions.
A listing of the ways to get LibreOffice Online is available on the
`official download page <LOOL_>`_ by The Document Foundation.

Assume you chose `collabora/code`_. Pull the image from dockerhub and create
a container:

::
  
  [isabell@stardust ~]$ udocker pull collabora/code
  Downloading layer: sha256:84ed7d2f608f8a65d944b40132a0333069302d24e9e51a6d6b338888e8fd0a6b
  Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
  [...]
  Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
  [isabell@stardust ~]$ udocker create --name=collabora-code collabora/code
  c974f5ce-60c2-3643-8405-30b31e67165b
  [isabell@stardust ~]$ 

.. note::

  The output of the second command is the UUID of the container named
  ``collabora-code``. If you leave out the ``--name`` flag, you must later use
  the UUID instead.


Configuration
=============

First, configure `udocker`_ to use `fakechroot`_ instead of `proot`_:
::

  [isabell@stardust ~]$ udocker setup --execmode=F1 collabora-code
  [isabell@stardust ~]$

.. note::

  By default, `udocker`_ uses `proot`_ to fake `chroot`_. However, `proot`_ does
  not support real multi-threading and leads to a noticeable lag when editing
  documents. An overview over the execmodes of udocker can be found in the
  `udocker manual <https://github.com/indigo-dc/udocker/blob/master/doc/user_manual.md#327-setup>`_.

Configuration file
------------------

To proceed, create a configuration directory, and copy the configuration file
from the container:

::
  
  [isabell@stardust ~]$ mkdir -p $HOME/etc/libreoffice/
  [isabell@stardust ~]$ cp $HOME/.udocker/containers/collabora-code/ROOT/etc/loolwsd/loolwsd.xml $HOME/etc/libreoffice/
  [isabell@stardust ~]$ chmod 0600 $HOME/etc/libreoffice/loolwsd.xml
  [isabell@stardust ~]$

Most options can be set in the configuration file, but some only on the
commandline (see below). In ``$HOME/etc/libreoffice/loolwsd.xml`` you can see
the possible config file options with their descriptions and default values.
Some options can only be set on the If you change the configuration file while
LibreOffice is running, it shuts down and gets restarted by supervisord, if
configured right.

.. note::

  * The permissions are set because ``loolwsd.xml`` will contain the admin console password.
  * The option ``user_interface.mode=classic|notebookbar`` is present in the config file but
    for the docker image `collabora/code`_ must be set on the commandline.
  * Exhaustive information about the commandline and environment options is
    available in the `docker setup instructions
    <https://www.collaboraoffice.com/code/docker/>`_ by Collabora.

Commandline configuration
-------------------------

Now create a startup script ``$HOME/etc/libreoffice/run`` with the following content:

.. warning::

  * Replace ``<dot-escaped-file-host-domain>`` by the domain of your file host
    with escaped dots, e.g. ``cloud\.example\.org``. You can separate multiple
    domains by ``|``.
  * Replace ``<my-super-secret-password>``. This will be the password for the
    admin console.
  * Set ``container`` to the container name you chose.

.. code-block:: sh

  #!/bin/bash
  # script checked with shellcheck, https://www.shellcheck.net/
  
  container=collabora-code
  config_file="$HOME"/etc/libreoffice/loolwsd.xml
  
  start_collabora="$HOME"/.udocker/containers/"$container"/ROOT/start-libreoffice.sh
  map_start_collabora=()
  [ -e "$start_collabora" ] && map_start_collabora=(-v "$start_collabora":/bin/start-libreoffice.sh)
  
  udocker run --env='domain=<dot-escaped-file-host-domain>' \
         --env=username=admin --env=password=<my-super-secret-password> \
         --env=DONT_GEN_SSL_CERT=1 \
         --env='extra_params=--o:security.capabilities=false --o:ssl.enable=false --o:ssl.termination=true' \
         -v /etc/ssl/certs/ca-bundle.trust.crt:/etc/loolwsd/ca-chain.cert.pem \
         -v "$config_file":/etc/loolwsd/loolwsd.xml \
         "${map_start_collabora[@]}" \
         --user=101 \
         "$container"

.. note::

  * By default, LibreOffice assumes the file host to be a WOPI host.
  * Options given as ``extra_params`` override options from the config file.
    The tags ``<ssl><enable>true</enable></ssl>`` in the config file have the
    same meaning as ``--o:ssl.enable=true`` passed on the command line.
    The set of options given in the example startup script is the minimal
    required one for the service to run without root capabilities and to let
    web backends handle TLS.
  * ``DONT_GEN_SSL_CERT`` must be set so that LibreOffice does not generate its
    own certificate.
  * The option ``-v <host path>:<guest path>`` maps a path in the host file
    system to a path in the container. ``map_start_collabora`` is a hack
    specific to the docker image `collabora/code`_, which otherwise doesn't
    find its internal startup script.
  * ``--user=101`` lets udocker emulate the correct user ID in the container.

The script must be executable and should only be readable by your user, because
it contains the admin password:

::

  [isabell@stardust ~]$ chmod 0700 $HOME/etc/libreoffice/run
  [isabell@stardust ~]$


Configure webserver
-------------------

The LibreOffice web server listens on port 9980 by default. You can find out if
another service is already listening on this port by running ``netstat -tulpen
| grep 9980``. If nothing is displayed, everything is fine. If the port is
blocked, choose another port ``<port>`` for LibreOffice by appending the flag
``--port=<port>`` to ``extra_params`` in ``$HOME/etc/libreoffice/run``.

.. include:: includes/web-backend.rst

If you setup the web backend to a subpath of the document root, you must also
assign it to the option ``net.service_root`` in ``extra_params`` (with
``--o:``) or in ``$HOME/etc/libreoffice/loolwsd.xml``.

Last, if you want to embed LibreOffice in a website served from another
domain or port than ``isabell.uber.space:443``, such as a Nextcloud,
you must change the :manual:`web headers <web-headers>`. This is necessary
because Uberspace sets ``X-Frame-Options: SAMEORIGIN`` by default, which allows
embedding only in websites served from the same domain and port.

::

  [isabell@stardust ~]$ uberspace web header suppress isabell.uber.space X-Frame-Options
  [isabell@stardust ~]$


Setup daemon
------------

Create a service configuration file ``$HOME/etc/services.d/libreoffice.ini``

.. code-block:: ini

  [program:libreoffice]
  command=%(ENV_HOME)s/etc/libreoffice/run
  startsecs=45
  autorestart=yes
  stopasgroup=yes
  killasgroup=yes

.. include:: includes/supervisord.rst

Test and use the service
========================

Run on the command line:

::

  [isabell@stardust ~]$ curl -k https://isabell.uber.space
  OK
  [isabell@stardust ~]$

If you get an ``OK`` the service is running and can be accessed.

Now you can navigate to https://isabell.uber.space/loleaflet/dist/admin/admin.html
to try out the admin console and configure your file host at
``cloud.example.org`` to use your libreoffice installation.

If you configured local file system storage, you can edit files *accessible in
the container* under the URL
https://isabell.uber.space/loleaflet/dist/loleaflet.html?file_path=file:///PATH/TO_DOC.
This is mainly intended for development and described in more detail in the
`development instructions <https://cgit.freedesktop.org/libreoffice/online/tree/loleaflet/README>`_.
To make a file or directory accessible in the container, add a ``-v``-mapping
to the ``$HOME/etc/libreoffice/run``.

Best practices
==============

When you have a settled installation and don't regularly build new containers
from the same image, clean up images using ``udocker rmi``. You don't need the
image when the container is built.

Security
--------

  * Unlike Docker, the processes started by `udocker`_ with `fakechroot`_
    are not isolated. This is less secure than using native Docker.
  * LibreOffice changes the config file ``loolwsd.xml``, for example to contain
    the admin password. The password is also contained in the ``run`` script.
    Therefore, maintain the restrictive permissions given above!

  * Set restrictive HTTP :manual:`web headers <web-headers>` such as

   - ``Content-Security-Policy: frame-ancestors 'self' cloud.example.org``
     at ``isabell.uber.space``
   - ``Content-Security-Policy: child-src 'self' isabell.uber.space``
     at ``cloud.example.org``.

  * LibreOffice only allows the configured *domain* as a file host, but it
    does not check the *path*. Hence it is advisable to have only the
    file host accessible under the given domain.

Tuning
======

Some performance statistics can be viewed in the admin console.
To tune it, you can set additional configuration options, for example

memproportion
  which sets the maximal percentage of memory consumed
  by LibreOffice, after which idle documents are cleaned up. Set it to a value
  below the 1.5 GB limit of your Uberspace, e.g. ``5.0``,
per_document.max_concurrency
  the number of threads one document renderer may use. An Uberspace has plenty of
  cpus, so you can set this to a higher value, e.g. ``10``, if you edit only
  few different documents simultaneously.

Troubleshooting
===============

Watch the :manual_anchor:`logs <daemons-supervisord#logging>`:

::

  [isabell@stardust ~]$ supervisorctl tail -f libreoffice stderr
  [isabell@stardust ~]$

If you stop the service and
run the startup script ``$HOME/etc/libreoffice/run`` directly in the terminal,
you even get nice colorful output!

* *I restarted the service, but it keeps dying, because it cannot listen at the
  port.* Sometimes the old instance doesn't shut down correctly, especially if
  aborted while starting. Kill it in ``htop``.

Other trouble? `Mail the author <johannes@jorsn.eu>`_, post under an existing
issue or create an `issue on GitHub <https://github.com/Uberspace/lab/issues>`_.

Updates
=======

.. tip::

  Check the `CODE feed`_ regularly to stay informed about the newest version of CODE.
  Unfortunately, there is no automatic way to get informed about docker image updates.
 
To update, for example to CODE version 6.5, run the following:

::

  [isabell@stardust ~]$ udocker pull collabora/code
  [isabell@stardust ~]$ udocker create --name=collabora-code-65 collabora/code
  e5abc845-e867-3331-85f6-9324f0a4e867
  [isabell@stardust ~]$ cp $HOME/.udocker/containers/collabora-code-65/etc/loolwsd/loolwsd.xml $HOME/etc/libreoffice/loolwsd-65.xml
  [isabell@stardust ~]$ chmod 0600 $HOME/etc/libreoffice/loolwsd-65.xml
  [isabell@stardust ~]$ diff --side-by-side $HOME/etc/libreoffice/loolwsd{,-65}.xml
  [isabell@stardust ~]$

Now migrate your config to the ``loolwsd-65.xml`` and update the variables
``container`` and ``config_file`` in ``$HOME/etc/libreoffice/run``.
Then, run ``supervisorctl restart libreoffice``.

.. admonition:: Edit note
  :class: warning

  Is the tip too editor specific? The style guide discourages mentioning
  specific editors.

.. tip::

  For migration, a diff tool like ``vimdiff`` in vim or ``ediff`` in emacs is
  useful, if you know the respective editor.

Check the logs, and if anything went wrong, you can still change back
``container`` and ``config_file`` in ``$HOME/etc/libreoffice/run``. After
``supervisorctl restart libreoffice`` the old version is running.

If everything is well, you can delete the old container and the config file:

::

  [isabell@stardust ~]$ udocker rm collabora-code
  [isabell@stardust ~]$ rm $HOME/etc/libreoffice/loolwsd.xml
  [isabell@stardust ~]$


.. _chroot: https://linux.die.net/man/2/chroot
.. _CODE: https://www.collaboraoffice.com/code/
.. _CODE feed: https://www.collaboraoffice.com/feed
.. _Collabora: https://www.collaboraoffice.com/
.. _Collabora Online: https://www.collaboraoffice.com/collabora-online/
.. _Docker Terms of Service: https://www.docker.com/legal/docker-terms-service
.. _fakechroot: https://github.com/dex4er/fakechroot/wiki
.. _Libreoffice powered by CIB: https://libreoffice.cib.de/
.. _LOOL: https://www.libreoffice.org/download/libreoffice-online/
.. _proot: https://proot-me.github.io/
.. _udocker: https://github.com/indigo-dc/udocker/

----

Tested with
LibreOffice Online 2020-08-09, CODE 6.4, udocker 1.1.4, on Uberspace 7.7.7,
connected to a Nextcloud 19.0.3 with the app Collabora Online 3.7.4.

.. author_list::
