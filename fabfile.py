from fabric.api import env,hosts,run,execute,roles,sudo
from fabric.contrib.files import append

env.user = 'greg'
env.hosts = ['mesos01','mesos02','mesos03','mesos04','mesos05','mesos06']
env.password = 'password'

env.roledefs = {
   'master': ['mesos01','mesos02','mesos03'],
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
#	sudo("echo t | ufw enable")   
#	sudo("ufw allow 22/tcp")	
#	sudo("ufw allow 5050/tcp")	
#	sudo("ufw allow 2181/tcp")	
#	sudo("ufw allow 2888/tcp")	
#	sudo("ufw allow 3888/tcp")	
#	sudo("ufw allow 53/udp")	
	sudo("add-apt-repository ppa:webupd8team/java -y")
	sudo("apt-get update")
	sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections")
	sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | /usr/bin/debconf-set-selections")
	sudo("apt-get install oracle-java8-installer -y")
	sudo("apt-get install mesosphere")
@roles('slave')
def install_slave():
	run("yum -y install mesos")
	run("systemctl stop mesos-master.service")
	run("systemctl disable mesos-master.service")
	run("firewall-cmd --zone=public --permanent --add-port=5051/tcp")	
	run("firewall-cmd --zone=public --permanent --add-port=2181/tcp")	
        run("rm -rf /etc/mesos/zk")
        append('/etc/mesos/zk', 'zk://mesos01:2181,mesos02:2181,mesos03:2181/mesos', use_sudo=True)
	run("mkdir -p /etc/marathon/conf")
	run("cp /etc/mesos-master/hostname /etc/marathon/conf")
	run("cp /etc/mesos/zk /etc/marathon/conf/master")
	run("cp /etc/marathon/conf/master /etc/marathon/conf/zk")
        run("service mesos-slave restart")
        run("systemctl restart firewalld")
	run("systemctl stop mesos-master.service")
	run("systemctl disable mesos-master.service")
	run("firewall-cmd --zone=public --permanent --add-port=5051/tcp")	
	run("firewall-cmd --zone=public --permanent --add-port=2181/tcp")	
        run("rm -rf /etc/mesos/zk")
        append('/etc/mesos/zk', 'zk://mesos01:2181,mesos02:2181,mesos03:2181/mesos', use_sudo=True)
	run("mkdir -p /etc/marathon/conf")
	run("cp /etc/mesos-master/hostname /etc/marathon/conf")
	run("cp /etc/mesos/zk /etc/marathon/conf/master")
	run("cp /etc/marathon/conf/master /etc/marathon/conf/zk")
        run("service mesos-slave restart")
        run("systemctl restart firewalld")	
