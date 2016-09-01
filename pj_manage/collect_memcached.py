#!/usr/bin/python

import os
import time,datetime
import commands
memcached_cmd = os.popen('ps axf| grep memcached | grep -v grep| grep -v python').readlines()

mem_cmd = ""
backup_dir= "/data/backup/memcached"
memcached_file="/etc/rc.d/start_memcached.sh"


backup_file= "start_memcached.sh_" + time.strftime('%Y-%m-%d')

if os.path.isdir(backup_dir)==False:
   os.mkdir(backup_dir)
else:
   (status, output) = commands.getstatusoutput("cp -f " + memcached_file + " " + backup_dir +"/" + backup_file)
   print output 
   
fp= open(memcached_file, "w")
for  mem_process  in memcached_cmd:
   mem_process = mem_process.strip()
   for mem in mem_process.split()[4:]:
        mem_cmd += mem + " "
   fp.write(mem_cmd +"\n");
   mem_cmd = ""

fp.close()
   
