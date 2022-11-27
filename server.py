from  datetime import datetime
import json
import socket 
import base64
from typing import List

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("0.0.0.0", 9990))
listener.listen(0)
print("[+] Waiting for incoming connections")
cl_socket, remote_address = listener.accept()
print(f"[+] Got a connection from {remote_address} ")


def uploading ():
    cl_socket.send("uploading".encode())
    file_name = input("Input name file:")
    cl_socket.send(file_name.encode())
    try:
        file = open(file_name, 'rb')
        while True:
            line = file.readline(1024)
            cl_socket.send(line)
            if not line:
                cl_socket.send("break_program.gg".encode())
                break
    except:
        print("File not funnd")
    file.close()


def download():
    cl_socket.send("download".encode())
    file_name = input("Input name file:")
    cl_socket.send(file_name.encode())
    flag = cl_socket.recv(1024)
    if flag.decode() == '255':
        print("File not funnd")
    else:
        print("ff")
        file = open('serv/' + file_name, 'wb')
        while True:
            line = cl_socket.recv(1024)
            print(line)
            if not line or line.decode() == 'break_program.gg':
                break
            file.write(line)
        file.close()


def server_comand():
    try:
        while True:
            command :str = input(">> ")
            if "uploading" in command:
                uploading()
            elif "download" in command:
                download()
            else:
                cl_socket.send(command.encode())
                response = cl_socket.recv(1024).decode()
                print(response)
            
    except KeyboardInterrupt:
        listener.close()
        exit()


if __name__ == "__main__":
    server_comand()