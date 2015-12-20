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
