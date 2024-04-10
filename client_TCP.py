import socket 
import threading
import os

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.0.52.32', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    connected=True
    while connected:
        try:
            msg_type=input("")
            msg_length=len(msg_type)
            
            send_length=str(msg_length).encode()
            send_length+=b' '*(64-len(send_length))
            
            client.send(send_length)
            client.send(msg_type.encode())

            if msg_type.strip().lower()=='broadcast':
                message = f'{nickname}: {input("")} '
                msg_length=len(message)
            # print(msg_length)
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
            
                client.send(send_length)
            
                client.send(message.encode())

            elif msg_type.strip().lower()=='unicast':
                
                nick=input('Whom to send : ')
                msg_length=len(nick)
            
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
                
                client.send(send_length)
                client.send(nick.encode())
                
                message = f'{nickname}: {input("")} '
                msg_length=len(message)
            # print(msg_length)
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
            
                client.send(send_length)
            
                client.send(message.encode())  
        except e:
            print(e)
        # connected=False

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()