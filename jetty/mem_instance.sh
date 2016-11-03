#function getiptablesLine(){
#    ip=$1
#    port=$2
#    ret=`awk -v dport=$port -v ip=$ip '/-p tcp/&& /--dport/ &&/ACCEPT/ && /-s '"$ip"'\/32/ {for (i=1; i<=NR; i++){if( $i=="--dport"){port=i+1;if($port ==dport){print NR; exit}}}}' $iptables_config`
#}

function isInIptables(){
    port=$1
    iptable_ret=`grep "\-\-dport $port"  $iptables_config|grep tcp| wc -l`
    echo $iptable_ret
}

function deleteMemInstance(){
    echo $port | grep -Eio "[0-9]+" 2>&1 >/dev/null
    if [ $? -ne 0 ] 
    then
        echo "not a int"
        exit
    fi
    ss -tln| grep $port 2>&1 >/dev/null
    if [ $? -eq 0 ]
    then
        mem_pid=`lsof -i:$port -sTCP:LISTEN | sed -n 2p| awk '{print $2}'`
        if [ $mem_pid -lt 0 ] 
        then
            exit_ret=1
            echo "process has down"
            exit $exit_ret
        fi
        cat /proc/${mem_pid}/cmdline > /data/backup/mem_instance.txt

        if [ `kill -9 $mem_pid  2>&1 >/dev/null` ] 
        then
            echo "destroy memached  Instance"
        fi
    else
        echo "process has down"
    fi
}

function deleteMemIptables(){
    if [ $iptable_ret -gt 0 ]
    then
        time=`date +"%Y-%m-%d_%H%M"`
        cp $iptables_config /data/backup/iptables_$time
        echo "delete time $time" >> /data/backup/del_iptables.txt 
        #sed -n "${ret}p" $iptables_config >> /data/backup/del_iptables.txt
        sed  -n "/-m tcp --dport $port/p" $iptables_config >> /data/backup/del_iptables.txt
        sed  -i "/-m tcp --dport $port/d" $iptables_config
        #sed  -i "${ret}d" $iptables_config
        if [ $? -eq 0 ]
        then
            exit_ret=0
            echo "delete iptables item success"
            restart_iptables
            exit  $exit_ret
            
        else
            exit_ret=1
            echo "delete iptables item failed" 
            exit  $exit_ret
        fi
    else
        exit_ret=0
        echo "no iptables item need to delete"
        exit  $exit_ret
    fi
}

function restart_iptables(){
    `/etc/init.d/iptables restart`
    if [ $? -eq 0 ]; then
        exit_ret=0
        echo "restart iptables success"
    else
        exit_ret=1
        echo "restart iptables failed"
    fi
}

exit_ret=1
if [ $# -ne 1 ]
then
    echo "please input right params"
    exit $exit_ret
fi
iptables_config='/etc/sysconfig/iptables'
#iptables_config='iptables'
isInIptables $1
#iptable_ret=0
if  [  $iptable_ret -eq 0 ]
then 
    echo "hello "
    exit $exit_ret
else
    echo "good" 
    deleteMemInstance
    deleteMemIptables
    restart_iptables
    exit $exit_ret
fi
