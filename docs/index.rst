.. f5-dns-automation-demo-12-1-x documentation master file, created by
   sphinx-quickstart on Thu Mar 30 15:01:24 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to f5-dns-automation-demo-12-1-x's documentation!
=========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


**Lab 1 **

Lab 1 will cover the process of connecting to UDF 2.0.

.. toctree::
   :maxdepth: 2
   :caption: Lab 2: Traditional BIG-IP DNS Deployment

   lab2/sync-group.rst

** Lab 2 **
 
Lab 2 will deploy the setup without Automation.  This will cover the basic steps of:

#. Creating BIT-IP LTM configuration
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

** Lab 3 **

During Lab  3 we will utilize the F5 Python SDK to script the steps that 
were previously performed manually.  The Application Services iApp will
also be leveraged to provide Service Catalog of L4-L7 services.




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
