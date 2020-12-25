import threading
import _thread
import socket
from multiprocessing import Queue
import datetime
import sys

#Log lock
lQueueLock = threading.Lock()

#Log queue
lQueue = Queue()
#Dict for registered users
registeredUsers = []

currentUsers = {}

class WriteThread (threading.Thread):
    def __init__(self, name, csoc, address, tQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.address = address
        self.tQueue = tQueue
    def run(self):
        self.toLog("Starting", self.name)
        while True:
            qMessage = self.tQueue.get()
            komut, msg = qMessage.split(", ")
            try:
                self.csoc.send((komut+" "+msg).encode())
            except:
                break
        self.toLog("Exiting", self.name)

    def toLog(self, komut, message):
        toQueue = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": %s"%(komut) + message
        lQueueLock.acquire()
        lQueue.put(toQueue)
        lQueueLock.release()

class ReadThread (threading.Thread):
    def __init__(self, name, csoc, address,tQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.address = address
        self.lQueue = lQueue
        self.tQueue = tQueue
        self.loginState = False
        self.nickName = "Unknown"
        self.registeredUser = "Default"
        self.unregisteredUser = " "
        self.writeQueueLock = threading.Lock()
        self.message = ""
        
    def parser(self, data):
        data = data.strip()
        try:
            komut, param = data.split(" ",1)
        except: # bu durumlarda girilen komutlar parametre almayacağı için splite gerek yok.
            if data == "PIN":
                self.toLog("PIN", "")
                return 4
            elif data == "GLS":
                if not self.loginState:
                    return 0
                else:
                    return 6     
            elif data == "QUI":
                return 5
            else:    
                return 0
        
        if(self.loginState == False): #NIC komutunu çalıştırmazsa yaşanılacak caseler için
            #Debugging için.
            #print("login false a girdi")
            #print(komut)
            #Connection test
            if(komut == "PIN"):
                self.toLog("PIN", "")              
                return 4
            elif data == "QUI":
                self.toLog("QUI", "")
                return 5
            #User auth.
            elif komut == "NIC":
                self.toLog("NIC", param)
                #print("nıce girdi-DEBUG")
                try:
                    nickName = param
                    for key in registeredUsers:  # kullanıcı adı daha önceden alınmış mı ?
                        if key == nickName:
                            self.unregisteredUser = nickName
                            return 3 #registered user listesinde olan bir isimle NIC komutu çalıştırılırsa verilecek durum.
                    self.registeredUser = nickName
                    self.nickName = nickName
                    self.loginState = True
                    #Genel mesaj atarken kullanıcağım bir kullanıcı dictionary si, liste şeklinde tutmak burada işime yaramıyor. 
                    currentUsers.setdefault(self.nickName, []).append(self.tQueue)
                    currentUsers.setdefault(self.nickName, []).append(self.loginState)
                    currentUsers.setdefault(self.nickName, []).append(self.address)
                    registeredUsers.append(nickName)
                    #Yeni bir kullanıcı girdiğinde WRN uyarısı vermek gerekiyor.
                    for user in currentUsers:
                        x = currentUsers[user]
                        tQueue = x[0]
                        tQueue.put("WRN" + ", "+self.registeredUser+": "+ "giriş yaptı"+"\n")
                    self.toLog("WRN", param)                    
                    #print("DEBUG")
                    return 2 # if not signed in before send  WEL
                except:
                    #Wrong comment error
                    #print("LRR error alıyorum-DEBUG")
                    return 1
            #User signed in succesfully!
            else: # yukarıdaki durumlardan hiçbiri değilse yanlış komut.
                return 1
        else:  ## NIC komutu kullanılarak giriş yapıldı.
            #pın komutu bağlantı testi için kullanılır.
            if(komut == "PIN"):
                #print("girdi-DEBUG")
                return 4
            #Exit
            elif(komut == "QUI"):
                return 5
            #User list
            elif(komut == "GLS"):
                return 6
            #Genel mesaj gönderme
            elif(komut == "GNL"):
                for user in currentUsers:
                    x = currentUsers[user]
                    tQueue = x[0]
                    tQueue.put("GNL" + ", "+self.registeredUser+": "+ param+"\n")
                self.toLog("GNL", param)
                return 7
            #özel mesaj gönderme
            elif(komut == "PRV"):
                nick, message = param.split(":")
                for key in registeredUsers:
                    if key == nick:
                        user = currentUsers[nick]
                        tQueue = user[0]
                        tQueue.put("PRV "+self.nickName + ":, " + message+"\n")
                        self.toLog("PRV", param)
                        return 8
                self.toWrite("NOP", nick)
                self.toLog("NOP", nick) 
            else:
                return 0
            
    def run(self):
        self.lQueue.put("Starting " + self.name)
            
        while True:
            try:
                entry = str(self.csoc.recv(1024).decode())
                self.toLog(entry.strip, str(self.address))
            except:
                break
            response = self.parser(entry) ## 
            if response == 0:
                self.toWrite("ERR", "")
                self.toLog("ERR", "")
            elif response == 1:
                self.toWrite("LRR", "")
                self.toLog("LRR", "")
            elif response == 2:
                self.toWrite("WEL",self.registeredUser)
                self.toLog("WEL", self.registeredUser)
            elif response == 3:
                self.toWrite("REJ",self.unregisteredUser)
                self.toLog("REJ", self.unregisteredUser)
            elif response == 4:
                self.toWrite("PON", "") 
                self.toLog("PON", "")
            elif response == 5:
                try:
                    self.loginState = False  # çıkış yapacağımız için loginstate i false yapıyoruz.
                    pop_counter = -1  #çıkış yapan kişinin registered user listten silinmei gerekmektedir, silme işleminin yapılacağı indexi buluyorum.
                    for key in registeredUsers:
                        pop_counter += 1
                        if key == self.nickName:
                            registeredUsers.pop(pop_counter)
                        self.toWrite("BYE", self.nickName)
                        self.toLog("BYE", self.nickName)
                    break 
                except:
                    break
            elif response == 6: ##gls durumu
                #print("error-DEBUG")
                for key in registeredUsers:
                    self.message += key+":"
                seperator = ":"
                self.message =seperator.join(registeredUsers) 
                print(self.message)
                self.toWrite("LST", self.message)
                self.toLog("LST", self.message)
            elif response == 7: # gnl mesajı, param değişkeni yukarıda olduğu için  mesajı gönderme işlemini yukarıda yaptım sadece teyit burada
                self.toWrite("OKG", "")
                self.toLog("OKG", "")
            elif response == 8: #private mesaj cevabı
                self.toWrite("OKP", "")
                self.toLog("OKP", "" )  
        self.csoc.close()
    ## Hangi komutun ne zaman yapıldığını log queueye yazan fonksiyon
    def toLog(self, komut, message):
        toQueue = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": %s "%(komut) + message
        lQueueLock.acquire()
        lQueue.put(toQueue)
        lQueueLock.release()
    #hangi komutların çalıştırıldığını ve cevaplarını komut satırında görebilmek için kuyruğa yazma işleminin yapıldığı fonksiyon.
    def toWrite(self, komut, message):
        self.writeQueueLock.acquire()
        self.tQueue.put("%s, %s\n"%(komut, message))
        self.writeQueueLock.release()

#Logfile oluşturmak için kullandığım fonksiyon, verileri yazmak için log queue den çekiyoruz.
def logger():
    while True:
        if not lQueue.empty():
            f = open('logfile.txt', 'a')
            f.write(lQueue.get()+ "\n")
            f.close()
            
def Main():
    counter = 0
    
    s = socket.socket()
    port = int(sys.argv[1])
    host = "127.0.0.1" 
    s.bind((host,port))
    
    s.listen()
    _thread.start_new_thread(logger, ( ))
    while True:
        c, addr = s.accept()
        try:
            print("Baglanti kuruldu :", addr)
            lQueueLock.acquire()
            lQueue.put(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": " + "Baglanti kuruldu : " + str(addr))
            lQueueLock.release()

            c.send("Kanala hosgeldin mesajlasmak icin giris yap!\n".encode())
           
            tQueue = Queue()
            writeThread = WriteThread("WriteThread-"+str(counter), c, addr, tQueue)
            writeThread.start()
            readThread = ReadThread("ReadThread-", c, addr,tQueue)
            readThread.start()
            counter += 1
            
        except:
            print("baglanti basarisiz!")
            lQueueLock.acquire()
            lQueue.put(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": " + "baglanti basarisiz!")
            lQueueLock.release()

    s.close()
     
if __name__ == '__main__': 
    Main() 