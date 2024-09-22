#!/bin/bash

for dns_ttl in 60
do
  for rtt in 122
  do
    for inter_mig_time in 5 20
    do
      for run_id in 0 1
      do
        curl https://orchestrator.lorenzogiorgi.com/dns/$dns_ttl
        sudo -E python3 single-client_dynamic_dns_long-run.py $inter_mig_time $rtt $run_id $dns_ttl
        sleep 60
      done
    done
  done
done