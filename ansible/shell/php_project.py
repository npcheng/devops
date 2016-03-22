import urllib
import json

project_url = urllib.urlopen("http://asset.wxshake.com/api/project/project").read()
project_en = json.loads(project_url);
for project_list in project_en:
        print project_list
