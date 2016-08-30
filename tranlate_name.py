#!/usr/bin/python
import os,time,re, urllib2
from shutil import copyfile

def tranlate_name():
    dav_dir = "/var/www/sync"
    url = "http://app70.s.weshaketv.com:9213/findSame/api/push?"
    for dirs, subdirs, files in os.walk(dav_dir):
        current_time = time.time()
        basename = os.path.basename(dirs)
        for _file in files:
           try:
               src_file= os.path.join(dirs, _file) 
               if not os.path.exists(src_file):
                   continue
               postfix = os.path.splitext(_file)[1]
               match = re.search("tmp", postfix)
               if match :
                   continue
               create_time = int(os.stat(src_file).st_mtime)
               delta_time =  create_time + 60 * 15
               mod = create_time % 2
               create_time -= mod
               create_time= time.localtime(create_time)
               fmt_time = time.strftime("%Y%m%d%H%M%S", create_time)
               request_param = "tvid=%s&filename=%s" %(basename, fmt_time)
               http_request =  url + request_param
               tm_file = fmt_time  + postfix 
               dst_file = os.path.join(dirs, tm_file)
               #if delta_time  <= current_time:
               #    os.remove(src_file)
               if not os.path.exists(dst_file):
                   print dst_file
                   copyfile(src_file, dst_file)
                   print http_request
                   #response = urllib2.urlopen(http_request)
                   #print response.read()
                   #with request.urlopen(http_request) as f:
                   #    print "go"
                   #    print  "status:%s %s" %(f.status, f.reason)
           except Exception , e:
               log(str(e))
               
def log(log):
    with open("/data/log/dav.log", "a") as fp:
        fp.write(log +"\n")              

def run():
    while True:
        time.sleep(0.1)
        tranlate_name()
    
if __name__ == "__main__":
    # do nothing
    run()
