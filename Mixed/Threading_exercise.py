import threading as t
import time

def Fab1(parametro):
    while True:
        print('Fab %s\t'%parametro,(t.current_thread()),"\t",t.main_thread(),'\t',t.active_count())
        time.sleep(1)

def Fab2(parametro):
    while True:
        print('Fab %d\t'%parametro,(t.current_thread()),"\t",t.main_thread(),'\t',t.active_count())
        time.sleep(1)

x = t.Thread(target = Fab1, args=(1000,))
x.start()

y = t.Thread(target = Fab2, args=(2000,))
y.start()

