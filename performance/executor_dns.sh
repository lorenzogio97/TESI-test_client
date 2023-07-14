#!/bin/bash

for dns_ttl in 1 60
do
  for rtt in 7
  do
    for inter_mig_time in 5
    do
      for run_id in 0 1
      do
        curl https://orchestrator.lorenzogiorgi.com/dns/$dns_ttl
        sudo -E python3 single-client_static_dns_long-run.py $inter_mig_time $rtt $run_id $dns_ttl
        sleep 60
      done
    done
  done
done