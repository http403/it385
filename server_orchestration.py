#!/bin/env python3

import pexpect
from pexpect import spawn as Spawn
import sys
import time

PROMPT = 'PROMPT#> '   # The universal prompt for easy expect

login_user = 'justincase'
login_pass = 'Password01'

web_user = 'www'
web_pass = 'SecurePass01'

db_user = 'dba'
db_pass = 'SecurePass01'

hosts = {
    "web": ['192.168.0.111', '192.168.0.112'],
    "db": ['192.168.0.121', '192.168.0.122']
}


def set_prompt(m: Spawn):
    time.sleep(2)  # Wait a bit to compensate the missing expect
    m.sendline(f"PS1='{PROMPT}'")


def useradd(m: Spawn, user: str, passwd: str):
    global PROMPT

    m.expect_exact(PROMPT)
    m.sendline(f'useradd {user}')

    m.expect_exact(PROMPT)
    m.sendline(f'passwd {user}')
    m.expect('password')
    m.sendline(passwd)
    m.expect('Retype')
    m.sendline(passwd)


def priv_escalation(m: Spawn):
    global PROMPT

    m.expect_exact(PROMPT)
    m.sendline('sudo su -')
    m.expect('password')
    m.sendline(login_pass)

    time.sleep(2)   # wait a bit
    set_prompt(m)   # Set it again in case the PS1 changed


def basic_setup(m: Spawn):
    global PROMPT

    # login
    m.expect('password')
    time.sleep(0.2)     # So the password won't get printed
    m.sendline(login_pass)

    # set prompt
    set_prompt(m)

    # escalate privilege
    priv_escalation(m)

    # update repo
    m.expect_exact(PROMPT)
    m.sendline('apt-get -q update')


def web_orchestration(hosts: list):
    global PROMPT

    for host in hosts:
        # create client
        client = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {login_user}@{host}', timeout=60)
        client.logfile = sys.stderr.buffer

        # get the foundation set
        basic_setup(client)

        # # validation: leave a test file
        # client.expect_exact(PROMPT)
        # client.sendline('whoami >> iwashere.txt')
        # client.expect_exact(PROMPT)
        # client.sendline('date >> iwashere.txt')

        # add user
        useradd(client, web_user, web_pass)

        # install apache2
        client.expect_exact(PROMPT)
        client.sendline('apt-get install -qy apache2')

        # start service
        client.expect_exact(PROMPT, timeout=120)    # wait a bit in case apache2 took longer time to install
        client.sendline('systemctl start apache2.service')

        # enable auto start
        client.expect_exact(PROMPT)
        client.sendline('systemctl enable apache2.service')

        # close the connection
        client.expect_exact(PROMPT)  # wait until the last command finish
        client.close()


def db_orchestration(hosts: list):
    global PROMPT

    for host in hosts:
        # create client
        client = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {login_user}@{host}')
        client.logfile = sys.stderr.buffer

        # get the foundation set
        basic_setup(client)

        # add user
        useradd(client, db_user, db_pass)

        # install mysql server
        client.expect_exact(PROMPT)
        client.sendline('apt-get install -qy mysql-server')

        # start service
        client.expect_exact(PROMPT, timeout=180)  # wait a bit in case mysql took longer time to install
        client.sendline('systemctl start mysql.service')

        # enable auto start
        client.expect_exact(PROMPT)
        client.sendline('systemctl enable mysql.service')

        # close the connection
        client.expect_exact(PROMPT)  # wait until the last command finish
        client.close()


if __name__ == '__main__':
    web_orchestration(hosts['web'])
    db_orchestration(hosts['db'])
