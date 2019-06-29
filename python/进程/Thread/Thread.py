from threading import Thread
#import threading

def wocao(a,b):
    print("ABC")
    print(a,b)
    
if __name__ == '__main__':

    thread1 = Thread(target= wocao,args=("wocao","nima"))
    thread1.start()

    thread1.join()