# -*- coding: utf-8 -*-
#from __future__ import print_function
import urllib
import httplib2
import json
import sys,os,config
import yaml,argparse


class  wyInventory(object):
    def __init__(self):
        self._tengine_config = config.group_vars

    def get_host(self, project):
        http = httplib2.Http()
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'npcheng'
                }
        try:
            response, content = http.request(config.api_url, headers=headers)
            if response.status == 200:
                project_url = urllib.urlopen(config.api_url).read()
                project_en = json.loads(project_url)
            else:
                print "API not avaiable"
                sys.exit(1)
        except Exception, e:
            print( e )
            sys.exit(1)

        #加载project配置文件
        try:
            f_read = open(self._tengine_config, "r")
            var_content = yaml.safe_load(f_read.read())
            f_read.close()
        except Exception, e:
            print "can't open the file"
            var_content=[]

        for project_list in project_en:
            project_domain = project_en[project_list]["project_domain"]
            if " " in project_domain:
                domain =  project_domain.split(" ")[0]
            else:
                domain = project_domain
            if os.path.exists(config.template_path + domain +".conf.j2"):
                project_en[project_list]["template_file"]=[{"src": domain + ".conf.j2" ,
                             "dest": domain + ".conf"}]
            else:
                project_en[project_list]["template_file"]= [{"src": "standard.conf.j2" ,
                             "dest":  domain + ".conf"}]

            project_en[project_list]["log_file"] = domain


       #更新hosts文件
        try:
            f=open(config.ansible_hosts, "w")
        except BaseException, e:
            print e
            exit()

        for k, v in project_en.items():
            f.write("[" +k + "]\n")
            for ip in v["ip"]:
                if ip != None:
                    f.write(ip +"\n")
        f.close()


        #更新group/all
        try:
            f = open(self._tengine_config, "w")
        except Exception, e:
            print(e)
        finally:
            print("success")
        yaml.safe_dump(project_en[project], f, default_flow_style=False )
        f.close()

    def gen_playbook(self, project, action):
        if action not in ["add", "del"]:
            print "action not support"
            exit(1)
        if action == "add":
            playbook_role = "tengine_config"
        else:
            playbook_role = "tengine_config_del"

        playbook = [{"hosts": project,"gather_facts": "no",
                     "roles":[playbook_role]
                     }]
        try:
            f = open(config.playbook_path, "w+")
        except Exception,e:
            print e

        print yaml.safe_dump(playbook, default_flow_style=False)
        yaml.safe_dump(playbook, f,default_flow_style=False)
        f.close()



    def gen_init_script(self, project):
        #
        try:
            f=open(config.shell_file, "w")
        except BaseException, e:
            print e
            exit()

        f.write("ansible-playbook -i /data/ansible/ansible_hosts go.yml")
        f.close()

def install_phpenv(project):
    try:
        f= open(config.install_script, "w")
    except Exception, e:
        print e
        exit();

    # copy to install_script to remote server
    f.write("ansible -i /data/ansible/ansible_hosts " + project + " -m copy -a \"src=/data/ansible/shell/setup_lnmp.sh dest=/root\"\n")
    f.write("ansible -i /data/ansible/ansible_hosts " + project + " -m copy -a \"src=/data/ansible/shell/setup_lnmp.sh dest=/root\"\n")
    f.write("ansible -i /data/ansible/ansible_hosts " + project + " -m copy -a \"src=/data/ansible/resource/pkg.tar.gz dest=/root\"\n")
    f.write("ansible -i /data/ansible/ansible_hosts " + project + " -m shell -a \"sh /root/setup_lnmp.sh\"\n")
    f.write("rm -f $0\n");
    # run script
    #f.write
    f.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', help='add project', type=str)
    parser.add_argument('-d', '--delete', help='delete project', type=str)
    parser.add_argument('-i', '--install', help='install php env', type=str)

    arg = parser.parse_args()
    inventory = wyInventory()
    if arg.add !=None:
        inventory.get_host(arg.add)
        inventory.gen_playbook(arg.add, "add")
        inventory.gen_init_script(arg.add)

    elif arg.delete != None and arg.add == None :
        inventory.get_host(arg.delete)
        inventory.gen_playbook(arg.delete, "del")
        inventory.gen_init_script(arg.delete)
    elif  arg.install !=None and arg.delete == None:
        inventory.get_host(arg.install)
        install_phpenv(arg.install)
    else:
        print "亲再试试吧!"
        exit()

