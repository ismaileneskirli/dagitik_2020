import sys
import socket
import threading
from datetime import datetime
import random
# -*- coding: utf-8 -*-
## Kodum suan kismen calisiyor duzeltip bonuslarida yapmak isterim.


class connThread(threading.Thread):
    def __init__(self, threadID,conn, c_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
        self.c_addr = c_addr
        
    def run(self):
        self.conn.send("Sayi bulmaca oyununa hosgeldiniz!".encode())
         
        numberofguesses=0  
 
        while True:
            guess = self.conn.recv(1024)
            guess_str= guess.decode().strip()             
            print(guess_str)
            numberofguesses  +=1 
            running=0
            command_list= guess_str.split(" ")
            command = command_list[0]
            print(command_list)
            if command == "STA":
                numbertoguess = generatenumber()   
                self.conn.send("RDY".encode())
                running =1
            if command == "TRY":
                guess = int(command_list[1])
                if isinstance(guess,int):
                    if guess == numbertoguess:
                        self.conn.send("WIN".encode())
                        break

                    if guess > numbertoguess:
                        self.conn.send("GTH".encode())
                    if guess < numbertoguess:
                        self.conn.send("LTH".encode())
                else:
                    self.conn.send("PRR".encode())    

            if command =="TIC":
                self.conn.send("TOC".encode())
            if command=="QUI":
                self.conn.send("BYE".encode())
                running =0

            if running == 0:
                if command =="TRY":
                    self.conn.send("GRR".encode())    
            
            
            if command != "STA" and command != "TRY" and command != "TIC" and command != "QUI":
                self.conn.send("ERR".encode())
        conn.close()
        #print("Thread %s kapaniyor" % self.threadID)
        
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
