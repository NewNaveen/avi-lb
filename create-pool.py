
"""
{'name': 'production_pool', 'default_server_port': 80, 'servers': [{'ip': {'addr': '10.10.90.120', 'type': 'V4'}},
{'ip': {'addr': '10.10.90.121', 'type': 'V4'}}], 'lb_algorithm': 'LB_ALGORITHM_LEAST_CONNECTIONS'}
"""

"""
We need to get cloud details
tenant ref
Health monitor details
"""

import json
import requests
from requests.auth import HTTPBasicAuth
import time


"""
Get the CSRF token by running the below API 
curl -X POST  --data "username=admin&password=pass" "https://<ip>/login" -H "accept: application/json" -H "X-Avi-Version: 30.2.1" --insecure  -v

"""
username = 'admin'
password = 'pass'

controller_url = "https://<ip>"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1", "X-CSRFToken": "xxxxxxxxx"}


data = {
    "name":"Test-pool",
    "default_server_port":80,
    "tenant_ref": "https://<ip>/api/tenant/admin",
    "cloud_ref": "https://<ip>/api/cloud/cloud-43948b03-771f-4d99-ba28-ef6d584db699",
    "servers":[
        {
            "enabled": True,
            "hostname": "100.64.141.100",
            "ip":{
                "addr":"100.64.141.100",
                "type":"V4"
            }
        },
        {
            "enabled": True,
            "hostname": "100.64.141.101",
            "ip":{
                "addr":"100.64.141.101",
                "type":"V4"
            }
        }
    ],
    "lb_algorithm":"LB_ALGORITHM_LEAST_CONNECTIONS"
}


def create_pool(content):
    # Tenant is required
    pool_url = f"{controller_url}/api/pool"
    res = requests.post(pool_url, auth=HTTPBasicAuth(username, password), headers=Headers, data=json.dumps(content), verify=False)
    time.sleep(2)
    if res.status_code == 200:
        output = res.json()
        return output
    else:
        return res.status_code


if __name__ == "__main__":
    print(create_pool(data))
