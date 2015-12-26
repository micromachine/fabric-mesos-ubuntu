from fabric.api import env,hosts,run,execute,roles,sudo
from fabric.contrib.files import append

env.user = 'greg'
env.hosts = ['mesos01','mesos02','mesos03','mesos04','mesos05','mesos06']
env.password = 'password'

env.roledefs = {
   'master': ['mesos01','mesos02','mesos03'],
   'all': ['mesos01','mesos02','mesos03','mesos04','mesos05','mesos06'],
   'slave': ['mesos04','mesos05','mesos06']}

def set_hosts():
	sudo("rm -rf /etc/hosts")
        append('/etc/hosts', '127.0.0.1       localhost', use_sudo=True)
	append('/etc/hosts', '192.168.0.115	mesos01', use_sudo=True)
	append('/etc/hosts', '192.168.0.117	mesos02', use_sudo=True)
	append('/etc/hosts', '192.168.0.118	mesos03', use_sudo=True)
	append('/etc/hosts', '192.168.0.119	mesos04', use_sudo=True)
	append('/etc/hosts', '192.168.0.120	mesos05', use_sudo=True)
	append('/etc/hosts', '192.168.0.121	mesos06', use_sudo=True)
	sudo("cat /etc/hosts")
def set_hostname():
	sudo("rm -rf /etc/hostname")
	append('/etc/hostname', env.host_string,use_sudo=True)
	sudo("hostname -F /etc/hostname")
        sudo("cat /etc/hostname")
def add_repository():
	sudo("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv E56151BF")
	sudo ("echo deb http://repos.mesosphere.com/ubuntu trusty main > /etc/apt/sources.list.d/mesosphere.list")
@roles('master')
def install_master():
	sudo("ufw disable")
	sudo("ufw allow 22/tcp")	
	sudo("ufw allow 5050/tcp")	
	sudo("ufw allow 2181/tcp")	
	sudo("ufw allow 2888/tcp")	
	sudo("ufw allow 3888/tcp")	
	sudo("ufw allow 53/udp")
       	sudo("echo t | ufw enable")  
	append('/etc/sysctl.conf', 'net.ipv6.conf.all.disable_ipv6 = 1', use_sudo=True)
	append('/etc/sysctl.conf', 'net.ipv6.conf.default.disable_ipv6 = 1', use_sudo=True)
	append('/etc/sysctl.conf', 'net.ipv6.conf.lo.disable_ipv6 = 1', use_sudo=True)
	sudo("sysctl -p")  
	sudo("add-apt-repository ppa:webupd8team/java -y")
	sudo("apt-get update")
	sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections")
	sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | /usr/bin/debconf-set-selections")
	sudo("apt-get install oracle-java8-installer -y")
	sudo("apt-get install mesosphere -y")
        sudo("echo 2 > /etc/mesos-master/quorum")
	sudo("echo zk://mesos01:2181,mesos02:2181,mesos03:2181/mesos > /etc/mesos/zk")
	append('/etc/zookeeper/conf/zoo.cfg', '# specify all zookeeper servers', use_sudo=True)
        append('/etc/zookeeper/conf/zoo.cfg', 'server.1=mesos01:2888:3888', use_sudo=True)
        append('/etc/zookeeper/conf/zoo.cfg', 'server.2=mesos03:2888:3888', use_sudo=True)
        append('/etc/zookeeper/conf/zoo.cfg', 'server.3=mesos02:2888:3888', use_sudo=True)
	if env.host == "mesos01": 
		sudo("echo 1 > /var/lib/zookeeper/myid")
		sudo("echo mesos01 > /etc/mesos-master/hostname")
		sudo("cat /etc/hosts | grep mesos01  | awk {'print $1'} > /etc/mesos-master/ip")
        if env.host == "mesos02": 
		sudo("echo 2 > /var/lib/zookeeper/myid")
		sudo("echo mesos02 > /etc/mesos-master/hostname")
		sudo("cat /etc/hosts | grep mesos02  | awk {'print $1'} > /etc/mesos-master/ip")
        if env.host == "mesos03": 
		sudo("echo 3 > /var/lib/zookeeper/myid")
		sudo("echo mesos03 > /etc/mesos-master/hostname")
                sudo("cat /etc/hosts | grep mesos02  | awk {'print $1'} > /etc/mesos-master/ip")
	sudo("echo Cluster01 | sudo tee /etc/mesos-master/cluster")
	sudo("mkdir -p /etc/marathon/conf")	
	sudo("cp /etc/mesos-master/hostname /etc/marathon/conf")
	sudo("cp /etc/mesos/zk /etc/marathon/conf/master")
	sudo("cp /etc/marathon/conf/master /etc/marathon/conf/zk")
        sudo("echo zk://mesos01:2181,mesos02:2181,mesos03:2181/marathon > /etc/marathon/conf/zk")
	sudo("echo manual | sudo tee /etc/init/mesos-slave.override")
	sudo("echo docker,mesos | sudo tee /etc/mesos-slave/containerizers")
	sudo("echo 5mins | sudo tee /etc/mesos-slave/executor_registration_timeout")
@roles('slave')
def install_slave():
	sudo("apt-get update")
	sudo("apt-get -y install mesos")
	sudo("service zookeeper stop")
	sudo("update-rc.d -f zookeeper remove")
	sudo("echo zk://mesos01:2181,mesos02:2181,mesos03:2181/mesos > /etc/mesos/zk")
	sudo("apt-get -y remove --purge zookeeper")
	sudo("service mesos-slave restart")
	sudo("echo manual | sudo tee /etc/init/mesos-master.override")
	sudo("apt-get install haproxy -y")
	sudo("mkdir /etc/haproxy-marathon-bridge/")
 	append('/etc/haproxy-marathon-bridge/marathons', 'mesos01:8080', use_sudo=True)
        append('/etc/haproxy-marathon-bridge/marathons', 'mesos02:8080', use_sudo=True)
        append('/etc/haproxy-marathon-bridge/marathons', 'mesos03:8080', use_sudo=True)
	sudo("wget -O /usr/bin/haproxy-marathon-bridge https://raw.githubusercontent.com/mesosphere/marathon/master/bin/haproxy-marathon-bridge")
	sudo("chmod +x /usr/bin/haproxy-marathon-bridge")
	sudo("/usr/bin/haproxy-marathon-bridge install_cronjob")
	sudo("reboot")
@roles('all')
def reboot_all():
	sudo("reboot")
