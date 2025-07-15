#!/bin/bash

get_backup_files() {
 get_backup_files="";
 i=1;
 
for entry in backups/*; do
  entry=$(basename "$entry")
  file_name="backups/$entry";
  if [ "$entry" == ".files" ] || [[ "$entry" == *"site_config"* ]]; then
   :; # echo "$entry found. Doing nothing";
  elif [[ "$entry" == *"database"* ]]; then
   read -p "$entry found. Is it a database backup file? [Y/n] " ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files+=" backups/$entry";
   else
    echo 1; # echo "I don't know yet";
    exit
   fi
  elif [[ "$entry" == *"private-files"* ]]; then
   read -p "$entry found. Is it a backup of private files? [Y/n] " ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files=" --with-private-files backups/$entry$get_backup_files";
   else
    echo 1; # echo "I don't know yet";
    exit
   fi
  elif [[ "$entry" == *"files"* ]]; then
   read -p "$entry found. Is it a backup of public files? [Y/n] " ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_backup_files=" --with-public-files backups/$entry $get_backup_files";
   else
    echo 1; # echo "I don't know yet";
    exit
   fi
  else
   if [ $i == 1 ]; then
    echo ""
    read -ep $'No backup files could be recognized automaticaly. You will nedd to supply the filenames.\nPlease supply a filename of the database backup.\n' ans;
    get_backup_files+="backups/$ans ";
    ((i++));
   elif [ $i == 2 ]; then
    read -ep $'We need to know if you have public files backup.\nIf you do, please supply a filename of the public files backup.\n Otherwise, leave blanck.\n' ans;
    if [ -z "$ans" ]; then
     read -ep $'So, please supply a filename of the private files backup.\n' ans;
     get_backup_files+="--with-private-files backups/$ans ";
    else
     get_backup_files+="--with-public-files backups/$ans ";
    fi
    ((i++));
   elif [ $i == 3 ]; then
    read -ep $'Please supply a filename of the private files backup.\n' ans;
    get_backup_files+="--with-private-files backups/$ans ";
   fi
  fi
 done
 echo $get_backup_files
}


if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
 cat << EOF

usage: ./setup.sh [-r][-h|--help]

-r		activate site restore process, where you are prompted for
		the files that contains the different backup files.
		In order for you to perform a restore process, you will need:
		
		1. A database backup file. It's name should be
		{something}database{something else}.sql or .sql.gz.
		
		2. Optional: A Public Files backup file. It's name should be
		{something}files{something else}.tar or .tar.gz.";
		It must *NOT* contain the string "private-files"!
		
		3. Optional: A Private Files backup file. It's name should be
		{something}private-files{something else}.tar or .tar.gz.
		
		
-h		Also --help, shows this prompt.

EOF
 exit
fi

create_site=$(docker ps -a | grep "${PWD##*/}")

if [ -z "$create_site" ] ; then
 mkdir -p output;
 mkdir -p assets;
 read -p "Please enter port number [8080]: " port_num;
 if [ -z "$port_num" ] ; then
  port_num=8080;
 fi
 echo "port_num=$port_num" > .env;
 echo "create_site=\"\"" >> .env;
 else
  echo "create_site=\"don't\"" >> .env;
fi

if [ "$1" == "-r" ]; then
 get_backup_files=$(get_backup_files)
 if [ $get_backup_files == 1 ]; then
  echo "Please make sure you have up to three files for your backup:";
  echo "1. A database backup file. It's name should be {something}database{something else}.sql or .sql.gz.";
  echo "This is a mandatory file.";
  echo "2. Optional: A Public Files backup file. It's name should be {something}files{something else}.tar or .tar.gz.";
  echo "   It must *NOT* contain the string \"private-files\"!";
  echo "3. Optional: A Private Files backup file. It's name should be {something}private-files{something else}.tar or .tar.gz.";
  echo "Make sure you have the database file with a correct naming scheme at least, and restart the setup-restore process.";
  exit
 fi
 echo "db_backup=\"$get_backup_files\"" >> .env;
fi

if [ -f Dockerfile ]; then 
 docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .;
fi

docker compose -f pwd.yml up --force-recreate -d
sleep 2;

sed -i '/^create_site/d' .env
sed -i '/^db_backup/d' .env
