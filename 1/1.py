import FlagDao

flagDao = FlagDao()

#查找节点
print flagDao.getValueByName('execute')
#修改节点
flagDao.setValueByName('execute', 'false')
#打印修改的节点
print flagDao.getValueByName('execute')
#添加节点
flagDao.addTag('zhangcan', 'bendan')
#删除节点
flagDao.deleteTagByName('other')
