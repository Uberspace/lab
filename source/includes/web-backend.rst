To make the application accessible from the outside, configure a `web backend <webbackend_>`_:

::

  [isabell@stardust ~]$ uberspace web backend set / --http --port <port>
  Set backend for / to port <port>; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html
