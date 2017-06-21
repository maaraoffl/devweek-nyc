import requests
import json
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import base64
import time
import datetime

timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d%-H:%M:%S')

username = "admin"
password = "Password@123"
volume_name = "MyVolume-"+ timestamp

def main():

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

    # time.sleep(60)

    # snapshot_resource_key_response = requests.get(volume_snapshot_location, headers=headers, verify=False)
    # snapshot_resource_key_response_content=json.loads(snapshot_resource_key_response.text)
    # print json.dumps(snapshot_resource_key_response_content, indent=2)
    # snapshot_resource_key = snapshot_resource_key_response_content["result"]["records"][0]["resource_key"]

    retry_count=0
    max_retry=10
    while retry_count < max_retry:
        snapshot_resource_key_response = requests.get(volume_snapshot_location, headers=headers, verify=False)
        snapshot_resource_key_response_content=json.loads(snapshot_resource_key_response.text)
        print json.dumps(snapshot_resource_key_response_content, indent=2)
        # snapshot_resource_key = snapshot_resource_key_response_content["result"]["records"][0]["resource_key"]
        temp=snapshot_resource_key_response_content["result"]["records"][0]["status"]
        if temp == "STARTED":
            time.sleep(20)
            retry_count = retry_count + 1
            continue
        else:
            retry_count = max_retry
            snapshot_resource_key = snapshot_resource_key_response_content["result"]["records"][0]["resource_key"]



    snapshot_request_url = "https://52.41.164.218:8443/api/2.0/ontap/snapshots/%s" %(snapshot_resource_key)
    snapshot_response = requests.get(snapshot_request_url, headers=headers, verify=False)
    snapshot_response_content=json.loads(snapshot_response.text)
    print json.dumps(snapshot_response_content, indent=2)

def lambda_handler(event, context)
    main()
