#!/usr/bin/shell

#cat xiaxian.txt  |while read i
cat noname_project_list.txt |while read i
do
    #echo $i
    project=`echo $i|awk '{print $2}'`
    alias=`echo $i|awk '{print $1}'`
    if test -z $project 
    then
        echo $i >> need_check.txt
    else
        #echo $project
        if ! grep $project haolinexport.txt 2>&1 >/dev/null 
        then
            #echo $i >> need_check.txt
            echo $project"	"$alias >> n_c.txt
        else
            #awk -v project=$project -v alias=$alias '{if( NF==3 && $3~project ) {print $0 "	" alias "	"project }}' asset.txt
            #awk -F, -v project=$project -v alias=$alias '{if( NF==3 && $1~project ) {print $0 "	" alias "	"project }}' haolinexport.txt
            awk -F, -v project=$project -v alias=$alias '{if( NF==3 && $1~project ) {print $0}}' haolinexport.txt
            #grep $project noname_check.txt
        fi
    fi
done
