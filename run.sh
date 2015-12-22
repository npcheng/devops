# !/ bin / bash


java_classpath=.:/root/soft/RocketMq/libs/rocketmq-client-3.2.6.jar:/root/soft/RocketMq/libs/rocketmq-common-3.2.6.jar:/root/soft/RocketMq/libs/fastjson-1.2.3.jar:/root/soft/RocketMq/libs/netty-all-4.0.25.Final.jar:/root/soft/RocketMq/libs/rocketmq-remoting-3.2.6.jar:/root/soft/RocketMq/libs/slf4j-api-1.7.5.jar:/root/soft/RocketMq/libs/slf4j-nop-1.7.13.jar:$CLASSPATH


useage()
{
    echo  "usesage:" $0  "-e [arg] -c [arg]"
    echo "-e execute test_file"
    echo "-c compile jave"
}

execute_java()
{
    java -classpath "$java_classpath" $run_file
}

compile_java()
{
    cd com/sean
    javac -classpath "$java_classpath" $compile_file
    ls -l 
    cd ../..
}

ls_dir()
{
    ls -l com/sean
}
while  getopts  " e:c:l"  arg #选项后面的冒号表示该选项需要参数
do
         case  $arg  in
             e)
                echo  " a's arg:$OPTARG "  #参数存在$OPTARG中
		
		run_file=com.sean.$OPTARG
		execute_java
                ;;
             c)
		compile_file=${OPTARG}.java
		echo $compile_file
		compile_java
		
                ;;
             l)
		ls_dir
                ;;
              ? )  #当有不认识的选项的时候arg为 ?
            echo  " unkonw argument "
        	exit  1
        	;;
        esac
done

if [ $# -lt 1 ]
then
  useage
fi
