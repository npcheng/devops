#!/usr/bin/bash

tengine_dir=/data/tengine
tengine_config=/data/tengine/conf
crtfile=1__.s.weshaketv.com_bundle.crt
keyfile=2__.s.weshaketv.com.key


##copy ssl key and cert into config dir
add_ssl(){
if [ ! -d $tengine_config/ssl ];then
    echo "mkdir ssl"
    mkdir  -p $tengine_config/ssl
fi

if [ ! -f  $tengine_config/ssl/$crtfile ]  ;then
    echo "download certfile"
fi
if [ ! -f $tengine_config/ssl/$keyfile ] ; then
    echo "download keyfile"
fi

cat > $tengine_conf/ssl_params<<EOF
    ssl_certificate      $tengine_ssl/ssl/$crtfile;
    ssl_certificate_key  $tengine_ssl/ssl/$keyfile;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  5m;
    ssl_ciphers ECDHE-RSA-AES256-SHA384:AES256-SHA256:RC4:HIGH:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!AESGCM;
    ssl_prefer_server_ciphers on;
EOF
}


##cpu_affinity
add_cpu_affinity(){
cpu_count=`cat /proc/cpuinfo | grep -c process`

echo $cpu_count
proc_num=$(($cpu_count*2))
perl -pi -e "s/^worker_processes  [0-9]/worker_processes  $proc_num/" $tengine_config/nginx.conf

case $cpu_count in
    2)
         affinity="worker_cpu_affinity 01 10";;
    4)
         affinity="worker_cpu_affinity 0001 0010 0100 1000";;
    8)
         affinity="worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000";;
    *)
         affinity="worker_cpu_affinity 01 10";;
esac
/bin/grep "worker_cpu_affinity" $tengine_config/nginx.conf > /dev/null

if [ $? -eq 0 ]; then
    sed -i "/worker_cpu_affinity/d" $tengine_config/nginx.conf
fi
sed -i "/worker_processes/ a\\$affinity\;" tengine_config/nginx.conf
}
