from socket import *
import threading
import time

lock = threading.Lock()
broadcast_info = ""
sockets = []

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostname(), 3780))

serverSocket.listen(2)
print("the server is ready to receive information...\n")

def handle_client(connectionSocket, address):
    global broadcast_info, sockets
    print(address, "connected")
    while True:
        info = connectionSocket.recv(1024).decode()
        with lock:
            if not info:
                print(address, "cut the connection")
                sockets.remove(connectionSocket)
                break
            print(address, info)
            broadcast_info = str(address) +" "+ str(info)

def broadcast_sys():
    global broadcast_info, lock, sockets
    while True:
        with lock:
            if broadcast_info is not None:
                for s in sockets:
                    s.send(broadcast_info.encode())
                broadcast_info = None
        time.sleep(0.1)

t_send = threading.Thread(target=broadcast_sys)
t_send.start()
while True:
    try:
        connectionSocket, address = serverSocket.accept()
        t_recv = threading.Thread(target=handle_client, args=(connectionSocket, address))
        sockets.append(connectionSocket)
        t_recv.start()
    except KeyboardInterrupt:
        serverSocket.close()
        print("Server shutdown!")
        break
