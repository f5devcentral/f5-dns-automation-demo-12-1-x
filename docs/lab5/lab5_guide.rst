Jenkins Pipeline
================

During the prior lab :doc:`../lab4/lab4_guide` Jenkins was used to provide a frontend tool to launch the automation scripts from :doc:`../lab3/scripted`.

This lab will leverage Jenkins Pipeline to create a workflow that will validate the individual steps that are executing in a more declarative manner.

Restoring the BIG-IP Configuration
==================================

This step is to cleanup the BIG-IP config that was created in prior Labs.
RDP into the Windows jump host.

Reset both BIG-IP to be the same state as after Lab 1.

Find the "Resetting" links on the Desktop.

.. image:: ../lab1/resetting-links.png
   :scale: 75%
   :align: center

Double-click on both of these and you should see a window appear briefly like the following.

.. image:: ../lab1/resetting-bigip.png
   :scale: 50%
   :align: center

Verify that you no longer see the changes that were previously deployed.

Creating a pipeline
===================

Jenkins allows you to put together a collection of actions, branch on conditions, and measure the results.

This can be put together to put together a series of stages.

 * Stage 1: Enable DNS Sync
 * Stage 2: Cluster DNS Devices
 * Stage 3: Add additional DNS Configuration
 * Stage 4: Import App Svcs iApp Template
 * Stage 5: Deploy App Svcs iApp Template
 * Stage 6: Add DNS Configuration
 * Stage 7: Verify Configuration
 
To describe these stages we can create a "Jenkinsfile" that will instruct Jenkins to execute these stages.

The following will pull down a copy of the scripts used in this lab and execute the steps to create a DNS cluster.

.. code-block:: groovy
  
  stage('clone git repo') {
     node {
       git url: 'https://github.com/f5devcentral/f5-dns-automation-demo-12-1-x.git', branch:'master'
     }
  }
  stage('enable dns sync') {
    node {
      dir ('lib') {                    
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action enable_sync'
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action add_datacenter --datacenter SUBNET_10'
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action add_datacenter --datacenter SUBNET_30'
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action add_server  --datacenter SUBNET_10 --server_name bigip1 --server_ip=10.1.10.240'
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action add_server  --datacenter SUBNET_30 --server_name bigip2 --server_ip=10.1.30.240'
                    sh 'python bigip_dns_helper.py --host=10.1.1.7 --action save_config'
      }
    }
  }
  stage('gtm add') {
    node {
      dir ('lib') {                    
                    sh 'sleep 3'
                    sh 'python bigip_dns_helper.py --host=10.1.1.8 --action gtm_add --peer_host=10.1.1.7 --peer_selfip 10.1.10.240'
                    sh 'sleep 3'
      }
    }
  }  

The full code can be found on `GitHub <https://github.com/f5devcentral/f5-dns-automation-demo-12-1-x/blob/master/f5-udf-2.0/Jenkinsfile>`_.  
  
Launching the pipeline
======================

After both BIG-IP are active again open Chrome in the RDP Session and click on the Jenkins link.

.. image:: ../lab4/Jenkins-link.png
   :scale: 50%
   :align: center

Login to the jenkins server. 
The credentials are on the RDP Desktop in the "Jenkins credentials.txt" file.

After login to the Jenkins Web interface, please note the UDF-demo-pipeline folder.

.. image:: udf-demo-pipeline-folder.png
   :scale: 75%
   :align: center

Click on "UDF-demo-pipeline" and you should see.

.. image:: udf-demo-pipeline-page.png
   :scale: 50%
   :align: center

In order to run the project click on the left side the "Build Now" link.  While the build is running you will see.

.. image:: udf-demo-pipeline-running.png
   :scale: 50%
   :align: center
   
When the pipeline is complete you will see:

.. image:: udf-demo-pipeline-finished.png
   :scale: 50%
   :align: center
   
Failing Tests
=============

In the previous exercise we deployed a successful deployment.  In this exercise we will purposely break the pipeline.

Reset both BIG-IP to be the same state as after Lab 1.

Find the "Resetting" links on the Desktop.

.. image:: ../lab1/resetting-links.png
   :scale: 75%
   :align: center

Double-click on both of these and you should see a window appear briefly like the following.

.. image:: ../lab1/resetting-bigip.png
   :scale: 50%
   :align: center

Verify that you no longer see the changes that were previously deployed.

Go back to the 'UDF-demo-pipeline' page.

.. image:: udf-demo-pipeline-page.png
   :scale: 50%
   :align: center
   
This time click on the "Configure" link.

Find the "Pipeline" section.

.. image:: udf-demo-pipeline-configure-pipeline.png
   :scale: 50%
   :align: center

Select the pulldown for "Pipeline script from SCM" and change to "Pipeline Script".

Go to `GitHub <https://raw.githubusercontent.com/f5devcentral/f5-dns-automation-demo-12-1-x/master/f5-udf-2.0/Jenkinsfile>`_ and copy the text into your clipboard.  

Paste the contents into the script text area.

Comment out the following lines (around line 100).

.. code-block:: groovy

  //sh 'python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: region /Common/region_1 server: region /Common/region_1"'
  //sh 'python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: region /Common/region_2 server: region /Common/region_2"'
  //sh 'python  bigip_dns_helper.py --host 10.1.1.8  --action create_topology_record --name "ldns: region /Common/region_1 server: region /Common/region_1"'
  //sh 'python  bigip_dns_helper.py --host 10.1.1.8  --action create_topology_record --name "ldns: region /Common/region_2 server: region /Common/region_2"'

The result should look something like:

.. image:: udf-demo-pipeline-configure-pipeline-comment-out.png
   :scale: 50%
   :align: center

Now click on the Save Button.

.. image:: save-button.png
   :scale: 75%
   :align: center

Back on the pipeline page find the "Build Now" link and click on it.

.. image:: udf-demo-pipeline-finished.png
   :scale: 50%
   :align: center

Once the build completes you should see a failure.

.. image:: udf-demo-pipeline-failure.png
   :scale: 50%
   :align: center

Hover your mouse over the failure.

.. image:: udf-demo-pipeline-failure-hover.png
   :scale: 75%
   :align: center

Click on "Logs" to see the detail and expand the failing task.

Hover your mouse over the failure.

.. image:: udf-demo-pipeline-failure-detail.png
   :scale: 75%
   :align: center

In this case the script "test-internal.py" exited with a non-zero exit code.  This causes Jenkins to treat this as a failure.  In this case the script was only expecting to see responses from a single Data Center and instead received responses from both Data Centers due to the lack of topology records.