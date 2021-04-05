.. highlight:: console
.. author:: GodMod <godmod@eqdkp-plus.eu>

.. tag:: lang-php
.. tag:: web
.. tag:: analytics

.. sidebar:: Logo

  .. image:: _static/images/matomo.png
      :align: center

#########
Matomo
#########

.. tag_list::

Matomo_ (formerly known as Piwik) is an open source website tracking tool (like Google Analytics) written in PHP. Hosting a website tracker by yourself gives you full data ownership and privacy protection of any data collected and stored, especially with regard to data laws like the EU's General Data Protection Regulation (GDPR).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=============

Matomo_ is released under the `GPLv3 License`_.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

If you want to use Matomo with your own domain you need to add it first:

.. include:: includes/web-domain-list.rst

Installation
============

If you want to install Matomo into a subfolder of your domain, download and unzip it in your :manual:`document root <web-documentroot>`:
::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ wget https://builds.matomo.org/matomo.zip
 [isabell@stardust html]$ unzip matomo.zip
 [isabell@stardust html]$ rm matomo.zip

Now point your browser to your Matomo URL. In this example, it is ``https://isabell.uber.space/matomo``. Follow the instructions in your browser.

You will need to enter the following information:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your Matomo database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: isabell_matomo
  * Administrator (*Super User*) username and password: choose a username (maybe not *admin*) and a strong password for the super user
  * Name and URL of the first website you want to track with Matomo (more can be added after installation)


Best practices
==============

auto-archive
------------

archiving can slow down Matomo quite a bit. So if you want to have a more fluent workflow this is recommended.

enter crontab with

.. code-block:: console

  [isabell@stardust ~]$ crontab -e

and enter with your url (more configuration-details about :manual:`cron <daemons-cron>`):

.. code-block::

  5 * * * * /usr/bin/php /home/$USER/html/matomo/console core:archive --url=https://isabell.uber.space/ > /dev/null


Tracking
========
There are different ways to use Matomo for website tracking. The easiest way is to embed the provided JavaScript Tracking Code into your website. It should be added into the head section before the closing ``</head>`` tag.

::

  <!doctype html>

  <html lang="en">
  <head>
    <meta charset="utf-8">
    <title>The HTML5 Herald</title>
    <meta name="description" content="Isabells Blog">
    <meta name="author" content="Isabell">

    <!-- Matomo -->
    <script type="text/javascript">
      var _paq = _paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="//isabell.uber.space/matomo/";
        _paq.push(['setTrackerUrl', u+'piwik.php']);
        _paq.push(['setSiteId', '1']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <!-- End Matomo Code -->

  </head>

  [...]

Moreover, Matomo provides Image Tracking and the importing of server logs. Also it offers a `Tracking HTTP API <https://developer.matomo.org/api-reference/tracking-api>`_, which lets you integrate the Matomo Tracking for example in your PHP application.


Privacy
=======

By default, Matomo respects `DoNotTrack`. As Uberspace shortens IP addresses by default, there are no additional privacy settings needed.

Nevertheless, you should update your Privacy Policy to explain how Matomo is used and what data it gathers. For this, Matomo provides a `Privay Policy template <https://matomo.org/privacy-policy/>`_.

Also, you can provide your users an Opt-Out Feature using iframes. Therefore, go to ``Administration >> Privacy >> Users opt-out`` and copy the provided HTML-Code into your website, e.g. in your Privacy Policy.

.. warning:: If you want to track a website outside of your uberspace, be aware that you won't be able to place an opt-out iFrame due to the option ``X-Frame-Options: SAMEORIGIN`` which is enabled by default. This implicates a breach of the GDPR laws and should be solved otherwise. Use a solution like the official plugin  `Ajax Opt Out <https://plugins.matomo.org/AjaxOptOut/>`_ instead to serve a opt-out option for your visitors.

Updates
=======

The easiest way to update Matomo is to use the web updater provided in the admin section of the Web Interface. Matomo will show you a hint if there is an update available.

.. note:: Check the `changelog <https://matomo.org/changelog/>`_ regularly to stay informed about new updates and releases.

Backup
======

Backup the following directories:

  * ``~/html/matomo/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_matomo | xz - > ~/isabell_matomo.sql.xz


.. _Matomo: https://matomo.org/
.. _GPLv3 License: https://github.com/matomo-org/matomo/blob/4.x-dev/LICENSE

----

Tested with Matomo 3.5.0, Uberspace 7.1.3

.. author_list::
