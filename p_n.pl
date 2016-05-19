#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

project_name = []
try:
    f = open('project.txt', 'r')
    f1 = open('project_name.txt')
    for line1 in f1.readlines():
        line1 = line1.strip("\r\n");
        lx= line1.split('\t')
        if len(lx) == 3:
            project_name.append(lx)
    #print(f.read())
    for line in f.readlines():
        line = line.strip("\r\n")
        sx=line.split(',')
        for  project_info in project_name:
            if sx[6] == project_info[1]:
                #print sx[6], project_info[1], project_info[1] , sx[2]
                match_str = re.match(project_info[1],sx[2])
                if match_str == None:
                      sx[3] = project_info[2]
                else:
                      print "xxx"
        for x in sx:
            print x +",",

        print 

       
        #print  sx[6],
        #for x in sx:
        #   print x
finally:
    if f:
        f.close()

#print project_name

