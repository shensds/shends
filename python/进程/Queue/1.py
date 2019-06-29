
from multiprocessing import Queue ,Process

import time


def write_task(q):
    if not q.full():
        for i in range(5):
            message = '消息'+str(i)
            q.put(message)
            print('写入：%s' % message)


def read_task(q):
    time.sleep(1)
    while not q.empty():
        print('读取：%s'% q.get(True,2))


if __name__ == '__main__':
    print("主进程开始")
    q = Queue()
    pw = Process(target=write_task,args=(q,))
    pr = Process(target=read_task,args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.join()
    print("主进程结束")
    
if __name__ == "__m1ain__":
    pass
    '''
    q = Queue(3)
    q.put("消息1")
    q.put("消息1")
    q.put("消息1")

    Queue.qsize()   #返回当前列表包含的消息数量
    Queue.empty()   #队列空返回True,反之返回False
    Queue.full()    #队列满了返回True,反之返回False
    #获取队列中的一条消息，然后将其从队列移除
    #block 默认值True，当block为False且队列为空抛出异常，
    Queue.get([block[,timeout]])    
    Queue.get_nowait()   #相当于Queue.get(False)
    #将item消息写入队列，block 默认值True
    Queue.put(item,[block[,timeout]])
    Queue.put_nowait()   #相当于Queue.put(False)
    '''




