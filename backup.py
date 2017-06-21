import requests
import json
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import base64
import time

username = "admin"
password = "Password@123"
volume_name = "MyVolume10"

encoded_cred = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
storage_vm_req_url = "https://52.41.164.218:8443/api/2.0/ontap/storage-vms?name=svm_ONTAP_ELVIS"
headers = {
    "Authorization" : "Basic %s" % encoded_cred,
    "Content-type" : "application/json",
    "Accept" : "application/json"
}
storage_vm_resp = requests.get(storage_vm_req_url, headers=headers, verify=False)

storage_vm_resp_content=json.loads(storage_vm_resp.text)
storage_vm_key=storage_vm_resp_content["result"]["records"][0]["key"]

print storage_vm_key

storage_vm_volume_request_url="https://52.41.164.218:8443/api/2.0/ontap/storage-vms/%s/volumes?name=MyVolume" %(storage_vm_key)
storage_vm_volume_resp = requests.get(storage_vm_volume_request_url, headers=headers, verify=False)
storage_vm_volume_resp_content=json.loads(storage_vm_volume_resp.text)

storage_disk_volume_key=storage_vm_volume_resp_content["result"]["records"][0]["key"]

print storage_disk_volume_key

snapshot_request_url="https://52.41.164.218:8443/api/2.0/ontap/snapshots"

snapshot_request_data = {
    "volume_key" : storage_disk_volume_key,
    "name" : volume_name + "-snapshot"
}

snapshot_response=requests.post(snapshot_request_url, data=json.dumps(snapshot_request_data),headers=headers, verify=False)
volume_snapshot_location = snapshot_response.headers.get("Location")

snapshot_resource_key_response = requests.get(volume_snapshot_location, headers=headers, verify=False)
snapshot_resource_key_response_content=json.loads(snapshot_resource_key_response.text)

print json.dumps(snapshot_resource_key_response_content, indent=2)

snapshot_resource_key = snapshot_resource_key_response_content["result"]["records"][0]["resource_key"]


snapshot_request_url = "https://52.41.164.218:8443/api/2.0/ontap/snapshots/%s" %(snapshot_resource_key)
snapshot_response = requests.get(snapshot_request_url, headers=headers, verify=False)
snapshot_response_content=json.loads(snapshot_response.text)
print json.dumps(snapshot_response_content, indent=2)

# print json.dumps(snapshot_response_content, indent=2)


# storage_vm_key = storage_vm_resp.content["records"][0]["key"]
# print storage_vm_key
