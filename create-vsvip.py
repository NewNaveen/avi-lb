import json
import requests
from requests.auth import HTTPBasicAuth
import time

username = 'admin'
password = 'password'

controller_url = "https://<ip-address>"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1"}


def get_all_tenants():
    all_tenants = {}
    tenant_url = f"{controller_url}/api/tenant"
    tenant = requests.get(tenant_url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
    time.sleep(2)
    tenant = tenant.json()

    for i in tenant["results"]:
        all_tenants.update({i["name"]: i["uuid"]})

    return all_tenants


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
            # VS with SNAT
            list_vs_with_snat = [i["name"] for i in vs["results"] if i["use_vip_as_snat"]]
            vs_with_snat[name] = list_vs_with_snat
    return vs_with_snat, vs_without_snat


if __name__ == "__main__":
    tenants = get_all_tenants()
    vs = all_vs(tenants)
    print("Tenant_name: UUID")
    print(tenants)
    print("VS With SNAT , VS Without SNAT")
    print(vs)
    print("Total VS")
    count = 0
    for i in vs:
        for key, value in i.items():
            count += len(value)
    print(count)
