import threading
import socket


host = socket.gethostbyname(socket.gethostname())
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    # print(f"activve clients {clients}")
    for client in clients:
        client.send(message)
        # print(f"[MESSAGE SENT]  {message}")

def unicast(nickname,msg):
    print(nickname)
    index=nicknames.index(nickname)
    client=clients[index]
    client.send(msg)
    print(f"msg sent to {nickname}")

def handle(client):
    while True:
        try:
            
            msg_length=int(client.recv(64).decode())
            # print(msg_length)
            msg_type = client.recv(msg_length).decode()
            # print(msg_type)
            
            
            if msg_type.strip().upper()=='BROADCAST':
                # print('hi')
                msg_length=int(client.recv(64).decode())
                # print(msg_length)
                
                message=client.recv(msg_length).decode()
                # print(message)
                broadcast(message.encode())
            elif msg_type.strip().upper()=='UNICAST':
                msg_length=int(client.recv(64).decode())
                nickname=client.recv(msg_length).decode()
                
                msg_length=int(client.recv(64).decode())
                # print(msg_length)
                
                message=client.recv(msg_length).decode()
                # msg=client.recv(1024)
                message+='(Unicasted)'
                unicast(nickname,message.encode())
        except:
            # print(e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the Network!'.encode())
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} has joined the Network!".encode())
        client.send('Connected to the server!'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()