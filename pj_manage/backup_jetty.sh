#!/usr/bin/shell

function jettystatus()
{
    ret=`ps axf | grep "$jetty_project" | grep -v "grep"| grep -v "${shell_name}"|wc -l`
    echo $ret
    #echo "ps axf | grep "$1" | grep -v grep| grep -v "${shell_name}""
    if [[ $ret -ne 0 ]]
    then
        action='cp'
    else
       action='mv'
    fi
    echo $action
}
backup_dir=/data/backup
backup_date=`date +%Y%m%d`
jetty_dir=/data/webapp

shell_name=`basename $0`
echo $0
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

jettystatus $jetty_project
echo "$project_dir $backup_dir/jetty-${jetty_project}_$backup_date" 
$action  $project_dir $backup_dir/jetty-${jetty_project}_$backup_date
