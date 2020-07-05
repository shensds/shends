1.安装vsftp软件包
yum  -y install  vsftpd*

2.启动vsftpd服务器
systemctl  restart  vsftpd
systemctl enable vsftpd

3.检查服务是否正常启动
ps -ef|grep vsftp   &&  netstat -tunlp|grep 21

#允许匿名用户上传
vim   /etc/vsftpd/vsftpd.conf
anon_upload_enable=YES                       #允许匿名用户上传
anon_mkdir_write_enable=YES               #允许匿名用户创建目录 