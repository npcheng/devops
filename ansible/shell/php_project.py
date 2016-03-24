import urllib
import json

project_url = urllib.urlopen("http://asset.wxshake.com/api/project/project").read()
project_en = json.loads(project_url);

for project_list in project_en:
        if not project_list:
		print "this project not exist"
		exit()
	print project_list
