#!/usr/bin/shell

cat xiaxian.txt  |while read i
#cat noname.txt |while read i
do
    #echo $i
    project=`echo $i|awk '{print $2}'`
    alias=`echo $i|awk '{print $1}'`
    if test -z $project 
    then
        echo $i >> need_check.txt
    else
        if ! grep $project project_list.txt 2>&1 >/dev/null 
        #if ! grep $project asset.txt 2>&1 >/dev/null 
        then
            #echo $i >> need_check.txt
            echo $i >> n_c.txt
        else
            awk -v project=$project -v alias=$alias '{if( NF==3 && $3~project ) {print $0 "	" alias "	"project }}' project_list.txt
            #awk -v project=$project -v alias=$alias '{if( NF==3 && $3~project ) {print $0 "	" alias "	"project }}' asset.txt
            #grep $project asset.txt
        fi
    fi
done
