import queue
import threading
import time
import sys
import string

 # String kütüphanesi ile lowercase lerden oluşan alfabeyi shift kadar kaydırarak yeni alfabe ile değiştirdim.
 
def caesarCipher(text,shift) :
    text = text.lower()
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)
exitFlag = 0

## Ders notlarındaki thraed oluşturma fonksiyonu
class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)
#yazdığım şifreleme programını bu fonksiyonda çalıştırıyorum.

def process_data(threadName, q):
   while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            print ("%s processing %s" % (threadName, data))
            outputFile.write(caesarCipher(data,s).upper())
            queueLock.release()
           
           
   
        else:
            queueLock.release()
        time.sleep(1)


s = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])
outputFile = open("crypted_thread_12_10_48.txt","w")
myfile=open('input.txt','r')
text_data=myfile.read()
print(len(text_data))

queueLock = threading.Lock()
workQueue = queue.Queue(len(text_data))
threads = []
threadID = 1

# Create new threads
for tName in range(0,n):
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
index = 0
for i in range(0,len(text_data),l):
    workQueue.put(text_data[index:index+l])
    index +=l
    
#for word in nameList:
#   workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")
