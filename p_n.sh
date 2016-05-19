#!/usr/bin/shell

#cat xiaxian.txt  |while read i
cat project_name.txt |while read i
do
    #echo $i
    project=`echo $i|awk '{print $2}'`
    gc=`echo $i|awk '{print $1}'`
    name=`echo $i|awk '{if (NF==3){print $3}else{print "NULL"}}'`
    echo $name
#    if test -z $project 
#    then
#        echo $i >> need_check.txt
#    else
#        if ! grep $project noname_check.txt 2>&1 >/dev/null 
#        then
#            echo $i >> need_check.txt
#            echo $project"	"$alias >> n_c.txt
#        else
#            #awk -v project=$project -v alias=$alias '{if( NF==3 && $3~project ) {print $0 "	" alias "	"project }}' asset.txt
#            awk -v project=$project -v alias=$alias '{if( NF==2 && $2~project ) {print $0 "	" alias "	"project }}' noname_check.txt
#            #grep $project noname_check.txt
#        fi
#    fi
done
