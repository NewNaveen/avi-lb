import json
import requests
from requests.auth import HTTPBasicAuth
import time


"""
Get the CSRF token by running the below API 
curl -X POST  --data "username=admin&password=AviUser@123" "https://<controller-ip>/login" -H "accept: application/json" -H "X-Avi-Version: 30.2.1" --insecure  -v

This script will create multiple VS VIP at once
"""
username = 'admin'
password = 'password'

controller_url = "https://<controller-ip>"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1", "X-CSRFToken": "xxxxxx"}

vsip = [f"100.64.149.{i}" for i in range(55,60)]

content = []
for j in vsip:
    data = {
        "name": f"production_vsvip-{j}",
        "vip": [
            {
                "subnet": {
                    "ip_addr": {
                        "addr": "100.64.149.0",
                        "type": "V4"
                    },
                    "mask": 24
                },
                "auto_allocate_ip": True,
                "ip_address": {
                    "addr": f"{j}",
                    "type": "V4"
                }
            }
        ],
        "east_west_placement": False
    }
    content.append(data)


def create_vsvip(content):
    # Tenant is required
    vsvip_url = f"{controller_url}/api/vsvip"
    res = requests.post(vsvip_url, auth=HTTPBasicAuth(username, password), headers=Headers, data=json.dumps(content), verify=False)
    time.sleep(2)
    if res.status_code == 200:
        output = res.json()
        return output
    else:
        return res.status_code


if __name__ == "__main__":
    for vip in content:
        print(create_vsvip(vip))
