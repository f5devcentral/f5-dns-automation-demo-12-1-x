.. F5 DNS Automation Demo 12.1.x documentation master file, created by
   sphinx-quickstart on Mon Mar 27 07:59:15 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

F5 DNS Automation Demo 12.1.x
=============================

This is a Demo of using the F5 Python SDK to automate the process of deploying BIG-IP DNS.

 

.. toctree::
   :maxdepth: 2
   :caption: Lab 1: Connecting to UDF 2.0
   
   lab1/connecting.rst
   lab1/license_reset_bigip.rst

Lab 1 will cover the process of connecting to UDF 2.0.

.. toctree::
   :maxdepth: 2
   :caption: Lab 2: Traditional BIG-IP DNS Deployment

   lab2/sync-group.rst

Deploying without Automation.  This will cover the basic steps of:

#. Adding BIG-IP servers to BIG-IP DNS
#. Creating BIG-IP DNS Cluster

This provides some context of what the automation will be performing.  

Additional optional exercises.

#. Creating BIG-IP LTM Virtual Server and Pools
#. Creating BIG-IP DNS Virtual Server and Pools
#. Creating BIG-IP DNS Wide-IP

.. toctree::
   :maxdepth: 2
   :caption: Lab 3: Deploying BIG-IP DNS with F5 Python SDK

   lab3/scripted.rst

During Lab  3 we will utilize the F5 Python SDK to script the steps that 
were previously performed manually.  The Application Services iApp will
also be leveraged to provide Service Catalog of L4-L7 services.

.. toctree::
   :maxdepth: 2
   :caption: Lab 4: Using Jenkins to Orchestrate

   lab4/lab4_guide.rst

In Lab 3 we launched the automation scripts via ssh/shell scripts.  During this
lab we will utilize Jenkins to perform the automation steps.  

Jenkins can provide a more standard way of deploying and monitoring the health 
of automated workflows.

The goal of this lab is to demonstrate how complex automation tasks can be hidden behind a generic automation engine. 
In this case the deployment is in UDF 2.0. Running through the Lab demonstrates how easy it is to change the destination 
to AWS or Azure or private cloud environments with keeping the shim layer unchanged.

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
