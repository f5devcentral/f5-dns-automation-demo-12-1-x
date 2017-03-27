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
