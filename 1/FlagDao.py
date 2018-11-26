#!usr/bin/env python
#coding:utf-8
import XmlDao

class FlagDao():

    def __init__(self,filename=None):
        if filename is None:
            self.__filename = '../grapdata/flag.xml'
        else:
            self.__filename = filename
    #获取节点属性
    def getValueByName(self,name):
        tree = XmlDao.openXml(self.__filename)
        print 'tree',tree,self.__filename
        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, 'flag')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            return nodes[0].attrib['value']
        return None
    #设置节点
    def setValueByName(self,name,value):
        tree = XmlDao.openXml(self.__filename)
        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, 'flag')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            nodes[0].attrib['value'] = value
            XmlDao.saveAs(tree, self.__filename)
    #添加节点
    def addTag(self,name,value):
        tree = XmlDao.openXml(self.__filename)
        XmlDao.add_child_node([tree.getroot()],XmlDao.create_node('flag', {'name':name,'value':value}))
        XmlDao.saveAs(tree, self.__filename)
    #删除节点
    def deleteTagByName(self,name):
        tree = XmlDao.openXml(self.__filename)
        XmlDao.del_node_by_tagkeyvalue([tree.getroot()], 'flag', {'name':name})
        XmlDao.saveAs(tree, self.__filename)
