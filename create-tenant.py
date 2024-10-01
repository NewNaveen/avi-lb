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
curl -X POST  --data "username=admin&password=xxxxxxxx" "https://10.206.255.115/login" -H "accept: application/json" -H "X-Avi-Version: 30.2.1" --insecure  -v

"""
username = 'admin'
password = 'xxxxx'

controller_url = "https://xxxxxxxxx"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1", "X-CSRFToken": "xxxxxxxx"}

tenant_name = [f"Test-tenant-{i}" for i in range(2, 140)]

tenant_data = []

for j in tenant_name:
    data = {
        "config_settings": {
            "se_in_provider_context": True,
            "tenant_access_to_provider_se": True,
            "tenant_vrf": False
        },
        "enforce_label_group": False,
        "local": True,
        "macro_in_progress": 0,
        "name": f"{j}",
        "tenant_force_delete_in_progress": False
    }
    tenant_data.append(data)


def create_tenant(content):
    # Tenant is required
    pool_url = f"{controller_url}/api/tenant"
    res = requests.post(pool_url, auth=HTTPBasicAuth(username, password), headers=Headers, data=json.dumps(content),
                        verify=False)
    time.sleep(2)
    if res.status_code == 200:
        output = res.json()
        return output
    else:
        return res.status_code


if __name__ == "__main__":
    for tenant in tenant_data:
        print(create_tenant(tenant))
