# fabric-mesos-ubuntu

### Available options  

fab -l

    add_repository
    install_master
    install_slave
    set_hostname
    set_hosts

##### Installation using ROLES 

fab -R master install_master

###### add_repository
	
Adding mesos repository 

######	install_master 

Install mesos master host, zookeeper and configure firewall 

######	set_hostname
	
Set hostname 

######	set_hosts

Set hosts entry in /etc/hosts

