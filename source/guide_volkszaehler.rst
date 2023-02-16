.. highlight:: console

.. author:: Christoph Reißig - REISSIG|DIGITAL info@reissig-digital.com

.. tag:: lang-php
.. tag:: web
.. tag:: smart-meter
.. tag:: audience-private

.. sidebar:: Logo

    .. image:: _static/images/volkszaehler-logo.png
        :align: center

################
Volkszaehler.org
################

.. tag_list::

Volkszaehler.org is a free smart meter implementation with focus on data privacy. You keep perfect control over your data regarding water, energy and power consumption. Volkszaehler.org is based on a modular setup of different software solutions. This guide is focused on the middleware. To get some proper data shown there you need at least one source as a second module (e.g. a raspberry pi with vzlogger daemon).

The software is written in PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

    * :manual:PHP <lang-php>
    * :manual:MySQL <database-mysql>
    * :manual:domains <web-domains>

License
=======

Volkszaehler.org is released under the GNU General Public License v3.0. The LICENSE_ and Terms can be found on the Volkszaehler.org_ website and on github.

Prerequisites
=============

We're using PHP in the stable version 8.1:

.. code-block:: console

    [isabell@stardust ~]$ uberspace tools version show php
    Using 'PHP' version: '8.1'
    [isabell@stardust ~]$

For proper function of volkszaehler.org add this to a php.ini file in ~/etc/php.d/

.. code-block:: ini

    memory_limit = 512M

.. include:: includes/my-print-defaults.rst

Your domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We will be installing volkszaehler.org using composer.
cd to your :manual:DocumentRoot <web-documentroot> and download the latest Release_, and install the dependencies using composer:

.. code-block:: console

    [isabell@stardust ~]$ cd /var/www/virtual/$USER/
    [isabell@stardust isabell]$ git clone https://github.com/volkszaehler/volkszaehler.org volkszaehler
    Cloning into 'volkszaehler'...
    remote: Enumerating objects: 134, done.
    […]
    [isabell@stardust isabell]$ cd volkszaehler
    [isabell@stardust volkszaehler]$ composer install
    Loading composer repositories with package information
    Installing dependencies (including require-dev) from lock file
    […]
    [isabell@stardust ~]$

Remove your empty :manual:DocumentRoot <web-documentroot> and create a new symbolic link to the /var/www/virtual/vzgs/volkszaehler/htdocs directory.

.. code-block:: console

    [isabell@stardust ~]$ cd /var/www/virtual/$USER/
    [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
    [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/volkszaehler/htdocs html
    [isabell@stardust ~]$

Database Setup
==============

Volkszaehler.org saves your data in a MySQL database. Please use an :manual_anchor:additional database <database-mysql.html#additional-databases>. You need to create this database before you enter the database credentials in the config file.

.. code-block:: console

    [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_volkszaehler"
    [isabell@stardust ~]$

Configuration
=============

After setting up the database we have to change the config file in /var/www/virtual/$USER/volkszaehler/etc/config.dist.yaml.

.. code-block:: ini

    db:
    driver: pdo_mysql (default)
    host: localhost (default)
    # port: 3306

    user: isabell (your username)
    password: your MySQL password from my_print_defaults client
    charset: utf8 (default)
    dbname: isabell_volkszaehler (the name of the database you created)
    path: volkszaehler # only used for sqlite
    db admin credentials (used by doctrine cli and setup script)

    admin:
    user: isabell (your username)
    password: your MySQL password from my_print_defaults client

After these changes save the file as config.yaml

Check the Documentation_ for further questions.

Create Database Structure
-------------------------

If you don't use a backup of a former volkszaehler.org database, you need to create the database structure via doctrine

::

    [isabell@stardust ~]$ cd /var/www/virtual/$USER/volkszaehler
    [isabell@stardust volkszaehler]$ php bin/doctrine orm:schema-tool:create
    [isabell@stardust ~]$

Tuning
======

Aggregation
-----------

To automatically aggregate we need to setup some cronjobs.

::

    */10 * * * * php /var/www/volkszaehler.org/bin/aggregate run -m delta -l minute >/dev/null
    1 * * * * php /var/www/volkszaehler.org/bin/aggregate run -m delta -l hour >/dev/null
    0 1 * * * php /var/www/volkszaehler.org/bin/aggregate run -m delta -l day >/dev/null

    You can learn more about cronjobs in the :manual:uberspace manual cron article <daemons-cron>.

Updates
=======

Check the Release_ on Github regularly to stay informed about the newest version.

To update Volkszaehler.org_ you can run the following commands in the root directory of the application.
The --force arguments are needed to prevent warnings about the application running in production mode.

.. code-block:: console

    [isabell@stardust ~]$ cd /var/www/virtual/$USER/volkszaehler
    [isabell@stardust volkszaehler]$ git pull
    [isabell@stardust volkszaehler]$ php /composer/composer.phar update
    [isabell@stardust volkszaehler]$

Debugging
=========

If something fails please try these steps in the following order:

1. Attach /frontend/ to your url (e.g. https://isabell.uber.space/frontend/). If the url cannot be resolved then you have to change the rewrite settings.
2. To Check the middleware without the frontend try to call a direct channel (e.g. https://isabell.uber.space/middleware.php/data/d3aa8c0-9e87-11e6-878f-b724ca3bd16b.json)
3. To check the database access you can call (e.g. https://isabell.uber.space/middleware.php/capabilities/database.json?)

If you get
       
.. code-block:: ini

 {„version“:„0.3“,„capabilities“:{„database“:{„data“:{„rows“:0,„size“:49152},„aggregation“:{„rows“:0,„size“:49152,„ratio“:0}}}}
            
then youre fine.
       
If you get
       
.. code-block:: ini
            
 {„version“:„0.3“,„exception“:{„message“:„Class \“Doctrine\Common\Annotations\AnnotationRegistry\„ not found“,„type“:„Error“,„code“:0}}
 
then you have an mistake in your developer system e.g. composer.
       
If you get
        
.. code-block:: ini
            
 {„version“:„0.3“,„exception“:{„message“:„An exception occurred in driver: SQLSTATE[HY000] [2002] Connection refused“,„type“:„ConnectionException“,„code“:0}}
 
you have a wrong port/server combination.
       
If you get
       
.. code-block:: ini

 {„version“:„0.3“,„exception“:{„message“:„An exception occurred in driver: SQLSTATE[HY000] [1045] Access denied for user 'xxxx'@'xxxx' (using password: YES)“,„type“:„ConnectionException“,„code“:0}}
 
you have the wrong database credentials.

For deeper insights on database access errors use the following script

.. code-block:: ini
 
    <?php
        $servername = "localhost";
        $username = "isabell";
        $password = "your MySQL password from my_print_defaults client";
        $database = "isabell_volkszaehler";
 
        $conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
 
        $sql = ("SELECT * FROM entities");
        foreach ($conn->query($sql) as $row) {
        echo $row['uuid']."<br />";
                                            }
    ?>
    
Backup
======

All generated data is saved to the database and should be backuped along with your config file in /var/www/virtual/$USER/volkszaehler/etc/config.yaml on regular base.

.. _Volkszaehler.org: https://volkszaehler.org
.. _Source: https://github.com/volkszaehler/volkszaehler.org/
.. _LICENSE: https://www.gnu.org/licenses/gpl-3.0.html
.. _Release: https://wiki.volkszaehler.org/software/releases/start
.. _Documentation: https://wiki.volkszaehler.org/

Tested with Volkszaehler.org 1.0, Uberspace 7.15, PHP 8.1

.. author_list::
