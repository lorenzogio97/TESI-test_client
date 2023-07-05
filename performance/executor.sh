#!/bin/bash

for rtt in 122
do
  for inter_mig_time in 5 20
  do
    for run_id in 0 1
    do
      sudo -E python3 single-client_dynamic_no-migration_long-run.py $inter_mig_time $rtt $run_id
    done
  done
done