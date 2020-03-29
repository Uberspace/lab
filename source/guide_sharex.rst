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

Step 1
------
Firstly we need to add a domain(in this case a subdomain).

::

  [isabell@stardust ~] uberspace web domain add cdn.uberspace.de
  The webserver's configuration has been adpated.
  Now you can use the following records for your dns:
     A -> 185.26.156.55
     AAAA -> 2a00:d0c0:200:0:b9:1a:9c:37

Step 2
------

Now we need to create the coresponding directory for our subdomain.

::

  [isabell@stardust ~] mkdir /var/www/virtual/$user/cdn.uberspace.de && cd "$_"
  [isabell@stardust cdn.uberspace.de]




Installing and configuring the Windows client
=============================================
Go to your Windows PC and download the ShareX software from the `ShareX Website <https://getsharex.com/downloads/>`_.

Step 1
------
Start the installer and follow the instructions.

Step 2
------
Open ShareX and navigate to ":menuselection:`Destinations settings --> FTP / FTPS / SFTP`"
Now click "**Add**" to create a new destination for our pictures.

Step 3
------
Now write the following in the coresponding fields.

::

  Name: IMG Uberspace
  Protocol: SFTP
  Host: stardust.uberspace.de
  Username: $ssh_user
  Password: $ssh_password
  Remote directory: /var/www/virtual/$user/cdn.uberspace.de/img/%y/%mo/%d
  URL path: https://   cdn.uberspace.de


**The two checkboxes should be unchecked!**
You can now close the "**Destination settings**" window.

Step 4
------
To setup your Workflow do the following:


 1. Navigate to ":menuselection:`Destinations --> Image Uploader`" and check **FTP**.
 2. Navigate to "**After Capture tasks**" and be sure to activate "**Open in image editor**", "**Save image to file**" and finaly "**Upload image to host**".
 3. Navigate to "**After upload tasks**" and be sure to activate "**Copy URL to clipboard**".


Step 5
------
Now it’s time to setup your Hotkeys:


 Navigate to ":menuselection:`Destinations --> Hotkeys`" then do the following:

  1. Remove all Hotkeys.
  2. Click "**Add**"
  3. Select "**Task: None**" and navigate to: ":menuselection:`Screen capture --> capture region`"
  4. Close the Task settings window and click on **None** and press your Hotkey (for example "**PRINT SCREEN**")


Step 6 (Optional)
-----------------
Optional you can change the filename to something fancier.
To do so, navigate to ":menuselection:`Task settings --> File nameing`" and change the two text fields to:
::

  %y-%mo-%d_%h-%mi-%s

Usage
=====

Step 1
------
Press your Hotkey.

Step 2
------
Make a screenshot.

Step 3
------
If needed edit your screenshot in the popup window.

Then press "**enter**" to upload your screenshot and copy the corresponding URL to your clipboard.


.. _ShareX: https://getsharex.com/

----

That's it, you have successfully configured an automatically uploading screenshot tool with your own domain!

.. author_list::