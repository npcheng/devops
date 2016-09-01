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

jettystatus $jetty_project
echo "$project_dir $backup_dir/jetty-${jetty_project}_$backup_date" 
$action  $project_dir $backup_dir/jetty-${jetty_project}_$backup_date
if [ $? -eq 0 ]
then
   cd $backup_dir
   if [ $? -eq 0 ]
   then
       tar cvfz jetty-${jetty_project}_${backup_date}.tar.gz jetty-${jetty_project}_${backup_date} 2>&1 >/dev/null
       rm -rf $backup_dir/jetty-${jetty_project}_$backup_date
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


backup_dir=/data/backup
backup_date=`date +"%Y-%m-%d_%H%M"`
jetty_dir=/data/webapp

shell_name=`basename $0`
if [ $# -ne 1 ]
then
    echo "no jetty project"
    exit 1
else
   
    jetty_project=$1
    project_dir=$jetty_dir/jetty-$jetty_project
    if [ ! -d $project_dir ]
    then
        echo $project_dir is not exist
        exit 1
    fi
fi
/data/webapp/jetty-root.sh stop $jetty_project

if [ $? -eq 0 ]
then
   backup
else
   echo "echo app not running $?"
   backup
   exit 
fi
