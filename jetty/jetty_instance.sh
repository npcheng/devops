#!/usr/bin/shell

function jettystatus()
{
    ret=`ps axf | grep "$jetty_project" | grep -v "grep"| grep -v "${shell_name}"|wc -l`
    echo $ret
    if [[ $ret -ne 0 ]]
    then
        action='cp -rf'
    else
       action='mv'
    fi
    echo $action
}

function backup(){

#jettystatus $jetty_project
#project_count=`wc -l $project_dir/webapps`
project_count=`ls -F $project_dir/webapps| grep '/$'| wc -l`
mount_s=`cat /proc/mounts |grep $project_dir | awk '{print $1}'`
mount_d=`cat /proc/mounts |grep $project_dir | awk '{print $2}'`

if [ $project_count -eq 1 ]
then
    
    /data/webapp/jetty-root.sh stop $jetty_project
    #chceckmount myumount
    mv $backup_project $backup_dir/${backup_dst}
    rm -rf $project_dir
else
    mv $backup_project $backup_dir/${backup_dst}
    /data/webapp/jetty-root.sh stop $jetty_project
    /data/webapp/jetty-root.sh start $jetty_project
fi

if [ $? -eq 0 ]
then
   cd $backup_dir
   if [ $? -eq 0 ]
   then
       tar cvfz ${backup_dst}.tar.gz ${backup_dst} 2>&1 >/dev/null
       rm -rf $backup_project
       echo "$action success"
       exit 0
   else
       echo "tar package failed"
       exit 1
   fi
else
   echo "$action failed"
   exit 1
fi
}

function checkmount()
{
 if [ ! $mount_s -o ! $mount_d ]; then
  echo "The project no mount!"
 else
  case $1 in
   myumount)
    umount $mount_d
    if [ ! $? -eq 0 ]; then
     echo "umount $mount_d failed!"
     exit 1
    else
     echo "umount $mount_d succeed!"
     sleep 1
    fi
   ;;
   mymount)
    mount -t nfs $mount_s $mount_d
    if [ ! $? -eq 0 ]; then
     echo "mount $mount_s failed!"
     exit 1
    else
     echo "mount $mount_s succeed!"
     sleep 1
    fi
   ;;
  esac
 fi
}


backup_dir=/data/backup
backup_date=`date +"%Y-%m-%d_%H%M"`
jetty_dir=/data/webapp

shell_name=`basename $0`
if [ $# -ne 2 ]
then
    echo "no jetty project"
    exit 1
else
   
    jetty_project=$1
    project_instance=$2
    project_dir=$jetty_dir/jetty-$jetty_project
    backup_project=$project_dir/webapps/${project_instance}
    backup_dst=jetty-${jetty_project}_${project_instance}_${backup_date}
    if [ ! -d $backup_project ]
    then
        echo $backup_project not exist
        exit 1
    fi
    #sh /data/webapp/jetty-root.sh stop $project_instance
    backup
fi
