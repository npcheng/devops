#!/usr/bin/bash
rpm_need="libmemcached-1.0.18-.el6.x86_64.rpm
libmcrypt-2.5.8-9.el6.x86_64.rpm
php-7.0.4-0.el6.x86_64.rpm
yaf-3.0.2-1.el6.x86_64.rpm
php7-memcached-2.2.0_beta-4.el6.x86_64.rpm
tengine-2.1.2-0.x86_64.rpm
"
rpm_depens="
libtool-ltdl
freetype
libjpeg-turbo
libpng
"

RETZERO=0
# 删除可能存在冲突的rpm包
rm_rpm(){

php_version=0
if [ -x "/usr/bin/php" ] || [ -x "/data/php7/bin/php" ]
then
php_version=`php -v| grep -Eio "PHP [0-9]+"| grep -Eio "[0-9]"`
fi

if [ php_version  -ne 7 ] ;then
rpm -qa php &&  for i in `rpm -qa | grep php`; do rpm -e $i --nodeps  2>&1 >/dev/null; done
rpm -q yaf && rpm -e yaf
rpm -q libmemcached 2>&1 >/dev/null && rpm -e libmemcached --nodeps 2>&1 >/dev/null
rpm -q libmemcached-devel 2>&1 >/dev/null && rpm -e libmemcached-devel --nodeps 2>&1 >/dev/null
fi
}

# 安装rpm包
install_rpm(){
for rpm_package in $rpm_need
do
     echo $rpm_package
     if ! rpm -q ${rpm_package%.*} >/dev/null;then
          rpm -ivh $rpm_package
     else
         echo $rpm_package is install
     fi
done
}

# 删除安装包
rm_package(){
rm -f pkg.tar.gz
for _package in $rpm_need
do
    rm -f $_package
done
}



tar xvfz pkg.tar.gz
# 检测安装tengine
rpm -q tengine  2>&1 >/dev/null || rpm -ivh `ls tengine*.rpm`

# yum安装所需的软件包
for _package in $rpm_depens
do
    rpm -q $_package 2>&1 >/dev/null || yum install  -y $_package  2>&1 >/dev/null
done

rm_rpm
install_rpm
rm_package
rm -f $0
exit $RETZERO
