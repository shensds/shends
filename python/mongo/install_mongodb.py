Mongo下载地址
www.mongodb.com/download-center#community
客户端下载
https://robomongo.org/

注册服务
管理员权限运行
mongod --bind_ip 0.0.0.0 --logpath D:\www\mongodb\data\logs\mongo.log --logappend --dbpath D:\www\mongodb\data --port 27017 --serviceName "MongoDB" --install

--bind_ip 0.0.0.0 任意IP可访问
--logpath D:\www\mongodb\data\logs\mongo.log 日志手动创建
--logappend 日志追加方式
--dbpath D:\www\mongodb\data 数据存放地址
--port 27017 端口号
--serviceName "MongoDB"  服务名称

