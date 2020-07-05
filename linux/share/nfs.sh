yum -y install nfs-utils rpcbind
vim /etc/exports 
/data/nfs 172.16.1.0/24(rw,sync)
exportfs -r  

# 先启动rpc 
/etc/init.d/rpcbind start           
centos 8
/usr/bin/rpcbind start

#启动NFS
/etc/init.d/nfs start                  
systemctl start nfs-server.service

systemctl enable nfs-server.service

showmount -e localhost

#设置服务为开机自启 ；
chkconfig nfs on
chkconfig nfs-server on

#加入到开机自启中 
tail -2 /etc/rc.local           
/etc/init.d/rpcbind start 
/etc/init.d/nfs  start




mount -t nfs 172.16.1.9:/data/nfs /mnt


### ######################  NFS客户端挂载排错思路  ###########################
客户端排查三部曲
①. 检查服务端房源信息是否还在
    rpcinfo -p 172.16.1.9
②. 检查服务端共享目录信息是否存在
    showmount -e 172.16.1.9
③. 直接进行目录挂载测试
    mount -t nfs 172.16.1.9:/data /mnt
	
#########################  服务端排查三部曲  ################################# 
①. 检查服务端房源信息是否还在
    rpcinfo -p localhost
	如果没有注册的房源信息了，会是什么情况？
	①. nfs服务没有启动
	②. nfs服务于rpc服务启动顺序不正确
②. 检查服务端共享目录信息是否存在
    showmount -e localhost
	①. nfs配置文件编写格式错误
③. 直接进行目录挂载测试
    mount -t nfs 172.16.1.9:/data /mnt


# 实现nfs客户端开机自动挂载方式
①. 将挂在命令追加到/etc/rc.local开机自启动文件中
②. 编写fstab文件，并且需要配合netfs服务使用，实现开机自动挂载



