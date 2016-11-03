#ip_list="14.211.159.150 36.62.11.255"
#ip_list="60.181.149.231"
#ip_list="60.211.137.230"
#ip_list="124.132.84.101 117.151.227.130 14.211.169.187 14.120.104.65 61.163.197.3 14.117.81.65"
#ip_list="119.181.114.40"
#ip_list="123.132.82.89"
#ip_list="123.174.42.244 117.91.70.192"
#ip_list="124.132.84.113"
ip_list="117.151.231.2"
ip_list="36.34.93.178"
#ip_list="116.9.24.102"
ip_list="14.120.106.10 49.74.27.100 124.132.84.116"
ip_list="123.174.44.215 114.83.66.50 42.235.134.143"
ip_list="14.120.104.110"
#for ip in $ip_list
#do
#   sed -i "/:OUTPUT/a\-A INPUT -s $ip/32 -p tcp -m tcp --dport 15230 -j DROP" /etc/sysconfig/iptables
#done

ip=$1
sed -i "/:OUTPUT/a\-A INPUT -s $ip/32 -p tcp -m tcp --dport 15230 -j DROP" /etc/sysconfig/iptables
