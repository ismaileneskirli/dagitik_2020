import socket
import sys


def main():
    s = socket.socket()
    host = str(sys.argv[1])
    port = int(sys.argv[2])

    s.connect((host,port))
    print(s.recv(1024).decode())
    while True:
        userInput = input()
        s.send(userInput.encode())
        receivedMessage = s.recv(1024).decode()
        print(receivedMessage)
        if receivedMessage == "Kapan":
            break
    s.close()


if __name__ == "__main__":
    main()
