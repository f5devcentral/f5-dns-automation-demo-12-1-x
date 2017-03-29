cd /home/user/f5-icontrol-codeshare-python/aws-dns-example
python bigip_dns_helper.py --host=10.1.1.7 --action enable_sync
python bigip_dns_helper.py --host=10.1.1.7 --action add_datacenter --datacenter SUBNET_10
python bigip_dns_helper.py --host=10.1.1.7 --action add_datacenter --datacenter SUBNET_30

python bigip_dns_helper.py --host=10.1.1.7 --action add_server  --datacenter SUBNET_10 --server_name bigip1 --server_ip=10.1.10.240
python bigip_dns_helper.py --host=10.1.1.7 --action add_server  --datacenter SUBNET_30 --server_name bigip2 --server_ip=10.1.30.240


python bigip_dns_helper.py --host=10.1.1.7 --action save_config
sleep 3
python bigip_dns_helper.py --host=10.1.1.8 --action gtm_add --peer_host=10.1.1.7 --peer_selfip 10.1.10.240
sleep 3
python bigip_dns_helper.py --host=10.1.1.7  --action create_dns_cache
python bigip_dns_helper.py --host=10.1.1.8  --action create_dns_cache

python bigip_dns_helper.py --host=10.1.1.7  --action create_external_dns_profile
python bigip_dns_helper.py --host=10.1.1.8  --action create_external_dns_profile

python bigip_dns_helper.py --host=10.1.1.7  --action create_internal_dns_profile
python bigip_dns_helper.py --host=10.1.1.8  --action create_internal_dns_profile

python bigip_dns_helper.py --host=10.1.1.7  --action create_external_dns_listener --listener_ip 10.1.10.13
python bigip_dns_helper.py --host=10.1.1.8  --action create_external_dns_listener --listener_ip 10.1.30.13

python bigip_dns_helper.py --host=10.1.1.7  --action create_internal_dns_listener --listener_ip 10.1.10.13 --internal_network 10.1.0.0/16
python bigip_dns_helper.py --host=10.1.1.8  --action create_internal_dns_listener --listener_ip 10.1.10.13 --internal_network 10.1.0.0/16


python bigip_dns_helper.py --host=10.1.1.7 --action save_config
sleep 3
python iapps/import_template_bigip.py  --impl iapps/iapp.tcl --apl iapps/iapp.apl 10.1.1.7 appsvcs_integration_v2.0.003
python iapps/import_template_bigip.py  --impl iapps/iapp.tcl --apl iapps/iapp.apl 10.1.1.8 appsvcs_integration_v2.0.003
python iapps/deploy_iapp_bigip.py -r 10.1.1.7 iapps/sample_http.json --strings pool__addr=10.1.10.10 \
       --pool_members=0:10.1.240.10:80:0:1:10:enabled:none,0:10.1.250.10:80:0:1:0:enabled:none --iapp_name external_vs

python iapps/deploy_iapp_bigip.py -r 10.1.1.8 iapps/sample_http.json --strings pool__addr=10.1.30.10 \
       --pool_members=0:10.1.250.10:80:0:1:10:enabled:none,0:10.1.240.10:80:0:1:0:enabled:none --iapp_name external_vs

python iapps/deploy_iapp_bigip.py -r 10.1.1.7 iapps/sample_http.json --strings pool__addr=10.1.10.100 \
       --pool_members=0:10.1.240.10:80:0:1:10:enabled:none,0:10.1.250.10:80:0:1:0:enabled:none --iapp_name internal_vs

python iapps/deploy_iapp_bigip.py -r 10.1.1.8 iapps/sample_http.json --strings pool__addr=10.1.30.100 \
       --pool_members=0:10.1.250.10:80:0:1:10:enabled:none,0:10.1.240.10:80:0:1:0:enabled:none --iapp_name internal_vs

python bigip_dns_helper.py --host=10.1.1.7 --action save_config
sleep 3
python bigip_dns_helper.py --host=10.1.1.7  --action create_vs --vip 10.1.10.10:80 --vip_translate 10.1.10.10:80 --vs_name external_vs --server_name bigip1
python bigip_dns_helper.py --host=10.1.1.7  --action create_vs --vip 10.1.10.100:80 --vip_translate 10.1.10.100:80 --vs_name internal_vs --server_name bigip1

python bigip_dns_helper.py --host=10.1.1.7  --action create_vs --vip 10.1.30.10:80 --vip_translate 10.1.30.10:80 --vs_name external_vs --server_name bigip2
python bigip_dns_helper.py --host=10.1.1.7  --action create_vs --vip 10.1.30.100:80 --vip_translate 10.1.30.100:80 --vs_name internal_vs --server_name bigip2
sleep 3
python bigip_dns_helper.py --host=10.1.1.7  --action create_pool --name external_pool
python bigip_dns_helper.py --host=10.1.1.7  --action create_pool --name internal_pool

python bigip_dns_helper.py --host=10.1.1.7  --action create_pool_members --name external_pool --vs_name bigip1:external_vs,bigip2:external_vs
python bigip_dns_helper.py --host=10.1.1.7  --action create_pool_members --name internal_pool --vs_name bigip1:internal_vs,bigip2:internal_vs
sleep 3
python bigip_dns_helper.py --host=10.1.1.7  --action create_wideip --name www.f5demo.com --pool external_pool,internal_pool

python bigip_dns_helper.py --host 10.1.1.7   --action create_region --name internal_network --internal_network 10.1.240.0/20
python bigip_dns_helper.py --host 10.1.1.7   --action create_region --name region_1 --internal_network 10.1.240.0/24,10.1.10.0/24
python bigip_dns_helper.py --host 10.1.1.7   --action create_region --name region_2 --internal_network 10.1.250.0/24,10.1.30.0/24
sleep 3
python bigip_dns_helper.py --host=10.1.1.7 --action save_config
python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: region /Common/internal_network server: pool /Common/internal_pool"
python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: not region /Common/internal_network server: pool /Common/external_pool"
python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: region /Common/region_1 server: region /Common/region_1"
python  bigip_dns_helper.py --host 10.1.1.7  --action create_topology_record --name "ldns: region /Common/region_2 server: region /Common/region_2"
python  bigip_dns_helper.py --host 10.1.1.8  --action create_topology_record --name "ldns: region /Common/region_1 server: region /Common/region_1"
python  bigip_dns_helper.py --host 10.1.1.8  --action create_topology_record --name "ldns: region /Common/region_2 server: region /Common/region_2"

sleep 3
python bigip_dns_helper.py --host=10.1.1.7 --action save_config
