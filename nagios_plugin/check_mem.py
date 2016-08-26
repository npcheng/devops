#!/usr/local/bin/python2.7
#coding=utf-8   
import socket,time,sys,os,rrdtool
from optparse import OptionParser


critical_msg=""
warning_msg = ""
service_status={"ok":0, "warning":1, "critical":2, "unkown":3}
status = service_status['ok']
output= ""
rrd_dir =  "/data/rrdtool/RRD/"


def get_stats(stats_data):
    stats = {}
    stats_list = stats_data.split("\r\n")
    for stat in stats_list:
        stat_list= stat.split(" ")
        if stat_list[0] == "STAT":
            stats[stat_list[1]] = stat_list[2]
    stats['total_request'] = int(stats['cmd_get']) + int(stats['cmd_set']) + int(stats['delete_hits']) + int(stats['delete_misses'])
    return stats

def  create_rrd(rrd_dir, host, port):
    rrdtool.create(rrd_dir + host + "_" + port + "_mem_status.rrd",
           "--start", '-10s',
           "--step", "60",
           "DS:total_request:COUNTER:1800:0:U",
           "DS:get_request:COUNTER:1800:0:U",
           "DS:set_request:COUNTER:1800:0:U",
           "DS:total_mem:GAUGE:1800:0:U",
           "DS:used_mem:GAUGE:1800:0:U",
           "RRA:AVERAGE:0.5:1:360",
           "RRA:AVERAGE:0.5:5:288",
           "RRA:AVERAGE:0.5:30:336",
           "RRA:AVERAGE:0.5:120:372",
           "RRA:AVERAGE:0.5:1440:366",
           "RRA:AVERAGE:0.5:10080:262",
           "RRA:MAX:0.5:5:288",
           "RRA:MAX:0.5:30:336",
           "RRA:MAX:0.5:120:372",
           "RRA:MAX:0.5:1440:366",
           "RRA:MAX:0.5:10080:262",
           "RRA:MAX:0.5:10:228",
           "RRA:MIN:0.5:5:288",
           "RRA:MIN:0.5:30:336",
           "RRA:MIN:0.5:120:372",
           "RRA:MIN:0.5:1440:366",
           "RRA:MIN:0.5:10080:262",
            ) 

def update_rrd(rrd_dir, host, port, stats):
    port = str(port)
    if os.path.exists(rrd_dir + host + "_" + port + "_mem_status.rrd") == False:
        create_rrd(rrd_dir, host, port)

    rrdtool.update(rrd_dir + host + "_" + port + "_mem_status.rrd",
            '%s:%s:%s:%s:%s:%s' %(time.strftime("%s", time.localtime(time.time()-10)), str(stats['total_request']), str(stats['cmd_get']),
             str(stats['cmd_set']), str(stats['limit_maxbytes']), str(stats['bytes'])))


def ansys_stats(stats):
    global output
    global status
    global critical_msg
    get_ratio = 0
    #total_request  = stats['get']  
    if stats['uptime'] <  60 * 60 * 24:
        pass
    if stats['uptime'] < 60*60*24*7:
        pass
    
    #if int(stats['cmd_get']) !=0  or int(stats['get_hits']) != 0 :
    if int(stats['cmd_get']) !=0:
        get_ratio = ((float(stats['get_hits']) / int(stats['cmd_get']))) * 100

    mem_ratio = int(stats['bytes'])/float(stats['limit_maxbytes']) * 100

    if mem_ratio >=80 :
        if status != 2:
            status =2
        critical_msg = "%s, mem_ratio:%f%%" %(critical_msg, mem_ratio)

    if int(stats['bytes']) < 1024 * 1024:
        mem = int(stats['bytes']) / 1024
        used_mem  = "%dK" %mem
    else:
        mem = int(stats['bytes']) / 1024 / 1024
        used_mem  = "%dM" %mem
    total_mem = int(stats['limit_maxbytes'])/1024/1024
         
    output = "%s,avaible_mem:%dM, used_mem:%s, mem_ratio:%s%%, total_requst: %d, get_ratio:%f%%" %(output, total_mem, used_mem, mem_ratio, stats['total_request'], get_ratio )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="host", help="memcached server hostname/IP", default="127.0.0.1")
    parser.add_option("-P", "--port", dest="port", help="memcached server port(defaults to 11211)", default=11211)

    (options, args) = parser.parse_args()

    host = options.host
    port = int(options.port)

    try:
         s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         s.connect((host, port))
         cmd = "stats\n"
         s.sendall(cmd)
         data = s.recv(1024)
         s.close()
    except Exception, e:
        print e
        sys.exit(service_status["critical"])
        #sys.exit()
    stats = get_stats(data)
    ansys_stats(stats)
    update_rrd(rrd_dir, host, port, stats)
    print output
    #sys.exit(status)
