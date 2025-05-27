#!/bin/bash

read -rp "Please enter port number [8080]: " port_num
if [ $port_num=='' ] ; then
  port_num=8080;
fi

mkdir -p output
mkdir -p assets
if [ -f Dockerfile ]; then 
  docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .;
fi


port_num=$port_num:8080
sed -i "s/port_num/\"$port_num\"/" pwd.yml
docker compose -f pwd.yml up --force-recreate -d
sed -i '96d' pwd.yml
sed -i '96s/.*/        bench migrate;/' pwd.yml
sed -i 's/read/# read/' setup.sh
sed -i 's/sed/# sed/' setup.sh
