#!/usr/bin/env python
from __future__ import print_function
import requests
import pymysql
import json
import datetime

conn = pymysql.connect(host='34.211.233.152', port=3306, user='root', passwd='Netapp1!', db='mysql')
cur = conn.cursor()
cur.execute("SELECT * FROM owner")

base_url = "https://v3v10.vitechinc.com/solr/policy_info/select?indent=on&q=*:*&wt=json"
start = 0
limit = 1000

index = 0
count = 100

table_name="policy_info"
policy_info_base_sql="INSERT INTO policy_info (participant_id, insurance_product, insurance_coverage, insurance_premium, id, insurance_plan, policy_start_date, collection_id, _version_, promocodes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#participant_base_sql="INSERT INTO participant (`id`, `last_name`, `email`) VALUES (%s, %s, %s)"

def getData(url):
    r = requests.get(url)
    return json.loads(r.content)

def convertDateTime(dateTimeString):
    return datetime.datetime.strptime(dateTimeString, "%Y-%m-%dT%H:%M:%SZ")


def insert_data(policy_info):
    try:
        promocodes=None
        if "promocodes" in policy_info.keys():
            promocodes = policy_info["promocodes"]

        cur.execute(policy_info_base_sql,
            (
            policy_info["participant_id"],
            policy_info["insurance_product"],
            policy_info["insurance_coverage"],
            policy_info["insurance_premium"],
            policy_info["id"],
            policy_info["insurance_plan"],
            convertDateTime(policy_info["policy_start_date"]),
            policy_info["collection_id"],
            str(policy_info["_version_"]),
            promocodes,
            )
        )

        # cur.execute(participant_base_sql, (participant["zip"], participant["last_name"], participant["email"]))
    except:
        # print(cur._last_executed)
        raise


while index < count:
    request_url = base_url + "&start=" + str(start + 1) + "&rows=" + str(limit);
    start = start + limit;
    print(request_url)

    # Get data
    data = getData(request_url)
    # print(json.dumps(data, indent=2))
    for record in data["response"]["docs"]:
        insert_data(record)
    conn.commit()
    index = index + 1


cur.close()
conn.close()
