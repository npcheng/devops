backup(){
    project_dir=${1%/*}
    project_name=${1##*/}
    ext=$2
    if [ -d $1 ] ; then
        cd $project_dir
        echo $project_name $project_dir $ext $#
    else
        echo $backup_date " " $project_name "not exist" >> $log_file
        return 1
    fi
    if [ $# -gt 2 ];then
        for exclude in $3; do
            exclude_dir="--exclude=$exclude $exclude_dir"
        done
    fi
        #echo $exclude_dir
    tar cvfz ${project_name}_$ext.tar.gz $project_name $exclude_dir &>/dev/null
    if [ -d $backup_dir ] ; then 
        mv ${project_name}_$ext.tar.gz $backup_dir
    else
        echo $backup_date " " $project_name "move to backup diretory failed" >> $log_file
    fi

 
    
}

rm_file(){
    cd $backup_dir &&find $backup_dir -ctime +7 -exec rm -rf {} \;
}
backup_dir=/data/back
log_file=/data/backup.log

backup_date=`date +%Y%m%d`
project="/data/django/mysite"
exclude="templates"
backup $project $backup_date $exclude
rm_file
