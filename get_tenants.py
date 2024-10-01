import json
import requests
from requests.auth import HTTPBasicAuth
import time

"""
{'name': 'production_pool', 'default_server_port': 80, 'servers': [{'ip': {'addr': '10.10.90.120', 'type': 'V4'}},
{'ip': {'addr': '10.10.90.121', 'type': 'V4'}}], 'lb_algorithm': 'LB_ALGORITHM_LEAST_CONNECTIONS'}
"""

"""
We need to get cloud details
tenant ref
Health monitor details
"""

"""
Get the CSRF token by running the below API 
curl -X POST  --data "username=admin&password=xxxxx" "https://10.206.255.115/login" -H "accept: application/json" -H "X-Avi-Version: 30.2.1" --insecure  -v

"""
username = 'admin'
password = 'xxxxxx'

controller_url = "https://xxxxxxx"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1"}


def get_tenant():
    # Tenant is required
    all_tenants = []
    count = 0
    pool_url = f"{controller_url}/api/tenant"
    res = requests.get(pool_url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
    time.sleep(2)

    if res.status_code == 200:
        output = res.json()
        count = count + output["count"]
        for i in output["results"]:
            all_tenants.append(i["name"])
        while len(all_tenants) != count:
            extra_tenants = more_tenants(output)
            all_tenants.extend(extra_tenants[0])
            output = extra_tenants[1]
        return all_tenants
    else:
        return res.status_code


def more_tenants(data):
    tenants = []
    new_url = data.get("next")
    url = f"{controller_url}{new_url}"
    res = requests.get(url, auth=HTTPBasicAuth(username, password), headers=Headers, verify=False)
    output = res.json()
    for i in output.get("results"):
        tenants.append(i.get("name"))
    return tenants, output


if __name__ == "__main__":
    x = get_tenant()
    print(x)
    print(len(x))
