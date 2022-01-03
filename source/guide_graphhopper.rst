.. highlight:: console

.. author:: Thomas S. <https://github.com/Thomas--S/>

.. tag:: lang-java
.. tag:: self-hosting
.. tag:: navigation
.. tag:: audience-admins

.. sidebar:: Logo

  .. image:: _static/images/graphhopper.png
      :align: center

###########
GraphHopper
###########

.. tag_list::

GraphHopper_ is a routing engine for OpenStreetMap.
It can be used as a Java library or as a standalone web server.

Please refer to the `official documentation`_ on how to use the web server's API.

----


License
=======

License information can be found here

  * https://github.com/graphhopper/graphhopper/blob/master/LICENSE.txt


Installation
============

First of all, start with creating a directory for GraphHopper and enter it:

::

 [isabell@stardust ~]$ mkdir ~/graphhopper
 [isabell@stardust ~]$ cd ~/graphhopper
 [isabell@stardust graphhopper]$


Before actually installing GraphHopper, a ``.osm.pbf`` map file must be downloaded into this directory.
Such files can be found at Geofabrik_ (`more information`_), for example.
In order to minimize resource usage, please choose only a small map, preferably at district level.

.. warning::

  A map of Berlin will be used as an example.
  Please replace the map names according to your needs.
  Choose small maps in order to not overuse the shared resources.


::

 [isabell@stardust graphhopper]$ wget http://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf
 [isabell@stardust graphhopper]$


Next, you should download the default configuration file.

::

 [isabell@stardust graphhopper]$ wget -O config.yml https://raw.githubusercontent.com/graphhopper/graphhopper/4.x/config-example.yml
 [isabell@stardust graphhopper]$


In order to make GraphHopper work with Uberspace web backends, change the ``bind_host`` setting in the ``server`` section of this configuration file from ``localhost`` to ``0.0.0.0``.
Additionally, you should set the setting ``graph.dataaccess`` to ``MMAP`` in order to reduce RAM usage.
Feel free to make further changes as you see fit.

Finally, you can download the actual GraphHopper Java archive:

::

 [isabell@stardust graphhopper]$ wget https://graphhopper.com/public/releases/graphhopper-web-4.0.jar
 [isabell@stardust graphhopper]$


Setup Daemon
============

Create the file ``~/etc/services.d/graphhopper.ini`` with the following content:

.. note:: Remember to use your own username instead of isabell and adjust the file names according to the used version and map.

.. code-block:: ini

 [program:graphhopper]
 command=java -Ddw.graphhopper.datareader.file=berlin-latest.osm.pbf -jar graphhopper-web-4.0.jar server config.yml
 directory=%(ENV_HOME)s/graphhopper
 autostart=true
 autorestart=true

.. include:: includes/supervisord.rst


Setup Web Backend
=================

.. note:: GraphHopper is running on port 8989.
.. include:: includes/web-backend.rst


Map Tiles
=========

A map interface should now be available at ``https://isabell.uber.space/``.
You will probably see messages that your map tiles API key is invalid.
In case you only need to use the GraphHopper Routing API, you can ignore this warning.
In the upper right-hand corner, there's a layer button, where you can choose the map tiles provider.
The option "OpenStreetMap" likely works without further configuration.
Further information on map tiles configuration can be found in a `guide by GraphHopper`_.


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To update GraphHopper, follow the installation procedure described above.


.. _GraphHopper: https://www.graphhopper.com/open-source/
.. _official documentation: https://github.com/graphhopper/graphhopper/blob/master/docs/web/api-doc.md
.. _Geofabrik: http://download.geofabrik.de/
.. _more information: http://www.geofabrik.de/en/data/download.html
.. _feed: https://github.com/graphhopper/graphhopper/releases.atom
.. _guide by GraphHopper: https://github.com/graphhopper/graphhopper/blob/master/docs/core/deploy.md#api-tokens

----

Tested with GraphHopper 4.0, Uberspace 7.11.5

.. author_list::
