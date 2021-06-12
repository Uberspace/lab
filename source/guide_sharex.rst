.. author:: Spacelord <iamroot@uber.space>

.. tag:: lang-bash
.. tag:: screenshot
.. tag:: automation
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/sharex.png
      :align: center

######
ShareX
######

.. tag_list::

.. abstract::
  ShareX_ is a program that makes it easy to upload screenshots and share them with your friends. If you follow these instructions, you will end up with fully functional screenshot automation.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * :manual:`SFTP <basics-sftp>`
  * :manual:`domains <web-domains>`

License
=======

ShareX_ is licensed under the GNU General Public License v3.0
All relevant legal information can be found here

  * https://github.com/ShareX/ShareX/blob/master/LICENSE.txt


Prerequisites
=============

Your URL needs to be set up:

.. include:: includes/web-domain-list.rst

Installing and configuring the Windows client
=============================================

Install
-------
Go to your Windows PC and download the ShareX software from the `ShareX Website <https://getsharex.com/downloads/>`_. Start the installer and follow the instructions.

Configure
---------
Open ShareX and navigate to ":menuselection:`Destinations settings --> FTP / FTPS / SFTP`"
Now click "**Add**" to create a new destination for our pictures. Now write the following in the corresponding fields.

.. warning:: Make sure to replace "isabell" in the next step with your own username!

::

  Name: IMG Uberspace
  Protocol: SFTP
  Host: stardust.uberspace.de
  Username: $ssh_user
  Password: $ssh_password
  Remote directory: /var/www/virtual/isabell/html/img/%y/%mo/%d
  URL path: https://isabell.uber.space


**The two checkboxes should be unchecked!**
You can now close the "**Destination settings**" window.

Create workflow
---------------
To setup your Workflow do the following:


 1. Navigate to ":menuselection:`Destinations --> Image Uploader`" and check **FTP**.
 2. Navigate to "**After Capture tasks**" and be sure to activate "**Open in image editor**", "**Save image to file**" and finally "**Upload image to host**".
 3. Navigate to "**After upload tasks**" and be sure to activate "**Copy URL to clipboard**".


Test
----
Now it’s time to setup your Hotkeys:


 Navigate to ":menuselection:`Destinations --> Hotkeys`" then do the following:

  1. Remove all Hotkeys.
  2. Click "**Add**"
  3. Select "**Task: None**" and navigate to: ":menuselection:`Screen capture --> capture region`"
  4. Close the Task settings window and click on **None** and press your Hotkey (for example "**PRINT SCREEN**")

Usage
=====

1. Press the configured hotkey
2. Make a screenshot
3. If needed, edit your screenshot in the popup window. Then press "**enter**" to upload your screenshot and copy the corresponding URL to your clipboard.

That's it, you have successfully configured an automatically uploading screenshot tool with your own domain!

.. _ShareX: https://getsharex.com/

----

Tested with ShareX ?, Uberspace ?

.. author_list::
