#/usr/bin/python

import commands,os
import re
webapp_dir="/data/webapp/"

def get_project(project_dir):
    
    for x in os.listdir(project_dir):
       backup_project(project_dir + x, x)

def backup_project(project_path,  project_name):
    print project_path
    os.chdir(project_path)
    status = commands.getstatusoutput("jar -cvfM0 " +  project_name +".war * 2>&1 >/dev/null")
    if status[0] == 0 :
       #copy project to /data/backup/
       st = commands.getstatusoutput("mv " + project_name +".war " + backup_dir)
       if st[0] == 0:
           print "backup success"
       

backup_dir="/data/backup/warbackup"
if not  os.path.exists(backup_dir):
    os.makedirs(backup_dir)
a = [x for x in os.listdir(webapp_dir) if os.path.isdir(webapp_dir + x)]
for project in a:
    match = re.search(r"^jetty-(.*)", project)
    if match:
        dis_match = re.search(r"distribution-.*", match.group(1))
        if not dis_match:
             pro_dir = webapp_dir + "jetty-" + match.group(1)+"/webapps/"
             if os.path.exists(pro_dir):
                 get_project(pro_dir)
             else:
                 print "project dir is not exists"

