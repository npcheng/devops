# -*- coding: utf-8 -*-
#from __future__ import print_function
import urllib
import httplib2
import json
import sys,os,config
import yaml


class  wyInventory(object):
    def __init__(self):
        self._ansbile_host = "/data/ansible/ansible_host_bak"
        self._tengine_config = "/data/ansible/roles/tengine_config/vars"

    def get_host(self):
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
            print( e)
            sys.exit(1)
        try:
            f = open(self._ansbile_host, "w")
        except Exception, e:
            print(e)
        finally:
            print("success")
        print( project_en)

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
        print yaml.safe_dump(project_en, default_flow_style=False)
        yaml.safe_dump(project_en, f, default_flow_style=False )
        f.close()

    def gen_playbook(self):
        pass

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', help='add project', type=str)
    parser.add_argument('-d', '--delete', help='delete project', type=str)

    arg = parser.parse_args()

    if arg.add !=None:
        pass
    elif arg.del != None and arg.add == None :
        pass
    else:
        pass  
