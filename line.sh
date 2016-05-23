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
        mem_pid=`lsof -i:$port| sed -n 2p| awk '{print $2}'`
        if [ $mem_pid -lt 0 ] 
        then
            echo "process has down"
            exit
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
        #sed '${ret}p' $iptables_config
        sed  -i "${ret}d" $iptables_config
        if [ $? -eq 0 ]
        then
            echo "delete iptables item success"
        else
            echo "delete iptables item failed" 
        fi
    fi
}
iptables_config='iptables'
getiptablesLine 192.168.10.192 12268
if  test -z $ret  
then 
    echo "hello $ret"
else
    echo "good $ret" 
    deleteMemInstance
    deleteMemIptables
fi
