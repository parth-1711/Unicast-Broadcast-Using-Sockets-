import socket 
import threading
import os
import time

nickname = input("Choose a nickname: ")
password = input("Enter password to join the private network: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.2.0.152', 55555)) #replace your server's ip with the ip mentioned here.

BUFSIZE=1024

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            elif message == 'PASSWORD':
                client.send(password.encode())
            elif message == "Wrong Password":
                    print("Password is incorrect.")
                    client.close()
                    # exit()
                    break
            elif message=='Throughput':
                print('hello')
                testdata = 'x' * (BUFSIZE-1) + '\n'
                t1 = time.perf_counter()
                i = 0
                while i < 10:
                    i = i+1
                    client.send(testdata.encode())
                    data = client.recv(64).decode()
                t2 = time.perf_counter()
               
                t3 = time.perf_counter()
                
                throghput=round(((BUFSIZE+64)*10*0.001) / (t3-t1), 3)
                print('Throughput is : ',throghput,' Kbps')
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
            msg_type=input()
            msg_length=len(msg_type)
            
            send_length=str(msg_length).encode()
            send_length+=b' '*(64-len(send_length))
            
            client.send(send_length)
            client.send(msg_type.encode())

            if msg_type.strip().lower()=='broadcast':
                
                message = f'{nickname}: {input("")} '
                msg_length=len(message)
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
            
                client.send(send_length)
            
                client.send(message.encode())
                print('Message Sent !')

            elif msg_type.strip().lower()=='unicast':
                
                nick=input('Whom to send : ')
                msg_length=len(nick)
            
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
                
                client.send(send_length)
                client.send(nick.encode())
                
                message = f'{nickname}: {input("")} '
                msg_length=len(message)
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
            
                client.send(send_length)
            
                client.send(message.encode()) 
                print('Message Sent !')
                
            elif msg_type.strip().lower()=='multicast':
                
                group = [] 

                grplen = input("Enter number of people in the group : ")

                for i in range(int(grplen)):
                    temp = input("Select nickname to include in multicast : ")
                    group.append(temp)

                grp = " ".join(group)
                grplen = len(grp)
            
                send_length=str(grplen).encode()
                send_length+=b' '*(64-len(send_length))
                
                client.send(send_length)
                client.send(grp.encode())
                
                print("Enter message to multicast :")
                message = f'{nickname}: {input("")} '
                msg_length=len(message)
                
                send_length=str(msg_length).encode()
                send_length+=b' '*(64-len(send_length))
            
                client.send(send_length)
            
                client.send(message.encode()) 
                print('Message Sent !')
        except:
            print("An error occured !")
            # client.close()
            connected=False
            break
        # connected=False

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()