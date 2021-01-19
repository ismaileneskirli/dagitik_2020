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

#Kayıtlı kullanıcılar için dict
registeredUsers = {"a":"1","b":"2"}
#online kullanıcılar için dict
currentUsers = {}
#odalar için dict
#roomDict = { <room>: [ <admin list>, <non admin list>, <banned list>  ] }
roomDict={}



#Log lock
lQueueLock = threading.Lock()

#Log queue
lQueue = Queue()

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
            #debug
            print(komut)
            print(param)
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
            elif data =="RLS":
                return 18
            elif data =="MRL":
                x=currentUsers[self.registeredUser]
                seperator=":"
                self.message =seperator.join(x[4])
                return 21
                
            else:    
                return 0
        
        if(self.loginState == False): #SIN komutunu çalıştırmazsa yaşanılacak caseler için
            #Debugging için.
            print("login false a girdi")
            print(komut)
            #Connection test
            
            #kullanıcı kayıtı komutu 
            if(komut == "SUP"):
                try:
                    nickName,password = param.split(":")
                    #kullanıcı daha once kayıt olmus mu kontrol et
                    for key in registeredUsers.keys():
                        if key == nickName:
                            self.unregisteredUser = nickName
                            return 9 # REF
                        if(not password.isdecimal()):
                            #şifre sadece rakamlardan oluşmuyor. REJ
                            self.unregisteredUser = nickName
                            return 10
                    registeredUsers[nickName]= password
                    self.registeredUser = nickName
                    return 11  # Kayıt olma işlemi başarılı
                except :
                    ## Hatalı parametre girilmiş
                    return 0 
            #Kullanıcı girisi
            elif komut == "SIN":
                print("SIN girdi-DEBUG")
                try:
                    #debug
                    print("sin tryına girdi")
                    nickName,password = param.split(":")
                    #debug
                    print(nickName,password)
                    print(registeredUsers.keys())
                    if nickName not in currentUsers.keys():
                        for key in registeredUsers.keys():  # kullanıcı adı daha önceden alınmış mı ?
                            if nickName == key and registeredUsers[key] == password:
                                self.loginState = True
                                self.nickName = nickName
                                self.registeredUser= nickName
                                roomsList= list()
                                currentUsers.setdefault(self.nickName, []).append(password)
                                currentUsers.setdefault(self.nickName, []).append(self.tQueue)
                                currentUsers.setdefault(self.nickName, []).append(self.loginState)
                                currentUsers.setdefault(self.nickName, []).append(self.address)
                                currentUsers.setdefault(self.nickName, []).append(roomsList) ## kullanıcının girdiği odalar buraya eklenir.
                                print("current users append oldu")
                                for keys in currentUsers.keys(): #Yeni bir kullanıcı girdiğinde WRN uyarısı vermek gerekiyor.
                                    x = currentUsers[keys]
                                    tQueue = x[1]
                                    tQueue.put("WRN" + ", "+self.registeredUser+": "+ "giriş yaptı"+"\n")
                                self.toLog("WRN", nickName)                            
                                return 2 #registered user dictinde olan bir isimle SIN komutu çalıştırılırsa verilecek durum(giriş bşarılı artık onlineyiz).
                        else: 
                            return 12 #### Hatalı şifre veya  kullanıcı adı
                    else:
                        self.message = "zaten giris yapildi"
                        return 100
                except:
                    return 0 ## protokol mesajına uymayan bir parametre
            #User signed in succesfully!

            #Baglantı testi                
            elif(komut == "PIN"):
                self.toLog("PIN", "")              
                return 4
            #Cıkıs
            elif data == "QUI":
                self.toLog("QUI", "")
                return 5
            
            else: # yukarıdaki durumlardan hiçbiri değilse yanlış komut. sign in olmadan yapılamayacak komut
                return 1
            

        else:  ## SIN komutu kullanılarak giriş yapıldı.
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
                    tQueue = x[1]
                    tQueue.put("GNL" + ", "+self.registeredUser+": "+ param+"\n")
                self.toLog("GNL", param)
                return 7
            #özel mesaj gönderme
            elif(komut == "PRV"):
                try:
                    nick, message = param.split(":")
                    for key in registeredUsers.keys():
                        if key == nick:
                            user = currentUsers[nick]
                            tQueue = user[1]
                            tQueue.put("PRV "+self.nickName + ":, " + message+"\n")
                            self.toLog("PRV", param)
                            return 8
                    self.toWrite("NOP", nick)
                    self.toLog("NOP", nick)
                except:
                    ###hatalı parametre.
                    return 0
            elif(komut=="CHA"): ## şifreyi değiştir.
                nickName,password = param.split(":")
                if (nickName != self.registeredUser):
                    return 0                    
                elif(not password.isdecimal()):
                     #şifre sadece rakamlardan oluşmuyor. REJ
                    self.unregisteredUser = nickName
                    return 10               
                for key in registeredUsers.keys():
                    if nickName == key:
                        registeredUsers[key]=password
                        return 13
            elif(komut =="CRM"):
                for key in roomDict.keys():
                    if key == param: ## girilen oda ismi alınmış
                        return 15
                        
                users = list()
                admins = list()
                banned = list()
                admins.append(self.registeredUser)
                roomDict.setdefault(param, []).append(admins)
                roomDict.setdefault(param, []).append(users)
                roomDict.setdefault(param, []).append(banned)
                return 14

            elif (komut == "ERM"):
                try:
                    oda=roomDict[param]
                    banned=oda[2]
                    if param not in roomDict.keys():
                        self.message = param
                        return 101
                    if self.registeredUser not in banned: 
                        for key in roomDict.keys():
                            if key==param:
                                oda= roomDict[key]
                                oda[1].append(self.registeredUser)
                                ###### odaya giriş yapıldı, şimdi odadakilere giriş yapıldı mesajı gitmesi lazım.
                                for users in oda[1]:
                                    x = currentUsers[users]
                                    tQueue = x[1]
                                    tQueue.put("SKW" + ", "+self.registeredUser+": "+ param + " odasına giriş yaptı"+"\n")
                                    x[4].append(param)                              
                                return 16            
                        return 17
                    else:
                        self.message = " Bu odaya giremezsiniz banlisiniz."
                        return 30
                except:
                    return 0
                
            elif (komut == "RLS"): #odaları listeleme
                return 18
            
            elif (komut == "ULS"): # belirtilen odadaki kullanıcıları özellikleriyle listeleme
                try:
                    message = "Odadaki kullanicilar:"
                    x= roomDict[param]
                    isAdmin = 0
                    for user in x[1]:
                        if user in x[0]:
                            message = message + user+"(yonetici)"+":"
                        else:
                            message = message +user + "(normal)"+":"
                    self.message = message      
                    return 19
                except :
                    return 0
            
            elif (komut == "ALS"): # belirtilen odadaki adminleri listeleme
                try:
                    x= roomDict[param]
                    seperator = ":"
                    self.message =seperator.join(x[0])      
                    return 19
                except :
                    return 0
                
            elif (komut == "RGM"): ## odaya mesaj atma komutu
                try:
                    roomName,message =param.split(":")
                    if roomName not in roomDict.keys(): ##böyle bir oda yok.
                        self.message = roomName 
                        return 101
                    oda=roomDict[roomName]
                    if self.registeredUser not in oda[1]:
                        self.message=roomName
                        return 102
                    for key in roomDict.keys():
                        if key==roomName:
                            oda= roomDict[key]
                            ###### mesaj atılacak oda seçildi, şimdi odadakilere giriş yapıldı mesajı gitmesi lazım.
                            for users in oda[1]:
                                x = currentUsers[users]
                                tQueue = x[1]
                                tQueue.put("MSG"+", "+roomName +" kanalindan mesaj:"+self.registeredUser+":"+message+"\n")                              
                                return 20            
                    return 17               
                except:
                    return 0
            elif (komut == "QUR"):## odadan çıkma komutu
                ## current users dict valuesinin 4. değerindeki roomsListten belirtilen roomu çıkar.
                try:
                    x=currentUsers[self.registeredUser]
                    pop_counter = -1
                    users = x[4]  # kullanıcının girdği odalar burada
                    for room in users:
                        pop_counter +=1
                        if param == room:
                            users.pop(pop_counter)
                    ## roomDict teki user listesinden de kullanıcıyı çıkarmak gerek
                    room =roomDict[param]
                    pop_counter =-1
                    roomDict_users = room[1]
                    for user in roomDict_users:
                        pop_counter += 1
                        if  user == self.registeredUser:
                            roomDict_users.pop(pop_counter)
                            self.message = param
                            for users in roomDict_users:
                                x = currentUsers[users]
                                tQueue = x[1]
                                tQueue.put("SKQ" + ", "+self.registeredUser+": "+ param + " odasından çıkış yaptı yaptı"+"\n")                            
                            return 22
                    return 23 ##arattıgımız odada degiliz RNF
                except:
                    return 24  ##arattığımız oda mevcut olmayacağı için excepte girecektir.
            
            elif (komut == "KIC"): ## kıcklenen kullanıcı tekrar girebilir.
                try:
                    user,room = param.split(":")
                    ### kickleme yapmaya çalışan odanın admini mi ?
                    x= roomDict[room]
                    pop_counter = -1
                    users =x[1]## kullanıcıların olduğu 
                    admins =x[0]
                    y=currentUsers[user]
                    userRooms = y[4]
                    for userx in admins:
                        if userx == self.registeredUser:
                            #print("admin girisi")
                            for roomy in userRooms:
                                pop_counter +=1
                                if roomy == room:
                                    userRooms.pop(pop_counter)
                            pop_counter =-1
                            for birey in users:
                                pop_counter +=1
                                if birey == user:
                                    for user in users:
                                        x = currentUsers[user]
                                        tQueue = x[1]
                                        tQueue.put("SKG" + ", "+user+": "+ room + " odasindan kicklendi"+"\n")
                                    users.pop(pop_counter)
                                    self.message = user
                                    print("kicklendi")
                                    return 25
                                self.message = user
                                return 26 ## USer not found
                    self.message = "NOT ADMIN "
                    return 27 ##admin yetkisi yok     
                except:
                    return 0        
            elif (komut == "BAN"):  ## KIC komutunun yaptığı şeyi yapıp üstüne banlı listesine ekleyecek.
                try:
                    user,room = param.split(":")
                    x= roomDict[room]
                    pop_counter = -1
                    users =x[1]## kullanıcıların olduğu 
                    admins =x[0]
                    y=currentUsers[user]
                    userRooms = y[4]
                    print("ustteki fora girmedi")
                    for userx in admins:
                        print("üstteki fora girdi")
                        if userx == self.registeredUser and user not in x[0]:    ### kickleme yapmaya çalışan odanın admini mi ?
                            print("admin girisi")
                            for roomy in userRooms:
                                pop_counter +=1
                                if roomy == room:
                                    userRooms.pop(pop_counter)
                            pop_counter =-1
                            for birey in users:
                                x = currentUsers[birey]
                                tQueue = x[1]
                                tQueue.put("SKG" + ", "+self.registeredUser+": "+ room + " odasindan banlandı"+"\n")
                                pop_counter +=1
                                if birey == user:
                                    users.pop(pop_counter)
                                    self.message = user
                                    print("banlandı")
                                    x[2].append(user)
                                    return 28
                            self.message = user
                            return 26 ## USer not found
                    print("27 ye geldi")
                    return 27 ##admin yetkisi yok     
                except:
                    return 0
            elif (komut == "BLS"): ##BAN list
                try:
                    roomName=roomDict[param]
                    seperator = ":"
                    self.message =seperator.join(roomName[2])      
                    return 29
                except :
                    return 0                
            
            elif (komut == "CLR"): ##ODAYI kapatma komutu
                try:
                    if param not in roomDict.keys():
                        return 23
                    roomName=roomDict[param]
                    admins=roomName[0]
                    me = currentUsers[self.registeredUser]
                    myrooms = me[4]
                    odalar=roomDict[param]

                    if self.registeredUser in admins:
                        for user in odalar[1]:
                            x = currentUsers[user]
                            tQueue = x[1]
                            tQueue.put("SRC" +": "+ room + "odasi kapatildi"+"\n")
                        roomDict.pop(param)
                        myrooms.remove(param)
                        self.message = param
                        return 31
                    self.message = self.registeredUser
                    return 27 ## not admin
                except:
                    return 0
            
            elif (komut == "MKA"):## admin yapma komutu make admin
                try:
                    user,room = param.split(":")
                    roomName=roomDict[room]
                    admins = roomName[0]
                    if user not in currentUsers.keys():
                        self.message = user
                        return 26 ## User not found
                    if self.registeredUser in admins:
                        roomName[0].append(user)
                        self.message = user 
                        return 32
                    else:
                        return 27 ##NOT admin
                                            
                except:
                    return 0
                                            
                          
                                            
            else:
                return 0
     ####################### Returnlerin geldiği yer  aynı mesajı bir kaç defa vermek gerekebileceği için mesajları değerlere atadım.       
    def run(self):
        self.lQueue.put("Starting " + self.name)
            
        while True:
            try:
                entry = str(self.csoc.recv(1024).decode())
                self.toLog(entry.strip, str(self.address))
            except:
                break
            response = self.parser(entry)
            if response == 0:  ### Protokole uygun olmayan mesaj
                self.toWrite("ERR", "")
                self.toLog("ERR", "")
            elif response == 1: ## Giriş yapılması gereken protokol mesajı çalıştırma hatası
                self.toWrite("LRR", "")
                self.toLog("LRR", "")
            elif response == 2:
                self.toWrite("WEL",self.registeredUser)
                self.toLog("WEL", self.registeredUser)
            elif response == 3:
                self.toWrite("REJ",self.unregisteredUser)
                self.toLog("REJ", self.unregisteredUser)
            elif response == 100:
                self.toWrite("ASI",self.message)
                self.toLog("ASI",self.message)
            elif response == 4:
                self.toWrite("PON", "") 
                self.toLog("PON", "")
            elif response == 5:
                try:
                    self.loginState = False  # çıkış yapacağımız için loginstate i false yapıyoruz.
                     #çıkış yapan kişinin current user listten silinmei gerekmektedir, silme işleminin yapılacağı indexi buluyorum.
                    for key in currentUsers.keys():
                        if key == self.registeredUser:
                            currentUsers.pop(key)
                        self.toWrite("BYE", self.nickName)
                        self.toLog("BYE", self.nickName)
                    break 
                except:
                    break
            elif response == 6: ##gls durumu
                #print("error-DEBUG")
                for key in registeredUsers.keys():
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
            elif response == 9: #Aynı isimde başka kullanıcı var kayıt olma hatası
                self.toWrite("REF",self.unregisteredUser)
                self.toLog("REF",self.unregisteredUser)
            elif response == 10: #Belirlenen şifre uygun şartlarda değil
                self.toWrite("REJ",self.unregisteredUser)
                self.toLog("REJ",self.unregisteredUser)
            elif response == 11:
                self.toWrite("SUC",self.registeredUser)
                self.toLog("SUC",self.registeredUser)
            elif response == 12:
                self.toWrite("NOP","")
                self.toLog("NOP","")
            elif response == 13:
                self.toWrite("OKC",self.registeredUser)
                self.toLog("OKC",self.registeredUser)
            elif response == 14: # oda basariyla olusturuldu
                self.toWrite("ODA",self.registeredUser)
                self.toLog("ODA",self.registeredUser)
            elif response == 15: # girilen oda ismi zaten var
                self.toWrite("NOD",self.registeredUser)
                self.toLog("NOD",self.registeredUser)
            elif response == 16:
                self.toWrite("BIE",self.registeredUser)
                self.toLog("BIE",self.registeredUser)
            elif response == 17:
                self.toWrite("NRM",self.registeredUser)
                self.toLog("NRM",self.registeredUser)
            elif response == 18:
                #print("error-DEBUG")
                for key in roomDict.keys():
                    self.message += key+":"
                seperator = ":"
                self.message =seperator.join(roomDict) 
                print(self.message)
                self.toWrite("LST", self.message)
                self.toLog("LST", self.message)
            elif response == 19:# odadaki kullanıcıları listeleme
                self.toWrite("LST", self.message)
                self.toLog("LST", self.message)
            elif response == 20: ## odaya genel mesaj gönderildi
                self.toWrite("SEN",self.message)
                self.toLog("SEN",self.message)
            elif response == 21:
                self.toWrite("LSM",self.message)
                self.toLog("LSM",self.message)
            elif response == 22:
                self.toWrite("RQU",self.message)
                self.toLog("RQU",self.message) 
            elif response == 23: ##cıkmak istedigin odada degilsin
                self.toWrite("RNF","")
                self.toLog("RNF","")
            elif response ==24 : ##cıkmak istedigin oda mevcut değil ROOM NOT EXIST
                self.toLog("RNE","")
                self.toWrite("RNE","")
            elif response == 25:
                self.toLog("OKK",self.message)
                self.toWrite("OKK",self.message)
            elif response == 26:  ## banlanacak user not found
                self.toLog("UNF",self.message)
                self.toWrite("UNF",self.message)
            elif response == 27: ## banlama işlemini yapmak isteyen admin değil
                self.toLog ("NAD",self.message)
                self.toWrite("NAD",self.message)
            elif response == 28: # banlama basarili
                self.toLog ("OKB",self.message)
                self.toWrite("OKB",self.message)
            elif response == 29:  ##Banlı listesi
                self.toLog ("LSB",self.message)
                self.toWrite("LSB",self.message) 
            elif response == 30 : #banlisin odaya giremezsin.
                self.toLog("BND",self.message)
                self.toWrite("BND",self.message)
            elif response == 31:
                self.toLog("OKC",self.message)
                self.toWrite("OKC",self.message) 
            elif response == 32:
                self.toLog("AMK",self.message)
                self.toWrite("AMK",self.message)
            elif response == 101:
                self.toLog("NRM",self.message)
                self.toWrite("NRM",self.message)
            elif response == 102: ## odaya giriş yapmadan listeleme yapılamaz.
                self.toLog("NEN",self.message)
                self.toWrite("NEN",self.message)                                          
                
                
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