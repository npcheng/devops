#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import sys,os 
import time
import pexpect
import xlrd


def ssh_login(ip):
    cmd = '/usr/bin/ssh -l admin ' + ip
    print cmd
    child = pexpect.spawn(cmd)
    index = child.expect(["yes/no", "password" ])
    if i == 2:
        print "Time out"
        return None
    if index == 0 :
        child.sendline("yes")
        child.expect("password:")
        child.sendline(passwd)
    if index == 1 :
        print passwd
        time.sleep(1)
        child.sendline(passwd)
        time.sleep(1)
    child.sendline("system-view")
    return  child

def S3600V2_28TP_command(ssh_hd):
    scheme_list =["radius scheme neiwang",
               "server-type extended",
               "primary authentication 10.2.21.33 key cipher $c$3$X6HnhI1HkClFRY086noxdpvblaMQusjHTGig",
               "user-name-format without-domain",
              ]
    domain_list =["domain neiwang",
                  "authentication login radius-scheme neiwang local",
                  "authorization login radius-scheme neiwang local"
            ]
    for item in scheme_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)

    ssh_hd.sendline("quit")

    for item in domain_list:
        ssh_hd.sendline(item)
        time.sleep(1)

    ssh_hd.sendline("quit")
    ssh_hd.sendline("domain default enable neiwang")
    ssh_hd.sendline("quit")
    ssh_hd.sendline("save")
    ssh_hd.sendline("y")
    ssh_hd.send("\n")
    ssh_hd.sendline("y")
    time.sleep(5)
    ssh_hd.sendline("quit")

def S5100_48P_EI_command(ssh_hd):
    scheme_list =["radius scheme neiwang",
                "server-type extended",
                "server-type huawei",
                "primary authentication 10.2.21.33",
                "key authentication Pof7UcBD",
                "timer response-timeout 1",
                "user-name-format without-domain"
              ]
    domain_list =["domain neiwang",
                "scheme radius-scheme neiwang local",
                "authentication radius-scheme neiwang local",
                "accounting optional"
            ]
    save_list = ["save","y",""]

    for item in scheme_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)

    ssh_hd.sendline("quit")

    for item in domain_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)

    ssh_hd.sendline("quit")
    ssh_hd.sendline("domain default enable neiwang")
    ssh_hd.sendline("ssh authentication-type default all")
    ssh_hd.sendline("quit")

    for item in save_list:
        ssh_hd.sendline(item)
        time.sleep(1)

    time.sleep(5)
    ssh_hd.sendline("quit")

def S5700_command(ssh_hd):
    scheme_list =["radius-server template neiwang",
                "radius-server shared-key cipher Pof7UcBD",
                "radius-server authentication 10.2.21.33 1812",
                "aaa",
                "authentication-scheme neiwang",
                "authentication-mode radius local"
                ]
    domain_list =["domain default",
                "authentication-scheme neiwang",
                "radius-server  neiwang",
                "quit","domain default admin"
            ]
    save_list = ["save","y",""]


    for item in scheme_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)

    ssh_hd.sendline("quit")

    for item in domain_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)
    ssh_hd.sendline("quit")

    for item in save_list:
        ssh_hd.sendline(item)
        print item
        time.sleep(1)
      
passwd = "duduadmin"
excel = xlrd.open_workbook('neiwang-20140506.xls')
table = excel.sheets()[1]
nrows = table.nrows
ncols = table.ncols
print nrows 

for i in range(nrows):
    sw_type = table.cell(i,2).value
    sw_ipaddr = table.cell(i,1).value.strip()
#    print sw_type + sw_ipaddr
    if (sw_type == 'S3600V2-28TP' or  sw_type =='S3600V2-52TP' or sw_type == 'S3600V2-53TP' or sw_type =="S3600V2-28TP-PWR-EI" or sw_type == 'S3600V2-52TP-PWR-EI'):
        continue
        child = ssh_login(sw_ipaddr)
        if (child != None):
            print sw_ipaddr
            index = child.expect(['>', ']'])
            if index == 0:
                child.sendline("system-view")
            S3600V2_28TP_command(child)
    #if sw_type == 'S5100-48P-EI' and sw_ipaddr != '172.23.200.9':
    if sw_type == 'S5100-48P-EI':
#        continue
        child = ssh_login(sw_ipaddr)
        if (child != None):
            print sw_ipaddr
            index = child.expect(['>', ']'])
            if index == 0:
                child.sendline("system-view")
            
            #child.sendline("domain default enable system")
            #child.sendline('quit')
            #child.sendline('quit')
            S5100_48P_EI_command(child)
    if (sw_type == 'S5700-52C-SI' or sw_type == "S5700-53C-SI"):
        continue
        print sw_ipaddr
        child = ssh_login(sw_ipaddr)
        if (child != None):
            print sw_ipaddr
            index = child.expect(['>', ']'])
            if index == 0:
                child.sendline("system-view")
            S5700_command(child)
