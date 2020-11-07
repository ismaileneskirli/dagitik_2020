import queue
import threading
import time
import sys
import string
import multiprocessing
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Lock, Process, Queue, current_process
## NOT : Verilen argümanlarda n = 8 den sonrası düzgün çalışmıyor. Bilgisayardaki işlemci sayısıyla alakalı bir durum olabilir mi ?
outputFile = open("output.txt","w")
myfile=open('input.txt','r')
#print(len(text_data))


s = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])

def caesarCipher(text,shift) :
    text = text.lower()
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)

def worker(work_queue,shift,my_lock):
    my_lock.acquire()
    for text in iter(work_queue.get, 'STOP'):
        cryptedText = caesarCipher(text,shift)
        outputFile.write(cryptedText.upper())
        #print(cryptedText)
    my_lock.release()    

def main():
    text_data=myfile.read()
    print(n,len(text_data),l)
    work_queue = Queue(len(text_data))
    processes = []
    my_lock = multiprocessing.Lock()

    my_lock.acquire()    
    index=0
    for i in range(0,len(text_data),l):
        work_queue.put(text_data[index:index+l])
        index += l
    my_lock.release()
    
    for i in range(0,n):
        p=multiprocessing.Process(target=worker,args=(work_queue,s,my_lock))
        p.start()
        processes.append(p)
        work_queue.put('STOP')
        
    for p in processes:
        p.join()
        
    #empty the list.
    del processes[:]
    
    print("Succesfull")
    
if __name__ == '__main__':
    main()
