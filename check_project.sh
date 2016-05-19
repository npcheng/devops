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
        if ! grep $project noname_check.txt 2>&1 >/dev/null 
        then
            echo $i >> need_check.txt
            echo $project"	"$alias >> n_c.txt
        else
            #awk -v project=$project -v alias=$alias '{if( NF==3 && $3~project ) {print $0 "	" alias "	"project }}' asset.txt
            awk -v project=$project -v alias=$alias '{if( NF==2 && $2~project ) {print $0 "	" alias "	"project }}' noname_check.txt
            #grep $project noname_check.txt
        fi
    fi
done
