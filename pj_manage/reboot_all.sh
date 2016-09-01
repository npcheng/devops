jetty_dir=/data/webapp
jetty=`ls -l $jetty_dir| awk '{print $9}'| grep -v jetty-distri| grep -Eio ^jetty-.*| awk -F- '{print $2}'`
echo $jetty
for proc in $jetty 
do
    jj stop $proc; jj start $proc
done
