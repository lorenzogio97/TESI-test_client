# Test client for Edge Platform
This repository contains client and results for tests.

## Description of the directories

- `data_elaboration`: this folder contains data elaboration script and experiment result
- `edge_http`: a python wrapper for HTTPX library to implement HTTP Alt-Svc advertising mechanism. NOTE: this **IS NOT** a 
 complete implementation, it doesn't cover any security/alternative validation. It is useful only for test.
- `performance`: this folder contains the scripts used for performance testing
- `test-platform`: this folder contains a utility script to test the platform Orchestrator performance (results are collected by the Orchestrator)
- `validation`: this folder contains scripts for platform validation. 