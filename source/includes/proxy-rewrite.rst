Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your port!

.. code-block:: apache
 :emphasize-lines: 4

 DirectoryIndex disabled

 RewriteEngine On
 RewriteRule ^(.*) http://localhost:<yourport>/$1 [P]

In our example this would be:

.. code-block:: apache

 DirectoryIndex disabled

 RewriteEngine On
 RewriteCond %{REQUEST_FILENAME} !-f
 RewriteBase /
 RewriteRule ^(.*)$ http://127.0.0.1:9000/$1 [P]
