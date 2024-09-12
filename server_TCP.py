import threading
import socket
# import sys

host = socket.gethostbyname(socket.gethostname())
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

PASSWORD = "password"

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

def multicast(message, group):
    # print(f"active clients {clients}")
    for client in group:
        index=nicknames.index(client)
        clt=clients[index]
        # clt.send(msg)
        clt.send(message)

def handle(client):
    while True:
        try:    
            msg_length=int(client.recv(64).decode())
            # print(msg_length)
            msg_type = client.recv(msg_length).decode()
            print(msg_type)
            
            
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
                
                message=client.recv(msg_length).decode() +'(unicasted)'
                # msg=client.recv(1024)
                unicast(nickname,message.encode())

            elif msg_type.strip().upper()=='MULTICAST':    
                

                grouplen = client.recv(64).decode()
                grouplen = int(grouplen)
                group = client.recv(grouplen).decode()
                group = group.split(' ')

                msg_length=int(client.recv(64).decode())                
                message=client.recv(msg_length).decode()

                # msg=client.recv(1024)
                message+='(Multicast)'
                multicast(message.encode(), group)
        except:
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

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        client.send('PASSWORD'.encode())
        password = client.recv(1024).decode()

        if password != PASSWORD:
            client.send("Wrong Password".encode())
            client.close()
        else:
            print(f"Connected with {str(address)}")

            nicknames.append(nickname)
            clients.append(client)


            print(f"Nickname of the client is {nickname}!")
            broadcast(f"{nickname} has joined the Network!".encode())
            # client.send('Connected to the server!'.encode())
            
            client.send('Throughput'.encode())
            iter=0
            BUFSIZE=1024
            ack=b' '*64
            while iter<10:
                data = client.recv(BUFSIZE)
                    # print(data.decode())
                client.send(ack)
                iter+=1
                # conn.close()
            #     print ('Done')
            # print('done2')

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()



print('Server is listening...')
receive()


# -------------------------------------



# def main():
#     if len(sys.argv) < 2:
#         usage()
#     if sys.argv[1] == '-s':
#         server()
#     elif sys.argv[1] == '-c':
#         client()
#     else:
#         usage()


# def usage():
#     sys.stdout = sys.stderr
#     print ('Usage:    (on host_A) throughput -s [port]')
#     print ('and then: (on host_B) throughput -c count host_A [port]')
#     sys.exit(2)


# def server():
#     if len(sys.argv) > 2:
#         port = eval(sys.argv[2])
#     else:
#         port = MY_PORT
#     s = socket(AF_INET, SOCK_STREAM)
#     s.bind(('', port))
#     s.listen(1)
#     print ('Server ready...')
#     while 1:
#         conn, (host, remoteport) = s.accept()
#         while 1:
#             data = conn.recv(BUFSIZE)
#             if not data:
#                 break
#             del data
#         conn.send('OK\n')
#         conn.close()
#         print ('Done with', host, 'port', remoteport)


# def client():
#     if len(sys.argv) < 4:
#         usage()
#     count = int(eval(sys.argv[2]))
#     host = sys.argv[3]
#     if len(sys.argv) > 4:
#         port = eval(sys.argv[4])
#     else:
#         port = MY_PORT
#     testdata = 'x' * (BUFSIZE-1) + '\n'
#     t1 = time.time()
#     s = socket(AF_INET, SOCK_STREAM)
#     t2 = time.time()
#     s.connect((host, port))
#     t3 = time.time()
#     i = 0
#     while i < count:
#         i = i+1
#         s.send(testdata)
#     s.shutdown(1) # Send EOF
#     t4 = time.time()
#     data = s.recv(BUFSIZE)
#     t5 = time.time()
#     print (data)
#     print ('Raw timers:', t1, t2, t3, t4, t5)
#     print ('Intervals:', t2-t1, t3-t2, t4-t3, t5-t4)
#     print ('Total:', t5-t1)
#     print ('Throughput:', round((BUFSIZE*count*0.001) / (t5-t1), 3),)
#     print ('K/sec.')


# main()
# cd "Final Code"  
# python client_TCP.py