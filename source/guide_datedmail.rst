.. highlight:: console

.. author:: Marvin Dickhaus <https://marvindickhaus.de>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-pwsh
.. tag:: mail

##########
DatedMail
##########

.. tag_list::

DatedMail_ is a PowerShell module intended to provide a simple way for expiring email addresses. Ultimately this should reduce spam as mail addresses are only available for a certain amount of time.

This can be very useful for example if an imprint email address is required.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * `PowerShell <https://learn.microsoft.com/en-us/powershell/scripting/overview>`_
  * :manual:`cronjobs <daemons-cron>`
  * :manual:`Sieve filters <mail-filters>`

License
=======

All relevant legal information can be found here

  * https://github.com/Weishaupt/DatedMail/blob/main/LICENSE

Prerequisites
=============

DatedMail uses Sieve filters to reject mails. Therefore the spamfolder needs to be enabled. So first we check that the spamfolder is correctly enabled.

.. code-block:: console

 [isabell@stardust ~]$ uberspace mail spamfolder status
 The spam folder is enabled.

Next we need a new mailbox that is exclusively used to forward or reject mails based on the expiry status of the mail address. In this example we use the mailbox ``temp``.
Of course other names can be used. Note the name choosen for the installation:

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ uberspace mail user add temp
 Enter a password for the mailbox:
 Please confirm your password:
 New mailbox created for user: 'temp', it will be live in a few minutes...
 [isabell@stardust ~]$

Installation
============

Install the PowerShell module
-----------------------------

Launch PowerShell and use ``Install-Module`` to install the DatedMail module. Confirm the Untrusted repository warning with Yes.

.. code-block:: pwsh
 :emphasize-lines: 1,5,10

 [isabell@stardust ~]$ pwsh
 PowerShell 7.2.24
 Copyright (c) Microsoft Corporation.

 PS /home/isabell> Install-Module DatedMail

 Untrusted repository
 You are installing the modules from an untrusted repository. If you trust this repository, change its InstallationPolicy value by
  running the Set-PSRepository cmdlet. Are you sure you want to install the modules from 'PSGallery'?
 [Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): Y
 PS /home/isabell>

Configuration
=============

Initialize the module
---------------------
Still within the PowerShell console perform the initial configuration. If you choose another name then ``temp`` for your mailbox make sure to enter it here.

.. code-block:: pwsh

 PS /home/isabell> Initialize-DatedMailConfiguration -MailAddressPrefix "temp+" -MailAddressDomain "isabell.uber.space" -SieveFilterPath /home/isabell/users/temp/sieve/datedmail.sieve -ForwardingEmailAddress isabell@uber.space
 PS /home/isabell>

Configure the expiration timer
------------------------------
Once a mail address expires, it needs to be removed from the sieve filter. This is the job of the command ``Update-DatedMailAddress``. We configure a new cronjob which will run this every hour.
The command to call is ``/usr/bin/pwsh -Command "Update-DatedMailAddress"``.

.. code-block:: pwsh

 PS /home/isabell> crontab -e

Add the following line to your crontab: ``44 * * * *  /usr/bin/pwsh -Command "Update-DatedMailAddress"``. This will call ``Update-DatedMailAddress`` every hour on minute 44. Then save and close your crontab.

Finishing installation
======================

Create your first expiring mail address
---------------------------------------
To add your first expiring mail address, call ``New-DatedMailAddress -ValidDays 8 -ReturnMailAddress``

.. code-block:: pwsh

 PS /home/isabell> New-DatedMailAddress -ValidDays 8 -ReturnMailAddress
 temp+72lv4xdbh4yqu40@isabell.uber.space
 PS /home/isabell>

In a scenario where you regularly roll over to a new expiring mail address, you could also export the newly generated email address to a file for further processing:

.. code-block:: pwsh

 PS /home/isabell> New-DatedMailAddress -ValidDays 14 -ExportFilePath /home/isabell/dated.mail
 PS /home/isabell> cat dated.mail
 temp+yt3ju2ya17pvp28@isabell.uber.space
 PS /home/isabell>

Enable the Sieve filter for the mailbox
---------------------------------------
Now what's left to do is to enable the filter on the temp mailbox, so it is getting applied:

.. code-block:: pwsh

 PS /home/isabell> New-Item -Path /home/isabell/users/temp/.dovecot.sieve -Value /home/isabell/users/temp/sieve/datedmail.sieve -ItemType SymbolicLink
     Directory: /home/isabell/users/temp

 UnixMode   User             Group                 LastWriteTime           Size Name
 --------   ----             -----                 -------------           ---- ----
 lrwxrwxrwx isabell          isabell               16/02/2025 17:23          43 .dovecot.sieve ->
                                                                                /home/isabell/users/temp/sieve/datedmail.sieve

 PS /home/isabell>

Best practices
==============

The mailbox used (in our example ``temp``) must not be used for any other purpose.

The sieve script generated by DatedMail should not be updated by hand. Any change will be overwritten whenever a new expiring mail address is added, or an existing address expires.

If you want to use expiring mail addresses for websites, you should automate the deployment of new mail addresses, too. E.g. create a script that calls ``New-DatedMailAddress`` and then copy the new mail address to the correct place so it gets served to website visitors.

Tuning
======

You can adapt the cronjob to your needs. Typically running once an hour should suffice, but more frequent runs are also possible.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

.. _feed: https://github.com/Weishaupt/DatedMail/tags.atom

To update to the newest module version just run `Update-Module`.

.. code-block:: pwsh
 :emphasize-lines: 6

 PS /home/isabell> Update-Module DatedMail

 Untrusted repository
 You are installing the modules from an untrusted repository. If you trust this repository, change its InstallationPolicy value by
  running the Set-PSRepository cmdlet. Are you sure you want to install the modules from 'PSGallery'?
 [Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): Y
 PS /home/isabell>

That's it. Next time you run any command the new version is automatically used.

Debugging
=========

If something fails you can try to debug using the ``-Debug`` and ``-Verbose`` switches with the PowerShell commands to get more output from the commands.

Backup
======

The only data you should regularly backup the configuration in your ``.config`` folder (``~/.config/DatedMail/``)

----

Tested with DatedMail 1.0.0, Uberspace 7.16.5

.. author_list::
