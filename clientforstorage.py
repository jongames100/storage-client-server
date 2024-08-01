import os
import socket
import time

def getting_connection(ip,port,my_socket,where_to_download):
    while True:
        try:
            data='before using this server pls look at the # that I put in both server and client code\n'
            print(data)
            time.sleep(5)
            print("Trying to connect to server...")
            my_socket.connect((ip, port))
            print("Connection established.")
            server_default=my_socket.recv(1024).decode()
            time.sleep(1)
            info_and_input(my_socket,server_default,where_to_download)
            break
        except:
            print("Connection error. Retrying...")
        
def info_and_input(my_socket,server_default,where_to_download):
    while True:
        try:
            data=my_socket.recv(1024).decode()
            print(data)
            time.sleep(1)
            where_server=my_socket.recv(1024).decode()
            print(where_server)
            time.sleep(1)
            command=input('enter a command: ')
            inputs(my_socket,command,where_server,server_default,where_to_download)
        except Exception as e:
            print('error:',e)

def inputs(my_socket,command,where_server,server_default,where_to_download):
    print(server_default)
    if command[0:6]=='upload':
        my_socket.send(command.encode())
        file_path=command[7:]
        upload(my_socket,file_path)
    elif command[:12]=='createfolder':
        create_folder(my_socket,command)
    elif command[:4]=='open':
        open_folder(my_socket,command)
    elif command=='back':
        back_a_folder(my_socket,command,where_server,server_default)
    elif command[:6]=='delete':
        file_deletion(my_socket,command)
    elif command[:8]=='download':
        download_from_server(my_socket,command,where_to_download)
        
def download_from_server(my_socket,command,where_to_download):
    my_socket.sendall(command.encode())
    file_name=command[9:]
    download_path=os.path.join(where_to_download,file_name)
    with open(download_path,'wb') as file:
        while True:
            data=my_socket.recv(1024)
            if  data==b' END_OF_DATA1122333445566':
                print('no more data frodm client')
                break
            file.write(data)
            file.flush()
        
def upload(my_socket,file_path):
    with open(file_path,'rb') as file:
        while True:
            data=file.read(1024)
            if not data:
                time.sleep(1)
                end_of_data_massage=b' END_OF_DATA1122333445566'
                my_socket.sendall(end_of_data_massage)
                break
            my_socket.sendall(data)

def create_folder(my_socket,command):
    my_socket.send(command.encode())

def open_folder(my_socket,command):
    my_socket.send(command.encode())
    
def back_a_folder(my_socket,command,where_server,server_default):
        my_socket.send(command.encode())

def file_deletion(my_socket,command):
    my_socket.send(command.encode())


if __name__ == "__main__":
    ip='10.0.0.22'               #change the ip to the servers ip
    port=8965               #change the port to the servers port
    where_to_download=r'C:\Users\harus\Downloads' #change this path to where you want to put the downloaded files from server
    my_socket = socket.socket()
    getting_connection(ip,port,my_socket,where_to_download)