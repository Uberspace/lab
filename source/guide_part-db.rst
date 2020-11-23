
.. highlight:: console
.. author:: 927589452

.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/partdb.png
      :align: center

#######
Part-DB
#######

.. tag_list::

Part-DB-symfony_ is a rewrite of the Part-DB_, a web-based database for managing electronic components. It is distributed under the AGPL-3.0 License.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`cronjobs <daemons-cron>`
  * composer_

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Installation
============


``cd`` to the folder above your  :manual:`document root <web-documentroot>`, then clone the repository of Part-DB-symfony and change into it:

::

 [isabell@stardust ~]$ cd /var/www/virtual/${USER}
 [isabell@stardust isabell]$ git clone https://github.com/Part-DB/Part-DB-symfony.git
 Cloning into 'Part-DB-symfony'...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  100 37.5M  100 37.5M    0     0  5274k      0  0:00:07  0:00:07 --:--:-- 6062k
 [isabell@stardust isabell]$ cd Part-DB-symfony
 [isabell@stardust Part-DB-symfony]$

For the initial configuration you need to copy the `.env` to ´.env.local` as follows:

::

 [isabell@stardust Part-DB-symfony]$ cp .env .env.local
 [isabell@stardust Part-DB-symfony]$

And change the database url in the `.env.local` as follows:

TODO:
- comment sqlite line
- uncomment mysql line and change to the following
  DATABASE_URL=mysql://MYSQL_USER:MYSQL_PASSWORD@127.0.0.1:3306/USER_partdb

Install the composer dependencies:

::

 [isabell@stardust Part-DB-symfony]$ composer install --no-dev

 Installing dependencies from lock file
 Verifying lock file contents can be installed on current platform.
 Package operations: 158 installs, 0 updates, 0 removals
     0 [>---------------------------]    0 [>---------------------------]  - Installing composer/package-versions-deprecated (1.11.99): Extracting archive
   - Installing symfony/flex (v1.9.4): Extracting archive
 The "symfony/flex" plugin was skipped because it is not compatible with Composer 2+. Make sure to update it to version 1.9.8 or greater.
   - Installing symfony/polyfill-php80 (v1.18.1): Extracting archive
   - Installing symfony/polyfill-mbstring (v1.18.1): Extracting archive
   - Installing symfony/polyfill-intl-normalizer (v1.18.1): Extracting archive
   - Installing symfony/polyfill-intl-grapheme (v1.18.1): Extracting archive
   - Installing symfony/polyfill-ctype (v1.18.1): Extracting archive
   - Installing symfony/string (v5.1.6): Extracting archive
   - Installing psr/container (1.0.0): Extracting archive
   - Installing symfony/service-contracts (v2.2.0): Extracting archive
   - Installing symfony/polyfill-php73 (v1.18.1): Extracting archive
   - Installing symfony/console (v5.1.6): Extracting archive
   - Installing doctrine/lexer (1.2.1): Extracting archive
   - Installing doctrine/annotations (1.10.4): Extracting archive
   - Installing doctrine/reflection (1.2.1): Extracting archive
   - Installing doctrine/event-manager (1.1.1): Extracting archive
   - Installing doctrine/collections (1.6.7): Extracting archive
   - Installing doctrine/cache (1.10.2): Extracting archive
   - Installing doctrine/persistence (2.0.0): Extracting archive
   - Installing doctrine/instantiator (1.3.1): Extracting archive
   - Installing doctrine/inflector (1.4.3): Extracting archive
   - Installing doctrine/dbal (2.10.4): Extracting archive
   - Installing doctrine/common (3.0.2): Extracting archive
   - Installing doctrine/orm (v2.7.3): Extracting archive
   - Installing beberlei/doctrineextensions (v1.2.8): Extracting archive
   - Installing brick/math (0.9.1): Extracting archive
   - Installing symfony/stopwatch (v5.1.6): Extracting archive
   - Installing psr/log (1.1.3): Extracting archive
   - Installing zendframework/zend-eventmanager (3.2.1): Extracting archive
   - Installing zendframework/zend-code (3.4.1): Extracting archive
   - Installing ocramius/proxy-manager (2.2.3): Extracting archive
   - Installing doctrine/migrations (3.0.1): Extracting archive
   - Installing doctrine/sql-formatter (1.1.1): Extracting archive
   - Installing sabberworm/php-css-parser (8.3.1): Extracting archive
   - Installing phenx/php-svg-lib (v0.3.3): Extracting archive
   - Installing phenx/php-font-lib (0.5.2): Extracting archive
   - Installing dompdf/dompdf (v0.8.6): Extracting archive
   - Installing erusev/parsedown (1.7.4): Extracting archive
   - Installing psr/simple-cache (1.0.1): Extracting archive
   - Installing psr/http-message (1.0.1): Extracting archive
   - Installing php-http/message-factory (v1.0.2): Extracting archive
   - Installing psr/http-client (1.0.1): Extracting archive
   - Installing php-http/promise (1.1.0): Extracting archive
   - Installing php-http/httplug (2.2.0): Extracting archive
   - Installing php-http/discovery (1.12.0): Extracting archive
   - Installing symfony/http-client-contracts (v2.2.0): Extracting archive
   - Installing symfony/http-client (v5.1.6): Extracting archive
   - Installing florianv/exchanger (2.5.3): Extracting archive
   - Installing symfony/deprecation-contracts (v2.2.0): Extracting archive
   - Installing symfony/routing (v5.1.6): Extracting archive
   - Installing symfony/http-foundation (v5.1.6): Extracting archive
   - Installing psr/event-dispatcher (1.0.0): Extracting archive
   - Installing symfony/event-dispatcher-contracts (v2.2.0): Extracting archive
   - Installing symfony/event-dispatcher (v5.1.6): Extracting archive
   - Installing symfony/var-dumper (v5.1.6): Extracting archive
   - Installing symfony/error-handler (v5.1.6): Extracting archive
   - Installing symfony/http-kernel (v5.1.6): Extracting archive
   - Installing symfony/finder (v5.1.6): Extracting archive
   - Installing symfony/filesystem (v5.1.6): Extracting archive
   - Installing symfony/dependency-injection (v5.1.6): Extracting archive
   - Installing symfony/config (v5.1.6): Extracting archive
   - Installing symfony/var-exporter (v5.1.6): Extracting archive
   - Installing psr/cache (1.0.1): Extracting archive
   - Installing symfony/cache-contracts (v2.2.0): Extracting archive
   - Installing symfony/cache (v5.1.6): Extracting archive
   - Installing symfony/framework-bundle (v5.1.6): Extracting archive
   - Installing florianv/swap (4.2.0): Extracting archive
   - Installing florianv/swap-bundle (dev-master 6df4691): Extracting archive
   - Installing twig/twig (v3.0.5): Extracting archive
   - Installing symfony/translation-contracts (v2.2.0): Extracting archive
   - Installing symfony/twig-bridge (v5.1.6): Extracting archive
   - Installing symfony/twig-bundle (v5.1.6): Extracting archive
   - Installing symfony/property-info (v5.1.6): Extracting archive
   - Installing symfony/property-access (v5.1.6): Extracting archive
   - Installing symfony/options-resolver (v5.1.6): Extracting archive
   - Installing symfony/intl (v5.1.6): Extracting archive
   - Installing symfony/polyfill-intl-icu (v1.18.1): Extracting archive
   - Installing symfony/form (v5.1.6): Extracting archive
   - Installing symfony/expression-language (v5.1.6): Extracting archive
   - Installing symfony/asset (v5.1.6): Extracting archive
   - Installing friendsofsymfony/ckeditor-bundle (2.2.0): Extracting archive
   - Installing symfony/translation (v5.1.6): Extracting archive
   - Installing gregwar/captcha (v1.1.8): Extracting archive
   - Installing gregwar/captcha-bundle (v2.1.3): Extracting archive
   - Installing league/html-to-markdown (4.10.0): Extracting archive
   - Installing symfony/templating (v5.1.6): Extracting archive
   - Installing symfony/process (v5.1.6): Extracting archive
   - Installing symfony/polyfill-php72 (v1.18.1): Extracting archive
   - Installing paragonie/random_compat (v9.99.99): Extracting archive
   - Installing symfony/polyfill-php70 (v1.18.1): Extracting archive
   - Installing symfony/polyfill-intl-idn (v1.18.1): Extracting archive
   - Installing symfony/mime (v5.1.6): Extracting archive
   - Installing imagine/imagine (1.2.3): Extracting archive
   - Installing liip/imagine-bundle (2.3.1): Extracting archive
   - Installing composer/ca-bundle (1.2.8): Extracting archive
   - Installing ua-parser/uap-php (v3.9.14): Extracting archive
   - Installing symfony/security-core (v5.1.6): Extracting archive
   - Installing symfony/security-http (v5.1.6): Extracting archive
   - Installing symfony/security-csrf (v5.1.6): Extracting archive
   - Installing nelmio/security-bundle (v2.10.1): Extracting archive
   - Installing nikic/php-parser (v4.10.2): Extracting archive
   - Installing psr/http-factory (1.0.1): Extracting archive
   - Installing nyholm/psr7 (1.3.1): Extracting archive
   - Installing omines/datatables-bundle (0.5.1): Extracting archive
   - Installing symfony/validator (v5.1.6): Extracting archive
   - Installing php-translation/common (3.0.1): Extracting archive
   - Installing php-translation/symfony-storage (2.2.0): Extracting archive
   - Installing php-translation/extractor (2.0.2): Extracting archive
   - Installing webmozart/assert (1.9.1): Extracting archive
   - Installing nyholm/nsa (1.2.1): Extracting archive
   - Installing php-translation/symfony-bundle (0.12.1): Extracting archive
   - Installing phpdocumentor/reflection-common (2.2.0): Extracting archive
   - Installing phpdocumentor/type-resolver (1.4.0): Extracting archive
   - Installing yubico/u2flib-server (1.0.2): Extracting archive
   - Installing symfony/security-guard (v5.1.6): Extracting archive
   - Installing symfony/security-bundle (v5.1.6): Extracting archive
   - Installing thecodingmachine/safe (v1.2.1): Extracting archive
   - Installing paragonie/constant_time_encoding (v2.3.0): Extracting archive
   - Installing beberlei/assert (v3.2.7): Extracting archive
   - Installing spomky-labs/otphp (v10.0.1): Extracting archive
   - Installing lcobucci/jwt (3.3.3): Extracting archive
   - Installing scheb/two-factor-bundle (v4.18.3): Extracting archive
   - Installing r/u2f-two-factor-bundle (0.8.0): Extracting archive
   - Installing s9e/sweetdom (1.0.1): Extracting archive
   - Installing s9e/regexp-builder (1.4.4): Extracting archive
   - Installing s9e/text-formatter (2.7.5): Extracting archive
   - Installing sensio/framework-extra-bundle (v5.6.1): Extracting archive
   - Installing nikolaposa/version (3.2.0): Extracting archive
   - Installing shivas/versioning-bundle (3.2.3): Extracting archive
   - Installing symfony/apache-pack (v1.0.1): Extracting archive
   - Installing symfony/css-selector (v5.1.6): Extracting archive
   - Installing symfony/doctrine-bridge (v5.1.6): Extracting archive
   - Installing symfony/dotenv (v5.1.6): Extracting archive
   - Installing egulias/email-validator (2.1.22): Extracting archive
   - Installing symfony/mailer (v5.1.6): Extracting archive
   - Installing monolog/monolog (2.1.1): Extracting archive
   - Installing symfony/monolog-bridge (v5.1.6): Extracting archive
   - Installing symfony/monolog-bundle (v3.5.0): Extracting archive
   - Installing doctrine/doctrine-bundle (2.1.2): Extracting archive
   - Installing doctrine/doctrine-migrations-bundle (3.0.1): Extracting archive
   - Installing symfony/orm-pack (v2.0.0): Extracting archive
   - Installing symfony/serializer (v5.1.6): Extracting archive
   - Installing phpdocumentor/reflection-docblock (5.2.2): Extracting archive
   - Installing symfony/serializer-pack (v1.0.3): Extracting archive
   - Installing psr/link (1.0.0): Extracting archive
   - Installing symfony/web-link (v5.1.6): Extracting archive
   - Installing symfony/webpack-encore-bundle (v1.7.3): Extracting archive
   - Installing symfony/yaml (v5.1.6): Extracting archive
   - Installing tecnickcom/tc-lib-color (1.12.15): Extracting archive
   - Installing tecnickcom/tc-lib-barcode (1.16.1): Extracting archive
   - Installing tijsverkoyen/css-to-inline-styles (2.2.3): Extracting archive
   - Installing twig/cssinliner-extra (v3.0.5): Extracting archive
   - Installing twig/extra-bundle (v3.0.5): Extracting archive
   - Installing twig/html-extra (v3.0.5): Extracting archive
   - Installing lorenzo/pinky (1.0.5): Extracting archive
   - Installing twig/inky-extra (v3.0.5): Extracting archive
   - Installing twig/intl-extra (v3.0.5): Extracting archive
   - Installing twig/markdown-extra (v3.0.5): Extracting archive
    0/146 [>---------------------------]   0%
    8/146 [=>--------------------------]   5%
   10/146 [=>--------------------------]   6%
   12/146 [==>-------------------------]   8%
   13/146 [==>-------------------------]   8%
   20/146 [===>------------------------]  13%
   29/146 [=====>----------------------]  19%
   39/146 [=======>--------------------]  26%
   49/146 [=========>------------------]  33%
   59/146 [===========>----------------]  40%
   67/146 [============>---------------]  45%
   76/146 [==============>-------------]  52%
   85/146 [================>-----------]  58%
   95/146 [==================>---------]  65%
  104/146 [===================>--------]  71%
  114/146 [=====================>------]  78%
  124/146 [=======================>----]  84%
  134/146 [=========================>--]  91%
  143/146 [===========================>]  97%
  146/146 [============================] 100%Package zendframework/zend-code is abandoned, you should avoid using it. Use laminas/laminas-code instead.
 Package zendframework/zend-eventmanager is abandoned, you should avoid using it. Use laminas/laminas-eventmanager instead.
 Generating autoload files
 83 packages you are using are looking for funding.
 Use the `composer fund` command to find out more!
 > symfony-cmd
 Script symfony-cmd handling the auto-scripts event returned with error code 127
 Script @auto-scripts was called via post-install-cmd
 [isabell@stardust Part-DB-symfony]$


Installing the yarn dependencies is done using `yarn install` and `yarn build`:

::

 [isabell@stardust Part-DB-symfony]$ yarn install
 yarn install v1.22.5
 [1/5] Resolving packages...
 [2/5] Fetching packages...
 info fsevents@1.2.13: The platform "linux" is incompatible with this module.
 info "fsevents@1.2.13" is an optional dependency and failed compatibility check. Excluding it from installation.
 info fsevents@2.1.3: The platform "linux" is incompatible with this module.
 info "fsevents@2.1.3" is an optional dependency and failed compatibility check. Excluding it from installation.
 [3/5] Linking dependencies...
 [4/5] Building fresh packages...
 [5/5] Cleaning modules...
 Done in 56.51s.
 [isabell@stardust Part-DB-symfony]$  yarn build
 yarn run v1.22.5
 $ encore production --progress
 Running webpack ...

  DONE  Compiled successfully in 42587ms11:06:50

  I  83 files written to public/build
 Entrypoint app [big] = runtime.d94b3b43.js 0.836ff1c3.css 0.085f90f4.js app.92c72916.css app.81fe66ba.js
 Entrypoint ru2ftwofactor = runtime.d94b3b43.js ru2ftwofactor.29500168.js
 Done in 44.91s.
 [isabell@stardust Part-DB-symfony]$

.. note::
   Take note of the password for the admin account the initial migration creates. It can be replaced by using `php bin/console app:set-password admin`.

Create/migrate the database. If you had a previous installation of Part-DB_ < 1.0, you should make a backup now.

::

 [isabell@stardust Part-DB-symfony]$ mysql -e "CREATE DATABASE ${USER}_partdb" && echo "Created database ${USER}_partdb"
 [isabell@stardust Part-DB-symfony]$ php bin/console doctrine:migrations:migrate
 WARNING! You are about to execute a database migration that could result in schema changes and data loss. Are you sure you wish to continue? (yes/no) [yes]:
 >

 11:26:32 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:32 WARNING   [app]
 11:26:32 WARNING   [app] The initial password for the "admin" user is: 90845803fc
 11:26:32 WARNING   [app]
 11:26:32 WARNING   [app] Empty database detected. Skip migration. ["migration" => DoctrineMigrations\Version20190902140506 { …}]
 11:26:32 WARNING   [app] Migration DoctrineMigrations\Version20190902140506 was executed but did not result in any SQL statements. ["version" => "DoctrineMigrations\Version20190902140506"]
 11:26:32 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:33 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!
 11:26:35 WARNING   [app] [!!!] Permissions were updated! Please check if they fit your expectations!

 [isabell@stardust Part-DB-symfony]$

Check the default settings in `config/parameters.yml`, especially the currency in partdb.default_currency, as it can not be changed after prices have been added.

Clear the cache and warm it up, if anything changed:

::

 [isabell@stardust Part-DB-symfony]$ php bin/console cache:clear
 // Clearing the cache for the prod environment with debug false

 [OK] Cache for the "prod" environment (debug=false) was successfully cleared.
 [isabell@stardust Part-DB-symfony]$ php bin/console cache:warmup


 // Warming up the cache for the prod environment with debug false

 [OK] Cache for the "prod" environment (debug=false) was successfully warmed.

 [isabell@stardust Part-DB-symfony]$


To enable the the webfrontend you replace the `/var/www/virtual/${USER}/html` folder with a symlink to`/var/www/virtual/${USER}/Part-DB-symfony/public`:

::

 [isabell@stardust Part-DB-symfony]$ rmdir /var/www/virtual/${USER}/html
 [isabell@stardust Part-DB-symfony]$ ln -s /var/www/virtual/${USER}/Part-DB-symfony/public/ /var/www/virtual/${USER}/html
 [isabell@stardust Part-DB-symfony]$

On your first visit you will need to change the password for the admin account.

Updates
=======

To update Part-DB you pull the new version and work through the installation guide again.

.. _Part-DB: https://github.com/Part-DB/Part-DB
.. _Part-DB-symfony: https://github.com/Part-DB/Part-DB-symfony
.. _composer: https://getcomposer.org


----

Tested with Part-DB 0.5.9, Uberspace 7.7.10.0

.. author_list::
