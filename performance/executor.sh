#!/bin/bash

for rtt in 7
do
  for inter_mig_time in 5
  do
    for run_id in 0 1
    do
      sudo -E python3 single-client_dynamic_no-migration_long-run.py $inter_mig_time $rtt $run_id
      sleep 60
      sudo -E python3 single-client_dynamic_alt-svc_long-run.py $inter_mig_time $rtt $run_id
      sleep 60
    done
  done
done