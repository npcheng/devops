#!/usr/bin/python
import ansible.runner, re, shutil, commands,os
import config
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def run_ansible(cmd, group):
    if isinstance(group,int):
        group = str(group)
    run= ansible.runner.Runner(
            module_name = 'raw',
            module_args = cmd,
            host_list= "/etc/ansible/hosts",
            pattern = group ,
    )
    ret = run.run()
    return ret['contacted']

def setup_memservice(memhost):
    global result
    memcache = {}
    if type(memhost) == list:
        for host in memhost:
            results = run_ansible("ps axf| grep memcached | grep -v grep", host)
            for key, value in results.items():
                print value['rc']
                cmd_list = value['stdout'].split("\r\n")
                for ps_list in cmd_list:
                    if len(ps_list) != 0 :
                        ps = ps_list.split()
                        if key  in memcache.keys():
                            memcache[key].append(ps[11])
                        else:
                            memcache[key] = []
    else:
        result = False
    try:
       fp = open("services.cfg", "a")
    except Exception, e:
       print e
    for key, value in memcache.items():
        host = get_ipaddr(key)
        if host == False:
            result = False
            break 
        for v in value:
            fp.write("define service {\n")
            fp.write("    use local-service\n")
            fp.write("    host_name  " + host.replace(".", "-") + "\n")
            fp.write("    service_description    memcached_"  + v + "\n")
            fp.write("    check_command  check_memcached!"  + v+ "\n")
            fp.write("    notifications_enabled    1\n")
            fp.write("}\n")
    fp.close()
    if result != False:
        result = True

def setup_dbservice(dbhost):
    global result 
    with open("services.cfg", "w") as fp:
       for ipaddr, hostname in dbhost.items():
           fp.write("define service {\n")
           fp.write("    use local-service\n")
           fp.write("    host_name %s\n" %ipaddr.replace(".", "-"))
           fp.write("    service_description check_mysqlstatus\n")
           fp.write("    check_command  check_mysql\n")
           fp.write("    notifications_enabled    1\n")
           fp.write("}\n")
    fp.close()

def dict_key_value(dbdict):
    host= {}
    for key, value in dbdict.items():
         host[value['host']] = key
    return host       

def get_ipaddr(host):
    with open("/etc/hosts", "r") as fp:
        for line in fp.readlines():
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+" + host, line)
            if match:
                return match.group(1)
        return False
            
def setup_hostgroup( hostgroup):
    global result
    if type(hostgroup) == list:
        with open("hostgroups.cfg", "w") as fp:
            fp.write("define hostgroup{\r\n")
            fp.write("    hostgroup_name	jetty_instance\r\n")
            fp.write("    alias		jetty_instance\r\n")
            host_list = ",".join(hostgroup)
            fp.write("    members    %s\n" %host_list.replace(".", "-"))
            fp.write("}\r\n")
        result = True

        with open("hosts.cfg", "w") as fp:
            for host in hostgroup:
                fp.write("define host {\r\n")
                fp.write("   use linux-server\r\n")
                fp.write("   host_name %s\r\n" %host.replace(".", "-"))
                fp.write("   alias %s\r\n" %db_dict[host])
                fp.write("   address %s\r\n" %host)
                fp.write("}\r\n")
        result = True
    else:
        result = False



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def sendmail(result):
    sender ="nagios@localhost"
    recevier = ["xxx@xxx.com"]
    message = MIMEText(result, 'plain', 'utf-8')
    message['From'] = _format_addr("%s" %sender)
    message['To'] =  _format_addr("%s" %recevier[0])
    message['Subject'] = Header("nagios problem", "utf-8").encode()
    try:
        server = smtplib.SMTP("localhost", 25)
        server.sendmail(sender, recevier, message.as_string())
        print "sendmail success"
    except smtplib.SMTPException:
        print "sendmail failed"
if __name__ == "__main__":
    ret = False
    host = ["mem"]
    hostgroup = []
    src_dir = "/root/xxx"
    dst_dir = "/etc/nagios/objects"
    for ipaddr in host:
        ip= get_ipaddr(ipaddr)
        if ipaddr != False:
            hostgroup.append(ip)
    for key, value in config.db_config.items():
        if value['host'] not in hostgroup:
            hostgroup.append(value['host'])
    db_dict = dict_key_value(config.db_config)
    setup_hostgroup(hostgroup)
    setup_dbservice(db_dict)
    setup_memservice(host)

    #copy file 
    nagios_file = ['services.cfg', 'hosts.cfg', 'hostgroups.cfg']

    for cfg in nagios_file:
        try:
            shutil.move( os.path.join(src_dir, cfg), os.path.join(dst_dir, cfg) )
        except Exception, e:
            print e

    #check nagios file
    (status, output) = commands.getstatusoutput("nagios -v /etc/nagios/nagios.cfg")
    if status == 0 :
        commands.getstatusoutput("/etc/init.d/nagios restart")
    else:
        sendmail(output)
