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

.. abstract::
  `LibreOffice Online <LOOL_>`_ is a free online office suite based on the
  desktop office suite LibreOffice. It comprises a word processor, a spreadsheet
  and a presentation software.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * :manual:`web backends <web-backends>`

.. note::

  `LibreOffice Online`_ is prebuilt as Linux distribution packages and as Docker
  images. As a user one cannot install the former and Docker is not supported in
  Uberspace. So this guide uses `udocker`_ instead, a tool for running docker
  containers using fake `chroot`_ techniques.

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

`LibreOffice Online`_ is only an editor. To store the files and provide access
to them you must have WOPI host or a WebDAV server running.
For example, :lab:`Nextcloud <guide_nextcloud>` with the Collabora app and
:lab:`Seafile <guide_seafile>` Professional Edition integrate LibreOffice
Online via WOPI. A list of integrations can be found at the `CODE`_ website.

For this guide, WebDAV was not tested.
It is assumed that you use a WOPI host accessible at ``cloud.example.org``.

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
    active development version of LibreOffice Online by Collabora_
    provided as docker image `collabora/code
    <https://hub.docker.com/r/collabora/code>`_.
  * `LibreOffice Powered by CIB`_ is a commercially supported distribution with
    the stable docker image `cibsoftware/libreoffice-online
    <https://hub.docker.com/r/cibsoftware/libreoffice-online>`_. It is not
    covered in this guide, as there is no reliable licensing information
    available for it.

On first sight, the main differences are the sizes of the docker images
and slightly different default configurations and look-and-feels. However, the new
*notebookbar* (ribbon-styled) design `introduced in CODE 6.4
<https://www.collaboraoffice.com/press-releases/code-6-4-0-release/>`_ does not
yet work correctly in the `libreoffice/online`_ docker image at the time of
writing (2021-02-16).

In the following, LibreOffice refers to both `LibreOffice Online`_ and `CODE`_.
A listing of the ways to get LibreOffice Online is available on the
`official download page <LOOL_>`_ by The Document Foundation.

Assume you chose `collabora/code`_. Pull the image from dockerhub and create
a container:

::

  [isabell@stardust ~]$ udocker pull collabora/code
  Downloading layer: sha256:7595c8c21622ea8a8b9778972e26dbbe063f7a1c4b0a28a80a34ebb3d343b586
  Downloading layer: sha256:d13af8ca898f36af68711cb67c345f65046a78ccd802453f4b129adf9205b1f8
  [...]
  Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
  [isabell@stardust ~]$ udocker create --name=collabora-code collabora/code
  dbe828ab-d8a7-3a09-bf41-5deea8ec162c
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
  documents. An overview of the execution modes of udocker can be found in the
  `udocker manual <https://github.com/indigo-dc/udocker/blob/master/doc/user_manual.md#327-setup>`_.

Configure webserver
-------------------

.. note::

    The LibreOffice web server is running on port 9980.

.. include:: includes/web-backend.rst

If you want to embed LibreOffice in a website served from a domain or port
other than ``isabell.uber.space:443``, such as a Nextcloud at ``cloud.example.org``,
you must change the :manual:`web headers <web-headers>`. This is necessary
because Uberspace sets ``X-Frame-Options: SAMEORIGIN`` by default, which allows
embedding only in websites served from the same domain and port.

::

  [isabell@stardust ~]$ uberspace web header suppress isabell.uber.space X-Frame-Options
  [isabell@stardust ~]$

Configuration file
------------------

There is a configuration file ``$HOME/.udocker/containers/collabora-code/ROOT/etc/loolwsd/loolwsd.xml``,
which contains also explanations of the configuration options.
But since some options cannot be set there, in this guide configuration
is done via the commandline.

Documentation about the commandline and environment options is
available in the `docker setup instructions
<https://www.collaboraoffice.com/code/docker/>`_ by Collabora.

Setup daemon
------------

Create a service definition file ``$HOME/etc/services.d/libreoffice.ini``
and set the file permissions (it will contain a password):

::

  [isabell@stardust ~]$ touch $HOME/etc/services.d/libreoffice.ini
  [isabell@stardust ~]$ chmod 0600 $HOME/etc/services.d/libreoffice.ini

Open the file and insert the following content:

.. code-block:: ini
  :emphasize-lines: 2-8

  [program:libreoffice]
  environment=
      fileserver=cloud.example.org
      ,container="collabora-code"
      ,dictionaries="de_DE en_GB en_US"
      ,username="admin"
      ,password="<my super secret password>"
      ,extra_params=""
  command=bash -c '\
      %(ENV_HOME)s/bin/udocker run \
      --user="$(jq -r .container_config.User \
                   < %(ENV_HOME)s/.udocker/containers/"$container"/container.json)" \
      --env=DONT_GEN_SSL_CERT=1 \
      --workdir=/ \
      --env=domain="$(echo "$fileserver" | sed "s/\./\\\\./g")" \
      --env=username="$username" --env=password="$password" \
      --env=dictionaries="$dictionaries" \
      --env="extra_params=--o:ssl.enable=false --o:ssl.termination=true --o:security.capabilities=false $extra_params" \
      "$container" \
      '
  startsecs=45
  autorestart=yes
  stopasgroup=yes
  killasgroup=yes

.. warning::

  * Replace ``<my super secret password>``. This will be the password for the
    admin console.

.. note::

  * You can configure the service via the ``environment`` variables (highlighted!).
  * Multiple file server domains can be separated by ``|``.
  * By default, LibreOffice assumes the file server to be a WOPI host.
  * If you setup the web backend to a subpath of the document root, you must also
    set ``--o:net.service_root=<subpath>`` in ``extra_params``.
  * Options given as ``extra_params`` override options from the config file.
    The tags ``<ssl><enable>true</enable></ssl>`` in the config file have the
    same meaning as ``--o:ssl.enable=true`` passed on the command line.
    The set of options given in the example startup script is the minimal
    required one for the service to run without root capabilities and to let
    web backends handle TLS.

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
to try out the admin console. You can also configure your file host at
``cloud.example.org`` to use your libreoffice installation.


Best practices
==============

When you have a settled installation and don't regularly build new containers
from the same image, clean up images using ``udocker rmi``. You don't need the
image when the container is built.

Security
--------

  * Unlike Docker, the processes started by `udocker`_ with `fakechroot`_
    are not isolated. This is less secure than using native Docker.

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
  [isabell@stardust ~]$ udocker setup --execmode=F1 collabora-code-65
  [isabell@stardust ~]$

Now update the variable ``container`` in the service definition
``$HOME/etc/services.d/libreoffice.ini``
and run ``supervisorctl reread && supervisorctl update``.

Check the logs, and if anything went wrong, you can still change back
``container`` in the service definition to run the old version.

If everything is fine, you can delete the old container:

::

  [isabell@stardust ~]$ udocker rm collabora-code
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
LibreOffice Online 2020-09-08, CODE 6.4.6.2, udocker 1.1.4, on Uberspace 7.9.0,
connected to a Nextcloud 19.0.7 with the app Collabora Online 3.7.14.

.. author_list::
