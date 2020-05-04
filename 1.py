#A是属于B生成
isinstance(A,B)
#是否可迭代
from collections import Iterable,Iterator
print(isinstance([1,2,3,],Iterable))
class Classmaste(object):
    def __init__(self):
        sele.names = list()
    def add(self,name):
        self.name.append(name)
    def __iter__(self):
        return ClassIterator()
class ClassIterator(object):
    def __iter__( self):
        pass 
    def __next__(self):
        pass
        
classmate = Classmate()
classmate .add("老王")
classmate .add("王二")
#判断 classmate 是否是可以迭代的对象 ： 
isinstance(classmate,Iterable)
classmate_iterator = iter(classmate)
#判是classmate_iterator否是迭代器  
isinstance(classmate_iterator, Iterator)) 