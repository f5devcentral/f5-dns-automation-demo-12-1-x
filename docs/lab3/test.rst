F5 Python SDK
=============

The F5 Python SDK provides an interface to the iControl REST interface.

This provides the ability to translate from actions that you would have normally done via the GUI to actions that can be performed from Python.

**Via GUI**

.. image:: ../lab2/add-datacenter.png
   :scale: 50%
   :align: center

**Via Code**

.. code-block:: python

   def add_datacenter(self,datacenter):
         "add datacenter in BIG-IP DNS"
         self.mgmt.tm.gtm.datacenters.datacenter.create(name=datacenter,partition=self.partition)

This Lab will combine the process of creating a BIG-IP DNS deployment in Lab 2 and automate the process using the F5 Python SDK.  Python code itself can be run as a script and this is used to be able to create our own utility to deploy BIG-IP configurations.  Think of it like a remote tmsh.  Command Line Interface (CLI) to the BIG-IP.  Here's an example of adding a server to BIG-IP DNS using the script.
