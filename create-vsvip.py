import json
import requests
from requests.auth import HTTPBasicAuth
import time

"""
Get the CSRF token by running the below API 
curl -X POST  --data "username=admin&password=Password" "https://<Ip-address>/login" -H "accept: application/json" -H "X-Avi-Version: 30.2.1" --insecure  -v

"""
username = 'admin'
password = 'AviUser@123'

controller_url = "https://<ip-address>"
Headers = {"accept": "application/json", "X-Avi-Version": "30.2.1", "X-CSRFToken": "xxxxxxxxxxx"}

cont = {
    "name": "production_vsvip-2",
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
                "addr": "100.64.149.55",
                "type": "V4"
            }
        }
    ],
    "east_west_placement": False
}


def create_vsvip():
    # Tenant is required
    vsvip_url = f"{controller_url}/api/vsvip"
    res = requests.post(vsvip_url, auth=HTTPBasicAuth(username, password), headers=Headers, data=json.dumps(cont), verify=False)
    time.sleep(2)
    if res.status_code == 200:
        output = res.json()
        return output
    else:
        return res.status_code


print(create_vsvip())
