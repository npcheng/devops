#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

db = MySQLdb.connect("127.0.0.1","root","","project_list" ,charset="utf8" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
# SQL 查询语句
sql = "select project_title, project_info, project_name from pj_list" 
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
except:
   print "Error: unable to fecth data"
print results
for row in results:
   title = row[0]
   info = row[1]
   name = row[2]
   # 打印结果
   print "%s,%s,%s" %(title, info, name)

# 关闭数据库连接
db.close()
