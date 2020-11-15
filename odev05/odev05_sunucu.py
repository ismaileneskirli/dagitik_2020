import sys
import socket
import threading
from datetime import datetime


class connThread(threading.Thread):
    def __init__(self, threadID,conn, c_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
        self.c_addr = c_addr
        
    def run(self):
        date = datetime.now()   
        d = str(date) 
        
        self.conn.send("Hosgeldiniz Saat:".encode())
        self.conn.send(d.encode())
        print("Baglanti kuruldu: %s" % str(self.c_addr))
        
        while True:
            data = self.conn.recv(1024)
            data_str= data.decode().strip()
            print(data_str)
            if data_str == "Selam":
                self.conn.send("Selam\n".encode( ))
            if data_str =="Naber":
                self.conn.send("Iyiyim, sagol\n".encode())
            if data_str=="Hava":
                self.conn.send("Yagmurlu\n".encode())
            if data_str =="Haber":
                self.conn.send("Korona\n".encode())
            if data_str == "Kapan":
                self.conn.send("Gule Gule".encode())
                break
            if data_str != "Selam" and data_str != "Naber" and data_str != "Hava" and data_str != "Haber"and data_str != "Kapan" :
                self.conn.send("Anlamadim\n".encode())
        conn.close()
        print("Thread %s kapanıyor" % self.threadID)
        
            
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
