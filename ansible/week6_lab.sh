#!/bin/env bash

BASE_CMD='ansible -i inventory.txt -b'

# Create user
create_user () {
    eval "$BASE_CMD $1 -m user -a 'name=$2 password=\$6\$RnOc8Sj/FjVSPDES\$AoPM5p7PB.bLVsoDS5dBzZEG5zzK5yzLJqIeVpBaymRMMs0rI6paSgydFn.HOaGaDVoWjXSbbPKN9TsGksUi6.'"
}

# Install package
install_pkg () {
    eval "$BASE_CMD $1 -m apt -a 'name=$2 state=present update_cache=yes'"
}

# Enable auto startup
auto_start () {
    eval "$BASE_CMD $1 -m systemd -a 'name=$2 state=started enabled=yes'"
}

# Web
create_user "web" "www"
install_pkg "web" "apache2"
auto_start  "web" "apache2.service"

# DB
create_user "db" "dba"
install_pkg "db" "mysql-server"
auto_start  "db" "mysql.service"