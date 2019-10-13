from threading import Thread, Lock

lock = Lock()

def function(numb, saver):
    for _ in range(numb):
        with lock:  
            a = saver[0]
            a += 1
            saver[0]=a

def main():
    threads = []
    saver = [0, ]
    for i in range(5):
        thread = Thread(target=function, args=(1000000, saver))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", saver[0] )  
main()