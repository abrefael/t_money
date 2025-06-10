#!/bin/bash

get_backup_files() {
 get_backup_files=" ";
 i=1;
 
for entry in backups/*; do
  entry=$(basename "$entry")
  file_name="backups/$entry";
  if [ "$entry"==".files" ] || [[ "$entry"==*"site_config"*]]; then
   echo "$entry found. Doing nothing";
  elif [[ "$entry"==*"database"* ]]; then
   read -rp "$entry found. Is it a database backup file? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files+="backup/$entry ";
   else
#    I don't know yet
   fi
  elif [[ "$entry"==*"private-files"* ]]; then
   read -rp "$entry found. Is it a backup of private files? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files+="--with-private-files backup/$entry ";
   else
#    I don't know yet
   fi
  elif [[ "$entry"==*"files"* ]]; then
   read -rp "$entry found. Is it a backup of public files? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files+="--with-public-files backup/$entry ";
   else
#    I don't know yet
   fi
  else
   if [ $i==1 ]; then
    echo "No backup files could be recognized automaticaly. You will nedd to supply the filenames."
    read -rp "Please supply a filename of the database backup." ans;
    get_backup_files+="backup/$ans ";
    ((i++));
   elif [ $i==2 ]; then
    echo "We need to know if you have public files backup? [Y\n]"
    read -rp "Now, please supply a filename of the public files backup. Leave blanck if none." ans;
    if [ $ans=='' ]; then
     read -rp "Now, please supply a filename of the private files backup." ans;
     get_backup_files+="--with-private-files backup/$ans ";
    else
     get_backup_files+="--with-public-files backup/$ans ";
    fi
    ((i++));
   elif [ $i==3 ]; then
    read -rp "Please supply a filename of the private files backup." ans;
    get_backup_files+="--with-private-files backup/$ans ";
   fi
  fi
 done
 echo $get_backup_files
}


if [ $1=="-h" ] || [ $1=="--help" ]; then
 cat << EOF
usage: ./setup.su [-r][-h|--help]
-r		activate site restore process, where you are prompted for
		the files that contains the different backup files.
-h		Also --help, shows this prompt.
EOF
 return
fi


read -rp "Please enter port number [8080]: " port_num
if [ $port_num=='' ] ; then
 port_num=8080;
fi

echo "port_num=$port_num" > .env

if [ $1=='-r' ]; then
 echo "db_backup=$(get_backup_files)" >> .env;
fi

create_site=$(docker ps -a | grep "${PWD##*/}")
echo "create_site=$create_site" >> .env

mkdir -p output
mkdir -p assets
if [ -f Dockerfile ]; then 
  docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .;
fi
