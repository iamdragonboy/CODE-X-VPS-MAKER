#!/bin/bash
userid=$1
port=$(shuf -i 2000-65000 -n 1)
ip=$(curl -s ifconfig.me)
docker run -d -p $port:22 ubuntu_vps_ssh
echo "UserID: $userid"
echo "SSH: ssh root@$ip -p $port"
echo "Password: lpnodes"
