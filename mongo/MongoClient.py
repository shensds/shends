import pymongo

#连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
# client = MongoClient('mongodb://localhost:27017/')

#列出数据库
dblist = client.list_database_names()
print(dblist)

#指定数据库
db = client.test
# db = client['test']

#指定集合
collection = db.students
# collection = db['students']

#列出集合
collist = db.list_collection_names()
print(collist)


#插入数据
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)
#result = collection.insert(student) 不推荐
print(result)
print(result.inserted_id)

#插入多条数据

student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}

result = collection.insert_many([student1, student2])
# result = collection.insert([student1, student2])   不推荐
print(result)



#查询
result = collection.find_one({'name': 'Mike'})
print(type(result))
print(result)