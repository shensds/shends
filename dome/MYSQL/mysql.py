#python -m pip install mysql-connector
import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.99.171",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="root",   # 数据库密码
  database="wocao_db" #连接数据库 必须已存在
)
mycursor = mydb.cursor()

#创建数据库
mycursor.execute("CREATE DATABASE wocao_db")

#显示数据库
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
    

#创建数据表 sites
mycursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")
#创建数据表 sites 并设置主键
mycursor.execute("CREATE TABLE sites (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url VARCHAR(255))")
#给sites表添加主键
mycursor.execute("ALTER TABLE sites ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

#显示数据表
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)


#向 sites 表插入一条记录。
sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
val = ("RUNOOB", "https://www.runoob.com")
mycursor.execute(sql, val)
print(sql, val)
mydb.commit()    # 数据表内容有更新，必须使用到该语句
print(mycursor.rowcount, "记录插入成功。")
#获取ID
print("ID:", mycursor.lastrowid)

#向 sites 表插入多条记录。
sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
val = [
  ('Google', 'https://www.google.com'),
  ('Github', 'https://www.github.com'),
  ('Taobao', 'https://www.taobao.com'),
  ('stackoverflow', 'https://www.stackoverflow.com/')
]
mycursor.executemany(sql, val)
mydb.commit()    # 数据表内容有更新，必须使用到该语句
print(mycursor.rowcount, "记录插入成功。")


#查询数据
mycursor.execute("SELECT * FROM sites")
myresult = mycursor.fetchall()     # fetchall() 获取所有记录
for x in myresult:
    print(x)
#查询指定字段
mycursor.execute("SELECT name, url FROM sites")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)
#只获取一条数据
mycursor.execute("SELECT * FROM sites")
myresult = mycursor.fetchone()
print(myresult)

#where
sql = "SELECT * FROM sites WHERE name ='RUNOOB'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)





#优化数据表
OPTIMIZE TABLE 























