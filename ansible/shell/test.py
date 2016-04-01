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
            'User-Agent': 'xxx'
                }
        url="http://asset.wxshake.com/api/project/project"
        try:
            response, content = http.request(url, headers=headers)
            if response.status == 200:
                project_url = urllib.urlopen("http://asset.wxshake.com/api/project/project").read()
                project_en = json.loads(project_url)
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

#        output_content =  yaml.safe_dump(project_en, default_flow_style=False)

#        if var_content == project_en:
#            return


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

        f.write("ansible-playbook -i /data/ansible/ansible_hosts go.yml")
        f.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', help='add project', type=str)
    parser.add_argument('-d', '--delete', help='delete project', type=str)

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
    else:
        print "亲再试试吧!"
        exit()


