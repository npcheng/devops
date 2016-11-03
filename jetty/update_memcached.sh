

update_mem(){
sed  "s/^memcache.address=.*/memcache.address=$1:$2/" $3
}

#update_mem "10.66.124.212", 9191, "/data/webapp/jetty-ronghe3_api/webapps/ronghe3_api/WEB-INF/classes/config/setup.properties"
if  [ $# -ne 3 ];then
    echo "param not match"
else
    echo "xxx"
    update_mem  $1 $2 "/root/setup.properties"
fi
