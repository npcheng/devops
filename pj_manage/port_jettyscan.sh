port=`ss -tln |awk '{print $3}'| awk -F \:+ '{if (NR > 1){print $NF}}' | uniq`

for p in $port
do
    process=`lsof -i:$p -sTCP:LISTEN| sed -n '2p'| awk '{print $2}'`
    if test ! -z $process
    then
         ps axf | grep  jetty\.home |grep -v grep | awk -v port=$p -v proc=$process '{if ($1==proc) {print port " " $13}}'| awk -F'[= ]' '{print $1 "," $3}'
    else
        echo "$p is NULL"
    fi
done
