import sys
import socket
import threading
from datetime import datetime
import random
# -*- coding: utf-8 -*-
#odevimi bonuslar ile birlikte tamamladim, try except ekleyerek hatami duzelttim, ek sure icin tesekkurler.

class connThread(threading.Thread):
    def __init__(self, threadID,conn, c_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
        self.c_addr = c_addr
        
    def run(self):
        self.conn.send("Sayi bulmaca oyununa hosgeldiniz!\n".encode())
        numberofguesses=0
        self.conn.send("Oyunu kazanmak icin 10 tahmin hakkiniz var.\n".encode())
        running = 0
 
        while True:
            guess = self.conn.recv(1024)
            guess_str= guess.decode().strip()             
            print(guess_str) 
            command_list= guess_str.split(" ")
            command = command_list[0]
            try:
                guess = int(command_list[1])
            except :
                print("Try komutu degil.")
            print(command_list)

            if command == "STA":
                numbertoguess = generatenumber()   
                print(numbertoguess)
                self.conn.send("RDY\n".encode())
                running =1

            if running == 0:
                if command =="TRY":
                    self.conn.send("GRR".encode())

            elif running ==1 :
                if command == "TRY":
                    numberofguesses  +=1
                    if isinstance(guess,int):
                        if guess == numbertoguess:
                            self.conn.send("WIN\n".encode())
                            break

                        if guess > numbertoguess:
                            self.conn.send("GTH\n".encode())
                            self.conn.send(str(numberofguesses).encode())
                            self.conn.send(" . tahmininiz.\n".encode())
                        if guess < numbertoguess:
                            self.conn.send("LTH\n".encode())
                            self.conn.send(str(numberofguesses).encode())
                            self.conn.send(" . tahmininiz.\n".encode())
                    else:
                        self.conn.send("PRR\n".encode())    

            if command =="TIC":
                self.conn.send("TOC\n".encode())
            if command=="QUI":
                self.conn.send("BYE\n".encode())
                break 

                
            
            
            if command != "STA" and command != "TRY" and command != "TIC" and command != "QUI":
                self.conn.send("ERR".encode())

            if(numberofguesses == 10):
                self.conn.send("Tahmin hakkiniz kalmadi, oyunu kaybettiniz.\n".encode())
                break
        conn.close()
        
        
def generatenumber():
    return random.randint(1, 99)

s = socket.socket()
ip ="0.0.0.0"
port = int(sys.argv[1])
addr_server = (ip, port)
s.bind(addr_server)
counter = 0
s.listen(5)
threads = []

while True:
    conn, addr = s.accept()  # blocking 
    newConnThread = connThread(counter, conn , addr)
    threads.append(newConnThread)
    newConnThread.start()
    counter += 1

s.close() 