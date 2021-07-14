
import pynput
import time

def fab(k3):
    print("processo 2i")
    
while True:
    print("processo 1")
    keyl = pynput.keyboard.Listener(on_press=fab)
    with keyl:
        keyl.join()
    time.delay(1)
