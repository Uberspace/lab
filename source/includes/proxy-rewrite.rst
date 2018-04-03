Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your port!

::

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteCond %{HTTPS} !=on
 RewriteCond %{ENV:HTTPS} !=on
 RewriteRule .* https://%{SERVER_NAME}%{REQUEST_URI} [R=301,L]
 RewriteRule (.*) http://localhost:<yourport>/$1 [P]

In our example this would be:

::

 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteCond %{HTTPS} !=on
 RewriteCond %{ENV:HTTPS} !=on
 RewriteRule .* https://%{SERVER_NAME}%{REQUEST_URI} [R=301,L]
 RewriteRule (.*) http://localhost:9000/$1 [P]
 