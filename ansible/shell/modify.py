#!/usr/local/bin/python

"""
---
template_file:
 - {src: asset.wxshake.com.conf.j2, dest: asset.wxshake.com.conf}

project_domain: tvodsapi.s.weshake.com
root_path: /data/www/weiyao_tvods
log_path: /data/logs/nginx

"""
import os
import config

def add_new_project(base_root_path, base_log_path):

    domain = raw_input("input domain:")
    if domain == '':
        print "please input domain"
        exit()
    if " " in domain:
        first_domain =  domain.split(" ")[0]
        if os.path.exists(config.template_path + first_domain +".conf.j2"):
            template_src=first_domin + ".conf.j2"
        else:
            template_src="standard.conf.j2"

        template_dest=first_domain +".conf"
        root_path = base_root_path + first_domain
        log_path = base_log_path + first_domain
    else:
        if os.path.exists(config.template_path + domain +"conf.j2"):
            template_src = domain + "conf.j2"
        else:
            template_src = "standard.conf.j2"

        template_dest = domain +".conf"
        root_path = base_root_path + domain
        log_path = base_log_path + domain
    return root_path, log_path, domain, template_src, template_dest

def write_ansible_config(yaml_List):
    (root_path, log_path, domain, template_src, template_dest) = yaml_List
    with open("/data/ansible/roles/tengine_config/vars/main.yml", "w") as f:
        f.write("---\n")
        f.write("template_file:\n")
        f.write(" - {src: " +template_src +", dest: " +template_dest+"}\n")
        f.write("root_path: " + root_path +"\n")
        f.write("log_path: " + log_path + "\n")
        f.write("project_domain: " + domain + "\n")
    f.close()

if __name__=="__main__":
    parm_list = add_new_project(config.base_root_path, config.base_log_path)
    write_ansible_config(parm_list)

