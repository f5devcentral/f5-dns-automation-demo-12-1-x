Connecting to UDF 2.0
=====================

This lab goes through the process of launching the demo environment, connecting via Windows RDP, and licensing/resetting the BIG-IP devices.

Launching Deployment
====================

From https://federate.f5.com find the "UDF" link and click on it.

.. image:: federate-udf-link.png
   :scale: 50%
   :align: center
   
You should see the main UDF page.  Click on the "Blueprints" link.

.. image:: udf-main-page.png
   :scale: 50%
   :align: center
   
Find the "DNS Automation Demo" Blueprint and click on "Deploy"

.. image:: udf-dns-automation-demo-blueprint.png
   :scale: 50%
   :align: center
   
You will see "Deploy From Blueprint" and click "Deploy" again.

.. image:: deploy-from-blueprint.png
   :scale: 50%
   :align: center
   
You should now see the "DNS Automation Demo" screen that has the "Start" button listed.

Click on "Start".

.. image:: start-deployment.png
   :scale: 50%
   :align: center
   
The Deployment is now starting.

.. image:: deployment-starting.png
   :scale: 50%
   :align: center
   
About the Demo Environment
==========================

This demo is designed to provide a solution with the following attributes.

 * Two BIG-IP devices in separate Data Centers (Regions, Availability Zone, etc...)
 * Two backend servers in separate DC 
 * The two DC are routable to each other via L3
 * Provide recursive DNS for internal clients
 
.. image:: demo-schematic.png
   :scale: 25%
   :align: center
 
The desired behavior for requests

 * External clients round-robin between backend servers
 * Persist External client requests to original DC server if requests move between DC
 * Internal client requests will have affinity to local DC server
 
.. image:: external-clients.png
   :scale: 25%
   :align: center
 
.. image:: internal-clients.png
   :scale: 25%
   :align: center

Servers in the Demo
===================

==================   ==================  =========================  ==============================================
    Hostname             MGMT IP             Network IP                    Login / Password
==================   ==================  =========================  ==============================================
    win2008-rdp         10.1.1.10              10.1.20.5             administrator / [see details page]
    bigip1              10.1.1.7               10.1.10.240           admin / admin
    bigip2              10.1.1.8               10.1.10.240           admin / admin
    server1              10.1.1.4              10.1.240.10           centos or user / [ssh key] 
    server2              10.1.1.5              10.1.250.10           centos or user / [ssh key]
    automation           10.1.1.6              10.1.20.8             centos or user / [ssh key]
    jenkins              10.1.1.11                                   ubuntu / [ssh key]
==================   ==================  =========================  ==============================================   
   
Connecting with Windows RDP
===========================
Once the Deployment is finished starting click on the "Components" tab to get a view like the following.
   

.. image:: deployment-components.png
   :scale: 50%
   :align: center

Find the win2008-rdp component and click on the "Access" button to display the "RDP" link.

.. image:: win2008-rdp-component.png
   :scale: 50%
   :align: center
   
Download/launch the RDP link.  

.. warning::  For MAC user, it is recommended to use Microsoft Remote Desktop. You may not be able to access your jumpbox otherwise. It is available in the App store (FREE).
 

The username is "Administrator" and the password can be found under the "Details" page of the win2008-rdp component.  
Note: copy/paste of the password into the RDP session does not work. You can copy the password, open the RDP session settings in your RPD clinet and paste the password there. Save it and open the RDP session. You should see a desktop that looks like the following.

.. image:: windows-desktop.png
   :scale: 50%
   :align: center

.. warning:: Help for small font/text.  The lab is optimized for a 1080p display.  For HiDPI displays you may want to re-size your screen first.  See :ref:`setup_hi_dpi` for some suggested tips.

For help on changing the Keyboard Language please see :ref:`setup_keyboard`
   
   
Licensing/Resetting BIG-IP
==========================

When a UDF Deployment is started you will need to re-license the device.  There are links on the Desktop to expedite this process.

First find the "License" links.

.. image:: license-links.png
   :scale: 75%
   :align: center

Double-click on both of these and you should see a window appear briefly like the following.

.. image:: license-bigip.png
   :scale: 50%
   :align: center

Next find the "Resetting" links.

.. image:: resetting-links.png
   :scale: 75%
   :align: center

Double-click on both of these and you should see a window appear briefly like the following.

.. image:: resetting-bigip.png
   :scale: 50%
   :align: center
   
| *The previous steps go through a scripted process of resetting the license and*
| *restoring the system to a known state via a UCS restore.*

You are now ready to start the next Lab: :doc:`../lab2/sync-group`
   
Appendix
========

.. _setup_hi_dpi:

HiDPI Displays
--------------

The default resolution is intended for low DPI monitors (i.e. 1080p).

If you need to change the DPI (make the font/text large) right click on the desktop.

.. image:: screen-resolution-menu.png
   :scale: 50%
   :align: center
   
Click on the "Make text and other items larger..."   

.. image:: screen-resolution-page.png
   :scale: 50%
   :align: center

Select "150%".  Logout/login.

.. image:: screen-resolution-text.png
   :scale: 50%
   :align: center   

   
.. _setup_keyboard:

Change keyboard input
---------------------

   The default keyboard mapping is set to english. If you need to change it, here is the method
   
   * Click on the start menu button and type 'Language' in the search field.
   * Click on 'change keyboards' option in the search list
   
   .. image:: change-keyboards.png
      :scale: 50 %
      :align: center

   * Click on 'Add a language' 
   
   .. image:: add-keyboard.png
      :scale: 50 %
      :align: center

   * Add the language you want to have for your keyboard mapping. 
   
   .. image:: select-keyboard.png
      :scale: 50 %
      :align: center
	  
   * Select the language (bottom right of screen).
