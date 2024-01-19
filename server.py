import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
list_of_nicknames = []

print("Server has started...")

def clientthread(conn, nickname):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print ("<" + nickname[0] + "> " + message)

                message_to_send = "<" + nickname[0] + "> " + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in list_of_nicknames:
        list_of_nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    list_of_nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    broadcast(message, conn)
    new_thread = Thread(target = clientthread, args = (conn,nickname))
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()