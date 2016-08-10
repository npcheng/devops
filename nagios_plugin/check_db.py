#!/usr/local/bin/python2.7
import MySQLdb ,re,datetime,time,rrdtool,os,sys,argparse
import config

critical_msg=""
warning_msg = ""
service_status={"ok":0, "warning":1, "critical":2, "unkown":3}
status = service_status['ok']
output= ""
rrd_dir =  "/data/rrdtool/RRD/"

def get_mysqlstatus(db_host):
    global status
    global output
    connection1 = 0.0
    slow_queries1 = 0.0
    com_select1 = 0
    com_update1 = 0
    com_delete1 = 0
    com_insert1 = 0
    com_questions1 = 0
    valid_count = 1
    sql='show global status where Variable_name in (\
        "Connections", \
        "Slow_queries", \
        "Qcache_hits",\
        "Qcache_inserts", \
        "Qcache_lowmem_prunes", \
        "Qcache_not_cached", \
        "Queries", \
        "Questions", \
        "Com_select", \
        "Com_insert", \
        "Com_update", \
        "Com_delete", \
        "Table_locks_waited", \
        "Uptime" \
         )';
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[0] == "Slow_queries":
                slow_queries = row[1]
            if row[0] == "Connections":
                connection = row[1]
            if row[0] == "Com_update":
                com_update = row[1]
            if row[0] == "Com_select":
                com_select= row[1]
            if row[0] == "Com_delete":
                com_delete= row[1]
            if row[0] == "Com_insert":
                com_insert= row[1]
            if row[0] == "Questions":
                questions = row[1]

        if os.path.exists(rrd_dir + host + "_mysql_status.rrd"):
            rrdtool.update(rrd_dir + host + "_mysql_status.rrd",
                           '%s:%s:%s:%s:%s:%s:%s:%s' %(time.strftime("%s", time.localtime(time.time()-10)), str(connection), str(slow_queries),
                                                       str(com_select), str(com_insert), str(com_update), str(com_delete), str(questions))
                         )
            (start , ds , data)= rrdtool.fetch(rrd_dir + host + "_mysql_status.rrd",
                          "AVERAGE", "-s", "-300s"
                    )
            for row in data:
                if row[0] != None:
                    connection1 +=  row[0]
                    slow_queries1 +=  row[1]
                    com_select1 +=  row[2]
                    com_insert1 +=  row[3]
                    com_update1 +=  row[4]
                    com_delete1 +=  row[5]
                    com_questions1 +=  row[6]
                    valid_count += 1
            slow_queries1 = slow_queries1/valid_count
            connection1 = connection1/valid_count
            com_select1 = com_select1/valid_count
            com_insert1 = com_insert1/valid_count
            com_update1 = com_update1/valid_count
            com_delete1 = com_delete1/valid_count
            com_questions1 = com_questions1/valid_count
            output += "slow_queries1:%f, connection1:%f, select:%f, insert:%f, update:%f, delete:%f, questions:%f" %(slow_queries1,
                                                         connection1, com_select1, com_insert1, com_update1, com_delete1, com_questions1)
            output += "connection:%s" %connection
            output += "slow_query:%s" %slow_queries
            if slow_queries1 > 100:
                output += "too many slow_queries"
                status = service_status['critical']
            if connection1 > 500:
                output += "too many connections"
                status = service_status['critical']
        else:
            rrdtool.create(rrd_dir + host + "_mysql_status.rrd",
                           "--start", '-10s',
                           "--step", "60",
                           "DS:connections:COUNTER:1800:0:U",
                           "DS:slow_queries:COUNTER:1800:0:U",
                           "DS:com_select:COUNTER:1800:0:U",
                           "DS:com_insert:COUNTER:1800:0:U",
                           "DS:com_update:COUNTER:1800:0:U",
                           "DS:com_delete:COUNTER:1800:0:U",
                           "DS:Questions:COUNTER:1800:0:U",
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
                
    except Exception, e:
        print e

def get_mysqlconfig(db_host):
    global status,output
    sql= 'show variables where Variable_name in ( \
          "sync_binlog", \
          "max_connections", \
          "max_user_connections", \
          "max_user_connections", \
          "max_connect_errors", \
          "table_open_cache",\
          "table_definition_cache", \
          "thread_cache_size", \
          "binlog_format", \
          "open_files_limit", \
          "max_binlog_size", \
          "max_binlog_cache_size" \
          )'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            #content += 
            if row[0] == 'max_connections':
                output += "max_connections: %s" %row[1]
                if row[1] < '2000':
                    print  "max_connections little %s" %row[1]
                    status = service_status['critical']
    except Exception , e:
        print e
    
#def get_Slowqueries():
if __name__ == "__main__":
    #dbname =  'project_list'
    output = ""
    dbname =  ''
    """
    if (len(sys.argv) != 2):
       print "param wrong"
       sys.exit(service_status["warning"])
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='add project', type=str)
    arg = parser.parse_args()
    if (arg.host != None):
        try:
            db_host = arg.host
            user= config.db_config[db_host]["user_name"]
            password = config.db_config[db_host]["passwd"]
            host = config.db_config[db_host]["host"]
        except Exception,e:
            print e
            exit()
    try:
        db = MySQLdb.connect(host, user, password, dbname, charset="utf8")
        cursor = db.cursor()
        dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_mysqlconfig(host)
        get_mysqlstatus(host)
        print output
        cursor.close()
        db.close()
        exit(status)
    except Exception,e:
        print e
        sys.exit(service_status["warning"])
