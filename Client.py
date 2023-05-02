from socket import *
import threading
import sys
import re

def recv_message(clientSocket):
    global clientIP, clientPort
    while True:
        reply = clientSocket.recv(1024)
        if not reply:
            break
        reply_decode = str(reply.decode())
        pattern_ip = r"'([^']*)'"
        match = re.search(pattern_ip, reply_decode)
        ip_address = match.group(1)        
        if ip_address == clientIP:
            pattern_replace = r"\((.*?)\)"
            reply_decode = re.sub(pattern_replace, r'(you)', reply_decode)
        print(reply_decode)


server_name = "192.168.0.109"
port_num = 3780      

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_name, port_num))
clientIP, clientPort = clientSocket.getsockname()
print("Client IP address:", clientIP)
print("Client port:", clientPort)
clientSocket.settimeout(1000) 

print("connection established!")
t_recv = threading.Thread(target=recv_message, args=(clientSocket,))
t_recv.start()

while True:
    message = input()
    if message == 'exit0':
        clientSocket.close()
        print("Farewell :)")
        sys.exit()
    clientSocket.send(message.encode())    

        



