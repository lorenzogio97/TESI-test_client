#!/bin/bash
# utility to copy test file on remote VM

echo "Copying file to remote machine ..."
sshpass -p "ubuntu" scp -r ./edge_http ./performance ./validation ubuntu@172.16.4.48:/home/ubuntu/clients

