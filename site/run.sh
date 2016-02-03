#!/bin/bash

cd /var/www/mf/
kill $(<mf.pid)
nohup python3 mf.py >> mf.log 2>&1 &
echo $! > mf.pid
sleep 1
tail -20 mf.log
