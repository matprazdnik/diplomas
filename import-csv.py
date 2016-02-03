#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import cymysql

config = {
    'db': {
        'host': '127.0.0.1',
        'user': 'mf',
        'passwd': '12345',
        'db': 'mf',
        'charset': 'utf8'
    }
}

users = csv.reader (open (sys.argv[1]))
dbc = config['db']
conn = cymysql.connect(host=dbc['host'], user=dbc['user'], passwd=dbc['passwd'], db=dbc['db'], charset=dbc['charset'])
cur = conn.cursor()
count = 0
for row in users:
  count += 1
  if count == 1:
    continue
  first_name, last_name, school, grade, gender, degree = row[3], row[4], row[7], row[6], row[5], row[8]
  cur.execute ('insert into users (first_name, last_name, school, grade, gender, degree, state) values (%s, %s, %s, %s, %s, %s, %s)', \
    [first_name, last_name, school, grade, gender, degree, '0'])
  if count % 100 == 0:
    print ('Imported ' + str (count - 1) + ' users')
conn.commit ()
print ('Total: ' + str (count - 1) + ' users')
