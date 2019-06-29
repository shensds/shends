#!/usr/bin/python3
#！-*- coding:utf-8 -*-
#使用进程池
from multiprocessing import Pool
import os,time

def task(name):
    print("子进程(%s)执行任务%s" %(os.getpid(),name))
    time.sleep(1)



if __name__ == "__main__":
    p = Pool(3)
    for i in range(10):
        p.apply_async(task,args=(i,)) #非阻塞方式执行进程
    p.close()   #关闭Pool,不接受新任务
    p.terminate() # 不管任务是否完成 立即终止
    p.join() #进程阻塞，等待子进程退出，必须在close或terminate方法后
    print("所有子进程结束")