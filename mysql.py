#!/usr/bin/env python
from __future__ import print_function

import pymysql

conn = pymysql.connect(host='34.211.233.152', port=3306, user='root', passwd='Netapp1!', db='mysql')

cur = conn.cursor()

cur.execute("SELECT * FROM owner")

print(cur.description)

print()

for row in cur:
    print(row)

cur.close()
conn.close()
