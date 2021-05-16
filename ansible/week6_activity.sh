#!/bin/env bash

# Apt update and install Ansible
sudo apt-get -q update && sudo apt-get -qy install ansible sshpass

# Write inventory.txt https://linuxize.com/post/bash-write-to-file/#writing-to-a-file-using-redirection-operators
cat << EOF > inventory.txt
[all]
csr1    ansible_host=192.168.0.11
csr2    ansbile_host=192.168.0.12
web1    ansible_host=192.168.0.111
web2    ansible_host=192.168.0.112
db1     ansible_host=192.168.0.121
db2     ansible_host=192.168.0.122

[all:vars]
ansible_ssh_extra_args='-o StrictHostKeyChecking=no'

[csr]
csr1
csr2

[linux]
web1
web2
db1
db2

[web]
web1
web2

[db]
db1
db2
EOF

# Testing ad-hoc commans 
echo Pinging all Linux machines
ansible -i inventory.txt linux -m ping -k

# Upgrade to use SSH public key and save me the headache of typing password
echo SSH Public Key!!!
ssh-keygen -q -t ed25519 -f ansible -N "" -C ""     # Generate one for ansible only
# ssh-agent bash      # Start up ssh-agent. It should be up already if using a DM
ssh-add ./ansible     # Add key to ssh-agent
SSH_PUBLIC_KEY=$(cat ansible.pub)      # Load SSH public key to env var

# ansible -i inventory.txt linux -m authorized_key -a "key=$SSH_PUBLIC_KEY" -k   # Upload key via Ansible
ansible -i inventory.txt linux -m file -a "mode=600 dest=/home/justincase/.ssh/authorized_keys state=touch" -k      # Create an empty file for storing ssh keys that only justincase can read and modify
ansible -i inventory.txt linux -a "echo $SSH_PUBLIC_KEY >> /home/justincase/.ssh/authorized_keys" -k                # Write the ssh key with command module

# Login again to see if password needed
ansible -i inventory.txt linux -m ping 
