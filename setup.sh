#!/bin/bash


set -euo pipefail
shopt -s nullglob
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



append_env() {
    local key=$1
    local val=$2
    local esc_val
    esc_val=$(printf '%s' "$val" | sed 's/"/\\"/g')
    printf '%s="%s"\n' "$key" "$esc_val" >> .env
}


if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
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
 exit 0
fi
if [[ -n "${1:-}" && "${1}" != "-r" ]]; then
  echo "Usage: ./setup.sh [-r] [-h|--help]"
  exit 1
fi

container_name="${PWD##*/}"
if docker ps -a --format '{{.Names}}' | grep -Fxq "$container_name"; then
    create_site="no"
else
    create_site="yes"
fi
append_env "create_site" "$create_site"

if [[ "$create_site" == "yes" ]]; then
    read -r -p "Please enter port number [8080]: " port_num
    port_num=${port_num:-8080}
    if ! [[ "$port_num" =~ ^[0-9]+$ ]]; then
        echo "Invalid port number – must be digits only." >&2
        sed -i '/^create_site=/d' .env
        sed -i '/^db_backup=/d' .env
        sed -i '/^port_num=/d' .env
        exit 1
    fi
    append_env "port_num" "$port_num"
fi

if [[ "${1:-}" == "-r" ]]; then
 sed -i 's/#COPY/COPY/g' Containerfile
 db_backup=$(get_backup_files)
 if [[ "$db_backup" == "1" ]]; then
  echo "Backup selection aborted – you need up to three files." >&2
  sed -i '/^create_site=/d' .env
  sed -i '/^db_backup=/d' .env
  sed -i '/^port_num=/d' .env
  exit 1
 fi
 append_env "db_backup" "$db_backup"
fi

if [[ -f Containerfile ]]; then
    docker build \
        --build-arg CACHEBUST="$(date +%s)" \
        -t tmoney/accounting \
        -f Containerfile .
fi
docker compose -f pwd.yml up --force-recreate -d
service_name="${PWD##*/}-create-site-1"
until docker ps --format '{{.Names}} {{.Status}}' \
  | awk '{print $1,$2}' \
  | grep -E "^${service_name} (Up|Running)"; do
  echo "Waiting for ${service_name} to start..."
  sleep 1
done
sed -i '/^create_site=/d' .env
sed -i '/^db_backup=/d' .env
docker logs -f "$service_name"
