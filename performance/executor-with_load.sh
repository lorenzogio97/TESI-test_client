#!/bin/bash

for client in  1 49 99 499
do
  for run_id in 0 1
  do
    echo "Esperimento"
    echo "Client $client"
    echo "RunId $run_id"
    sudo -E python3 static-client-filler-generator.py $client > output.log &
    sleep 200
    sshpass -p ubuntu ssh -oStrictHostKeyChecking=no -oCheckHostIP=no ubuntu@172.16.3.49 "sudo -E python3 /home/ubuntu/clients/performance/client-load-performance-test.py $client $run_id > output.log" &
    sleep 4820
    sleep 1200
  done
done