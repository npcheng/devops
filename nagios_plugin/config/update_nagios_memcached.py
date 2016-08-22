#!/usr/bin/python
import ansible.runner


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

def setup_service(memcache):
    try:
       fp = open("services.cfg", "a")
    except Exception, e:
       print e
    for key, value in memcache.items():
        if key == "mem":
             host = '10.249.169.202'
        for v in value:
            fp.write("define service {\n")
            fp.write("    use local-service\n")
            fp.write("    host_name  " + host.replace(".", "-") + "\n")
            fp.write("    service_description    memcached_"  + v + "\n")
            fp.write("    check_command  check_memcached!"  + v+ "\n")
            fp.write("    notifications_enabled    1\n")
            fp.write("}\n")
    fp.close()


def setup_hostgroup( hostgroup):
    if type(hostgroup) == "list":
        with open("hostgroups.cfg", "w") as fp:
            fp.write("define hostgroup{\r\n")
            fp.write("    hostgroup_name	jetty_instance\r\n")
            fp.write("    alias		jetty_instance\r\n")
            host_list = ",".join(hostgroup)
            fp.write("    members    host_list")
            fp.write("}\r\n")

        with open("hosts.cfg", "w") as fp:
            for host in hostgroup:
                fp.write("define host {\r\n")
                fp.write("   use linux-server\r\n")
                fp.write("   host_name %s\r\n" %host.replace(".", "-"))
                fp.write("   alias DB-C-1\r\n")
                fp.write("   address \r\n" %host)
                fp.write("}\r\n")
         


if __name__ == "__main__":
   host = "mem"
   memcached_info = {}
   results = run_ansible("ps axf| grep memcached | grep -v grep", host)
   for key, value in results.items():
       cmd_list = value['stdout'].split("\r\n")
       for ps_list in cmd_list:
           if len(ps_list) != 0 :
               ps = ps_list.split()
               if key  in memcached_info.keys():
                   memcached_info[key].append(ps[11])
               else:
                   memcached_info[key] = []
   with open("/data/django/pjcheck/memstat/memport.py", "w") as fp:
       mem_info = "mem_info = %s" %memcached_info
       fp.write(mem_info +"\r\n")
   fp.close()
   
   #setup_service(memcached_info)
