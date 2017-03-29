#!/usr/bin/python
import boto3
import json
import sys
from pprint import pprint
import os
from optparse import OptionParser
from bigip_dns_helper import DnsHelper
import logging

sys.path.insert(0, os.path.abspath('../lib'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dns_demo')
logger.setLevel(logging.DEBUG)

def create_eni(primary_stack_eni, secondary_stack_eni):
    pass

def create_stack(primary_stack, secondary_stack):
    pass

class Demo(object):
    def __init__(self, primary_stack, secondary_stack, password):
        self.primary_stack = primary_stack
        self.secondary_stack = secondary_stack
        self.password = password
        self.ec2 = boto3.resource('ec2')
        self.cloudformation = boto3.client('cloudformation')


        # primary
        primary_resp = self.cloudformation.describe_stacks(StackName=primary_stack)
        self.primary_stack_status = primary_resp['Stacks'][0]['StackStatus']

        # secondary
        resp = self.cloudformation.describe_stacks(StackName=secondary_stack)
        self.secondary_stack_status = resp['Stacks'][0]['StackStatus']

        if self.primary_stack_status == 'CREATE_IN_PROGRESS' or self.secondary_stack_status == 'CREATE_IN_PROGRESS':
            print 'CREATE_IN_PROGRESS'
            return

        outputs = dict([(a['OutputKey'],a['OutputValue']) for a in primary_resp['Stacks'][0]['Outputs']])
        self.primary_instance_id = outputs['Bigip1InstanceId']
        self.primary_instance = self.ec2.Instance(self.primary_instance_id)


        outputs = dict([(a['OutputKey'],a['OutputValue']) for a in resp['Stacks'][0]['Outputs']])
        self.secondary_instance_id = outputs['Bigip1InstanceId']
        self.secondary_instance = self.ec2.Instance(self.secondary_instance_id)
        
        self.primary_dev = self._get_ip(self.primary_instance.network_interfaces)
        self.secondary_dev = self._get_ip(self.secondary_instance.network_interfaces)

        self.primary_mgmt_ip = self.primary_dev[0][0][0]
        self.secondary_mgmt_ip = self.secondary_dev[0][0][0]

        self.primary_eni_1 = filter(lambda a: a.attachment['DeviceIndex'] == 1, self.primary_instance.network_interfaces)[0]
        self.secondary_eni_1 = filter(lambda a: a.attachment['DeviceIndex'] == 1, self.secondary_instance.network_interfaces)[0]

        self.primary_selfip = self.primary_dev[1][0][0]
        self.primary_selfip_eip = self.primary_dev[1][0][1]
        self.secondary_selfip = self.secondary_dev[1][0][0]
        self.secondary_selfip_eip = self.secondary_dev[1][0][1]

        self.primary_dns_listener = self.primary_dev[1][1][0]
        self.secondary_dns_listener = self.secondary_dev[1][1][0]

#        self.primary_ltm_vs1  = self.primary_dev[1][2][0]
#        self.secondary_ltm_vs1 = self.secondary_dev[1][2][0]

        self.primary_ltm_vs1  = self.primary_dns_listener
        self.secondary_ltm_vs1 = self.secondary_dns_listener

#        self.primary_ltm_vs1_eip  = self.primary_dev[1][2][1]
#        self.secondary_ltm_vs1_eip = self.secondary_dev[1][2][1]

        self.primary_ltm_vs1_eip  = self.primary_dev[1][1][1]
        self.secondary_ltm_vs1_eip = self.secondary_dev[1][1][1]

#        self.primary_ltm_vs2  = self.primary_dev[1][3][0]
#        self.secondary_ltm_vs2 = self.secondary_dev[1][3][0]



        self.primary_dc =  self.primary_instance.placement['AvailabilityZone']
        self.secondary_dc =  self.secondary_instance.placement['AvailabilityZone']


        self.dns_helper = DnsHelper(self.primary_mgmt_ip, 'admin', password, 
                               peer_host=self.secondary_mgmt_ip, peer_username='admin', peer_password=password)

        self.dns_helper_peer = DnsHelper(self.secondary_mgmt_ip, 'admin', self.password, 
                                    peer_host=self.primary_mgmt_ip, peer_username='admin', peer_password=self.password)



        print self.primary_dc, self.primary_mgmt_ip, self.primary_selfip, self.primary_dns_listener, self.primary_ltm_vs1
        print self.secondary_dc, self.secondary_mgmt_ip, self.secondary_selfip, self.secondary_dns_listener, self.secondary_ltm_vs1

        azs = set([s.availability_zone for s in self.primary_instance.vpc.subnets.all()])
        az_list = dict([(a,[]) for a in azs])

        for s in self.primary_instance.vpc.subnets.all():
            az_list[s.availability_zone].append(s.cidr_block)

        self.az_list = az_list

        logger.debug('__init__')
    def _get_ip(self, network_interfaces):
        num_devices = len(network_interfaces)
        devices = [None] * num_devices
        for y in range(num_devices):
            eni = network_interfaces[y]
            dev_idx =  eni.attachment['DeviceIndex']
            ips = []
            for x in range(len(eni.private_ip_addresses)):
                ip_obj = eni.private_ip_addresses[x]
                prv_ip =  ip_obj['PrivateIpAddress']
                pub_ip = None
                if 'Association' in ip_obj:
                    pub_ip = ip_obj['Association']['PublicIp']
                print prv_ip, pub_ip
                ips.append((prv_ip,pub_ip))
            devices[dev_idx] = ips
        return devices

    def setup_dns(self):

        self.dns_helper.enable_sync()
        logger.debug('setup_dns: sync enabled')

        self.dns_helper.add_datacenter(self.primary_dc)
        if self.primary_dc != self.secondary_dc:
            self.dns_helper.add_datacenter(self.secondary_dc)
        logger.debug('setup_dns: dc added')
        # add_server(self,server_name,server_ip, datacenter,translation=None)
        self.dns_helper.add_server(self.primary_stack, self.primary_selfip_eip, self.primary_dc, self.primary_selfip)
        self.dns_helper.add_server(self.secondary_stack, self.secondary_selfip_eip, self.secondary_dc, self.secondary_selfip)

        logger.debug('setup_dns: server added')
        self.dns_helper.save_config()

    def gtm_add(self):
        logger.debug('setup_dns: gtm_add started')        
        self.dns_helper_peer.gtm_add(self.primary_selfip_eip, self.primary_selfip)
        logger.debug('setup_dns: gtm_add complete')        
        # setup DNS 

    def setup_dns2(self):
        self.dns_helper.create_dns_cache()
        self.dns_helper_peer.create_dns_cache()

        self.dns_helper.create_external_dns_profile()
        self.dns_helper_peer.create_external_dns_profile()

        self.dns_helper.create_internal_dns_profile()
        self.dns_helper_peer.create_internal_dns_profile()
        
        self.dns_helper.create_external_dns_listener(self.primary_dns_listener)
        self.dns_helper_peer.create_external_dns_listener(self.secondary_dns_listener)

        self.dns_helper.create_internal_dns_listener(self.primary_dns_listener, self.primary_instance.vpc.cidr_block)
        self.dns_helper_peer.create_internal_dns_listener(self.secondary_dns_listener, self.primary_instance.vpc.cidr_block)

        self.dns_helper.create_region('vpc-cidr-block', [self.primary_instance.vpc.cidr_block])

        self.dns_helper.save_config()
        self.dns_helper_peer.save_config()

        for az in self.az_list:
            subnet_list = self.az_list[az]
            self.dns_helper.create_region(az,subnet_list)
            self.dns_helper.create_topology_record("ldns: region /Common/%s server: region /Common/%s" %(az, az))

        self.dns_helper.save_config()
        self.dns_helper_peer.save_config()

    def import_iapp(self, password_file):
        os.system("python iapps/import_template_bigip.py -u admin --password-file=%s --impl iapps/iapp.tcl --apl iapps/iapp.apl %s appsvcs_integration_v2.0.003" %(password_file, self.primary_mgmt_ip))
        os.system("python iapps/save_config_bigip.py -u admin --password-file admin_passwd.txt %s" %(self.primary_mgmt_ip))
        os.system("python iapps/import_template_bigip.py -u admin --password-file=%s --impl iapps/iapp.tcl --apl iapps/iapp.apl %s appsvcs_integration_v2.0.003" %(password_file, self.secondary_mgmt_ip))
        os.system("python iapps/save_config_bigip.py -u admin --password-file %s %s" %(password_file, self.secondary_mgmt_ip))

    def deploy_primary_vs1(self, password_file, pool_members):
        deploy_vs = "python iapps/deploy_iapp_bigip.py -r   -u admin --password-file=%s %s iapps/sample_http.json --strings pool__addr=%s --pool_members=%s --iapp_name sample_http_vs" 
        logger.debug('deploy: ' + deploy_vs %(password_file, self.primary_mgmt_ip, self.primary_ltm_vs1, pool_members))
        os.system(deploy_vs %(password_file, self.primary_mgmt_ip, self.primary_ltm_vs1, pool_members))
        os.system("python iapps/save_config_bigip.py -u admin --password-file %s %s" %(password_file, self.primary_mgmt_ip))

    def deploy_secondary_vs1(self, password_file, pool_members):
        deploy_vs = "python iapps/deploy_iapp_bigip.py -r   -u admin --password-file=%s %s iapps/sample_http.json --strings pool__addr=%s --pool_members=%s --iapp_name sample_http_vs" 
        logger.debug('deploy: ' + deploy_vs %(password_file, self.secondary_mgmt_ip, self.secondary_ltm_vs1, pool_members))
        os.system(deploy_vs %(password_file, self.secondary_mgmt_ip, self.secondary_ltm_vs1, pool_members))
        os.system("python iapps/save_config_bigip.py -u admin --password-file %s %s" %(password_file, self.secondary_mgmt_ip))


    def deploy_vs1_dns(self):
        dns_helper = DnsHelper(self.primary_mgmt_ip, 'admin', password, 
                               self.secondary_mgmt_ip, 'admin', password)

        dns_helper.create_vs(self.primary_stack, "sample_ext_vs", "%s:80" %self.primary_ltm_vs1_eip, "%s:80" %self.primary_ltm_vs1)
        dns_helper.create_vs(self.primary_stack, "sample_int_vs", "%s:80" %self.primary_ltm_vs1, "%s:80" %self.primary_ltm_vs1)

        dns_helper.create_vs(self.secondary_stack, "sample_ext_vs", "%s:80" %self.secondary_ltm_vs1_eip, "%s:80" %self.secondary_ltm_vs1)
        dns_helper.create_vs(self.secondary_stack, "sample_int_vs", "%s:80" %self.secondary_ltm_vs1, "%s:80" %self.secondary_ltm_vs1)

        dns_helper.create_pool("sample_ext_pool")
        dns_helper.create_pool_members("sample_ext_pool",["%s:sample_ext_vs" %(self.primary_stack),
                                                          "%s:sample_ext_vs" %(self.secondary_stack)])

        dns_helper.create_pool("sample_int_pool")
        dns_helper.create_pool_members("sample_int_pool",["%s:sample_int_vs" %(self.primary_stack),
                                                          "%s:sample_int_vs" %(self.secondary_stack)])

        dns_helper.create_topology_record("ldns: region /Common/vpc-cidr-block server: pool /Common/%s" %("sample_int_pool"))
        dns_helper.create_topology_record("ldns: not region /Common/vpc-cidr-block server: pool /Common/%s" %("sample_ext_pool"))
        # ldns: region /Common/us-east-1d server: region /Common/us-east-1d
        dns_helper.create_wideip("sample.f5demo.com",["sample_ext_pool","sample_int_pool"])

if __name__ == "__main__":
   parser = OptionParser()
   parser.add_option('-u','--user',dest='user',default='admin')
   parser.add_option('--primary_stack')
   parser.add_option('--secondary_stack')
   parser.add_option('--password-file',dest='password_file')
   parser.add_option('--action')
   parser.add_option('--pool_members')
   (options,args) = parser.parse_args()
   
   password = open(options.password_file).readline().strip()
   demo = Demo(options.primary_stack, options.secondary_stack, password)

   if options.action == 'setup_dns':
       demo.setup_dns()
   elif options.action == 'gtm_add':
       demo.gtm_add()
   elif options.action == 'setup_dns2':
       demo.setup_dns2()
   elif options.action == 'import_iapp':
       demo.import_iapp(options.password_file)
   elif options.action == 'deploy_primary_vs1':
       demo.deploy_primary_vs1(options.password_file, options.pool_members)
   elif options.action == 'deploy_secondary_vs1':
       demo.deploy_secondary_vs1(options.password_file, options.pool_members)
   elif options.action == 'deploy_vs1_dns':
       demo.deploy_vs1_dns()
   elif options.action == 'wait_for_stack':
       while demo.primary_stack_status == 'CREATE_IN_PROGRESS' or demo.secondary_stack_status == 'CREATE_IN_PROGRESS':
           import time
           time.sleep(3)
           demo = Demo(options.primary_stack, options.secondary_stack, password)
           print 'waiting'
