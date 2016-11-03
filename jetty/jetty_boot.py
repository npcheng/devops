#!/usr/bin/python

import os,commands,re,socket

def check_socket(ip,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
      sk.connect((ip,port))
      return 'connection success'
    except Exception:
      return 'connection fail'
    sk.close()

def jettyport_check(jetty_port):
    jetty_port = int(jetty_port)
    jettyport_status = check_socket('127.0.0.1',jetty_port)
    if jettyport_status == "connection success":
        return True
    else:
        return False




commands.getstatusoutput("grep  'jetty_autoboot' /etc/rc.d/rc.local ||  echo '/bin/sh /etc/rc.d/jetty_autoboot.sh' >> /etc/rc.d/rc.local")

jetty_dir="/data/webapp/"
#jetty_instance= [re.search("jetty-(.*)", x).group(1) for x in os.listdir(jetty_dir) if os.path.isdir(jetty_dir + x) and x != 'jetty-distribution-9.2.9.v20150224']
jetty_instance=[]
for x in os.listdir(jetty_dir):
    if os.path.isdir(jetty_dir + x) and x != 'jetty-distribution-9.2.9.v20150224':
        match = re.search("jetty-(.*)", x)
        if match:
           jetty_instance.append(match.group(1))
w_fp = open("/etc/rc.d/jetty_autoboot.sh", "w")

for instance in jetty_instance:
    try:
        fp = open(jetty_dir + "jetty-" +  instance + "/start.ini")
        for line in fp.readlines():
            line = line.strip();
            match = re.search("^jetty.port=(\d+)", line)
            if match:
                 port = match.group(1)
                 if jettyport_check(port) == True:
                      w_fp.write("/data/webapp/jetty-root.sh start " + instance +" 2>&1 >>/var/log/jetty_start.log\n");
                     
                 else:
                      w_fp.write("#/data/webapp/jetty-root.sh start " + instance +"\n");
                      print "Failed"
        fp.close()
    except Exception, e:
        print e

w_fp.close()

