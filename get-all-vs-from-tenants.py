import json
import requests
from requests.auth import HTTPBasicAuth
import time

"""
By using the virtualservice url we can get VS from all tenants
https://{ip}/api/virtualservice
Filter the VS that are enabled with VIP as SNAT 
-- We can separate the VIP as SNAT enabled and disabled

--> to change the network setting on VIP ip address we have to run 
/api/vsvip

auto_allocate_ip: 

placement_networks: https://10.206.255.115/api/network/dvportgroup-64-cloud-43948b03-771f-4d99-ba28-ef6d584db699

"""
username = 'admin'
password = 'xxxxxx'

controller_url = "https://<controlelr-ip-address>"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1"}


def get_tenant():
    # Tenant is required
    tenant_dict = {}
    all_tenants = []
    tenant_count = 0
    pool_url = f"{controller_url}/api/tenant"
    res = requests.get(pool_url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
    time.sleep(2)

    if res.status_code == 200:
        output = res.json()
        tenant_count = tenant_count + output["count"]
        for i in output["results"]:
            all_tenants.append(i["name"])
            tenant_dict.update({i["name"]: i["uuid"]})
        while len(all_tenants) != tenant_count:
            extra_tenants = more_tenants(output)
            all_tenants.extend(extra_tenants[0])
            tenant_dict.update(extra_tenants[2])
            output = extra_tenants[1]
        return tenant_dict
    else:
        return res.status_code


def more_tenants(data):
    m_tenant_dict = {}
    m_tenants = []
    new_url = data.get("next")
    url = f"{controller_url}{new_url}"
    res = requests.get(url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
    output = res.json()
    for j in output.get("results"):
        m_tenants.append(j.get("name"))
        m_tenant_dict.update({j["name"]: j["uuid"]})
    return m_tenants, output, m_tenant_dict


# Get all VS from all tenants
def all_vs(tenants):
    vs_url = f"{controller_url}/api/virtualservice"
    vs_with_snat = {}
    vs_without_snat = {}
    if len(tenants) > 0:
        for name, uuid in tenants.items():
            Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1", "X-Avi-Tenant-UUID": f"{uuid}"}
            vs = requests.get(url=vs_url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
            time.sleep(2)
            vs = vs.json()
            # VS without SNAT
            list_vs_without_snat = [i["name"] for i in vs["results"] if not i["use_vip_as_snat"]]
            vs_without_snat[name] = list_vs_without_snat
            print(name)
            print(list_vs_without_snat)
            print(len(list_vs_without_snat))
            # VS with SNAT
            list_vs_with_snat = [i["name"] for i in vs["results"] if i["use_vip_as_snat"]]
            vs_with_snat[name] = list_vs_with_snat
            print(list_vs_with_snat)
            print(len(list_vs_with_snat))
    return vs_with_snat, vs_without_snat


if __name__ == "__main__":
    full_tenants = get_tenant()
    vs = all_vs(full_tenants)
    print("Tenant_name: UUID")
    print(full_tenants)
    print("VS With SNAT , VS Without SNAT")
    print(vs)
    print("Total VS")
    total_vs = 0
    for allvs in vs:
        for key, value in allvs.items():
            total_vs += len(value)
    print(total_vs)
