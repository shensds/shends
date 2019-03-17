#!/usr/bin/python3
#！-*- coding:utf-8 -*-
from multiprocessing import Process

def test(a):
    print(a)
    
def main():
    #target 当前进程启动时执行的可调用对象
    #name    当前进程实例的别名 默认Process-N
    #args 传递给target函数的参数元组
    #kwargs 传递给target函数的参数字典
    #pid 当前进程实例的PID值
    p = Process(target=test, name = "name1"args=("哈哈",))
    p.start()       #启动进程实例 没有target默认为run()方法
    p.is_alive()    #判断进程实例是否还在执行
    p.join(timeout = 10)  #是否等待进程实例执行结束，或等待多少秒
    p.terminate() # 不管任务是否完成立即终止

if __name__ == "__main__":
    main()
