import os
import socket
import time

def startserver(host,port,file_path,defult_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    check_for_client(server_socket,file_path,defult_path)
    
def check_for_client(server_socket,file_path,defult_path):
    while True:
        print('listenning')
        server_socket.listen(1)
        client_socket, client_address = server_socket.accept()
        print('client connectioned')
        client_socket.sendall(file_path.encode())
        print(file_path)
        time.sleep(1)
        files_in_folder_and_massage(client_socket,server_socket,file_path,defult_path)

def files_in_folder_and_massage(client_socket,server_socket,file_path,defult_path):
    while True:
        try:
            contents = os.listdir(file_path)
            data=''
            for item in contents:
                data=data+item+'\n'
            print(data)
            data+='-----------------------------------------------------------------------\n'
            data+='download: download a file: to download a file input "download (file name)"\n'
            data+='open folder: to open a folder input "open (folder name)"\n'
            data+='back: to get out of the folder you can input "back"\n'
            data+='folder creation: to create a folder input "createfolder (foldername)"\n'
            data+='upload: to upload a file input "upload (computer path)"\n'
            data+='delete: to delete a file from the storage input "delete (file name)"\n'
            client_socket.sendall(data.encode())
            time.sleep(1)
            client_socket.sendall(file_path.encode())
            file_path=inputsfu(client_socket,server_socket,file_path,defult_path)
        except:
            print('client disconnected')
            break

def inputsfu(client_socket,server_socket,file_path,defult_path):
    command=client_socket.recv(1024).decode()
    if command[:6]=='upload':
        filep=command[7:]
        file_name=os.path.basename(filep)
        file_path=uploadfunc(client_socket,server_socket,file_path,file_name)
        return file_path
    elif command[:12]=='createfolder':
        file_path=folder_creation(client_socket,server_socket,file_path,command[13:])
        return file_path
    elif command[:4]=='open':
        file_path=folder_open(client_socket,server_socket,file_path,command[5:])
        return file_path
    elif command[:4]=='back':
        file_path=back(client_socket,server_socket,file_path,defult_path)
        return file_path
    elif command[:6]=='delete':
        file_path=delete_file(client_socket,server_socket,file_path,command[7:])
        return file_path
    elif command[:8]=='download':
        print(command)
        file_path=download_files(client_socket,server_socket,file_path,command[9:])
        return file_path
        
def download_files(client_socket,server_socket,file_path,file_name):
    file_download_path=os.path.join(file_path,file_name)
    with open(file_download_path,'rb') as file:
        while True:
            data=file.read(1024)
            if not data:
                time.sleep(1)
                end_of_data_massage=b' END_OF_DATA1122333445566'
                client_socket.sendall(end_of_data_massage)
                break
            client_socket.sendall(data)
    return file_path
    

def uploadfunc(client_socket,server_socket,file_path,file_name):
    file_creation=os.path.join(file_path, file_name)
    with open(file_creation, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if data == b' END_OF_DATA1122333445566':
                print('No more data from client. Exiting the loop.')
                break
            file.write(data)
            file.flush()
            print('Received data and wrote to file.')
    return file_path

def folder_creation(client_socket,server_socket,file_path,folder_name):
    folder_path = os.path.join(file_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print('folder already exists')
    return file_path

def folder_open(client_socket,server_socket,file_path,folder_name):
    file_path=os.path.join(file_path,folder_name)
    print(f'opened the folder {folder_name}')
    return file_path
    
def back(client_socket,server_socket,file_path,default_path1):
    if file_path!=default_path1:
        file_path=os.path.dirname(file_path)
        print(f'went back to {file_path}')
    return file_path
    
def delete_file(client_socket,server_socket,file_path,file_name):
    file_path_delete=os.path.join(file_path,file_name)
    if os.path.isfile(file_path_delete):
        os.remove(file_path_delete)
    else:
        os.rmdir(file_path_delete)
    return file_path


    
if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8965             #change the port to the port you want
    file_path=r'C:\Users\jongames100\Desktop\storge_for_project'                #change the path to where you want the server will store the files
    default_path=file_path
    startserver(HOST, PORT,file_path,default_path)
