Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your port!

::

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteRule ^(.*) http://localhost:<yourport>/$1 [P]

In our example this would be:

::

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteRule ^(.*) http://localhost:9000/$1 [P]
