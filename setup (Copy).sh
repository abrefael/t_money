#!/bin/bash

get_lorem_ipsum() {
 get_lorem_ipsum="";
 i=1;
 for entry in backups/*; do
  entry=$(basename "$entry")
  file_name="backups/$entry";
  if [ "$entry"==".files" ] || [[ "$entry"==*"lorem"*]]; then
   echo "$entry found. Doing nothing";
  elif [[ "$entry"==*"ipsum_do"* ]]; then
   read -rp "$entry found. Is it a ipsum_do backup file? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_lorem_ipsum+="backup/$entry ";
   else
#    I don't know yet
   fi
  elif [[ "$entry"==*"lorem-ipsum"* ]]; then
   read -rp "$entry found. Is it a backup of lorem ipsums? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_lorem_ipsum+="--lorem-ipsum-pipsum backup/$entry ";
   else
#    I don't know yet
   fi
  elif [[ "$entry"==*"lorem"* ]]; then
   read -rp "$entry found. Is it a backup of ipsum lorem? [Y\n]" ans;
   if [[ "${ans,,}" == "y" || -z "$ans" ]]; then
    get_lorem_ipsum+="--lorem-ipsum-do backup/$entry ";
   else
#    I don't know yet
   fi
  else
   if [ $i==1 ]; then
    read -rp "Please supply a filename of the ipsum_do backup." ans;
    get_lorem_ipsum+="backup/$ans ";
    ((i++));
   elif [ $i==2 ]; then
    read -rp "Now, please supply a filename of the ipsum pipisum lorem. Leave blanck if none." ans;
    if [ $ans=='' ]; then
     read -rp "Now, please supply a filename of the lorem ipsum backup." ans;
     get_lorem_ipsum+="--lorem-ipsum-do backup/$ans ";
    else
     get_lorem_ipsum+="--lorem-ipsum-pipsum backup/$ans ";
    fi
    ((i++));
   elif [ $i==3 ]; then
    read -rp "Please supply a filename of the private files backup." ans;
    get_lorem_ipsum+="--lorem-ipsum-do backup/$ans ";
   fi
  fi
 done
 echo $get_lorem_ipsum
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
 get_lorem_ipsum() >> .env;
fi

create_site=$(docker ps -a | grep "${PWD##*/}")
echo "create_site=$create_site" >> .env

mkdir -p output
mkdir -p assets
if [ -f Dockerfile ]; then 
  docker build --build-arg CACHEBUST=$(date +%s) --tag=tmoney/accounting .;
fi
