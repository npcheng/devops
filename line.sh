function getiptablesLine(){
    ip=$1
    port=$2
    ret=`awk -v dport=$port -v ip=$ip '/-p tcp/&& /--dport/ &&/ACCEPT/ && /-s '"$ip"'\/32/ {for (i=1; i<=NR; i++){if( $i=="--dport"){port=i+1;if($port ==dport){print NR; exit}}}}' $iptables_config`
}

function deleteMemInstance(){
    echo $port | grep -Eio "[0-9]+"
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

        if [ `kill -9 $mem_pid  2>&1 >/dev/null` ] 
        then
            echo "destroy memached  Instance"
        fi
    else
        echo "process has down"
    fi
}

function deleteMemIptables(){
    if [ $ret -gt 0 ]
    then
        time=`date +"%Y-%m-%d_%H%M"`
        echo "delete time $time" >> /data/backup/del_iptables.txt 
        sed -n "${ret}p" $iptables_config >> /data/backup/del_iptables.txt
        sed  -i "${ret}d" $iptables_config
        if [ $? -eq 0 ]
        then
            exit_ret=0
            echo "delete iptables item success"
            exit  $exit_ret
            
        else
            exit_ret=1
            echo "delete iptables item failed" 
            exit  $exit_ret
        fi
    fi
}
exit_ret=1
if [ $# -ne 2 ]
then
    echo "please input right params"
    exit $exit_ret
fi
iptables_config='iptables'
#getiptablesLine 10.104.130.206 12268
getiptablesLine $1 $2
if  test -z $ret  
then 
    echo "hello $ret"
    exit $exit_ret
else
    echo "good $ret" 
    deleteMemInstance
    deleteMemIptables
fi
