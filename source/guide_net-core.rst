.. highlight:: console

.. author:: Julian Oster <jlnostr@outlook.de>

.. sidebar:: Logo

  .. image:: https://manual.uberspace.de/en/_images/logo_dotnet.png
      :align: center

########
.NET Core
########

.NET Core is a free and open-source framework for Windows, macOS and Linux operating systems.

----

.. note:: For this guide you should follow the basic guide from `the Uberspace team`_.

License
=======

.NET Core is free and open source software licensed under the `MIT`_.

Installation
============

For the setup of .NET Core follow the basic guid from `the Uberspace team`_.

Configuration
=============

Using the Authentication middleware
-----------------------------------

In order to use the `Authentication middleware`_, you need to adjust the ``.htaccess`` file. This is due to the reason that your .NET Core application is not directly exposed to the web using the built-in Kestrel webserver, rather it's sitting behind an Apache proxy.
Therefore we need to tell the application a bit about the current hosting situation.

First of all, you need to install the ``Microsoft.AspNetCore.HttpOverrides`` NuGet package. After the installation is successful, add the following lines to the beginning your ``Configure()`` method in ``Startup.cs``:

::
 app.UseForwardedHeaders(new ForwardedHeadersOptions
 {
     ForwardedHeaders = ForwardedHeaders.All
 });

These lines should absolutely be placed at the top of the method, so that each following middleware can make use of the configuration. This is especially important for the already mentioned Authentication middleware.

When setup, your .NET Core app recognizes the ``X-Forwarded-For``, ``X-Forwarded-Proto`` and ``X-Forwarded-Host`` HTTP headers. These would be automatically set by Apache, if we could add custom ``.conf`` files, which we can't. Therefore we adjust the ``.htaccess`` to add these headers manually.

We need to add all three headers. Because Uberspace 7 only supports HTTPS, we can hardcode the protocol ``https``, we also can hardcode the ``X-Forwarded-For``. The only thing that needs to be adjusted is the ``X-Forwarded-Host`` header. Here you should enter the domain of your Uberspace account. This can be the default Uberspace domain, or a custom one.

::
 RequestHeader set "X-Forwarded-Proto" https
 RequestHeader set "X-Forwarded-For" 127.0.0.1
 RequestHeader set "X-Forwarded-Host" your.uber.space


For example, a complete ``.htaccess`` could look like this:

::
 RewriteEngine On
 RequestHeader set "X-Forwarded-Proto" https
 RequestHeader set "X-Forwarded-For" 127.0.0.1
 RequestHeader set "X-Forwarded-Host" my.uber.space
 RewriteRule ^(.*) http://localhost:63343/$1 [P]
 DirectoryIndex disabled

After that, everything should work as expected! 🎉

.. _the Uberspace team: https://manual.uberspace.de/en/lang-dotnet.html
.. _MIT: https://opensource.org/licenses/MIT
.. _Authentication middleware: https://docs.microsoft.com/en-us/aspnet/core/security/authentication/?view=aspnetcore-2.1

----

Tested with .NET Core 2.1.5, Uberspace 7.1.15.0

.. authors::
