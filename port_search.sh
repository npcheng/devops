port=`ss -tln |awk '{print $3}'| awk -F \:+ '{if (NR > 1){print $NF}}' | uniq`

for p in $port
do
    process=`lsof -i:$p -sTCP:LISTEN| sed -n '2p'| awk '{print $2}'`
    if test ! -z $process
    then
         ps axf | grep  jetty\.home |grep -v grep | awk -v port=$p -v proc=$process '$1~proc {print port " " $13}'| awk -F'[= ]' '{print $1 "," $3}'
    else
        echo "$p is NULL"
    fi
done


#for app in `seq -f "app%g" 10 33` ; do  sh cmd $app /mnt/bin/1/1.sh ; done| grep -v ^$| awk '/^app/{T=$1;next;}{print T","$0;}'



port=`ss -tln |awk '{print $3}'| awk -F \:+ '{if (NR > 1){print $NF}}' | uniq`

for p in $port
do
    process=`lsof -i:$p -sTCP:LISTEN| sed -n '2p'| awk '{print $2}'`
    if test ! -z $process
    then
         ps axf | grep -v jetty\.home |grep -v grep | awk -v port=$p -v proc=$process '$1~proc {print port " " $3}'
    else
        echo "$p is NULL"
    fi
done

#for app in `seq -f "app%g" 60 79` ; do  sh cmd $app /mnt/bin/1/3.sh ; done| grep -v ^$| awk '/^app/{T=$1;next;}{print T","$0;}'


for p in $port; do     process=`lsof -i:$p| sed -n '2p'| awk '{print $2}'`;     ps axf | grep jetty\.home| grep -v grep | awk -v port=$p -v proc=$process '$1~proc {print port " " $1 " " $13}'; done
