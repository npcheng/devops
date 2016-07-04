from random import choice
import string,os,commands


def GenPassword(length=10,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__=="__main__":
    try:
        fp = open("iplist1.txt", "r")
        fp_w = open("ip_passwd.txt", "w")
    except Exception,e:
        print e
    iplist = []
    for line in fp.readlines():
        line = line.strip().split()[1]
        passwd = GenPassword(10)
        print passwd  + " " + line
        status = commands.getstatusoutput("ansible -i /etc/ansible/hosts " + line + " -m raw -a 'echo \"root:" +passwd +"\"|chpasswd'")
        print status
        if status[0] == 0:
            print "init passwd success"
            fp_w.write(line + " " + passwd +" success \n")
        else:
            fp_w.write(line + " " + passwd +" failed\n")
            
        #break
        
        iplist.append(line)
